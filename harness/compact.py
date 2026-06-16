"""Yearly compaction — shrink storage for older papers.

Policy: when a year rolls over, papers from prior years are "compacted":
  * the digest is trimmed to its essential sections (TL;DR, Key Contributions,
    Results) — a concise, permanent record;
  * the downloaded PDF and the cached extracted text are deleted (the bulk of
    on-disk storage);
  * the row is marked `compacted` (it still appears on the site/Obsidian pages).

Current-year papers keep their full digest + PDF. This is deterministic (no LLM
call), so re-running is cheap and idempotent.

Run:  .venv/bin/python -m harness.orchestrate --compact-year 2025
Auto: the daily pipeline compacts any not-yet-compacted prior-year papers.
"""
from __future__ import annotations

import datetime as dt
import logging
import re

from . import config, state
from .config import Config

log = logging.getLogger("harness.compact")

KEEP = ("tl;dr", "key contribution", "results")  # sections retained when compacting


def _trim_digest(md: str) -> str:
    """Keep front matter, title, the visible meta line, and only the KEEP sections."""
    parts = md.split("---", 2)
    if len(parts) == 3:
        head = f"---{parts[1]}---"
        body = parts[2]
    else:
        head, body = "", md
    # Split body into the pre-H2 head (title + meta line) and the H2 sections.
    chunks = re.split(r"(?m)^##[ \t]+", body)
    pre = chunks[0].rstrip()
    kept = []
    for chunk in chunks[1:]:
        nl = chunk.find("\n")
        title = (chunk[:nl] if nl != -1 else chunk).strip()
        low = title.lower()
        if any(low.startswith(k) for k in KEEP):
            kept.append("## " + chunk.rstrip())
    out = (head + "\n" if head else "") + pre + "\n\n" + "\n\n".join(kept) + "\n"
    out += "\n> [!note] Compacted — PDF removed to save storage; full digest trimmed to essentials.\n"
    return out


def compact_paper(conn, cfg: Config, row) -> bool:
    rel = row["digest_path"]
    if not rel:
        return False
    path = config.ROOT / rel
    if path.exists():
        try:
            path.write_text(_trim_digest(path.read_text(encoding="utf-8")), encoding="utf-8")
        except OSError as e:
            log.warning("compact: cannot rewrite %s: %s", rel, e)
            return False
    # Delete the PDF (the big storage item) and cached extracted text.
    if row["pdf_path"]:
        (config.ROOT / row["pdf_path"]).unlink(missing_ok=True)
    cid = row["canonical_id"].split(":", 1)[-1]
    (config.TEXT_DIR / f"{cid}.txt").unlink(missing_ok=True)
    state.mark_compacted(conn, row["canonical_id"], row["topic_slug"], rel)
    return True


def compact_year(conn, cfg: Config, year: int) -> int:
    rows = conn.execute(
        """SELECT * FROM papers
           WHERE digest_status='digested' AND CAST(year AS INTEGER)=?""",
        (year,),
    ).fetchall()
    n = 0
    for row in rows:
        if compact_paper(conn, cfg, row):
            n += 1
        conn.commit()
    if rows:
        log.info("compacted %d/%d papers from %d", n, len(rows), year)
    return n


def maybe_autocompact(conn, cfg: Config) -> int:
    """Compact every not-yet-compacted paper published before the current year."""
    cur = dt.date.today().year
    rows = state.prior_year_digested(conn, cur)
    if not rows:
        return 0
    years = sorted({int(r["year"]) for r in rows if r["year"]})
    log.info("auto-compact: %d prior-year papers across %s", len(rows), years)
    total = sum(compact_year(conn, cfg, y) for y in years)
    state.meta_set(conn, "last_autocompact", dt.date.today().isoformat())
    conn.commit()
    return total
