"""Review / flowback loop (E 回流/复盘).

Once a week, synthesize what was collected & digested into a review note: dominant
themes, gaps, suggested next focus, suggested keywords (machine-parseable), and
candidate new skills. Stored in the `meta` table (no schema change) + written to
reviews/<ISO-week>.md, and surfaced on the site's Review dashboard. Flowback is
suggest-only — the user copies accepted keywords into config.yaml; the harness
never auto-edits config.
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import re

import yaml

from . import config, llm, rag, skills, state

log = logging.getLogger("harness.review")

MAX_CORPUS_CHARS = 60000
CARDS_PER_TOPIC = 40

_SYSTEM = (
    "You are the steward of a self-growing research knowledge base. Once a week you "
    "review what was collected and digested, judge what mattered, and propose how the "
    "knowledge base should evolve next. Be specific, opinionated, and grounded in the "
    "provided material; prefer concrete, actionable suggestions over generic advice."
)
_PROMPT = (
    "Weekly review for ISO week {week}.\n\n"
    "Tracked topics: {topics}\nExisting skills in the library: {skills}\n\n"
    "Below is this week's material — recently collected paper cards per topic plus the "
    "daily briefs and volume signals.\n\n"
    "Write a GitHub-flavored Markdown review using EXACTLY these H2 sections: "
    "## Week in review, ## Dominant themes, ## Gaps & blind spots, ## Suggested next focus, "
    "## Suggested keywords (a single fenced ```yaml block: add_keywords: {{slug: [..]}} using "
    "the exact topic slugs; omit slugs with no change), ## Candidate new skills.\n\n"
    "=== THIS WEEK'S MATERIAL ===\n{corpus}"
)


def iso_week(d: dt.date | None = None) -> str:
    iso = (d or dt.date.today()).isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def due(conn) -> bool:
    """True once per ISO week (until a review for the current week is recorded)."""
    return state.meta_get(conn, "review:latest_week") != iso_week()


def build_review_corpus(conn, cfg) -> str:
    cur_year = dt.date.today().year
    parts, total = [], 0
    for t in cfg.topics:
        cards = rag.cards_for(conn, t.slug, year=cur_year, limit=CARDS_PER_TOPIC, order="recent")
        brief = state.meta_get(conn, f"today_brief:{t.slug}") or ""
        lines = [f"### {t.name} ({t.slug}) — {len(cards)} recent cards"]
        if brief:
            lines.append(f"Latest brief: {brief}")
        for c in cards:
            v = f" [{c['venue']}]" if c.get("venue") else ""
            tl = " ".join((c.get("tldr") or "").split())[:160]
            lines.append(f"- {c['title']}{v} — {tl}")
        chunk = "\n".join(lines) + "\n\n"
        if total + len(chunk) > MAX_CORPUS_CHARS:
            chunk = chunk[: max(0, MAX_CORPUS_CHARS - total)]
        parts.append(chunk)
        total += len(chunk)
        if total >= MAX_CORPUS_CHARS:
            break
    return "".join(parts).strip()


def _extract_suggestions(body: str) -> dict:
    m = re.search(r"```ya?ml\s*\n(.*?)```", body, re.DOTALL | re.IGNORECASE)
    if not m:
        return {}
    try:
        d = yaml.safe_load(m.group(1)) or {}
        return d if isinstance(d, dict) else {}
    except yaml.YAMLError:
        return {}


def run_review(conn, cfg) -> bool:
    """Generate + store this week's review (one LLM call). Returns False on no data/failure."""
    week = iso_week()
    corpus = build_review_corpus(conn, cfg)
    if not corpus:
        log.info("review: no corpus yet; skipping")
        return False
    topics_str = ", ".join(f"{t.name} ({t.slug})" for t in cfg.topics)
    skill_names = ", ".join(sorted(p.stem for p in config.SKILLS_DIR.glob("*.md")
                                   if p.stem.lower() != "readme")) or "(none)"
    sk = skills.load_skill("review", {"system": _SYSTEM, "prompt": _PROMPT})
    prompt = sk.prompt.format(week=week, topics=topics_str, corpus=corpus, skills=skill_names)
    try:
        body = llm.strip_code_fence(llm.run_claude(
            prompt, cfg.trend_model, cfg, system=skills.with_profile(sk.system, cfg)))
    except llm.LLMError as e:
        log.warning("review failed: %s", e)
        return False

    config.REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    note = (f"---\ntitle: \"Weekly Review {week}\"\nweek: {week}\ngenerated: {today}\n---\n\n"
            f"# 🔁 Weekly Review — {week}\n\n*Generated {today}.*\n\n{body}\n")
    (config.REVIEW_DIR / f"{week}.md").write_text(note, encoding="utf-8")

    state.meta_set(conn, "review:latest", body)
    state.meta_set(conn, "review:latest_week", week)
    state.meta_set(conn, f"review:{week}", body)
    state.meta_set(conn, "review:suggestions", json.dumps(_extract_suggestions(body)))
    conn.commit()
    log.info("review written for %s", week)
    return True
