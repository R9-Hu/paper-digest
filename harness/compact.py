"""Periodic compaction — keep each period's best N papers per topic.

Policy:
  * 1st of each month → for the PREVIOUS month, keep the top `monthly_keep`
    (default 100) papers per topic.
  * 1st of each year  → for the PREVIOUS year, keep the top `yearly_keep`
    (default 400) papers per topic.

For a window we:
  1. Re-query the sources for that window and **pull in the highest-impact papers
     we're missing** (the small daily cap excludes good papers), filling the window
     up to `keep_n`, then digest them (LLM — runs only inside the digest window).
  2. Rank the window's digested papers by the same high-impact standard,
     **keep the top N** — storage-compacted (digest trimmed to essentials, PDF
     deleted) — and **drop the rest** (digest + PDF removed; row marked `dropped`
     so it no longer appears, and won't be re-fetched).

Ranking uses high citations (Semantic Scholar, recent-5yr proxy) and top-conference
awards/acceptance, then recency — see fetch.impact_score().

Run manually:  --compact-month YYYY-MM   |   --compact-year YYYY
Scheduled: the daily pipeline calls run_scheduled() (fires on the 1st, in-window).
"""
from __future__ import annotations

import datetime as dt
import logging
import re

from . import config, digest, fetch, state
from .sources import impact
from .config import Config, Topic

log = logging.getLogger("harness.compact")

KEEP_SECTIONS = ("tl;dr", "key contribution", "results")  # retained when storage-compacting


# --------------------------------------------------------------------------- #
# Storage compaction of a single kept paper (trim digest + delete PDF)
# --------------------------------------------------------------------------- #
def _trim_digest(md: str) -> str:
    parts = md.split("---", 2)
    head, body = (f"---{parts[1]}---", parts[2]) if len(parts) == 3 else ("", md)
    chunks = re.split(r"(?m)^##[ \t]+", body)
    pre = chunks[0].rstrip()
    kept = []
    for chunk in chunks[1:]:
        nl = chunk.find("\n")
        title = (chunk[:nl] if nl != -1 else chunk).strip().lower()
        if any(title.startswith(k) for k in KEEP_SECTIONS):
            kept.append("## " + chunk.rstrip())
    out = (head + "\n" if head else "") + pre + "\n\n" + "\n\n".join(kept) + "\n"
    return out + "\n> [!note] Compacted — PDF removed to save storage; digest trimmed to essentials.\n"


def compact_paper(conn, cfg: Config, row) -> bool:
    """Trim a kept paper's digest to essentials and delete its PDF/text cache."""
    rel = row["digest_path"]
    if rel and (config.ROOT / rel).exists():
        p = config.ROOT / rel
        try:
            p.write_text(_trim_digest(p.read_text(encoding="utf-8")), encoding="utf-8")
        except OSError as e:
            log.warning("compact: cannot rewrite %s: %s", rel, e)
            return False
    if row["pdf_path"]:
        (config.ROOT / row["pdf_path"]).unlink(missing_ok=True)
    (config.TEXT_DIR / f"{row['canonical_id'].split(':', 1)[-1]}.txt").unlink(missing_ok=True)
    state.mark_compacted(conn, row["canonical_id"], row["topic_slug"], rel)
    return True


def _drop_paper(conn, row) -> None:
    """Remove a paper that fell outside the keep-N cap (digest + PDF deleted)."""
    if row["digest_path"]:
        (config.ROOT / row["digest_path"]).unlink(missing_ok=True)
    if row["pdf_path"]:
        (config.ROOT / row["pdf_path"]).unlink(missing_ok=True)
    (config.TEXT_DIR / f"{row['canonical_id'].split(':', 1)[-1]}.txt").unlink(missing_ok=True)
    conn.execute(
        """UPDATE papers SET digest_status='dropped', digest_path=NULL, pdf_path=NULL
           WHERE canonical_id=? AND topic_slug=?""",
        (row["canonical_id"], row["topic_slug"]),
    )


# --------------------------------------------------------------------------- #
# Window compaction
# --------------------------------------------------------------------------- #
def _window_rows(conn, slug: str, start: dt.date, end: dt.date):
    return conn.execute(
        """SELECT * FROM papers
           WHERE topic_slug=? AND digest_status IN ('digested','compacted')
                 AND published >= ? AND published <= ?
           ORDER BY published DESC""",
        (slug, start.isoformat(), end.isoformat()),
    ).fetchall()


