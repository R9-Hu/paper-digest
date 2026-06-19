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
import math
import re
import time

import requests

from . import config, llm, naming, skills, state
from .config import Config, Topic
from .models import Paper
from .sources import arxiv_source, conf_source, hf_source, impact

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


# Award/selectivity signals in the arXiv `comment` field (e.g. "Accepted to CVPR
# 2025 (Oral)", "Best Paper Award"). Higher tiers => stronger high-impact signal.
_AWARD_RE = re.compile(
    r"\b(best paper|outstanding paper|award|oral|spotlight|highlight|notable)\b", re.IGNORECASE)
_AWARD_WEIGHT = {"best paper": 2500, "outstanding paper": 2500, "award": 2000,
                 "oral": 800, "spotlight": 500, "highlight": 400, "notable": 400}


def _award_bonus(comment: str) -> float:
    best = 0.0
    for m in _AWARD_RE.finditer(comment or ""):
        best = max(best, _AWARD_WEIGHT.get(m.group(1).lower(), 0))
    return best


def impact_score(venue: str, comment: str, citations: float, influential: float,
                 published, year: int) -> float:
    """High-impact ranking, shared by daily selection and monthly compaction.

    High citations (recent-5yr proxy) and top-conference awards dominate; venue
    acceptance, then recency within the year, break ties. Citations are 0 for
    brand-new papers, so for the current year the award/venue signal leads."""
    s = 0.0
    if venue:
        s += 1000.0
    s += _award_bonus(comment)
    s += math.log1p(max(0.0, float(citations or 0))) * 150.0   # diminishing returns
    s += float(influential or 0) * 60.0                        # influential cites weigh more
    if published:
        s += (published - dt.date(year, 1, 1)).days * 0.1
    return s


def _score(p: Paper, year: int) -> float:
    return impact_score(p.venue, p.extra.get("comment", ""),
                        p.extra.get("citations", 0), p.extra.get("influential", 0),
                        p.published, year)


RANK_SYSTEM = (
    "You are a meticulous research curator with broad, current knowledge of AI/ML "
    "research groups, labs, authors, and venues. You judge which new papers are most "
    "likely to be high-impact and worth a busy researcher's attention."
)
_RANK_PROMPT = (
    'Topic: "{topic}".\n'
    "From the {n} candidate papers below, choose the {k} MOST likely to be "
    "high-impact and influential for a researcher tracking this topic. Weigh: the "
    "reputation and track record of the authors and their research group/lab, the "
    "venue (top-tier acceptance/awards), and the novelty and significance of the work.\n"
    "Return ONLY a JSON array of the {k} chosen items, most important first. Each item is "
    '{{"i": <candidate number>, "why": "<<=15-word reason this paper is worth reading>"}}. '
    'Example: [{{"i": 3, "why": "DeepMind RLHF team; NeurIPS oral; first to scale verifier rewards"}}]. '
    "No prose outside the JSON.\n\n{candidates}"
)


# Bounds so a single ranking call stays cheap: never feed the LLM more than
# RANK_POOL_MAX candidates, and skip LLM curation when we're keeping a large set
# (k high) — there the heuristic is fine and the call would be huge.
RANK_POOL_MAX = 200
RANK_K_MAX = 150


def _llm_rank(cfg: Config, topic: Topic, papers: list[Paper], k: int) -> list[Paper] | None:
    """Ask the LLM to pick the `k` highest-impact papers from `papers`.

    The model weighs the reputation/track record of the authors and their group,
    the venue, and the novelty/significance of the work — i.e. "whose paper should
    we download". Returns the chosen papers (most important first), or None on any
    failure so the caller can fall back to the deterministic heuristic."""
    if len(papers) <= k:
        return papers
    lines = []
    for i, p in enumerate(papers):
        authors = ", ".join(p.authors[:5]) + (" et al." if len(p.authors) > 5 else "")
        abstract = " ".join((p.abstract or "").split())[:240]
        venue = f" [{p.venue}]" if p.venue else ""
        lines.append(f"{i}. {p.title}{venue} — {authors}. {abstract}")
    sk = skills.load_skill("impact-ranking", {"system": RANK_SYSTEM, "prompt": _RANK_PROMPT})
    prompt = sk.prompt.format(topic=topic.name, n=len(papers), k=k, candidates="\n".join(lines))
    try:
        # Don't block fetch/publish on a usage limit — fall back to the heuristic.
        out = llm.run_claude(prompt, cfg.rank_model, cfg,
                             system=skills.with_profile(sk.system, cfg), wait_on_limit=False)
    except llm.LLMError as e:
        log.warning("[%s] LLM rank failed (%s); using heuristic", topic.slug, e)
        return None
    picks = _parse_rank(out, len(papers))
    if not picks:
        log.warning("[%s] LLM rank returned nothing parseable; using heuristic", topic.slug)
        return None
    chosen, seen = [], set()
    for idx, why in picks:
        if idx in seen:
            continue
        seen.add(idx)
        p = papers[idx]
        if why:
            p.extra["select_reason"] = why
        chosen.append(p)
    return chosen[:k] if chosen else None


