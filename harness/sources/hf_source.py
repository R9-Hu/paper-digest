"""HuggingFace daily-papers source.

HF curates a daily list of (mostly arXiv) papers. We walk back day-by-day from
today, keyword-filter, and emit Paper objects that download from arXiv. A
`window_days` cap keeps the first backfill from hammering the API for years.
"""
from __future__ import annotations

import datetime as dt

import requests

from ..models import Paper

API = "https://huggingface.co/api/daily_papers"
DEFAULT_WINDOW_DAYS = 60
TIMEOUT = 20


def _matches(text: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    low = text.lower()
    return any(k.lower() in low for k in keywords)


def _fetch_day(date: dt.date) -> list[dict]:
    try:
        resp = requests.get(API, params={"date": date.isoformat()}, timeout=TIMEOUT)
        if resp.status_code != 200:
            return []
        data = resp.json()
        return data if isinstance(data, list) else []
    except (requests.RequestException, ValueError):
        return []


def search(
    keywords: list[str],
    earliest: dt.date,
    max_results: int,
    window_days: int = DEFAULT_WINDOW_DAYS,
) -> list[Paper]:
    today = dt.date.today()
    start = max(earliest, today - dt.timedelta(days=window_days))
    papers: list[Paper] = []
    seen: set[str] = set()

    day = today
    while day >= start and len(papers) < max_results:
        for item in _fetch_day(day):
            p = item.get("paper", item) if isinstance(item, dict) else {}
            arxiv_id = str(p.get("id") or "").strip()
            if not arxiv_id or arxiv_id in seen:
                continue
            title = (p.get("title") or item.get("title") or "").strip()
            summary = (p.get("summary") or "").strip()
            if not _matches(f"{title} {summary}", keywords):
                continue
            seen.add(arxiv_id)
            pub_raw = p.get("publishedAt") or item.get("publishedAt") or ""
            pub_ts = ""
            try:
                pub_dt = dt.datetime.fromisoformat(pub_raw.replace("Z", "+00:00"))
                pub, pub_ts = pub_dt.date(), pub_dt.isoformat()
            except (ValueError, AttributeError):
                pub = day
            authors = [a.get("name", "") for a in (p.get("authors") or []) if isinstance(a, dict)]
            papers.append(
                Paper(
                    canonical_id=f"arxiv:{arxiv_id}",
                    source="HuggingFace",
                    title=title,
                    authors=authors,
                    abstract=summary,
                    pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                    abs_url=f"https://huggingface.co/papers/{arxiv_id}",
                    published=pub,
                    published_ts=pub_ts,
                    extra={"upvotes": p.get("upvotes")},
                )
            )
            if len(papers) >= max_results:
                break
        day -= dt.timedelta(days=1)
    return papers
