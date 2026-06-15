"""Agent 2 — Digester.

For each fetched-but-not-digested paper: extract text with pdftotext, ask a
Claude agent for a structured digest, and write a Markdown note with reliable
YAML front matter (built in Python from known metadata).
"""
from __future__ import annotations

import json
import logging
import subprocess
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


def _front_matter(row, topic: Topic, digest_body: str) -> str:
    authors = json.loads(row["authors"] or "[]")
    fields = {
        "title": row["title"],
        "authors": authors,
        "source": row["source"],
        "venue": row["venue"] or "",
        "published": row["published"] or "",
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


def digest_paper(conn, cfg: Config, topic: Topic, row) -> bool:
    pdf_path = config.ROOT / row["pdf_path"]
    if not pdf_path.exists():
        state.mark_failed(conn, row["canonical_id"], topic.slug, "pdf missing")
        return False

    text = extract_text(pdf_path)
    if len(text) < 500:
        # Fall back to the abstract so we still produce something useful.
        text = (row["abstract"] or "")[:MAX_TEXT_CHARS]
    text = text[:MAX_TEXT_CHARS]
    if not text.strip():
        state.mark_failed(conn, row["canonical_id"], topic.slug, "no extractable text")
        return False

    prompt = PROMPT_TMPL.format(topic=topic.name, title=row["title"], text=text)
    try:
        body = llm.strip_code_fence(llm.run_claude(prompt, cfg.digest_model, cfg, system=SYSTEM))
    except llm.LLMError as e:
        log.warning("[%s] digest failed for %s: %s", topic.slug, row["title"][:60], e)
        state.mark_failed(conn, row["canonical_id"], topic.slug, str(e))
        return False

    out_dir = config.DIGEST_DIR / topic.slug
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(row["pdf_path"]).stem
    out_path = out_dir / f"{stem}.md"

    fm = _front_matter(row, topic, body)
    note = f"{fm}\n\n# {row['title']}\n\n{body}\n"
    out_path.write_text(note, encoding="utf-8")

    rel = out_path.relative_to(config.ROOT).as_posix()
    state.mark_digested(conn, row["canonical_id"], topic.slug, rel)
    log.info("[%s] digested: %s", topic.slug, out_path.name)
    return True


def digest_topic(conn, cfg: Config, topic: Topic) -> int:
    pending = state.pending_digests(conn, topic.slug)
    log.info("[%s] %d papers to digest", topic.slug, len(pending))
    done = 0
    for row in pending:
        if digest_paper(conn, cfg, topic, row):
            done += 1
    log.info("[%s] digested %d/%d", topic.slug, done, len(pending))
    return done
