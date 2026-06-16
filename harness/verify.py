"""Overnight-run verifier — prints a summary, writes logs/overnight-verify.txt, and
fires a desktop notification (notify-send, best-effort). Run by a one-shot systemd
timer in the morning so it pings independently of any Claude session.

Manual:  .venv/bin/python -m harness.verify
"""
from __future__ import annotations

import datetime as dt
import subprocess

from . import config, state


def _service_result() -> str:
    try:
        r = subprocess.run(["systemctl", "--user", "show", "paper-digest.service",
                            "-p", "Result"], capture_output=True, text=True, timeout=10)
        return r.stdout.strip().split("=", 1)[-1] or "unknown"
    except (subprocess.SubprocessError, FileNotFoundError):
        return "unknown"


def summary() -> str:
    with state.connect() as c:
        pending = c.execute(
            "SELECT COUNT(*) FROM papers WHERE digest_status IN ('failed','fetched')"
        ).fetchone()[0]
        h2025 = c.execute(
            "SELECT COUNT(*) FROM papers WHERE topic_slug='harness' AND year=2025 "
            "AND digest_status IN ('digested','compacted')"
        ).fetchone()[0]
        briefs = c.execute(
            "SELECT COUNT(*) FROM meta WHERE key LIKE 'today_brief:%' AND value != ''"
        ).fetchone()[0]
    return (f"service={_service_result()} · pending={pending} · "
            f"harness2025={h2025}/400 · in-brief={briefs}/{len(config.load_config().topics)}")


def main() -> int:
    s = summary()
    line = f"{dt.datetime.now().isoformat(timespec='minutes')}  {s}"
    print(line)
    try:
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        (config.LOG_DIR / "overnight-verify.txt").write_text(line + "\n", encoding="utf-8")
    except OSError:
        pass
    try:  # best-effort desktop ping (no-op without a graphical session)
        subprocess.run(["notify-send", "📚 Paper Digest — overnight run", s], timeout=10)
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
