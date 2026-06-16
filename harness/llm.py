"""Headless Claude (`claude -p`) invocation shared by the digest + trend agents.

Runs unattended (bypassPermissions) so it works from cron. The prompt is passed
on stdin to avoid argv size limits with long paper text. File-mutating tools are
disallowed by default — these agents only read/search and return text; the Python
orchestrator owns all writes.
"""
from __future__ import annotations

import logging
import subprocess

from .config import Config

log = logging.getLogger("harness.llm")

# Tools the agents must never use (they return text; Python does the writing).
_DISALLOWED = ["Bash", "Edit", "Write", "NotebookEdit"]


class LLMError(RuntimeError):
    pass


def run_claude(prompt: str, model: str, cfg: Config,
               system: str | None = None, allow_tools: bool = True,
               timeout: int | None = None) -> str:
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
    try:
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=to,
        )
    except subprocess.TimeoutExpired as e:
        raise LLMError(f"claude timed out after {to}s") from e
    except FileNotFoundError as e:
        raise LLMError(f"claude binary not found: {cfg.claude_bin}") from e
    if proc.returncode != 0:
        raise LLMError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:500]}")
    out = proc.stdout.strip()
    if not out:
        raise LLMError("claude returned empty output")
    return out


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
