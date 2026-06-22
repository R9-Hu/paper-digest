"""Headless Claude (`claude -p`) invocation shared by the digest + trend agents.

Runs unattended (bypassPermissions) so it works from cron. The prompt is passed
on stdin to avoid argv size limits with long paper text. File-mutating tools are
disallowed by default — these agents only read/search and return text; the Python
orchestrator owns all writes.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import logging
import re
import subprocess
import time

from . import config
from .config import Config

log = logging.getLogger("harness.llm")

# Content-addressed local response cache: identical (model, system, prompt) →
# identical-enough output, so re-runs / re-digests / re-publishes don't re-spend
# tokens. The key includes the full prompt + system, so any change (skill edit,
# model swap, grown corpus) misses automatically. ponytail: unbounded on disk —
# a digest is a few KB, prune state/llmcache/ if it ever grows large.
CACHE_DIR = config.STATE_DIR / "llmcache"


def _cache_key(model: str, system: str, prompt: str) -> str:
    return hashlib.sha256(f"{model}\0{system}\0{prompt}".encode("utf-8")).hexdigest()


def _cache_read(key: str) -> str | None:
    try:
        return (CACHE_DIR / f"{key}.txt").read_text(encoding="utf-8")
    except OSError:
        return None


def _cache_write(key: str, text: str) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        (CACHE_DIR / f"{key}.txt").write_text(text, encoding="utf-8")
    except OSError:
        pass

# Tools the agents must never use (they return text; Python does the writing).
_DISALLOWED = ["Bash", "Edit", "Write", "NotebookEdit"]

# Signals that we've exhausted the subscription's usage window (not a per-paper error).
_RATE_PAT = re.compile(
    r"usage limit|rate[ _-]?limit|limit reached|limit will reset|too many requests|"
    r"\b429\b|quota", re.IGNORECASE)
_POLL_FALLBACK_SEC = 900   # if no reset time is given, poll every 15 min
_RESET_BUFFER_SEC = 45     # wait a touch past the stated reset to be safe
_WEEKLY_MIN_SEC = 24 * 3600  # a reset more than ~a day out is the WEEKLY limit, not the 5h one

# Auto-learned weekly-session reset (epoch), captured from any rate-limit message.
# The orchestrator persists this so the weekly-usage window self-aligns — no manual input.
_OBSERVED_WEEKLY_RESET: float | None = None


def pop_weekly_reset() -> float | None:
    """Return + clear the most recently observed WEEKLY-limit reset epoch (or None)."""
    global _OBSERVED_WEEKLY_RESET
    r, _OBSERVED_WEEKLY_RESET = _OBSERVED_WEEKLY_RESET, None
    return r


class LLMError(RuntimeError):
    pass


class RateLimitError(LLMError):
    """Usage/rate limit hit and we couldn't wait it out within the budget."""
    def __init__(self, msg: str, reset_at: float | None = None):
        super().__init__(msg)
        self.reset_at = reset_at


def _is_rate_limited(text: str) -> bool:
    return bool(text and _RATE_PAT.search(text))


def _next_window_end(cfg) -> float:
    """Epoch of the next digest-window end (cfg.digest_window_end hour, local)."""
    now = dt.datetime.now()
    end = now.replace(hour=int(cfg.digest_window_end) % 24, minute=0, second=0, microsecond=0)
    if end <= now:
        end += dt.timedelta(days=1)
    return end.timestamp()


