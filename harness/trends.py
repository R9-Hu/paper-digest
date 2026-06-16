"""Agent 3 — Analyst.

Reads all digests for a topic and writes a trend report: how the topic developed,
its current state, open problems, and a prediction of likely next steps.
"""
from __future__ import annotations

import datetime as dt
import logging
import re

from . import config, llm, state
from .config import Config, Topic

log = logging.getLogger("harness.trends")

MAX_PAPERS = 80           # most-recent N digests fed to the analyst
PER_PAPER_CHARS = 1400    # truncation per digest
MAX_CORPUS_CHARS = 140000

SYSTEM = (
    "You are a senior research trend analyst. You synthesize many paper digests "
    "into a clear, opinionated map of a research area: its trajectory, current "
    "frontier, and where it is likely heading. You ground every claim in the "
    "provided digests and may use WebSearch/subagents to sanity-check recent "
    "developments, but the digests are your primary evidence."
)

PROMPT_TMPL = """\
You are analyzing the research topic: "{topic}".

Below are {n} paper digests (newest first), each with its date and venue. Write a
GitHub-flavored Markdown trend report using EXACTLY these H2 sections:

## Overview
(3-5 sentences framing the topic and the state of play.)

## Timeline
(A concise, abstract chronological timeline of how the topic developed — one bullet
per milestone/phase, each prefixed with a timestamp. Use the format
`- **YYYY-MM**: one-line milestone` (use `YYYY` alone if a month is not meaningful).
6-10 bullets, oldest first. Keep each to a single line; this is the at-a-glance
history, not the prose narrative below.)

## How the field developed
(A chronological narrative / phases, referencing dates and the shift in approaches.)

## Current state & major clusters
(The dominant approaches/sub-directions right now, with representative papers named.)

## Open problems
(Bulleted; what's unsolved or contested.)

## Predicted next steps
(Bulleted; specific, near-term, falsifiable predictions about where the field goes next, with reasoning grounded in the trajectory above.)

## Key papers
(Bulleted: "**Title** (date, venue) — one line on why it matters".)

Rules:
- Reference papers by their titles. Be specific and technical; avoid generic filler.
- Output ONLY the Markdown body starting at "## Overview". No preamble, no front matter.

=== DIGESTS ===
{corpus}
"""


def _strip_front_matter(md: str) -> str:
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return md.strip()


def _build_corpus_year(conn, topic: Topic, year: int) -> tuple[str, int]:
    rows = state.digested_for_topic_year(conn, topic.slug, year)[:MAX_PAPERS]
    chunks, total, used = [], 0, 0
    for row in rows:
        path = config.ROOT / (row["digest_path"] or "")
        if not path.exists():
            continue
        body = _strip_front_matter(path.read_text(encoding="utf-8"))
        body = re.sub(r"\n{3,}", "\n\n", body)[:PER_PAPER_CHARS]
        header = f"### [{row['published'] or '?'}] {row['title']}"
        if row["venue"]:
            header += f"  ({row['venue']})"
        chunk = f"{header}\n{body}\n"
        if total + len(chunk) > MAX_CORPUS_CHARS:
            break
        chunks.append(chunk)
        total += len(chunk)
        used += 1
    return "\n".join(chunks), used


def trend_path(topic: Topic, year: int):
    return config.TREND_DIR / topic.slug / f"{year}.md"


def analyze_topic_year(conn, cfg: Config, topic: Topic, year: int) -> bool:
    corpus, n = _build_corpus_year(conn, topic, year)
    if n == 0:
        return False
    prompt = PROMPT_TMPL.format(topic=f"{topic.name} ({year})", n=n, corpus=corpus)
    try:
        body = llm.strip_code_fence(llm.run_claude(prompt, cfg.trend_model, cfg, system=SYSTEM))
    except llm.LLMError as e:
        log.warning("[%s %d] trend analysis failed: %s", topic.slug, year, e)
        return False

    out_path = trend_path(topic, year)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    fm = (
        "---\n"
        f"title: \"Trend Analysis: {topic.name} ({year})\"\n"
        f"topic: {topic.name}\n"
        f"topic_slug: {topic.slug}\n"
        f"year: {year}\n"
        f"generated: {today}\n"
        f"papers_analyzed: {n}\n"
        "---\n"
    )
    note = (f"{fm}\n# Trend Analysis — {topic.name} ({year})\n\n"
            f"*Generated {today} from {n} digested {year} papers.*\n\n{body}\n")
    out_path.write_text(note, encoding="utf-8")
    log.info("[%s %d] trend report written (%d papers)", topic.slug, year, n)
    return True


def analyze_topic(conn, cfg: Config, topic: Topic) -> bool:
    """Generate per-year trend reports, regenerating a year only when its digested
    paper count has changed since the last report (saves repeated LLM calls)."""
    years = state.years_for_topic(conn, topic.slug)
    if not years:
        log.info("[%s] no digests yet; skipping trend analysis", topic.slug)
        return False
    any_done = False
    for year in years:
        n = len(state.digested_for_topic_year(conn, topic.slug, year))
        key = f"trendN:{topic.slug}:{year}"
        prev = state.meta_get(conn, key)
        if prev == str(n) and trend_path(topic, year).exists():
            continue  # unchanged since last report
        if analyze_topic_year(conn, cfg, topic, year):
            state.meta_set(conn, key, str(n))
            conn.commit()
            any_done = True
    return any_done
