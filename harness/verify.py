"""Overnight-run verifier — prints a summary, writes logs/overnight-verify.txt, and
fires a desktop notification (notify-send, best-effort). Run by a one-shot systemd
timer in the morning so it pings independently of any Claude session.

Manual:  .venv/bin/python -m harness.verify
"""
from __future__ import annotations

import datetime as dt
import subprocess

from . import config, state


def _service_result(unit: str = "paper-digest.service") -> str:
    try:
        r = subprocess.run(["systemctl", "--user", "show", unit, "-p", "Result"],
                            capture_output=True, text=True, timeout=10)
        return r.stdout.strip().split("=", 1)[-1] or "unknown"
    except (subprocess.SubprocessError, FileNotFoundError):
        return "unknown"


def summary() -> str:
    with state.connect() as c:
        pending = c.execute(
            "SELECT COUNT(*) FROM papers WHERE digest_status IN ('failed','fetched')"
        ).fetchone()[0]
        # 2026 per-topic counts — this is what tonight's monthly-compaction job touched.
        rows = c.execute(
            "SELECT topic_slug, COUNT(*) FROM papers WHERE year=2026 "
            "AND digest_status IN ('digested','compacted') GROUP BY topic_slug"
        ).fetchall()
        y2026 = ",".join(f"{r[0]}={r[1]}" for r in rows) or "none"
        briefs = c.execute(
            "SELECT COUNT(*) FROM meta WHERE key LIKE 'today_brief:%' AND value != ''"
        ).fetchone()[0]
    return (f"2026-job={_service_result('paper-digest-2026.service')} · pending={pending} · "
            f"2026[{y2026}] · in-brief={briefs}/{len(config.load_config().topics)}")


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
