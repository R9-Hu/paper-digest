"""Agent 2 — Digester.

For each fetched-but-not-digested paper: extract text with pdftotext, ask a
Claude agent for a structured digest, and write a Markdown note with reliable
YAML front matter (built in Python from known metadata).
"""
from __future__ import annotations

import json
import logging
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from . import config, llm, skills, state
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
- Write mathematical notation in LaTeX: $...$ for inline math and $$...$$ for display equations.

Paper title: {title}
Paper text (may be truncated):
---
{text}
---
"""


def _cache_path(canonical_id: str):
    return config.TEXT_DIR / f"{canonical_id.split(':', 1)[-1]}.txt"


def clear_text_cache() -> int:
    """Delete the PDF→text extraction cache. Called after a digest run — the cache
    only accelerates within-run retries/cross-topic reuse and is regenerable from
    the (retained) PDF, so it's unnecessary once the run completes."""
    n = 0
    for f in config.TEXT_DIR.glob("*.txt"):
        try:
            f.unlink()
            n += 1
        except OSError:
            pass
    if n:
        log.info("cleared %d cached text files", n)
    return n


def extract_text(pdf_path: Path, canonical_id: str | None = None) -> str:
    """pdftotext -> string (empty on failure), cached by paper id under state/text/.

    The cache is keyed on the paper id (not the topic), so a re-digest, a retry of
    a failed digest, or the same paper appearing under multiple topics all reuse a
    single extraction instead of re-running pdftotext. Compaction clears the cache."""
    cache = _cache_path(canonical_id) if canonical_id else None
    if cache and cache.exists():
        try:
            cached = cache.read_text(encoding="utf-8", errors="ignore")
            if len(cached) >= 500:
                return cached
        except OSError:
            pass
    try:
        proc = subprocess.run(
            ["pdftotext", "-q", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=120,
        )
        text = proc.stdout or ""
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        log.warning("pdftotext failed for %s: %s", pdf_path, e)
        return ""
    if cache and len(text) >= 500:
        try:
            config.TEXT_DIR.mkdir(parents=True, exist_ok=True)
            cache.write_text(text, encoding="utf-8")
        except OSError:
            pass
    return text


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


REL_SYSTEM = "You explain, concisely and concretely, why a paper matters to a specific research topic."
_REL_PROMPT = ("Paper: {title}\nTL;DR: {tldr}\n\nIn 2-4 sentences, explain this paper's "
               "relevance to the research topic \"{topic}\" — why it matters for someone "
               "tracking it and how it connects to the broader line of work. Output only prose.")


def _tldr_of(body: str) -> str:
    m = re.search(r"(?ims)^##\s*TL;DR\s*\n(.+?)(?=^##\s|\Z)", body)
    return " ".join(m.group(1).split()) if m else ""


def _split_relevance(body: str):
    """Split the LLM digest into (topic-agnostic body, the 'Relevance' section text)."""
    m = re.search(r"(?ims)^##\s*Relevance[^\n]*\n(.*?)(?=^##\s|\Z)", body)
    if not m:
        return body.strip(), ""
    return (body[:m.start()] + body[m.end():]).strip(), m.group(1).strip()


def _relevance(cfg: Config, topic: Topic, title: str, tldr: str) -> str:
    sk = skills.load_skill("relevance", {"system": REL_SYSTEM, "prompt": _REL_PROMPT})
    prompt = sk.prompt.format(title=title, tldr=tldr, topic=topic.name)
    return llm.strip_code_fence(llm.run_claude(
        prompt, cfg.digest_model, cfg, system=skills.with_profile(sk.system, cfg)))


def _produce(cfg: Config, topic: Topic, row, shared=None):
    """Heavy, DB-free digest work (runs in a worker thread).

    If `shared` (body, tldr) is given, the paper was already digested under another
    topic — reuse that body and only generate the per-topic Relevance (a tiny call,
    saving the full paper text). Otherwise produce the full digest and return the
    topic-agnostic body to cache.
    Returns (canonical_id, topic_slug, rel_path|None, error|None, tldr, shared_body|None)."""
    cid, slug = row["canonical_id"], topic.slug
    try:
        if shared:
            body, tldr = shared
            relevance = _relevance(cfg, topic, row["title"], tldr or (row["abstract"] or "")[:1500])
            shared_out = None
        else:
            pdf_path = config.ROOT / (row["pdf_path"] or "")
            if not pdf_path.exists():
                return cid, slug, None, "pdf missing", None, None
            cap = cfg.digest_max_chars
            text = extract_text(pdf_path, cid)
            if len(text) < 500:
                text = (row["abstract"] or "")[:cap]
            text = text[:cap]
            if not text.strip():
                return cid, slug, None, "no extractable text", None, None
            sk = skills.load_skill("digest", {"system": SYSTEM, "prompt": PROMPT_TMPL})
            prompt = sk.prompt.format(topic=topic.name, title=row["title"], text=text)
            full = llm.strip_code_fence(llm.run_claude(prompt, cfg.digest_model, cfg, system=sk.system))
            body, relevance = _split_relevance(full)
            tldr = _tldr_of(body)
            shared_out = body
    except llm.LLMError as e:
        return cid, slug, None, str(e), None, None

    out_dir = config.DIGEST_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(row["pdf_path"]).stem if row["pdf_path"] else cid.replace(":", "_")
    out_path = out_dir / f"{stem}.md"
    rel_block = f"\n\n## Relevance to {topic.name}\n\n{relevance}" if relevance else ""
    note = (f"{_front_matter(row, topic, body)}\n\n# {row['title']}\n\n"
            f"{visible_meta_line(row)}\n\n{body}{rel_block}\n")
    out_path.write_text(note, encoding="utf-8")
    return cid, slug, out_path.relative_to(config.ROOT).as_posix(), None, tldr, shared_out


def digest_topic(conn, cfg: Config, topic: Topic, should_continue=None,
                 max_per_topic: int | None = None, fetched_on: str | None = None) -> int:
    """Digest all pending papers for a topic, running `digest_concurrency`
    LLM calls in parallel. Worker threads do the LLM/file work; this (main)
    thread owns all sqlite writes — sqlite connections aren't thread-safe.

    Processed in waves of `digest_concurrency`; `should_continue()` is checked
    before each wave so the run can stop cleanly when the digest window closes.

    `max_per_topic` caps how many (newest-first) pending papers are digested this
    run — used by weekly-conserve mode to do only today's daily digests and defer
    the backlog until the weekly session renews."""
    pending = state.pending_digests(conn, topic.slug, fetched_on=fetched_on)   # newest first
    if max_per_topic is not None and len(pending) > max_per_topic:
        log.info("[%s] conserve mode: digesting newest %d of %d pending (rest deferred)",
                 topic.slug, max_per_topic, len(pending))
        pending = pending[:max_per_topic]
    log.info("[%s] %d papers to digest (concurrency=%d)",
             topic.slug, len(pending), cfg.digest_concurrency)
    if not pending:
        return 0
    # Reuse a topic-agnostic body already produced for this paper under another topic.
    shared_map = {}
    for r in pending:
        s = state.get_shared_digest(conn, r["canonical_id"])
        if s:
            shared_map[r["canonical_id"]] = s
    done = reused = 0
    workers = max(1, cfg.digest_concurrency)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i in range(0, len(pending), workers):
            if should_continue and not should_continue():
                log.info("[%s] digest window closed; stopping (%d still pending)",
                         topic.slug, len(pending) - i)
                break
            futures = [ex.submit(_produce, cfg, topic, row, shared_map.get(row["canonical_id"]))
                       for row in pending[i:i + workers]]
            for fut in as_completed(futures):
                cid, slug, rel, err, tldr, shared_out = fut.result()
                if err:
                    state.mark_failed(conn, cid, slug, err)
                    log.warning("[%s] digest failed %s: %s", slug, cid, err[:80])
                else:
                    state.mark_digested(conn, cid, slug, rel, tldr)
                    if shared_out is not None:
                        state.set_shared_digest(conn, cid, shared_out, tldr or "")
                    else:
                        reused += 1
                    done += 1
                conn.commit()
    log.info("[%s] digested %d/%d (%d reused a shared body)", topic.slug, done, len(pending), reused)
    return done
