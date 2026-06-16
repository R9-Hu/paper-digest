"""Model availability checking + auto-fallback.

The harness pins specific Anthropic model IDs in config.yaml (e.g.
``claude-sonnet-4-6``, ``claude-opus-4-8``). Models get superseded and
eventually retired, at which point ``claude -p --model <id>`` starts failing and
the digest/trend stages would break. This module:

  1. **Probes** each configured model live via ``claude -p`` (the same auth path
     the harness uses — no API key needed).
  2. If a pinned ID is unavailable, **falls back** to the model-family alias
     (``opus`` / ``sonnet`` / ``haiku``), which Claude Code always resolves to the
     latest model in that family — so a daily run keeps working after a model
     update, just on the newest equivalent.
  3. Optionally, if ``ANTHROPIC_API_KEY`` is set, queries the Models API
     (``GET /v1/models``) to report the currently available IDs so the user knows
     what to pin in config.yaml.

Reference (Anthropic model IDs/aliases, cached 2026-06): families resolve via
substring; ``opus``/``sonnet``/``haiku`` are the always-latest aliases.
"""
from __future__ import annotations

import logging
import os

import requests

from . import llm
from .config import Config

log = logging.getLogger("harness.modelcheck")

PROBE_TIMEOUT = 60
PROBE_PROMPT = "Reply with exactly: OK"

# Family substring -> Claude Code always-latest alias used as the fallback.
_FAMILY_ALIASES = {
    "opus": "opus",
    "sonnet": "sonnet",
    "haiku": "haiku",
    "fable": "opus",   # Fable has a distinct API surface; Opus is the safe latest fallback
}

# Informational only (goes stale): current known-good IDs as of 2026-06.
KNOWN_CURRENT = {
    "claude-fable-5", "claude-opus-4-8", "claude-opus-4-7", "claude-opus-4-6",
    "claude-sonnet-4-6", "claude-haiku-4-5", "claude-opus-4-5", "claude-sonnet-4-5",
}


def family_alias(model_id: str) -> str | None:
    low = model_id.lower()
    for key, alias in _FAMILY_ALIASES.items():
        if key in low:
            return alias
    return None


def probe_model(model: str, cfg: Config) -> tuple[bool, str]:
    """Return (ok, detail). ok = claude -p ran and produced output for this model."""
    try:
        out = llm.run_claude(PROBE_PROMPT, model, cfg, allow_tools=False,
                             timeout=PROBE_TIMEOUT)
        return True, out.strip()[:60]
    except llm.LLMError as e:
        return False, str(e)[:200]


def resolve_model(model: str, cfg: Config) -> tuple[str, str]:
    """Return (resolved_model, status).

    status: 'ok' (pinned model works), 'fell_back' (pinned failed, alias works),
    or 'unavailable' (both failed — likely transient/auth; keep pinned, warn).
    """
    ok, detail = probe_model(model, cfg)
    if ok:
        return model, "ok"

    alias = family_alias(model)
    log.warning("model '%s' failed to respond (%s)", model, detail)
    if alias and alias != model:
        alias_ok, _ = probe_model(alias, cfg)
        if alias_ok:
            log.warning("falling back '%s' -> alias '%s' (latest in family). "
                        "Update config.yaml to pin a current model ID.", model, alias)
            return alias, "fell_back"

    log.error("model '%s' unavailable and no working alias; keeping it (may be a "
              "transient/auth issue). Stage may fail until resolved.", model)
    return model, "unavailable"


def check_and_resolve(cfg: Config) -> list[dict]:
    """Probe + resolve both configured models, mutating cfg to the resolved IDs.

    Returns a per-model report. Distinct models are probed once each.
    """
    report: list[dict] = []
    resolved_cache: dict[str, tuple[str, str]] = {}

    for label, attr in (("digest", "digest_model"), ("trend", "trend_model")):
        pinned = getattr(cfg, attr)
        if pinned not in resolved_cache:
            resolved_cache[pinned] = resolve_model(pinned, cfg)
        resolved, status = resolved_cache[pinned]
        if resolved != pinned:
            setattr(cfg, attr, resolved)
        report.append({"role": label, "pinned": pinned,
                       "resolved": resolved, "status": status})
    return report


def list_api_models() -> list[str] | None:
    """If ANTHROPIC_API_KEY is set, return current model IDs via GET /v1/models.

    Returns None when no API key is available (the harness normally uses Claude
    Code subscription auth, where this endpoint isn't reachable).
    """
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    try:
        resp = requests.get(
            "https://api.anthropic.com/v1/models",
            headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
            params={"limit": 100}, timeout=20,
        )
        resp.raise_for_status()
        return [m["id"] for m in resp.json().get("data", [])]
    except (requests.RequestException, ValueError, KeyError) as e:
        log.warning("Models API query failed: %s", e)
        return None


def report_str(report: list[dict]) -> str:
    lines = []
    for r in report:
        flag = {"ok": "OK", "fell_back": "FELL BACK", "unavailable": "UNAVAILABLE"}[r["status"]]
        extra = "" if r["resolved"] == r["pinned"] else f" -> {r['resolved']}"
        note = "" if r["pinned"] in KNOWN_CURRENT else "  (not in known-current list)"
        lines.append(f"  [{flag:11}] {r['role']:6} {r['pinned']}{extra}{note}")
    api = list_api_models()
    if api:
        lines.append("  available via Models API: " + ", ".join(sorted(api)))
    return "\n".join(lines)
