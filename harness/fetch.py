"""Agent 1 — Collector.

Gathers candidate papers per topic from arXiv + HuggingFace + (best-effort)
conferences, dedups against the sqlite state, downloads new PDFs, and renames
them to "[<Place> <Year>] <Title>.pdf".
"""
from __future__ import annotations

import datetime as dt
import logging

import requests

from . import config, naming, state
from .config import Config, Topic
from .models import Paper
from .sources import arxiv_source, conf_source, hf_source

log = logging.getLogger("harness.fetch")

UA = {"User-Agent": "paperDigest/1.0 (research digest harness)"}
DOWNLOAD_TIMEOUT = 60


def gather_candidates(topic: Topic, earliest: dt.date, cap: int) -> list[Paper]:
    """Collect + dedup candidates across sources (no state/DB involvement)."""
    candidates: list[Paper] = []
    try:
        candidates += arxiv_source.search(topic.arxiv_categories, topic.keywords, earliest, cap)
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

    # Dedup by canonical_id; merge a venue in if a duplicate carries one.
    merged: dict[str, Paper] = {}
    for p in candidates:
        if p.canonical_id in merged:
            if not merged[p.canonical_id].venue and p.venue:
                merged[p.canonical_id].venue = p.venue
            continue
        merged[p.canonical_id] = p
    return list(merged.values())


def _unique_path(directory, stem: str, ext: str = "pdf"):
    path = directory / f"{stem}.{ext}"
    n = 2
    while path.exists():
        path = directory / f"{stem} ({n}).{ext}"
        n += 1
    return path


def _download(url: str, dest) -> bool:
    try:
        with requests.get(url, headers=UA, stream=True, timeout=DOWNLOAD_TIMEOUT) as r:
            r.raise_for_status()
            tmp = dest.with_suffix(dest.suffix + ".part")
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1 << 15):
                    if chunk:
                        f.write(chunk)
            # Basic sanity: a real PDF starts with %PDF and isn't tiny.
            if tmp.stat().st_size < 1024 or tmp.read_bytes()[:4] != b"%PDF":
                tmp.unlink(missing_ok=True)
                return False
            tmp.rename(dest)
        return True
    except (requests.RequestException, OSError) as e:
        log.warning("download failed %s: %s", url, e)
        return False


def fetch_topic(conn, cfg: Config, topic: Topic, dry_run: bool = False,
                since: dt.date | None = None) -> dict:
    earliest = since or topic.earliest_date
    cap = cfg.max_papers_per_topic_per_run
    candidates = gather_candidates(topic, earliest, cap)

    # Keep only genuinely new (per topic) papers, newest first.
    fresh = [p for p in candidates if not state.is_seen(conn, p.canonical_id, topic.slug)]
    fresh.sort(key=lambda p: p.published or dt.date.min, reverse=True)
    fresh = fresh[:cap]

    if dry_run:
        log.info("[%s] %d candidates, %d new (dry-run)", topic.slug, len(candidates), len(fresh))
        return {"candidates": len(candidates), "new": fresh, "downloaded": []}

    out_dir = config.PAPER_DIR / topic.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Paper] = []
    for p in fresh:
        stem = naming.build_stem(p.source, p.year, p.title)
        dest = _unique_path(out_dir, stem)
        if not p.pdf_url or not _download(p.pdf_url, dest):
            log.info("[%s] skip (no/failed PDF): %s", topic.slug, p.title[:80])
            continue
        rel = dest.relative_to(config.ROOT).as_posix()
        state.record_fetched(conn, p, topic.slug, rel)
        downloaded.append(p)
        log.info("[%s] saved: %s", topic.slug, dest.name)

    state.set_last_run(conn, topic.slug, len(downloaded))
    log.info("[%s] downloaded %d new papers", topic.slug, len(downloaded))
    return {"candidates": len(candidates), "new": fresh, "downloaded": downloaded}
