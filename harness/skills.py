"""Skill/Method library (C) — externalized, editable prompt methodologies.

Each skill lives in skills/<name>.md with YAML frontmatter + two named sections:

    ---
    name: digest
    description: ...
    placeholders: [topic, title, text]
    ---
    ## system
    <system prompt>

    ## prompt
    <user/template body with {placeholder} fields>

The harness loads a skill at the point of use, **falling back to the in-code
default** if the file (or a needed section) is missing or malformed — so behavior
is unchanged when no skill files exist. Skills accumulate and are user-editable:
the "self-growing" skill库. Models are NOT set here (they stay in config.yaml);
a skill only supplies the system + prompt text.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

import yaml

from . import config

log = logging.getLogger("harness.skills")


@dataclass
class Skill:
    system: str | None = None
    prompt: str | None = None
    meta: dict = field(default_factory=dict)


_CACHE: dict[str, tuple[float, Skill]] = {}   # name -> (mtime, parsed Skill)


def _section(body: str, name: str) -> str | None:
    # Capture from '## <name>' to the next KNOWN section header (system/prompt) or
    # EOF — NOT any '##', so '## TL;DR' etc. inside a prompt body don't truncate it.
    m = re.search(rf"(?ims)^##[ \t]*{name}[ \t]*\n(.*?)(?=^##[ \t]*(?:system|prompt)\b|\Z)", body)
    return m.group(1).strip() if m else None


def _parse(text: str) -> Skill:
    fm, body = {}, text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                fm = {}
            body = parts[2]
    return Skill(system=_section(body, "system"), prompt=_section(body, "prompt"),
                 meta=fm if isinstance(fm, dict) else {})


def load_skill(name: str, defaults: dict | None = None) -> Skill:
    """Load skills/<name>.md; fill any missing section from `defaults`
    ({"system":..., "prompt":...}). Never raises — returns defaults on any error."""
    defaults = defaults or {}
    path = config.SKILLS_DIR / f"{name}.md"
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return Skill(system=defaults.get("system"), prompt=defaults.get("prompt"))
    cached = _CACHE.get(name)
    if cached and cached[0] == mtime:
        sk = cached[1]
    else:
        try:
            sk = _parse(path.read_text(encoding="utf-8"))
            _CACHE[name] = (mtime, sk)
        except (OSError, ValueError) as e:  # noqa: BLE001
            log.warning("skill %s unreadable (%s); using defaults", name, e)
            return Skill(system=defaults.get("system"), prompt=defaults.get("prompt"))
    return Skill(
        system=sk.system if sk.system is not None else defaults.get("system"),
        prompt=sk.prompt if sk.prompt is not None else defaults.get("prompt"),
        meta=sk.meta,
    )


def with_profile(system: str, cfg) -> str:
    """Append the user identity/needs profile to a system prompt (additive).
    No-op when no profile is configured, so skills stay user-agnostic."""
    prof = getattr(cfg, "profile", None)
    ctx = prof.as_context() if prof else ""
    return f"{system}\n\n# About the user you are serving\n{ctx}" if ctx else system