def _parse_reset(text: str) -> float | None:
    """Best-effort parse of when the limit resets → epoch seconds (local), or None.

    Handles an explicit epoch, an ISO timestamp, or a clock time like
    'resets at 4am' / 'reset at 22:30' (interpreted as the next such local time)."""
    if not text:
        return None
    m = re.search(r"reset[^.]*?\b(\d{10})\b", text)          # unix epoch
    if m:
        return float(m.group(1))
    m = re.search(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?)", text)  # ISO
    if m:
        try:
            return dt.datetime.fromisoformat(m.group(1).replace(" ", "T")).timestamp()
        except ValueError:
            pass
    m = re.search(r"reset[^.]*?\bat\b[^.\d]*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text, re.IGNORECASE)
    if m:
        hour = int(m.group(1)) % 24
        minute = int(m.group(2) or 0)
        ap = (m.group(3) or "").lower()
        if ap == "pm" and hour < 12:
            hour += 12
        elif ap == "am" and hour == 12:
            hour = 0
        now = dt.datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target <= now:
            target += dt.timedelta(days=1)        # next occurrence
        return target.timestamp()
    return None


def run_claude(prompt: str, model: str, cfg: Config,
               system: str | None = None, allow_tools: bool = True,
               timeout: int | None = None, wait_on_limit: bool | None = None,
               respect_window: bool = True, cache: bool = False) -> str:
    ckey = _cache_key(model, system or "", prompt) if cache else None
    if ckey:
        hit = _cache_read(ckey)
        if hit is not None:
            return hit
    cmd = [
        cfg.claude_bin, "-p",
        "--model", model,
        "--output-format", "text",
        "--permission-mode", "bypassPermissions",
    ]
    if system:
        cmd += ["--append-system-prompt", system]
    if not allow_tools:
        cmd += ["--disallowedTools", "Bash", "Edit", "Write", "NotebookEdit",
                "Task", "WebSearch", "WebFetch", "Read", "Glob", "Grep"]
    else:
        cmd += ["--disallowedTools", *_DISALLOWED]
    to = timeout if timeout is not None else cfg.claude_timeout_sec
    # If the subscription's usage window is exhausted, wait for it to renew and retry
    # (up to cfg.rate_limit_max_wait_sec total) instead of failing the digest. Callers
    # that must stay responsive (e.g. paper-selection during the daytime fetch) pass
    # wait_on_limit=False so they fall back immediately instead of blocking.
    do_wait = cfg.wait_for_token_reset if wait_on_limit is None else wait_on_limit
    max_wait = cfg.rate_limit_max_wait_sec if do_wait else 0
    # Window-aware: never wait past the end of the digest window (so a depleted quota
    # resumes within the night, not into work hours). When the window is far off
    # (daytime manual runs), the max-wait cap dominates instead.
    if max_wait > 0 and respect_window:
        max_wait = min(max_wait, max(0.0, _next_window_end(cfg) - time.time()))
    wait_deadline = time.monotonic() + max_wait
    while True:
        try:
            proc = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True, timeout=to,
            )
        except subprocess.TimeoutExpired as e:
            raise LLMError(f"claude timed out after {to}s") from e
        except OSError as e:
            # FileNotFoundError, [Errno 8] Exec format error, etc. — never let a flaky
            # exec of `claude` crash the whole run; fail just this digest.
            raise LLMError(f"claude exec failed ({cfg.claude_bin}): {e}") from e

        out = proc.stdout.strip()
        if proc.returncode == 0 and out:
            if ckey:
                _cache_write(ckey, out)
            return out

        diag = f"{proc.stderr}\n{proc.stdout}".strip()
        if _is_rate_limited(diag):
            reset_at = _parse_reset(diag)
            # Auto-learn the WEEKLY reset (a reset >~24h out is the weekly limit, not the
            # 5-hour one), so the weekly-usage window self-aligns without manual input.
            if reset_at and reset_at - time.time() > _WEEKLY_MIN_SEC:
                global _OBSERVED_WEEKLY_RESET
                _OBSERVED_WEEKLY_RESET = reset_at
            if max_wait > 0:
                remaining = wait_deadline - time.monotonic()
                if remaining > 0:
                    sleep = (reset_at - time.time() + _RESET_BUFFER_SEC) if reset_at else _POLL_FALLBACK_SEC
                    sleep = min(max(60.0, sleep), remaining)   # >=1min, never past the deadline
                    until = dt.datetime.now() + dt.timedelta(seconds=sleep)
                    log.warning("usage/token limit reached — waiting %.0f min (until ~%s) for "
                                "renewal, then resuming", sleep / 60, until.strftime("%H:%M"))
                    time.sleep(sleep)
                    continue
                raise RateLimitError(f"usage limit; exceeded max wait ({max_wait}s)", reset_at)
            raise RateLimitError("usage/rate limit reached", reset_at)

        if proc.returncode != 0:
            raise LLMError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:500]}")
        raise LLMError("claude returned empty output")


def strip_code_fence(text: str) -> str:
    """If the model wrapped the whole reply in a ```markdown fence, unwrap it."""
    t = text.strip()
    if t.startswith("```"):
        lines = t.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return t


if __name__ == "__main__":   # self-check: cache key determinism + round-trip (no claude call)
    k1 = _cache_key("m", "sys", "hi")
    assert k1 == _cache_key("m", "sys", "hi"), "key not stable"
    assert k1 != _cache_key("m", "sys", "hello"), "key ignores prompt"
    assert k1 != _cache_key("m2", "sys", "hi"), "key ignores model"
    _cache_write(k1, "cached!")
    assert _cache_read(k1) == "cached!", "round-trip failed"
    assert _cache_read(_cache_key("x", "y", "z")) is None, "missing key not None"
    print("llm cache self-check OK")