def _row_score(row, impacts: dict, year: int) -> float:
    """High-impact score for an already-stored paper (no `comment` available)."""
    c, i = impacts.get(row["canonical_id"], (0, 0))
    pub = None
    try:
        pub = dt.date.fromisoformat(row["published"]) if row["published"] else None
    except (ValueError, TypeError):
        pub = None
    return fetch.impact_score(row["venue"], "", c, i, pub, year)


def compact_window(conn, cfg: Config, topic: Topic, start: dt.date, end: dt.date,
                   keep_n: int, should_continue=None, refetch: bool = True,
                   dry_run: bool = False, archive: bool = False) -> dict:
    """Keep the top `keep_n` papers in the window, drop the rest.

    `archive=False` (monthly): kept papers keep their full digest + PDF (the PDF
    cache is retained up to a year). `archive=True` (yearly): kept papers are
    storage-archived — digest trimmed to essentials and PDF/text removed."""
    slug = topic.slug
    added = 0

    # (1) Fill the window up to keep_n with the highest-impact papers we're missing
    #     (the LLM judges which groups/papers matter; heuristic fallback), then digest.
    if refetch and not dry_run and (should_continue is None or should_continue()):
        try:
            pool = fetch.gather_candidates(topic, start, keep_n * 3, until=end)
        except Exception as e:  # noqa: BLE001
            log.warning("[%s] compact refetch failed: %s", slug, e)
            pool = []
        impact.annotate(pool, conn)
        have = len(_window_rows(conn, slug, start, end))
        missed = [p for p in pool if state.get_version(conn, p.canonical_id, slug) is None]
        need = max(0, keep_n - have)
        if missed and need:
            chosen = fetch.select_top(cfg, topic, missed, need)
            added = len(fetch._download_selected(conn, cfg, topic, chosen))
        if added:
            digest.digest_topic(conn, cfg, topic, should_continue=should_continue)

    # (2) Rank the window by the same high-impact standard, keep top N, drop the rest.
    rows = _window_rows(conn, slug, start, end)
    impacts = impact.lookup(conn, [r["canonical_id"] for r in rows])
    rows = sorted(rows, key=lambda r: _row_score(r, impacts, start.year), reverse=True)
    keep, drop = rows[:keep_n], rows[keep_n:]
    result = {"in_window": len(rows), "keep": len(keep), "drop": len(drop), "added": added}
    if dry_run:
        return result
    if archive:                       # yearly: trim kept + remove their PDFs
        for r in keep:
            compact_paper(conn, cfg, r)
    for r in drop:                    # always remove the papers beyond the cap
        _drop_paper(conn, r)
    conn.commit()
    log.info("[%s] compacted %s..%s: kept %d (%s), dropped %d, added %d",
             slug, start, end, len(keep), "archived" if archive else "full",
             len(drop), added)
    return result


def compact_month(conn, cfg: Config, topic: Topic, year: int, month: int, **kw) -> dict:
    start = dt.date(year, month, 1)
    end = (dt.date(year + (month == 12), (month % 12) + 1, 1) - dt.timedelta(days=1))
    return compact_window(conn, cfg, topic, start, end, cfg.monthly_keep, **kw)


def compact_year(conn, cfg: Config, topic: Topic, year: int, **kw) -> dict:
    kw.setdefault("archive", True)   # yearly archive: trim + remove PDFs/text cache
    return compact_window(conn, cfg, topic, dt.date(year, 1, 1), dt.date(year, 12, 31),
                          cfg.yearly_keep, **kw)


def run_scheduled(conn, cfg: Config, topics, should_continue=None) -> int:
    """On the 1st of a month/year, compact the previous month/year (once each)."""
    today = dt.date.today()
    if today.day != 1:
        return 0
    n = 0
    prev_end = today - dt.timedelta(days=1)          # last day of previous month
    ym = prev_end.strftime("%Y-%m")
    if state.meta_get(conn, "compacted_month") != ym:
        log.info("monthly compaction for %s (keep %d/topic)", ym, cfg.monthly_keep)
        for t in topics:
            if should_continue and not should_continue():
                return n
            compact_month(conn, cfg, t, prev_end.year, prev_end.month, should_continue=should_continue)
        state.meta_set(conn, "compacted_month", ym)
        conn.commit()
        n += 1
    if today.month == 1:                              # Jan 1 → compact last year
        ly = today.year - 1
        if state.meta_get(conn, "compacted_year") != str(ly):
            log.info("yearly compaction for %d (keep %d/topic)", ly, cfg.yearly_keep)
            for t in topics:
                if should_continue and not should_continue():
                    return n
                compact_year(conn, cfg, t, ly, should_continue=should_continue)
            state.meta_set(conn, "compacted_year", str(ly))
            conn.commit()
            n += 1
    return n
