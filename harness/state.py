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
    published      TEXT,          -- ISO date (earliest version)
    published_ts   TEXT,          -- ISO datetime of the earliest version (v1)
    version        INTEGER,       -- latest known version (arXiv vN)
    doi            TEXT,          -- published/conference DOI, if any
    year           INTEGER,
    pdf_path       TEXT,          -- relative to project root
    digest_path    TEXT,          -- relative to project root
    tldr           TEXT,          -- cached TL;DR (reused by the daily 'In brief' + pages)
    digest_status  TEXT DEFAULT 'fetched',  -- fetched | digested | failed | compacted | dropped
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

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);

-- Topic-agnostic digest body, generated once per paper and reused across topics
-- (only the per-topic "Relevance" section is generated separately). Saves tokens
-- for papers tracked under more than one topic.
CREATE TABLE IF NOT EXISTS shared_digest (
    canonical_id TEXT PRIMARY KEY,
    body         TEXT,
    tldr         TEXT,
    created_at   TEXT
);

-- Citation/impact cache (Semantic Scholar). Keyed by canonical_id (topic-agnostic);
-- refreshed on a TTL so high-impact ranking doesn't re-query the API every run.
CREATE TABLE IF NOT EXISTS impact (
    canonical_id TEXT PRIMARY KEY,
    citations    INTEGER,
    influential  INTEGER,
    fetched_ts   TEXT
);
"""


@contextmanager
def connect(db_path: Path | str = None):
    db_path = Path(db_path) if db_path else config.DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout=30000")  # tolerate concurrent runs
        conn.executescript(SCHEMA)
        # Migrate older DBs that predate added columns.
        cols = {r[1] for r in conn.execute("PRAGMA table_info(papers)")}
        for col, decl in (("published_ts", "TEXT"), ("version", "INTEGER"),
                          ("doi", "TEXT"), ("tldr", "TEXT"), ("select_reason", "TEXT")):
            if col not in cols:
                conn.execute(f"ALTER TABLE papers ADD COLUMN {col} {decl}")
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
            abs_url, venue, published, published_ts, version, doi, year, pdf_path,
            select_reason, digest_status, fetched_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, 'fetched', ?)""",
        (
            paper.canonical_id, topic_slug, paper.source, paper.title,
            json.dumps(paper.authors), paper.abstract, paper.pdf_url,
            paper.abs_url, paper.venue,
            paper.published.isoformat() if paper.published else None,
            paper.published_ts or None, paper.version, paper.doi or None,
            paper.year, pdf_path, (paper.extra.get("select_reason") or None), _now(),
        ),
    )
    # A (re-)fetch may be a newer version — invalidate any cached shared body.
    conn.execute("DELETE FROM shared_digest WHERE canonical_id=?", (paper.canonical_id,))


def get_version(conn, canonical_id: str, topic_slug: str) -> int | None:
    row = conn.execute(
        "SELECT version FROM papers WHERE canonical_id=? AND topic_slug=?",
        (canonical_id, topic_slug),
    ).fetchone()
    return (row["version"] if row and row["version"] is not None else None) if row else None


def mark_digested(conn, canonical_id: str, topic_slug: str, digest_path: str,
                  tldr: str | None = None) -> None:
    conn.execute(
        """UPDATE papers SET digest_status='digested', digest_path=?, tldr=?,
           digested_at=?, error=NULL WHERE canonical_id=? AND topic_slug=?""",
        (digest_path, tldr, _now(), canonical_id, topic_slug),
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
        """SELECT * FROM papers
           WHERE topic_slug=? AND digest_status IN ('digested','compacted')
           ORDER BY published DESC""",
        (topic_slug,),
    ).fetchall()


def years_for_topic(conn, topic_slug: str) -> list[int]:
    """Distinct years that have digested papers, newest first."""
    rows = conn.execute(
        """SELECT DISTINCT CAST(year AS INTEGER) y FROM papers
           WHERE topic_slug=? AND digest_status IN ('digested','compacted')
                 AND year IS NOT NULL
           ORDER BY y DESC""",
        (topic_slug,),
    ).fetchall()
    return [r["y"] for r in rows]


def latest_digest_date(conn, topic_slug: str) -> str | None:
    """The most recent date (YYYY-MM-DD) on which this topic had a paper digested."""
    row = conn.execute(
        """SELECT MAX(substr(digested_at,1,10)) d FROM papers
           WHERE topic_slug=? AND digest_status IN ('digested','compacted')
                 AND digested_at IS NOT NULL""",
        (topic_slug,),
    ).fetchone()
    return row["d"] if row and row["d"] else None


def digested_for_topic_year(conn, topic_slug: str, year: int) -> list[sqlite3.Row]:
    return conn.execute(
        """SELECT * FROM papers
           WHERE topic_slug=? AND CAST(year AS INTEGER)=?
                 AND digest_status IN ('digested','compacted')
           ORDER BY published DESC""",
        (topic_slug, year),
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


def get_shared_digest(conn, canonical_id: str):
    row = conn.execute(
        "SELECT body, tldr FROM shared_digest WHERE canonical_id=?", (canonical_id,)
    ).fetchone()
    return (row["body"], row["tldr"]) if row else None


def set_shared_digest(conn, canonical_id: str, body: str, tldr: str) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO shared_digest (canonical_id, body, tldr, created_at) "
        "VALUES (?,?,?,?)", (canonical_id, body, tldr, _now()),
    )


def clear_shared_digest(conn, canonical_id: str) -> None:
    conn.execute("DELETE FROM shared_digest WHERE canonical_id=?", (canonical_id,))


def meta_get(conn, key: str) -> str | None:
    row = conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return row["value"] if row else None


def meta_set(conn, key: str, value: str) -> None:
    conn.execute("INSERT OR REPLACE INTO meta (key, value) VALUES (?,?)", (key, value))


def prior_year_digested(conn, before_year: int):
    """Digested (not yet compacted) papers published before `before_year`."""
    return conn.execute(
        """SELECT * FROM papers
           WHERE digest_status='digested' AND CAST(year AS INTEGER) < ?
           ORDER BY year, topic_slug""",
        (before_year,),
    ).fetchall()


def mark_compacted(conn, canonical_id: str, topic_slug: str, digest_path: str) -> None:
    conn.execute(
        """UPDATE papers SET digest_status='compacted', digest_path=?, pdf_path=NULL
           WHERE canonical_id=? AND topic_slug=?""",
        (digest_path, canonical_id, topic_slug),
    )
