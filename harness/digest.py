"""Agent 2 — Digester.

For each fetched-but-not-digested paper: extract text with pdftotext, ask a
Claude agent for a structured digest, and write a Markdown note with reliable
YAML front matter (built in Python from known metadata).
"""
from __future__ import annotations

import json
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from . import config, llm, state
from .config import Config, Topic

log = logging.getLogger("harness.digest")

MAX_TEXT_CHARS = 45000  # plenty for a digest; keeps prompt/cost bounded

SYSTEM = (
    "You are a meticulous research-paper digest agent for an expert researcher. "
    "You write dense, faithful, jargon-correct summaries. Never invent results or "
    "numbers that are not in the text. You may use WebSearch/subagents only if a "
    "critical term is unclear, but prefer the provided text."
)

PROMPT_TMPL = """\
Digest the following paper for a researcher tracking the topic "{topic}".

Write GitHub-flavored Markdown using EXACTLY these H2 sections, in order:

## TL;DR
(2-3 sentences.)

## Problem
(What gap/limitation it addresses.)

## Method
(Core approach; be concrete about the technique.)

## Key Contributions
(Bullet list.)

## Results
(Headline numbers/benchmarks and against what baselines. Bullet list. Only what's in the text.)

## Limitations
(Stated or evident limitations. Bullet list.)

## Relevance to {topic}
(2-4 sentences: why this matters for someone tracking this topic; how it connects to the broader line of work.)

## Tags
(5-8 lowercase #hashtags, space-separated, e.g. #vlm #benchmark)

Rules:
- Output ONLY the Markdown body starting at "## TL;DR". No preamble, no title, no front matter, no closing remarks.
- Be specific and technical. Do not pad.

Paper title: {title}
Paper text (may be truncated):
---
{text}
---
"""


def extract_text(pdf_path: Path) -> str:
    """pdftotext -> string (empty on failure)."""
    try:
        proc = subprocess.run(
            ["pdftotext", "-q", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=120,
        )
        return proc.stdout or ""
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        log.warning("pdftotext failed for %s: %s", pdf_path, e)
        return ""


def _fmt_ts(iso: str) -> str:
    """ISO datetime -> 'YYYY-MM-DD HH:MM UTC' (earliest-version time)."""
    import datetime as _dt
    try:
        d = _dt.datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return iso
    tz = "UTC" if d.utcoffset() in (_dt.timedelta(0), None) else (d.tzname() or "")
    return f"{d.strftime('%Y-%m-%d %H:%M')} {tz}".strip()


def visible_meta_line(row) -> str:
    """A one-line, human-visible header for a digest naming the publish time
    (earliest version), source and venue. Shown verbatim on the website."""
    ts = row["published_ts"] if "published_ts" in row.keys() else None
    when = _fmt_ts(ts) if ts else (row["published"] or "unknown date")
    bits = [f"🕒 **Published (v1):** {when}"]
    if row["source"]:
        bits.append(f"**Source:** {row['source']}")
    if row["venue"]:
        bits.append(f"**Venue:** {row['venue']}")
    url = row["abs_url"] or row["pdf_url"]
    if url:
        bits.append(f"[link]({url})")
    return "*" + "  ·  ".join(bits) + "*"


def _front_matter(row, topic: Topic, digest_body: str) -> str:
    authors = json.loads(row["authors"] or "[]")
    fields = {
        "title": row["title"],
        "authors": authors,
        "source": row["source"],
        "venue": row["venue"] or "",
        "published": row["published"] or "",
        "published_time": (row["published_ts"] or ""),  # earliest-version timestamp
        "year": row["year"],
        "topic": topic.name,
        "topic_slug": topic.slug,
        "canonical_id": row["canonical_id"],
        "url": row["abs_url"] or row["pdf_url"] or "",
        "pdf": row["pdf_path"] or "",
    }
    lines = ["---"]
    for k, v in fields.items():
        if isinstance(v, list):
            inner = ", ".join(json.dumps(a) for a in v)
            lines.append(f"{k}: [{inner}]")
        else:
            lines.append(f"{k}: {json.dumps(v) if isinstance(v, str) else v}")
    lines.append("---")
    return "\n".join(lines)


def _produce(cfg: Config, topic: Topic, row):
    """Heavy, DB-free digest work (runs in a worker thread).
    Returns (canonical_id, topic_slug, digest_rel_path | None, error | None)."""
    cid, slug = row["canonical_id"], topic.slug
    pdf_path = config.ROOT / (row["pdf_path"] or "")
    if not pdf_path.exists():
        return cid, slug, None, "pdf missing"
    text = extract_text(pdf_path)
    if len(text) < 500:
        text = (row["abstract"] or "")[:MAX_TEXT_CHARS]
    text = text[:MAX_TEXT_CHARS]
    if not text.strip():
        return cid, slug, None, "no extractable text"
    prompt = PROMPT_TMPL.format(topic=topic.name, title=row["title"], text=text)
    try:
        body = llm.strip_code_fence(llm.run_claude(prompt, cfg.digest_model, cfg, system=SYSTEM))
    except llm.LLMError as e:
        return cid, slug, None, str(e)
    out_dir = config.DIGEST_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{Path(row['pdf_path']).stem}.md"
    note = f"{_front_matter(row, topic, body)}\n\n# {row['title']}\n\n{visible_meta_line(row)}\n\n{body}\n"
    out_path.write_text(note, encoding="utf-8")
    return cid, slug, out_path.relative_to(config.ROOT).as_posix(), None


def digest_topic(conn, cfg: Config, topic: Topic) -> int:
    """Digest all pending papers for a topic, running `digest_concurrency`
    LLM calls in parallel. Worker threads do the LLM/file work; this (main)
    thread owns all sqlite writes — sqlite connections aren't thread-safe."""
    pending = state.pending_digests(conn, topic.slug)
    log.info("[%s] %d papers to digest (concurrency=%d)",
             topic.slug, len(pending), cfg.digest_concurrency)
    if not pending:
        return 0
    done = 0
    workers = max(1, cfg.digest_concurrency)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_produce, cfg, topic, row) for row in pending]
        for fut in as_completed(futures):
            cid, slug, rel, err = fut.result()
            if err:
                state.mark_failed(conn, cid, slug, err)
                log.warning("[%s] digest failed %s: %s", slug, cid, err[:80])
            else:
                state.mark_digested(conn, cid, slug, rel)
                done += 1
            conn.commit()
    log.info("[%s] digested %d/%d", topic.slug, done, len(pending))
    return done
