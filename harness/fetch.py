"""Agent 1 — Collector.

Daily mode: gather newest candidates per topic from arXiv + HuggingFace +
(best-effort) conferences, dedup against the sqlite state, download new PDFs, and
re-fetch when a newer version appears (so links/digests track the latest version).

Backfill mode: for a given past year, pull a large candidate pool, rank it
heuristically (top-tier-conference acceptance first, then HF upvotes / recency),
and take the top N per topic.
"""
from __future__ import annotations

import datetime as dt
import logging
import time

import requests

from . import config, naming, state
from .config import Config, Topic
from .models import Paper
from .sources import arxiv_source, conf_source, hf_source

log = logging.getLogger("harness.fetch")

UA = {"User-Agent": "paperDigest/1.0 (research digest harness)"}
DOWNLOAD_TIMEOUT = 60


def _dedup(candidates: list[Paper]) -> list[Paper]:
    """Dedup by canonical_id; merge a venue/doi in if a duplicate carries one."""
    merged: dict[str, Paper] = {}
    for p in candidates:
        cur = merged.get(p.canonical_id)
        if cur is None:
            merged[p.canonical_id] = p
            continue
        if not cur.venue and p.venue:
            cur.venue = p.venue
        if not cur.doi and p.doi:
            cur.doi = p.doi
        cur.version = max(cur.version, p.version)
    return list(merged.values())


def gather_candidates(topic: Topic, earliest: dt.date, cap: int,
                      until: dt.date | None = None) -> list[Paper]:
    candidates: list[Paper] = []
    try:
        candidates += arxiv_source.search(topic.arxiv_categories, topic.keywords,
                                          earliest, cap, until=until)
    except Exception as e:  # noqa: BLE001 — never let one source kill the run
        log.warning("[%s] arxiv source failed: %s", topic.slug, e)
    if topic.huggingface:
        try:
            candidates += hf_source.search(topic.keywords, earliest, cap)
        except Exception as e:  # noqa: BLE001
            log.warning("[%s] huggingface source failed: %s", topic.slug, e)
    if topic.conferences:
        try:
            candidates += conf_source.search(topic.conferences, topic.keywords, earliest, cap)
        except Exception as e:  # noqa: BLE001
            log.warning("[%s] conference source failed: %s", topic.slug, e)
    return _dedup(candidates)


def _score(p: Paper, year: int) -> float:
    """Heuristic 'quality' proxy (no external citation data): top-tier-conference
    acceptance dominates, then HF upvotes, then recency within the year."""
    s = 0.0
    if p.venue:
        s += 1000.0
    s += min(float(p.extra.get("upvotes") or 0), 500.0)
    if p.published:
        s += (p.published - dt.date(year, 1, 1)).days * 0.1
    return s


def _is_new_or_newer(conn, p: Paper, topic_slug: str) -> bool:
    """New paper, or a newer version of one we already have (→ re-digest)."""
    sv = state.get_version(conn, p.canonical_id, topic_slug)
    return sv is None or p.version > sv


def _unique_path(directory, stem: str, ext: str = "pdf"):
    path = directory / f"{stem}.{ext}"
    n = 2
    while path.exists():
        path = directory / f"{stem} ({n}).{ext}"
        n += 1
    return path


def _download(url: str, dest) -> bool:
    for attempt in range(4):
        try:
            with requests.get(url, headers=UA, stream=True, timeout=DOWNLOAD_TIMEOUT) as r:
                if r.status_code in (429, 403, 503):  # arXiv throttling
                    wait = 10 * (attempt + 1)
                    log.warning("download %s on %s; backoff %ds", r.status_code, url, wait)
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".part")
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1 << 15):
                        if chunk:
                            f.write(chunk)
                if tmp.stat().st_size < 1024 or tmp.read_bytes()[:4] != b"%PDF":
                    tmp.unlink(missing_ok=True)
                    return False
                tmp.rename(dest)
            return True
        except (requests.RequestException, OSError) as e:
            log.warning("download failed %s: %s", url, e)
            time.sleep(5)
    return False


def _download_selected(conn, cfg: Config, topic: Topic, selected: list[Paper]) -> list[Paper]:
    out_dir = config.PAPER_DIR / topic.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Paper] = []
    for p in selected:
        stem = naming.build_stem(p.source, p.year, p.title)
        dest = _unique_path(out_dir, stem)
        if not p.pdf_url or not _download(p.pdf_url, dest):
            log.info("[%s] skip (no/failed PDF): %s", topic.slug, p.title[:80])
            continue
        rel = dest.relative_to(config.ROOT).as_posix()
        state.record_fetched(conn, p, topic.slug, rel)  # resets status→fetched (re-digest)
        conn.commit()
        downloaded.append(p)
        log.info("[%s] saved v%d: %s", topic.slug, p.version, dest.name)
    return downloaded


def fetch_topic(conn, cfg: Config, topic: Topic, dry_run: bool = False,
                since: dt.date | None = None) -> dict:
    """Daily incremental fetch (newest-first, version-aware)."""
    earliest = since or topic.earliest_date
    cap = cfg.max_papers_per_topic_per_run
    candidates = gather_candidates(topic, earliest, cap)
    fresh = [p for p in candidates if _is_new_or_newer(conn, p, topic.slug)]
    fresh.sort(key=lambda p: p.published or dt.date.min, reverse=True)
    fresh = fresh[:cap]

    if dry_run:
        log.info("[%s] %d candidates, %d new/updated (dry-run)", topic.slug, len(candidates), len(fresh))
        return {"candidates": len(candidates), "new": fresh, "downloaded": []}

    downloaded = _download_selected(conn, cfg, topic, fresh)
    state.set_last_run(conn, topic.slug, len(downloaded))
    conn.commit()
    log.info("[%s] downloaded %d new/updated papers", topic.slug, len(downloaded))
    return {"candidates": len(candidates), "new": fresh, "downloaded": downloaded}


def backfill_topic(conn, cfg: Config, topic: Topic, year: int, target: int,
                   dry_run: bool = False) -> dict:
    """Pull the top `target` papers for `year`, ranked by the quality heuristic."""
    start, end = dt.date(year, 1, 1), dt.date(year, 12, 31)
    pool: list[Paper] = []
    try:
        pool += arxiv_source.search(topic.arxiv_categories, topic.keywords,
                                    start, target * 4, until=end)
    except Exception as e:  # noqa: BLE001
        log.warning("[%s] arxiv backfill failed: %s", topic.slug, e)
    if topic.conferences:
        try:
            pool += [p for p in conf_source.search(topic.conferences, topic.keywords, start, target * 2)
                     if p.published and p.published.year == year]
        except Exception as e:  # noqa: BLE001
            log.warning("[%s] conf backfill failed: %s", topic.slug, e)

    ranked = sorted(_dedup(pool), key=lambda p: _score(p, year), reverse=True)
    selected, seen_new = [], 0
    for p in ranked:
        if _is_new_or_newer(conn, p, topic.slug):
            selected.append(p)
            seen_new += 1
        if seen_new >= target:
            break

    log.info("[%s] backfill %d: pool=%d, selected=%d (top-tier first)",
             topic.slug, year, len(ranked), len(selected))
    if dry_run:
        return {"pool": len(ranked), "new": selected, "downloaded": []}

    downloaded = _download_selected(conn, cfg, topic, selected)
    state.set_last_run(conn, topic.slug, len(downloaded))
    conn.commit()
    log.info("[%s] backfill %d downloaded %d papers", topic.slug, year, len(downloaded))
    return {"pool": len(ranked), "new": selected, "downloaded": downloaded}
