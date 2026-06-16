"""Citation/impact lookup via the Semantic Scholar Graph API.

Used to rank papers by impact (high citations) alongside top-tier-venue
acceptance/awards. For the recent papers this harness tracks, the total
`citationCount` is effectively "citations in the last ~5 years" (the papers
aren't old enough to have older citations), so we use it directly.

Best-effort: any network/API failure leaves citations at 0 and the caller
falls back to the venue/award/recency heuristic — the run never breaks.
Results are cached in the `impact` table on a TTL so we don't re-query nightly.
"""
from __future__ import annotations

import datetime as dt
import logging
import os
import time

import requests

log = logging.getLogger("harness.impact")

S2_BATCH = "https://api.semanticscholar.org/graph/v1/paper/batch"
FIELDS = "citationCount,influentialCitationCount"
UA = {"User-Agent": "paperDigest/1.0 (research digest harness)"}
TTL_DAYS = 21          # citation counts move slowly; refresh every few weeks
CHUNK = 100            # smaller batches survive the unauthenticated rate limit better
# An (optional) API key lifts the shared ~1 req/s limit dramatically. Get one free at
# https://www.semanticscholar.org/product/api and export SEMANTIC_SCHOLAR_API_KEY.
_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()


def _headers() -> dict:
    h = dict(UA)
    if _API_KEY:
        h["x-api-key"] = _API_KEY
    return h


def _s2_id(canonical_id: str) -> str | None:
    """Our 'arxiv:2501.01234' -> Semantic Scholar 'ARXIV:2501.01234'."""
    if canonical_id.startswith("arxiv:"):
        return "ARXIV:" + canonical_id.split(":", 1)[1]
    return None


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def _batch(s2_ids: list[str]):
    """POST one batch to S2; return the aligned result list, or None on failure."""
    for attempt in range(5):
        try:
            r = requests.post(S2_BATCH, params={"fields": FIELDS},
                              json={"ids": s2_ids}, headers=_headers(), timeout=30)
            if r.status_code == 429:                       # rate limited — back off and retry
                wait = float(r.headers.get("Retry-After") or 0) or 8 * (attempt + 1)
                time.sleep(min(wait, 60))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as e:
            log.warning("S2 batch failed (%d ids): %s", len(s2_ids), e)
            time.sleep(3 * (attempt + 1))
    return None


def lookup(conn, canonical_ids, max_age_days: int = TTL_DAYS) -> dict:
    """Return {canonical_id: (citations, influential)} for arXiv ids.

    Serves fresh-enough rows from the `impact` cache; queries S2 for the rest
    and writes the results back. Non-arXiv / unresolved ids map to (0, 0)."""
    out: dict[str, tuple[int, int]] = {}
    need: list[str] = []
    now = dt.datetime.now()
    for cid in dict.fromkeys(canonical_ids):           # unique, order-preserving
        row = conn.execute(
            "SELECT citations, influential, fetched_ts FROM impact WHERE canonical_id=?",
            (cid,),
        ).fetchone()
        if row and row["fetched_ts"]:
            try:
                fresh = (now - dt.datetime.fromisoformat(row["fetched_ts"])).days <= max_age_days
            except ValueError:
                fresh = False
            if fresh:
                out[cid] = (row["citations"] or 0, row["influential"] or 0)
                continue
        if _s2_id(cid):
            need.append(cid)

    for chunk in _chunks(need, CHUNK):
        recs = _batch([_s2_id(c) for c in chunk])
        if recs is None:
            continue
        ts = now.isoformat(timespec="seconds")
        for cid, rec in zip(chunk, recs):
            c = (rec or {}).get("citationCount") or 0
            i = (rec or {}).get("influentialCitationCount") or 0
            out[cid] = (c, i)
            conn.execute(
                "INSERT OR REPLACE INTO impact (canonical_id, citations, influential, fetched_ts) "
                "VALUES (?,?,?,?)", (cid, c, i, ts),
            )
        conn.commit()
        time.sleep(1.0)                                # be polite to the shared API
    return out


def annotate(papers, conn) -> None:
    """Stamp p.extra['citations'/'influential'] on each Paper (best-effort)."""
    if conn is None or not papers:
        return
    m = lookup(conn, [p.canonical_id for p in papers])
    for p in papers:
        c, i = m.get(p.canonical_id, (0, 0))
        p.extra["citations"] = c
        p.extra["influential"] = i
