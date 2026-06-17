"""Headless Claude (`claude -p`) invocation shared by the digest + trend agents.

Runs unattended (bypassPermissions) so it works from cron. The prompt is passed
on stdin to avoid argv size limits with long paper text. File-mutating tools are
disallowed by default — these agents only read/search and return text; the Python
orchestrator owns all writes.
"""
from __future__ import annotations

import datetime as dt
import logging
import re
import subprocess
import time

from .config import Config

log = logging.getLogger("harness.llm")

# Tools the agents must never use (they return text; Python does the writing).
_DISALLOWED = ["Bash", "Edit", "Write", "NotebookEdit"]

# Signals that we've exhausted the subscription's usage window (not a per-paper error).
_RATE_PAT = re.compile(
    r"usage limit|rate[ _-]?limit|limit reached|limit will reset|too many requests|"
    r"\b429\b|quota", re.IGNORECASE)
_POLL_FALLBACK_SEC = 900   # if no reset time is given, poll every 15 min
_RESET_BUFFER_SEC = 45     # wait a touch past the stated reset to be safe


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
               respect_window: bool = True) -> str:
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
            return out

        diag = f"{proc.stderr}\n{proc.stdout}".strip()
        if max_wait > 0 and _is_rate_limited(diag):
            remaining = wait_deadline - time.monotonic()
            if remaining <= 0:
                raise RateLimitError(f"usage limit; exceeded max wait ({max_wait}s)",
                                     _parse_reset(diag))
            reset_at = _parse_reset(diag)
            sleep = (reset_at - time.time() + _RESET_BUFFER_SEC) if reset_at else _POLL_FALLBACK_SEC
            sleep = min(max(60.0, sleep), remaining)   # >=1min, but never past the budget deadline
            until = dt.datetime.now() + dt.timedelta(seconds=sleep)
            log.warning("usage/token limit reached — waiting %.0f min (until ~%s) for renewal, "
                        "then resuming", sleep / 60, until.strftime("%H:%M"))
            time.sleep(sleep)
            continue

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
