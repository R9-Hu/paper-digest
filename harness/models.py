"""Shared data structures."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field


@dataclass
class Paper:
    """A discovered paper, source-agnostic."""

    canonical_id: str          # e.g. "arxiv:2501.01234" — stable dedup key
    source: str                # display "Place": Arxiv, HuggingFace, MICCAI, ...
    title: str
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    pdf_url: str = ""
    abs_url: str = ""          # landing/abstract page URL
    published: dt.date | None = None
    venue: str = ""            # conference/journal if known (from arxiv comment etc.)
    extra: dict = field(default_factory=dict)

    @property
    def year(self) -> int:
        return self.published.year if self.published else dt.date.today().year

    @property
    def authors_str(self) -> str:
        return ", ".join(self.authors)
