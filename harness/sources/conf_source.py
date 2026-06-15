"""Best-effort conference source via the OpenReview API (v2).

Only conferences hosted on OpenReview are queryable here (ICLR, NeurIPS, ICML).
Others (CVPR/ICCV/MICCAI) are surfaced indirectly: arxiv_source detects their
venue from the arXiv `comment` field. This source NEVER raises to the caller —
on any error it returns what it has so the daily run is never blocked.
"""
from __future__ import annotations

import datetime as dt

import requests

from ..models import Paper

API = "https://api2.openreview.net/notes"
TIMEOUT = 25
PAGE = 1000

# Conferences that live on OpenReview, mapped to their group prefix.
OPENREVIEW_GROUPS = {
    "ICLR": "ICLR.cc",
    "NEURIPS": "NeurIPS.cc",
    "NIPS": "NeurIPS.cc",
    "ICML": "ICML.cc",
}


def _field(note: dict, key: str, default=""):
    val = note.get("content", {}).get(key)
    if isinstance(val, dict):  # v2 wraps values as {"value": ...}
        return val.get("value", default)
    return val if val is not None else default


def _query_venue(group: str, year: int, keywords: list[str], cap: int) -> list[Paper]:
    venueid = f"{group}/{year}/Conference"
    papers: list[Paper] = []
    offset = 0
    while len(papers) < cap:
        try:
            resp = requests.get(
                API,
                params={"content.venueid": venueid, "limit": PAGE, "offset": offset},
                timeout=TIMEOUT,
            )
            if resp.status_code != 200:
                break
            notes = resp.json().get("notes", [])
        except (requests.RequestException, ValueError):
            break
        if not notes:
            break
        for note in notes:
            title = str(_field(note, "title")).strip()
            abstract = str(_field(note, "abstract")).strip()
            blob = f"{title} {abstract}".lower()
            if keywords and not any(k.lower() in blob for k in keywords):
                continue
            note_id = note.get("id", "")
            authors = _field(note, "authors", []) or []
            papers.append(
                Paper(
                    canonical_id=f"openreview:{note_id}",
                    source=group.split(".")[0],
                    title=title,
                    authors=list(authors),
                    abstract=abstract,
                    pdf_url=f"https://openreview.net/pdf?id={note_id}",
                    abs_url=f"https://openreview.net/forum?id={note_id}",
                    published=dt.date(year, 1, 1),
                    venue=f"{group.split('.')[0]} {year}",
                )
            )
            if len(papers) >= cap:
                break
        offset += PAGE
    return papers


def search(
    conferences: list[str],
    keywords: list[str],
    earliest: dt.date,
    max_results: int,
) -> list[Paper]:
    today = dt.date.today()
    years = range(earliest.year, today.year + 1)
    papers: list[Paper] = []
    seen_groups: set[str] = set()
    for conf in conferences:
        group = OPENREVIEW_GROUPS.get(conf.upper())
        if not group or group in seen_groups:
            continue
        seen_groups.add(group)
        for year in years:
            if len(papers) >= max_results:
                return papers
            papers.extend(
                _query_venue(group, year, keywords, max_results - len(papers))
            )
    return papers
