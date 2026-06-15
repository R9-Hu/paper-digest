"""arXiv source — query by category + keyword within a date window.

Built on the `arxiv` package (the official export API wrapper, which rate-limits
politely). Returns source-agnostic Paper objects.
"""
from __future__ import annotations

import datetime as dt
import re

import arxiv

from ..models import Paper

# Conference acronyms we try to detect from the arXiv `comment` field.
_VENUES = [
    "CVPR", "ICCV", "ECCV", "NeurIPS", "NIPS", "ICLR", "ICML", "AAAI", "ACL",
    "EMNLP", "NAACL", "MICCAI", "IPMI", "ISBI", "MIDL", "KDD", "SIGGRAPH",
    "INTERSPEECH", "WACV", "BMVC", "COLM", "TMLR",
]
_VENUE_RE = re.compile(r"\b(" + "|".join(_VENUES) + r")\b", re.IGNORECASE)


def _detect_venue(comment: str | None) -> str:
    if not comment:
        return ""
    m = _VENUE_RE.search(comment)
    if not m:
        return ""
    venue = m.group(1).upper()
    # Try to capture a trailing year, e.g. "Accepted to CVPR 2025".
    ym = re.search(re.escape(m.group(1)) + r"\s*'?(\d{2,4})", comment, re.IGNORECASE)
    if ym:
        venue += " " + ym.group(1)
    return venue


def _build_query(categories: list[str], keywords: list[str]) -> str:
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    kw_clause = " OR ".join(f'all:"{k}"' for k in keywords)
    parts = []
    if cat_clause:
        parts.append(f"({cat_clause})")
    if kw_clause:
        parts.append(f"({kw_clause})")
    return " AND ".join(parts)


def search(
    categories: list[str],
    keywords: list[str],
    earliest: dt.date,
    max_results: int,
) -> list[Paper]:
    query = _build_query(categories, keywords)
    if not query:
        return []

    client = arxiv.Client(page_size=100, delay_seconds=3.0, num_retries=3)
    # Over-fetch a bit so the date filter still yields up to max_results.
    search = arxiv.Search(
        query=query,
        max_results=max_results * 5,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers: list[Paper] = []
    for r in client.results(search):
        pub = r.published.date()
        if pub < earliest:
            break  # results are newest-first, so we can stop here
        short_id = r.get_short_id()             # e.g. "2501.01234v2"
        base_id = re.sub(r"v\d+$", "", short_id)  # drop version suffix
        papers.append(
            Paper(
                canonical_id=f"arxiv:{base_id}",
                source="Arxiv",
                title=r.title.strip(),
                authors=[a.name for a in r.authors],
                abstract=r.summary.strip(),
                pdf_url=r.pdf_url,
                abs_url=r.entry_id,
                published=pub,
                venue=_detect_venue(r.comment),
                extra={"comment": r.comment or "", "primary_category": r.primary_category},
            )
        )
        if len(papers) >= max_results:
            break
    return papers
