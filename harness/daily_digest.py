"""One-off: digest ONLY today's daily collection (papers fetched today), bypassing
the digest window and leaving the paused backlog untouched, then publish.

Run:  .venv/bin/python -m harness.daily_digest
"""
from __future__ import annotations

import datetime as dt
import logging

from . import config, digest, publish, rag, state, trends


def main() -> int:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s",
        handlers=[logging.StreamHandler(),
                  logging.FileHandler(config.LOG_DIR / "daily-digest.log", encoding="utf-8")])
    logging.getLogger("arxiv").setLevel(logging.WARNING)
    log = logging.getLogger("harness.daily")

    cfg = config.load_config()
    today = dt.date.today().isoformat()
    always = lambda: True   # ignore the digest window for this manual daily run
    with state.connect() as conn:
        total = 0
        for t in cfg.topics:
            total += digest.digest_topic(conn, cfg, t, should_continue=always, fetched_on=today)
        log.info("daily digest: %d papers digested (fetched %s)", total, today)
        rag.build_index(conn)
        for t in cfg.topics:
            trends.analyze_topic(conn, cfg, t)
            trends.summarize_today(conn, cfg, t)
        digest.clear_text_cache()
        publish.publish(conn, cfg, deploy=True)
        log.info("daily digest done — site published")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
