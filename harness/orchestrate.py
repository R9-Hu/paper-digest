"""Main entry point — wires Collector -> Digester -> Analyst -> Publisher.

The unattended cron run calls this with no args (all topics, all stages, deploy).
Flags allow partial/manual runs for debugging.
"""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys

from . import compact, config, digest, fetch, modelcheck, publish, rag, review, state, trends

STAGES = ["fetch", "digest", "trends", "publish"]


def _in_digest_window(cfg) -> bool:
    """True if the current local hour is inside the configured digest window
    (which may wrap past midnight, e.g. 21:00–06:00)."""
    h = dt.datetime.now().hour
    s, e = cfg.digest_window_start, cfg.digest_window_end
    return (s <= h < e) if s < e else (h >= s or h < e)


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
    p.add_argument("--max-papers", type=int, help="override max papers per topic per run")
    p.add_argument("--dry-run", action="store_true", help="fetch stage: list matches, don't download")
    p.add_argument("--no-deploy", action="store_true", help="publish stage: build/sync but don't gh-deploy")
    p.add_argument("--check-models", action="store_true",
                   help="probe configured models (with fallback report) and exit")
    p.add_argument("--skip-model-check", action="store_true",
                   help="skip the pre-flight model availability check")
    p.add_argument("--backfill-year", type=int,
                   help="fetch stage: pull top --max-papers papers for this year (ranked)")
    p.add_argument("--compact-year", type=int,
                   help="compact a year to the top yearly_keep papers/topic, then exit")
    p.add_argument("--compact-month",
                   help="compact a month (YYYY-MM) to the top monthly_keep papers/topic, then exit")
    p.add_argument("--compact-months", type=int, metavar="YYYY",
                   help="run monthly compaction for every completed month of YYYY "
                        "(pulls in missed top-tier papers, caps to monthly_keep), then exit")
    p.add_argument("--no-compact", action="store_true",
                   help="skip the automatic prior-year compaction step")
    p.add_argument("--ignore-window", action="store_true",
                   help="digest now even outside the configured digest window")
    p.add_argument("--build-index", action="store_true",
                   help="(re)build the RAG card cache + FTS5/embedding index, then exit")
    p.add_argument("--rag-query", metavar="TEXT",
                   help="retrieve the most relevant paper cards for TEXT (debug), then exit")
    p.add_argument("--review", action="store_true",
                   help="run the weekly review/复盘 (E) now, publish, then exit")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    setup_logging()
    log = logging.getLogger("harness")

    cfg = config.load_config()
    if args.max_papers is not None:
        cfg.max_papers_per_topic_per_run = args.max_papers
    config.ensure_dirs()

    if args.check_models:
        report = modelcheck.check_and_resolve(cfg)
        log.info("model check:\n%s", modelcheck.report_str(report))
        return 0 if all(r["status"] != "unavailable" for r in report) else 1

    topics = [cfg.topic(args.topic)] if args.topic else cfg.topics
    if args.topic and topics[0] is None:
        log.error("unknown topic slug: %s", args.topic)
        return 2

    if args.build_index:
        with state.connect() as conn:
            log.info("rag: %s", rag.build_index(conn))
        return 0

    if args.review:
        with state.connect() as conn:
            ok = review.run_review(conn, cfg)
            log.info("[E] review %s", "written" if ok else "skipped (no data / failed)")
            publish.publish(conn, cfg, deploy=not args.no_deploy)
        return 0

    if args.rag_query:
        with state.connect() as conn:
            hits = rag.retrieve(conn, args.rag_query, topic_slug=args.topic, k=12)
        for h in hits:
            log.info("  [%.3f] %-12s %s (%s, cites=%s) — %s",
                     h["score"], h["topic_slug"], h["title"][:70],
                     h["year"], h["citations"], (h["tldr"] or "")[:100])
        return 0

    if args.compact_month or args.compact_year is not None or args.compact_months is not None:
        cont = lambda: args.ignore_window or _in_digest_window(cfg)  # refetch+digest gated to window
        if not cont():
            log.warning("outside digest window — missed-paper refetch will be skipped "
                        "(use --ignore-window to force)")
        with state.connect() as conn:
            # Honor the weekly-session guard: skip past-month compaction near the limit.
            used, budget = state.week_usage(conn), cfg.weekly_digest_budget
            if (budget > 0 and not args.ignore_window
                    and used >= cfg.weekly_conserve_threshold * budget):
                log.warning("weekly usage %d/%d (>=%.0f%%) — skipping past-month compaction until "
                            "the week renews (use --ignore-window to force)", used, budget,
                            cfg.weekly_conserve_threshold * 100)
                publish.publish(conn, cfg, deploy=not args.no_deploy)
                return 0
            if args.compact_months is not None:
                year = args.compact_months
                today = dt.date.today()
                if year < today.year:
                    months = list(range(1, 13))
                else:
                    # Fill THIS month first, then the previous months (newest-first).
                    months = [today.month] + list(range(today.month - 1, 0, -1))
                log.info("=== monthly compaction for %d (months %s, this-month first) ===",
                         year, months)
                for m in months:
                    if not cont():
                        log.info("digest window closed — stopping before month %02d", m)
                        break
                    for topic in topics:
                        if not cont():
                            break
                        res = compact.compact_month(conn, cfg, topic, year, m, should_continue=cont)
                        log.info("[%s] %d-%02d compaction: %s", topic.slug, year, m, res)
            else:
                for topic in topics:
                    if args.compact_month:
                        y, m = (int(x) for x in args.compact_month.split("-"))
                        res = compact.compact_month(conn, cfg, topic, y, m, should_continue=cont)
                    else:
                        res = compact.compact_year(conn, cfg, topic, args.compact_year, should_continue=cont)
                    log.info("[%s] compaction: %s", topic.slug, res)
            digest.clear_text_cache()
            rag.build_index(conn)          # refresh cards (drops compacted-away papers)
            publish.publish(conn, cfg, deploy=not args.no_deploy)
        return 0

    since = dt.date.fromisoformat(args.since) if args.since else None
    stages = [args.stage] if args.stage else STAGES
    log.info("=== cycle A收集→B处理→C技能→D输出→E复盘 | topics=%s | stages=%s ===",
             [t.slug for t in topics], stages)

    # Pre-flight: verify the pinned models still respond; auto-fall-back to the
    # family's latest alias if a model ID was retired. Only when an LLM stage runs.
    llm_stage = ("digest" in stages or "trends" in stages) and not args.dry_run
    if llm_stage and not args.skip_model_check:
        report = modelcheck.check_and_resolve(cfg)
        log.info("model check:\n%s", modelcheck.report_str(report))

    # Digesting (LLM-heavy) is confined to the digest window so it doesn't burn the
    # rate limit during work hours; fetch + publish run anytime so the site keeps updating.
    digest_ok = args.ignore_window or _in_digest_window(cfg)
    can_llm = lambda: args.ignore_window or _in_digest_window(cfg)
    if ("digest" in stages or "trends" in stages) and not args.dry_run and not digest_ok:
        log.info("outside digest window %02d:00-%02d:00 — skipping digest/trends "
                 "(fetch + publish still run)", cfg.digest_window_start, cfg.digest_window_end)

    totals = {"downloaded": 0, "digested": 0}
    with state.connect() as conn:
        # Weekly-session guard. The daily fetch+digest ALWAYS runs; the "makeup" of
        # previous papers (the pending backlog + month/year compaction) runs only while
        # weekly usage is below the threshold. At/above it, `conserve` digests just
        # TODAY's collection (papers fetched today) and defers the backlog until the
        # week renews.
        used = state.week_usage(conn)
        budget = cfg.weekly_digest_budget
        conserve = (budget > 0 and not args.ignore_window
                    and used >= cfg.weekly_conserve_threshold * budget)
        if not args.dry_run:
            log.info("weekly usage: %d/%d digests (%.0f%%)%s", used, budget,
                     (100.0 * used / budget) if budget else 0,
                     " — CONSERVE: today's daily digest only, backlog makeup deferred" if conserve else "")
        # Below threshold → digest everything pending (daily + backlog makeup).
        # At/above → only papers fetched today.
        conserve_day = dt.date.today().isoformat() if conserve else None

        for topic in topics:
            if "fetch" in stages:
                if args.backfill_year is not None:
                    res = fetch.backfill_topic(conn, cfg, topic, args.backfill_year,
                                               cfg.max_papers_per_topic_per_run,
                                               dry_run=args.dry_run)
                else:
                    res = fetch.fetch_topic(conn, cfg, topic, dry_run=args.dry_run, since=since)
                totals["downloaded"] += len(res["downloaded"])
                if args.dry_run:
                    for p in res["new"]:
                        log.info("  NEW [%s %s] %s", p.source, p.year, p.title[:90])
            if "digest" in stages and not args.dry_run and digest_ok:
                totals["digested"] += digest.digest_topic(conn, cfg, topic, should_continue=can_llm,
                                                           fetched_on=conserve_day)

        # Build the RAG card cache before synthesis so trend/brief steps run off
        # compact cards (not full papers). Incremental — cheap when nothing changed.
        if not args.dry_run and digest_ok and ("trends" in stages or "publish" in stages):
            rag.build_index(conn)

        if "trends" in stages and not args.dry_run and digest_ok:
            for topic in topics:
                trends.analyze_topic(conn, cfg, topic)
                trends.summarize_today(conn, cfg, topic)

        # E 回流/复盘: once per ISO week, on the first in-window non-conserve full run.
        # One cheap LLM call; results land on the Review dashboard at publish.
        if (not args.dry_run and digest_ok and not args.stage and not conserve
                and review.due(conn)):
            log.info("[E] weekly review/复盘 due — running")
            review.run_review(conn, cfg)

        # Auto-compaction of prior-year papers (storage saver) — opt-in, daily runs only.
        # Scheduled month/year compaction (fires on the 1st; needs the window for refetch+digest).
        # Skipped in conserve mode — it's past-month fetch+digest we defer near the weekly limit.
        if not args.dry_run and not args.no_compact and not args.stage and digest_ok and not conserve:
            compact.run_scheduled(conn, cfg, topics, should_continue=can_llm)

        # Drop the (regenerable) text-extraction cache once digesting is done.
        if not args.dry_run and digest_ok and "digest" in stages:
            digest.clear_text_cache()

        if "publish" in stages and not args.dry_run:
            rag.build_index(conn)          # reflect any compaction drops in the cards
            publish.publish(conn, cfg, deploy=not args.no_deploy)

    log.info("=== run done | downloaded=%d digested=%d compacted=%d ===",
             totals["downloaded"], totals["digested"], totals.get("compacted", 0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
