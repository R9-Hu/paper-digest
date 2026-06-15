"""Filename construction + sanitization.

Target format:  "[<Place> <Year>] <Title>.pdf"
e.g.            "[Arxiv 2025] Segment Anything in Medical Images.pdf"

Characters that are illegal / awkward in filenames are stripped (per the user's
request to simply ignore symbols that can't be used in a filename).
"""
from __future__ import annotations

import re
import unicodedata

# Characters illegal on common filesystems (Windows is the strictest superset).
_ILLEGAL = r'<>:"/\\|?*'
_ILLEGAL_RE = re.compile(f"[{re.escape(_ILLEGAL)}]")
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")
_WS_RE = re.compile(r"\s+")

MAX_TITLE_LEN = 150  # keep the whole filename comfortably under FS limits


def sanitize_title(title: str) -> str:
    """Drop illegal/control chars, normalize whitespace, trim length."""
    if not title:
        return "Untitled"
    # Normalize unicode (e.g. smart quotes) to a stable form.
    title = unicodedata.normalize("NFKC", title)
    title = _CONTROL_RE.sub("", title)
    title = _ILLEGAL_RE.sub("", title)
    # Collapse runs of whitespace (incl. newlines from PDF/metadata) to one space.
    title = _WS_RE.sub(" ", title).strip()
    # Trailing dots/spaces are illegal on Windows.
    title = title.rstrip(" .")
    if len(title) > MAX_TITLE_LEN:
        title = title[:MAX_TITLE_LEN].rstrip(" .")
    return title or "Untitled"


def build_stem(place: str, year: int | str, title: str) -> str:
    """Return the filename stem (no extension): '[Place Year] Title'."""
    place = _ILLEGAL_RE.sub("", str(place)).strip() or "Unknown"
    return f"[{place} {year}] {sanitize_title(title)}"


def build_filename(place: str, year: int | str, title: str, ext: str = "pdf") -> str:
    ext = ext.lstrip(".")
    return f"{build_stem(place, year, title)}.{ext}"


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str, max_len: int = 80) -> str:
    """URL-safe lowercase slug for website filenames."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = _SLUG_RE.sub("-", text.lower()).strip("-")
    return (text[:max_len].strip("-")) or "untitled"
