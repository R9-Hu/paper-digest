"""One-off / idempotent backfill of the earliest-version publish timestamp.

Existing digests predate the `published_ts` field. This re-queries arXiv (by
id_list, in batches — no LLM calls) for the v1 submission datetime of each
already-digested arXiv paper, writes it to the DB, and injects it into each
digest file (front-matter `published_time:` + the visible "Published (v1)" line).

Run:  .venv/bin/python -m harness.backfill_published
"""
from __future__ import annotations

import json
import logging
import re
import time

import arxiv

from . import config, digest, state

log = logging.getLogger("harness.backfill")
logging.basicConfig(level=logging.INFO, format="%(message)s")


CHUNK = 40
BACKOFFS = [20, 45, 90, 180]  # seconds, for HTTP 429 (in-process sleeps)


def _fetch_v1_times(arxiv_ids: list[str]) -> dict[str, str]:
    """Map base arXiv id -> ISO datetime of the original (v1) submission.

    Resilient to arXiv rate limiting (HTTP 429): retries each batch with
    exponential-ish backoff; skips a batch only after exhausting retries
    (re-running the backfill later fills any gaps — it's idempotent)."""
    out: dict[str, str] = {}
    client = arxiv.Client(page_size=CHUNK, delay_seconds=5.0, num_retries=5)
    for i in range(0, len(arxiv_ids), CHUNK):
        chunk = arxiv_ids[i:i + CHUNK]
        for attempt in range(len(BACKOFFS) + 1):
            try:
                for r in client.results(arxiv.Search(id_list=chunk, max_results=len(chunk))):
                    base = re.sub(r"v\d+$", "", r.get_short_id())
                    out[base] = r.published.isoformat()  # v1 = earliest version
                break
            except arxiv.HTTPError as e:
                if attempt < len(BACKOFFS):
                    wait = BACKOFFS[attempt]
                    log.warning("arxiv %s; backoff %ds (batch %d, try %d)",
                                getattr(e, "status", "error"), wait, i // CHUNK, attempt + 1)
                    time.sleep(wait)
                else:
                    log.error("batch %d failed after retries; skipping", i // CHUNK)
        log.info("  fetched %d/%d", len(out), len(arxiv_ids))
    return out


def _inject_into_file(path, ts: str, row) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3:
        return False
    yaml_block, rest = parts[1], parts[2]
    changed = False

    if "published_time:" not in yaml_block:
        lines, done = [], False
        for ln in yaml_block.split("\n"):
            lines.append(ln)
            if not done and ln.startswith("published:"):
                lines.append(f"published_time: {json.dumps(ts)}")
                done = True
        if not done:
            lines.append(f"published_time: {json.dumps(ts)}")
        yaml_block = "\n".join(lines)
        changed = True

    if "Published (v1)" not in rest:
        rlines, out, inserted = rest.split("\n"), [], False
        for ln in rlines:
            out.append(ln)
            if not inserted and ln.startswith("# "):
                out += ["", digest.visible_meta_line(row)]
                inserted = True
        rest = "\n".join(out)
        changed = True

    if changed:
        path.write_text("---".join([parts[0], yaml_block, rest]), encoding="utf-8")
    return changed


def main() -> int:
    with state.connect() as conn:
        rows = conn.execute(
            """SELECT * FROM papers
               WHERE digest_status='digested'
                 AND canonical_id LIKE 'arxiv:%'
                 AND (published_ts IS NULL OR published_ts='')"""
        ).fetchall()
        ids = sorted({r["canonical_id"].split(":", 1)[1] for r in rows})
        log.info("rows needing backfill: %d (unique arxiv ids: %d)", len(rows), len(ids))
        if not ids:
            return 0

        times = _fetch_v1_times(ids)
        log.info("fetched v1 times for %d/%d ids", len(times), len(ids))

        updated_db = files = 0
        for r in rows:
            base = r["canonical_id"].split(":", 1)[1]
            ts = times.get(base)
            if not ts:
                continue
            conn.execute(
                "UPDATE papers SET published_ts=? WHERE canonical_id=? AND topic_slug=?",
                (ts, r["canonical_id"], r["topic_slug"]),
            )
            conn.commit()
            updated_db += 1
            # Re-read the row so visible_meta_line sees the new ts.
            nr = conn.execute(
                "SELECT * FROM papers WHERE canonical_id=? AND topic_slug=?",
                (r["canonical_id"], r["topic_slug"]),
            ).fetchone()
            if r["digest_path"] and _inject_into_file(config.ROOT / r["digest_path"], ts, nr):
                files += 1
        log.info("done: DB rows updated=%d, digest files updated=%d", updated_db, files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
