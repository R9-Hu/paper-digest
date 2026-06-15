"""SQLite-backed dedup + run state.

A paper may match more than one topic, so the primary key is
(canonical_id, topic_slug). `digest_status` advances fetched -> digested / failed.
"""
from __future__ import annotations

import datetime as dt
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from . import config
from .models import Paper

SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    canonical_id   TEXT NOT NULL,
    topic_slug     TEXT NOT NULL,
    source         TEXT,
    title          TEXT,
    authors        TEXT,          -- JSON list
    abstract       TEXT,
    pdf_url        TEXT,
    abs_url        TEXT,
    venue          TEXT,
    published      TEXT,          -- ISO date
    year           INTEGER,
    pdf_path       TEXT,          -- relative to project root
    digest_path    TEXT,          -- relative to project root
    digest_status  TEXT DEFAULT 'fetched',  -- fetched | digested | failed
    error          TEXT,
    fetched_at     TEXT,
    digested_at    TEXT,
    PRIMARY KEY (canonical_id, topic_slug)
);

CREATE TABLE IF NOT EXISTS topic_state (
    topic_slug   TEXT PRIMARY KEY,
    last_run     TEXT,
    last_run_new INTEGER
);
"""


@contextmanager
def connect(db_path: Path | str = None):
    db_path = Path(db_path) if db_path else config.DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def is_seen(conn, canonical_id: str, topic_slug: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM papers WHERE canonical_id=? AND topic_slug=?",
        (canonical_id, topic_slug),
    ).fetchone()
    return row is not None


def record_fetched(conn, paper: Paper, topic_slug: str, pdf_path: str) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO papers
           (canonical_id, topic_slug, source, title, authors, abstract, pdf_url,
            abs_url, venue, published, year, pdf_path, digest_status, fetched_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?, 'fetched', ?)""",
        (
            paper.canonical_id, topic_slug, paper.source, paper.title,
            json.dumps(paper.authors), paper.abstract, paper.pdf_url,
            paper.abs_url, paper.venue,
            paper.published.isoformat() if paper.published else None,
            paper.year, pdf_path, _now(),
        ),
    )


def mark_digested(conn, canonical_id: str, topic_slug: str, digest_path: str) -> None:
    conn.execute(
        """UPDATE papers SET digest_status='digested', digest_path=?,
           digested_at=?, error=NULL WHERE canonical_id=? AND topic_slug=?""",
        (digest_path, _now(), canonical_id, topic_slug),
    )


def mark_failed(conn, canonical_id: str, topic_slug: str, error: str) -> None:
    conn.execute(
        """UPDATE papers SET digest_status='failed', error=?
           WHERE canonical_id=? AND topic_slug=?""",
        (error[:2000], canonical_id, topic_slug),
    )


def pending_digests(conn, topic_slug: str = None) -> list[sqlite3.Row]:
    """Papers fetched (or previously failed) but not yet digested."""
    q = "SELECT * FROM papers WHERE digest_status IN ('fetched','failed')"
    args: tuple = ()
    if topic_slug:
        q += " AND topic_slug=?"
        args = (topic_slug,)
    q += " ORDER BY published DESC"
    return conn.execute(q, args).fetchall()


def digested_for_topic(conn, topic_slug: str) -> list[sqlite3.Row]:
    return conn.execute(
        """SELECT * FROM papers WHERE topic_slug=? AND digest_status='digested'
           ORDER BY published DESC""",
        (topic_slug,),
    ).fetchall()


def set_last_run(conn, topic_slug: str, new_count: int) -> None:
    conn.execute(
        """INSERT OR REPLACE INTO topic_state (topic_slug, last_run, last_run_new)
           VALUES (?,?,?)""",
        (topic_slug, _now(), new_count),
    )


def get_last_run(conn, topic_slug: str) -> str | None:
    row = conn.execute(
        "SELECT last_run FROM topic_state WHERE topic_slug=?", (topic_slug,)
    ).fetchone()
    return row["last_run"] if row else None
