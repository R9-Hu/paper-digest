"""Main entry point — wires Collector -> Digester -> Analyst -> Publisher.

The unattended cron run calls this with no args (all topics, all stages, deploy).
Flags allow partial/manual runs for debugging.
"""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys

from . import config, digest, fetch, publish, state, trends

STAGES = ["fetch", "digest", "trends", "publish"]


def setup_logging() -> None:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    logfile = config.LOG_DIR / f"run-{dt.date.today().isoformat()}.log"
    fmt = "%(asctime)s %(levelname)s %(name)s | %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logfile, encoding="utf-8"),
        ],
    )
    # arxiv's client is chatty at INFO; quiet it down.
    logging.getLogger("arxiv").setLevel(logging.WARNING)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Paper digest meta-harness")
    p.add_argument("--topic", help="run only this topic slug")
    p.add_argument("--stage", choices=STAGES, help="run only this stage (default: all)")
    p.add_argument("--since", help="override earliest date (YYYY-MM-DD) for the fetch stage")
    p.add_argument("--dry-run", action="store_true", help="fetch stage: list matches, don't download")
    p.add_argument("--no-deploy", action="store_true", help="publish stage: build/sync but don't gh-deploy")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    setup_logging()
    log = logging.getLogger("harness")

    cfg = config.load_config()
    config.ensure_dirs()
    topics = [cfg.topic(args.topic)] if args.topic else cfg.topics
    if args.topic and topics[0] is None:
        log.error("unknown topic slug: %s", args.topic)
        return 2

    since = dt.date.fromisoformat(args.since) if args.since else None
    stages = [args.stage] if args.stage else STAGES
    log.info("=== run start | topics=%s | stages=%s ===",
             [t.slug for t in topics], stages)

    totals = {"downloaded": 0, "digested": 0}
    with state.connect() as conn:
        for topic in topics:
            if "fetch" in stages:
                res = fetch.fetch_topic(conn, cfg, topic, dry_run=args.dry_run, since=since)
                totals["downloaded"] += len(res["downloaded"])
                if args.dry_run:
                    for p in res["new"]:
                        log.info("  NEW [%s %s] %s", p.source, p.year, p.title[:90])
            if "digest" in stages and not args.dry_run:
                totals["digested"] += digest.digest_topic(conn, cfg, topic)
            if "trends" in stages and not args.dry_run:
                trends.analyze_topic(conn, cfg, topic)

        if "publish" in stages and not args.dry_run:
            publish.publish(conn, cfg, deploy=not args.no_deploy)

    log.info("=== run done | downloaded=%d digested=%d ===",
             totals["downloaded"], totals["digested"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