def _parse_rank(out: str, n: int) -> list[tuple[int, str]]:
    """Parse the ranker's JSON ([{i, why}, ...] preferred; bare [i, ...] tolerated)."""
    import json
    m = re.search(r"\[.*\]", out or "", re.DOTALL)
    if not m:
        return []
    picks: list[tuple[int, str]] = []
    try:
        data = json.loads(m.group(0))
        for item in data:
            if isinstance(item, dict) and "i" in item:
                idx = int(item["i"])
                why = " ".join(str(item.get("why", "")).split())[:200]
            else:
                idx, why = int(item), ""
            if 0 <= idx < n:
                picks.append((idx, why))
    except (ValueError, TypeError):
        for idx in (int(x) for x in re.findall(r"\d+", m.group(0))):
            if 0 <= idx < n:
                picks.append((idx, ""))
    return picks


def select_top(cfg: Config, topic: Topic, papers: list[Paper], k: int) -> list[Paper]:
    """Pick the top-`k` papers by impact: LLM judgment when enabled, else the
    deterministic venue/award/(citation)/recency heuristic (also the fallback)."""
    if k <= 0 or not papers:
        return []
    if len(papers) <= k:
        return papers
    year = papers[0].year
    heur = sorted(papers, key=lambda p: _score(p, year), reverse=True)
    if cfg.llm_rank and k <= RANK_K_MAX:
        pool = heur[:RANK_POOL_MAX] if len(heur) > RANK_POOL_MAX else heur
        ranked = _llm_rank(cfg, topic, pool, k)
        if ranked is not None:
            return ranked
    return heur[:k]


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
    # Pull a wider pool than `cap` so the high-impact ranking has something to choose from.
    candidates = gather_candidates(topic, earliest, max(cap * 5, 50))
    fresh = [p for p in candidates if _is_new_or_newer(conn, p, topic.slug)]

    # When more than `cap` are new, keep the highest-impact ones — and fill the
    # current month first (so this month's coverage is complete before older months).
    impact.annotate(fresh, conn)   # enriches the heuristic fallback if an S2 key is set; else a no-op
    today = dt.date.today()
    this_month = [p for p in fresh
                  if p.published and (p.published.year, p.published.month) == (today.year, today.month)]
    older = [p for p in fresh if p not in this_month]

    if dry_run:                    # preview: deterministic only (no LLM calls)
        this_month.sort(key=lambda p: _score(p, p.year), reverse=True)
        older.sort(key=lambda p: _score(p, p.year), reverse=True)
        fresh = (this_month + older)[:cap]
        log.info("[%s] %d candidates, %d selected (this-month %d, cap %d, dry-run)",
                 topic.slug, len(candidates), len(fresh), len(this_month), cap)
        return {"candidates": len(candidates), "new": fresh, "downloaded": []}

    # LLM judges which papers/groups are worth downloading (heuristic fallback).
    selected = select_top(cfg, topic, this_month, cap)
    selected += select_top(cfg, topic, older, cap - len(selected))
    fresh = selected[:cap]

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

    pool = _dedup(pool)
    impact.annotate(pool, conn)                       # enriches heuristic if an S2 key is set
    new = [p for p in pool if _is_new_or_newer(conn, p, topic.slug)]
    if dry_run:                                        # preview: deterministic, no LLM
        selected = sorted(new, key=lambda p: _score(p, year), reverse=True)[:target]
        log.info("[%s] backfill %d: pool=%d, selected=%d (dry-run)",
                 topic.slug, year, len(pool), len(selected))
        return {"pool": len(pool), "new": selected, "downloaded": []}

    selected = select_top(cfg, topic, new, target)     # LLM-judged when target is selective
    log.info("[%s] backfill %d: pool=%d, selected=%d", topic.slug, year, len(pool), len(selected))

    downloaded = _download_selected(conn, cfg, topic, selected)
    state.set_last_run(conn, topic.slug, len(downloaded))
    conn.commit()
    log.info("[%s] backfill %d downloaded %d papers", topic.slug, year, len(downloaded))
    return {"pool": len(pool), "new": selected, "downloaded": downloaded}
