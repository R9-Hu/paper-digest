"""arXiv source — query by category + keyword within a date window.

Built on the `arxiv` package (the official export API wrapper, which rate-limits
politely). Returns source-agnostic Paper objects.

Captures version + DOI so the harness can (a) link to the newest version and the
published/conference version when one exists, and (b) re-digest when a newer
version appears.
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


def _detect_venue(comment: str | None, journal_ref: str | None = None) -> str:
    for text in (comment, journal_ref):
        if not text:
            continue
        m = _VENUE_RE.search(text)
        if m:
            venue = m.group(1).upper()
            ym = re.search(re.escape(m.group(1)) + r"\s*'?(\d{2,4})", text, re.IGNORECASE)
            if ym:
                venue += " " + ym.group(1)
            return venue
    return ""


def _build_query(categories, keywords, start: dt.date | None, until: dt.date | None) -> str:
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    kw_clause = " OR ".join(f'all:"{k}"' for k in keywords)
    parts = []
    if cat_clause:
        parts.append(f"({cat_clause})")
    if kw_clause:
        parts.append(f"({kw_clause})")
    if start and until:
        parts.append(f"submittedDate:[{start:%Y%m%d}0000 TO {until:%Y%m%d}2359]")
    return " AND ".join(parts)


def _version(short_id: str) -> int:
    m = re.search(r"v(\d+)$", short_id)
    return int(m.group(1)) if m else 1


def search(
    categories: list[str],
    keywords: list[str],
    earliest: dt.date,
    max_results: int,
    until: dt.date | None = None,
) -> list[Paper]:
    """Return up to `max_results` papers submitted in [earliest, until].

    When `until` is given the date window is pushed into the query itself
    (year-bounded backfill); otherwise it's an open-ended 'since earliest' search.
    """
    query = _build_query(categories, keywords, earliest if until else None, until)
    if not query:
        return []

    client = arxiv.Client(page_size=100, delay_seconds=3.0, num_retries=5)
    s = arxiv.Search(
        query=query,
        max_results=max_results if until else max_results * 5,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers: list[Paper] = []
    for r in client.results(s):
        # r.published = datetime the ORIGINAL (v1) version was submitted (earliest).
        pub = r.published.date()
        if until and pub > until:
            continue
        if pub < earliest:
            break  # newest-first → nothing older remains we want
        short_id = r.get_short_id()              # e.g. "2501.01234v2"
        base_id = re.sub(r"v\d+$", "", short_id)
        doi = (r.doi or "").strip()
        # Newest/conference link: DOI (published version) if present, else latest abs.
        best_url = f"https://doi.org/{doi}" if doi else f"https://arxiv.org/abs/{base_id}"
        papers.append(
            Paper(
                canonical_id=f"arxiv:{base_id}",
                source="Arxiv",
                title=r.title.strip(),
                authors=[a.name for a in r.authors],
                abstract=r.summary.strip(),
                pdf_url=r.pdf_url,
                abs_url=best_url,
                published=pub,
                published_ts=r.published.isoformat(),
                version=_version(short_id),
                doi=doi,
                venue=_detect_venue(r.comment, r.journal_ref),
                extra={"comment": r.comment or "", "journal_ref": r.journal_ref or "",
                       "primary_category": r.primary_category,
                       "arxiv_abs": f"https://arxiv.org/abs/{base_id}"},
            )
        )
        if len(papers) >= max_results:
            break
    return papers
