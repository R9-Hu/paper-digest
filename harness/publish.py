"""Publishing — build the MkDocs site and sync Markdown into the Obsidian vault.

Both outputs are regenerated from the digests/ + trends/ + sqlite state, so they
always reflect the current corpus. The site is force-deployed to the gh-pages
branch via `mkdocs gh-deploy`.
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import re
import shutil
import subprocess

import yaml

from . import config, naming, state
from .config import Config

log = logging.getLogger("harness.publish")

TOPIC_EMOJI = {"vlm": "👁️", "med-foundation": "🩺", "agentic-ai": "🤖", "harness": "🛠️"}


def _emoji(slug: str) -> str:
    return TOPIC_EMOJI.get(slug, "📚")


# Custom theme for the MkDocs Material site (written to docs/stylesheets/extra.css).
SITE_CSS = """\
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap');
:root {
  --md-primary-fg-color: #4f46e5;
  --md-primary-fg-color--light: #6366f1;
  --md-primary-fg-color--dark: #3730a3;
  --md-accent-fg-color: #06b6d4;
}
[data-md-color-scheme="slate"] {
  --md-primary-fg-color: #6366f1;
  --md-accent-fg-color: #22d3ee;
  --md-default-bg-color: #0b1020;
  --md-default-bg-color--light: #11182f;
}
/* Gradient brand header + tabs */
.md-header { background: linear-gradient(90deg, #312e81 0%, #4f46e5 55%, #0891b2 100%); }
.md-tabs { background: rgba(15,18,40,.18); }
/* Display font + gradient H1 */
.md-typeset h1, .md-typeset h2, .md-typeset h3 {
  font-family: "Space Grotesk", var(--md-text-font-family, system-ui), sans-serif;
  font-weight: 700; letter-spacing: -.02em;
}
.md-typeset h1 {
  background: linear-gradient(90deg, var(--md-primary-fg-color), var(--md-accent-fg-color));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.md-typeset h2 { margin-top: 2rem; padding-bottom: .25rem;
  border-bottom: 2px solid var(--md-default-fg-color--lightest); }

/* Grid cards on the home page — uniform height regardless of title length */
.md-typeset .grid.cards > ul { align-items: stretch; }
.md-typeset .grid.cards > ul > li {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-top: 3px solid var(--md-accent-fg-color);
  border-radius: 14px; padding: 1rem 1.2rem;
  display: flex; flex-direction: column;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.md-typeset .grid.cards > ul > li:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 26px rgba(0,0,0,.12);
  border-color: var(--md-accent-fg-color);
}
/* Reserve two lines for the title so 1- and 2-line cards align identically. */
.md-typeset .grid.cards > ul > li > :first-child { min-height: 2.7em; margin-bottom: 0; }
/* Push the button row to the bottom of every card. */
.md-typeset .grid.cards > ul > li > :last-child { margin-top: auto; padding-top: .4rem; }

/* Tables */
.md-typeset table:not([class]) {
  border-radius: 10px; overflow: hidden; border: none;
  box-shadow: 0 1px 4px rgba(0,0,0,.10);
}
.md-typeset table:not([class]) th {
  background: var(--md-primary-fg-color); color: #fff; font-weight: 600;
}
.md-typeset table:not([class]) tbody tr:nth-child(2n) td {
  background: var(--md-default-fg-color--lightest);
}
.md-typeset table:not([class]) tbody tr:hover td {
  background: var(--md-accent-fg-color--transparent);
}

/* Admonitions / callouts (rendered from [!info] etc. by mkdocs-callouts) */
.md-typeset .admonition, .md-typeset details {
  border-radius: 12px; border-width: 0 0 0 .25rem;
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
}

/* Buttons + venue badges */
.md-typeset .md-button {
  border-radius: 999px; padding: .25rem .9rem; margin: .2rem .35rem .2rem 0;
  font-size: .72rem; border-width: 1.5px;
}
.md-typeset .venue {
  display: inline-block; padding: .1rem .5rem; border-radius: 6px;
  background: color-mix(in srgb, var(--md-accent-fg-color) 12%, transparent);
  color: var(--md-accent-fg-color);
  border: 1px solid color-mix(in srgb, var(--md-accent-fg-color) 30%, transparent);
  font-size: .7rem; font-weight: 600; white-space: nowrap; letter-spacing: .01em;
}
.md-typeset .venue-none { color: var(--md-default-fg-color--lighter); }
.md-typeset .reason { font-size: .78rem; color: var(--md-default-fg-color--light); font-style: italic; }
/* Tag chips (Material tags plugin) */
.md-typeset .md-tag {
  border-radius: 6px; font-size: .68rem; font-weight: 600;
  background: color-mix(in srgb, var(--md-primary-fg-color) 10%, transparent);
}
/* Keep Date + Venue columns tidy; let the Paper title take the room. */
.md-typeset table:not([class]) td:first-child { white-space: nowrap; color: var(--md-default-fg-color--light); font-variant-numeric: tabular-nums; }
.md-typeset table:not([class]) td:last-child { white-space: nowrap; text-align: right; }
.md-typeset .new-badge {
  display: inline-block; padding: .05rem .5rem; border-radius: 999px;
  background: #e8590c; color: #fff; font-size: .68rem; font-weight: 700;
}
"""

# MathJax config (pairs with pymdownx.arithmatex generic) to render LaTeX equations.
SITE_MATHJAX = """\
window.MathJax = {
  tex: {
    inlineMath: [["\\\\(", "\\\\)"]],
    displayMath: [["\\\\[", "\\\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: { ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex" }
};
"""

# Open paper links in a new tab (content area only; leaves the left nav alone).
SITE_JS = """\
(function () {
  function mark() {
    // Any link to an individual paper page (content tables/digests AND the
    // 'Key papers' entries in the left nav). 'papers-list' is left as-is.
    document.querySelectorAll('a[href*="papers/"]').forEach(function (a) {
      a.target = '_blank';
      a.rel = 'noopener';
    });
  }
  if (document.readyState !== 'loading') mark();
  else document.addEventListener('DOMContentLoaded', mark);
})();
"""

# Obsidian CSS snippet (written to <vault>/.obsidian/snippets/paper-digest.css).
OBSIDIAN_CSS = """\
/* Paper Digest — vault styling (auto-generated) */
.paper-home h1, .paper-index h1, .paper-today h1, .paper-trend h1 {
  background: linear-gradient(90deg, var(--color-accent), var(--color-accent-2, #00a99d));
  -webkit-background-clip: text; background-clip: text; color: transparent;
  font-weight: 800; letter-spacing: -.02em;
}
.paper-index h2, .paper-trend h2, .paper-today h2 {
  border-bottom: 2px solid var(--background-modifier-border); padding-bottom: .2em;
}
.markdown-rendered table { width: 100%; }
.markdown-rendered thead th { background: var(--background-secondary-alt); }
.markdown-rendered tbody tr:nth-child(2n) { background: var(--background-secondary); }
.paper-today .callout[data-callout="success"] { --callout-color: 34, 160, 90; }
.paper-trend .callout[data-callout="tip"] { --callout-color: 14, 120, 220; }
.markdown-rendered .tag { border-radius: 999px; }
"""


# ----------------------------------------------------------------------------- #
# Helpers
# ----------------------------------------------------------------------------- #
def _strip_front_matter(md: str) -> str:
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return md


def _topic_rows(conn, slug: str):
    return state.digested_for_topic(conn, slug)


def _fmt_ts(iso: str) -> str:
    """ISO datetime -> 'YYYY-MM-DD HH:MM UTC' (the earliest-version time)."""
    try:
        d = dt.datetime.fromisoformat(iso)
    except (ValueError, TypeError):
        return iso
    tz = "UTC" if d.utcoffset() in (dt.timedelta(0), None) else (d.tzname() or "")
    return f"{d.strftime('%Y-%m-%d %H:%M')} {tz}".strip()


# ----------------------------------------------------------------------------- #
# Shared overview-page sections (used by both the website and Obsidian)
# Order per topic page: intro -> timeline -> trend digest (+link) -> papers.
# ----------------------------------------------------------------------------- #
def _extract_section(trend_md: str, name: str) -> str | None:
    """Return the body of the `## <name>` section from a raw trend file."""
    body = _strip_front_matter(trend_md)
    for chunk in re.split(r"(?m)^##[ \t]+", body)[1:]:
        nl = chunk.find("\n")
        title = (chunk[:nl] if nl != -1 else chunk).strip()
        content = (chunk[nl + 1:] if nl != -1 else "").strip()
        if title.lower().startswith(name.lower()):
            return content
    return None


def _first_paragraph(text: str) -> str:
    for block in re.split(r"\n\s*\n", text.strip()):
        if block.strip():
            return block.strip()
    return ""


def _topic_intro(topic) -> str:
    if topic.intro:
        return topic.intro
    kw = ", ".join(topic.keywords[:5])
    return f"Research on {topic.name}." + (f" Tracked keywords: {kw}." if kw else "")


def _month_counts(rows) -> list[str]:
    counts: dict[str, int] = {}
    for row in rows:
        pub = row["published"]
        if pub and len(pub) >= 7:
            counts[pub[:7]] = counts.get(pub[:7], 0) + 1
    out = []
    for ym in sorted(counts):
        n = counts[ym]
        out.append(f"- **{ym}** — {n} paper{'s' if n != 1 else ''} digested")
    return out


def _timeline_bullets(trend_md: str | None, rows) -> list[str]:
    """Concise, timestamped timeline. Prefer the Analyst's Timeline section;
    fall back to per-month paper counts so the section is never empty."""
    if trend_md:
        section = _extract_section(trend_md, "Timeline")
        if section:
            bullets = [ln.rstrip() for ln in section.splitlines()
                       if ln.lstrip().startswith(("-", "*"))]
            if bullets:
                return bullets
    return _month_counts(rows)


def _intro_section(topic) -> list[str]:
    return ["> [!info] About this topic", _quote(_topic_intro(topic)), ""]


def _timeline_section(trend_md: str | None, rows) -> list[str]:
    bullets = _timeline_bullets(trend_md, rows)
    return ["## 🕒 Timeline", ""] + (bullets or ["_Not enough data yet._"]) + [""]


def _yearly_digest_lines(topic_name: str, year: int, trend_md: str | None,
                         n_papers: int) -> list[str]:
    """A compact 'year in review' for a passed year, assembled from that year's
    trend report (overview + timeline + key papers) — no extra LLM call."""
    lines = [f"# 🗓️ {year} in Review — {topic_name}", "",
             f"*Compact conclusion of {n_papers} digested {year} papers.*", ""]
    overview = _first_paragraph(_extract_section(trend_md, "Overview") or "") if trend_md else ""
    if overview:
        lines += ["> [!abstract] The year in one paragraph", _quote(overview), ""]
    timeline = _extract_section(trend_md, "Timeline") if trend_md else None
    if timeline:
        lines += ["## 🕒 Timeline", "", timeline, ""]
    key = _extract_section(trend_md, "Key papers") if trend_md else None
    if key:
        lines += ["## 📌 Key papers", "", key, ""]
    if not (overview or timeline or key):
        lines.append("_No trend analysis available for this year yet._")
    lines += ["", "➡️ **[Read the full trend analysis](trend.md)**"]
    return lines


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def _paper_name(title: str) -> str | None:
    """A *distinctive* citable method-name for a paper — the part before the first
    colon when it looks like a coined name: CamelCase (AgentSpec, FlowBank) or
    hyphenated with caps/digits (Claw-SWE-Bench, Orchestra-o1). Returns None for
    common-word acronyms (FOCUS, VISA) and generic phrases, to avoid false links."""
    name = (title or "").split(":", 1)[0].strip()
    if not (4 <= len(name) <= 45):
        return None
    camel = re.search(r"[a-z][A-Z]", name) is not None
    hyphen_distinct = "-" in name and any(c.isupper() or c.isdigit() for c in name)
    return name if (camel or hyphen_distinct) else None


def _key_titles(trend_md: str | None) -> list[str]:
    """Bold paper titles listed in the trend report's 'Key papers' section."""
    if not trend_md:
        return []
    sec = _extract_section(trend_md, "Key papers")
    if not sec:
        return []
    return [_norm_title(m) for m in re.findall(r"\*\*(.+?)\*\*", sec) if m.strip()]


def _is_key(title: str, key_norms: list[str]) -> bool:
    p = _norm_title(title)
    if not p:
        return False
    for k in key_norms:
        if not k:
            continue
        if k in p or p in k or p[:25] == k[:25]:
            return True
    return False


def _today_page_lines(topic_name: str, day: str, table_rows: list[str]) -> list[str]:
    """Body for a topic's dedicated 'Today's Digest' page — papers/posts collected
    on `day` (by fetched_at)."""
    n = len(table_rows)
    lines = [f"# 🆕 Today's Digest — {topic_name}", "",
             f"*New papers/posts collected {day}.*", ""]
    lines.append(f"> [!success] {n} new today" if n else "> [!note] Nothing new today")
    lines.append("")
    if table_rows:
        lines += ["| Date | Paper | Venue |", "| --- | --- | --- |"] + table_rows
    else:
        lines.append("_No new papers today — the next 8am run will refresh this._")
    return lines


def _trend_digest_section(trend_md: str | None, trend_link_md: str | None) -> list[str]:
    out = ["## 📈 Trend", ""]
    overview = _first_paragraph(_extract_section(trend_md, "Overview") or "") if trend_md else ""
    if overview:
        out += ["> [!abstract] Where the field stands", _quote(overview), ""]
    if trend_link_md:
        out += [f"➡️ **{trend_link_md}**", ""]
    elif not overview:
        out += ["_No trend analysis yet._", ""]
    return out


MIN_TAG_FREQ = 3      # a tag needs at least this many papers to be eligible
MAX_INDEX_TAGS = 60   # ... and only the top-N most common are kept (compact index)


def _raw_tags(md: str) -> list[str]:
    """Hashtags from a digest's '## Tags' section, normalized (lowercase, '-' seps)."""
    _, secs = _sections(_split_fm(md)[1])
    for title, body in secs:
        if title.lower().startswith("tag"):
            return [t.lower().replace("_", "-")
                    for t in re.findall(r"#([\w/-]+)", body.replace("/", "-"))]
    return []


def build_tag_vocab(conn) -> tuple[dict, set]:
    """Scan all digests once to build (alias, keep): merge plural→singular when both
    forms occur, then keep only tags shared by >= MIN_TAG_FREQ papers. Compacts the
    Tags index from a long tail of one-offs to a reasonable shared vocabulary."""
    raw = {}
    for row in conn.execute(
            "SELECT digest_path FROM papers WHERE digest_status IN ('digested','compacted') "
            "AND digest_path IS NOT NULL").fetchall():
        p = config.ROOT / row["digest_path"]
        if p.exists():
            for t in set(_raw_tags(p.read_text(encoding="utf-8"))):
                raw[t] = raw.get(t, 0) + 1
    # Merge a plural onto its singular only when the singular also exists (safe).
    present = set(raw)
    alias = {t: t[:-1] for t in present if t.endswith("s") and t[:-1] in present}
    counts: dict[str, int] = {}
    for t, c in raw.items():
        counts[alias.get(t, t)] = counts.get(alias.get(t, t), 0) + c
    ranked = sorted(((t, c) for t, c in counts.items() if c >= MIN_TAG_FREQ),
                    key=lambda kv: (-kv[1], kv[0]))
    keep = {t for t, _ in ranked[:MAX_INDEX_TAGS]}
    return alias, keep


def _canon_tags(raw: list[str], alias: dict, keep: set) -> list[str]:
    out = []
    for t in raw:
        t = alias.get(t, t)
        if t in keep and t not in out:
            out.append(t)
    return out[:5]


def _site_digest(md: str, alias: dict, keep: set, reason: str | None = None) -> str:
    """Website copy of a digest: hoist the body '## Tags' into canonical front-matter
    `tags:` (rendered as chips + a compact Tags index by the Material tags plugin) and
    drop the plain-text tag section. If `reason` is given, surface why the paper was
    selected as a callout below the title."""
    fm, content = _split_fm(md)
    head, secs = _sections(content)
    raw, body_secs = [], []
    for title, body in secs:
        if title.lower().startswith("tag"):
            raw += [t.lower().replace("_", "-")
                    for t in re.findall(r"#([\w/-]+)", body.replace("/", "-"))]
        else:
            body_secs.append((title, body))
    tags = _canon_tags(raw, alias, keep)
    if tags:
        fm["tags"] = tags
    parts = [f"---\n{_dump_fm(fm)}\n---", head]
    if reason:
        parts.append(f"> [!tip] Why this paper was selected\n> {reason}")
    for title, body in body_secs:
        parts.append(f"## {title}\n\n{body}" if body else f"## {title}")
    return "\n\n".join(parts) + "\n"


def _extract_tldr(digest_md: str) -> str:
    return (_extract_section(digest_md, "TL;DR") or "").strip()


def _rich_today_lines(topic_name: str, day: str, brief: str | None, items: list) -> list[str]:
    """Today's Digest: short whole-day overview, then a per-paper TL;DR (with
    expandable links to any cited corpus papers), then the table."""
    lines = [f"# 🆕 Today's Digest — {topic_name}", "",
             f"*New papers/posts collected {day}.*", ""]
    if not items:
        return lines + ["> [!note] Nothing new today", "",
                        "_The next overnight run will refresh this._"]
    lines += [f"> [!success] {len(items)} new today", ""]
    lines += ["## 📋 In brief", "",
              brief or "_The whole-day overview is written during the overnight run._", ""]
    lines += ["## 📝 Today's papers", ""]
    for it in items:
        vb = f'  <span class="venue">{_esc(it["venue"])}</span>' if it["venue"] else ""
        lines += [f'### [{it["title"]}](papers/{it["pslug"]}.md){vb}', "",
                  it["tldr"] or "_(no TL;DR)_", ""]
        if it.get("reason"):
            lines += [f'📌 *Why selected:* {it["reason"]}', ""]
        if it.get("cites"):
            lines.append(f'??? quote "🔗 Cites {len(it["cites"])} paper(s) in this corpus"')
            for (ct, rel, ctldr) in it["cites"]:
                snippet = " ".join((ctldr or "").split())[:160]
                lines.append(f"    - [{_esc(ct)}]({rel}) — {snippet}")
            lines.append("")
    lines += ["## 📄 Table", "", "| Date | Paper | Venue |", "| --- | --- | --- |"]
    lines += [it["row"] for it in items]
    return lines


# ----------------------------------------------------------------------------- #
# GitHub Pages (MkDocs Material)
# ----------------------------------------------------------------------------- #
def build_site(conn, cfg: Config) -> None:
    docs = config.SITE_DIR / "docs"
    if docs.exists():
        shutil.rmtree(docs)
    docs.mkdir(parents=True, exist_ok=True)

    today = dt.date.today().isoformat()
    nav = [{"Home": "index.md"}, {"Tags": "tags.md"}]
    tag_alias, tag_keep = build_tag_vocab(conn)   # compact, merged tag vocabulary
    name_loc, ambiguous = {}, set()   # paper name -> (display, slug, year, pslug)
    written_pages = []                # (page_path, self_name, body_lower) for cross-linking
    home_cards = []
    grand_total = grand_today = 0
    cur_year = dt.date.today().year
    for topic in cfg.topics:
        years = state.years_for_topic(conn, topic.slug)  # newest first
        tdir = docs / topic.slug
        tdir.mkdir(parents=True, exist_ok=True)

        topic_total = topic_today = 0
        year_nav = []        # nav groups, one per year (the left super-titles)
        year_index_lines = []
        topic_index, today_items, cur_ydir = {}, [], None
        latest_dd = state.latest_digest_date(conn, topic.slug)  # most recent digested batch

        for year in years:
            rows = state.digested_for_topic_year(conn, topic.slug, year)
            is_current = year == cur_year
            topic_total += len(rows)
            ydir = tdir / str(year)
            (ydir / "papers").mkdir(parents=True, exist_ok=True)

            tr_src = config.TREND_DIR / topic.slug / f"{year}.md"
            has_trend = tr_src.exists()
            trend_md = tr_src.read_text(encoding="utf-8") if has_trend else None
            if has_trend:
                (ydir / "trend.md").write_text(trend_md, encoding="utf-8")

            key_norms = _key_titles(trend_md)
            key_nav, paper_rows = [], []
            used_slugs: set[str] = set()
            for row in rows:
                src = config.ROOT / (row["digest_path"] or "")
                if not src.exists():
                    continue
                pslug = naming.slugify(row["title"])
                base, i = pslug, 2
                while pslug in used_slugs:
                    pslug = f"{base}-{i}"
                    i += 1
                used_slugs.add(pslug)
                raw = src.read_text(encoding="utf-8")
                reason = (row["select_reason"] if "select_reason" in row.keys() else None)
                (ydir / "papers" / f"{pslug}.md").write_text(
                    _site_digest(raw, tag_alias, tag_keep, reason), encoding="utf-8")
                tldr = (row["tldr"] or "").strip() or _extract_tldr(raw)   # cached TL;DR
                topic_index[_norm_title(row["title"])] = (row["title"], year, pslug, tldr)
                name = _paper_name(row["title"])   # original case — matched case-sensitively
                if name:
                    if name in name_loc:
                        ambiguous.add(name)
                    else:
                        name_loc[name] = (row["title"], topic.slug, year, pslug)
                written_pages.append((ydir / "papers" / f"{pslug}.md", name, raw))
                if _is_key(row["title"], key_norms):
                    key_nav.append({row["title"]: f"{topic.slug}/{year}/papers/{pslug}.md"})
                date = row["published"] or "—"
                v = row["venue"] or ""
                venue_cell = (f'<span class="venue">{_esc(v)}</span>' if v
                              else '<span class="venue-none">—</span>')
                tr = f"| {date} | [{_esc(row['title'])}](papers/{pslug}.md) | {venue_cell} |"
                why = " ".join((reason or "").split()).replace("|", "\\|")
                why_cell = (f'<span class="reason">{_esc(why)}</span>' if why
                            else '<span class="venue-none">—</span>')
                paper_rows.append(f"{tr} {why_cell} |")   # paper-list table adds a Why column
                if is_current and latest_dd and (row["digested_at"] or "").startswith(latest_dd):
                    today_items.append({"title": row["title"], "pslug": pslug,
                                        "venue": v, "row": tr, "tldr": tldr,
                                        "reason": reason, "text_norm": _norm_title(raw)})

            # Full paper-list page (the leaf 'Paper list' nav item opens this table).
            plist = [f"# {topic.name} — {year} · Paper list ({len(paper_rows)})", ""]
            plist += (["| Date | Paper | Venue | Why selected |",
                       "| --- | --- | --- | --- |"] + paper_rows
                      if paper_rows else ["_No papers yet._"])
            (ydir / "papers-list.md").write_text("\n".join(plist) + "\n", encoding="utf-8")

            if is_current:
                cur_ydir = ydir   # rich today.md is written after the loop (needs full index)
                digest_nav = {"Today's Digest": f"{topic.slug}/{year}/today.md"}
                digest_link = f"🆕 **[Today's Digest](today.md)** — {len(today_items)} in the latest batch"
                topic_today += len(today_items)
            else:
                (ydir / "yearly.md").write_text(
                    "\n".join(_yearly_digest_lines(topic.name, year, trend_md, len(rows))) + "\n",
                    encoding="utf-8")
                digest_nav = {"Yearly Digest": f"{topic.slug}/{year}/yearly.md"}
                digest_link = f"🗓️ **[{year} in Review](yearly.md)**"

            # Year overview page.
            trend_link = "[Read the full trend analysis](trend.md)" if has_trend else None
            page = [f"# {topic.name} — {year}", "", digest_link, ""]
            page += _timeline_section(trend_md, rows)
            page += _trend_digest_section(trend_md, trend_link)
            page += [f"## 📄 Papers ({len(paper_rows)})", "",
                     f"➡️ **[Paper list](papers-list.md)** — full table of {len(paper_rows)} papers."]
            if key_nav:
                page.append(f"  ·  ⭐ **{len(key_nav)} key papers** (see _Key papers_ in the left nav).")
            (ydir / "index.md").write_text("\n".join(page) + "\n", encoding="utf-8")

            # Year nav group (super-title) → Trend / digest / Key papers / Paper list.
            children = [f"{topic.slug}/{year}/index.md"]
            if has_trend:
                children.append({"Trend analysis": f"{topic.slug}/{year}/trend.md"})
            children.append(digest_nav)
            if key_nav:
                children.append({"Key papers": key_nav})        # expandable, key paper pages
            children.append({"Paper list": f"{topic.slug}/{year}/papers-list.md"})  # leaf → table
            year_nav.append({str(year): children})

            badge = f"{len(today_items)} in latest batch" if is_current else "year in review"
            year_index_lines.append(
                f"- **[{year}]({year}/index.md)** — {len(rows)} papers · {badge}")

        # Rich Today's Digest (built after the loop so cross-links can reference the
        # whole topic corpus). A paper "cites" another when that paper's title appears
        # in this one's digest text.
        if cur_ydir is not None:
            for it in today_items:
                cites = []
                for nt, (ct, cy, cpslug, ctldr) in topic_index.items():
                    if len(nt) >= 30 and ct != it["title"] and nt in it["text_norm"]:
                        rel = (f"papers/{cpslug}.md" if cy == cur_year
                               else f"../{cy}/papers/{cpslug}.md")
                        cites.append((ct, rel, ctldr))
                it["cites"] = cites[:8]
            brief = (state.meta_get(conn, f"today_brief:{topic.slug}")
                     if state.meta_get(conn, f"today_brief_date:{topic.slug}") == latest_dd else None)
            (cur_ydir / "today.md").write_text(
                "\n".join(_rich_today_lines(topic.name, latest_dd or today, brief or None,
                                           today_items)) + "\n",
                encoding="utf-8")

        # Topic landing: intro + by-year index.
        landing = [f"# {topic.name}", ""] + _intro_section(topic)
        landing += ["## 🗓️ By year", ""] + (year_index_lines or ["_No papers yet._"])
        (tdir / "index.md").write_text("\n".join(landing) + "\n", encoding="utf-8")

        # Topic nav: overview + per-year groups.
        nav.append({topic.name: [f"{topic.slug}/index.md"] + year_nav})

        # Home grid card — Overview, this year, last year.
        links = [f"[Overview]({topic.slug}/index.md){{ .md-button }}"]
        for yr in (cur_year, cur_year - 1):
            if yr in years:
                links.append(f"[{yr}]({topic.slug}/{yr}/index.md){{ .md-button }}")
        grand_total += topic_total
        grand_today += topic_today
        home_cards += [
            f"-   {_emoji(topic.slug)} **[{topic.name}]({topic.slug}/index.md)**",
            "",
            "    ---",
            "",
            f"    **{topic_total}** papers · <span class=\"new-badge\">{topic_today} new today</span>"
            f" · {len(years)} year(s)",
            "",
            "    " + " ".join(links),
            "",
        ]

    home_lines = [
        "---", "hide:", "  - navigation", "  - toc", "---",
        "# 📚 Paper Digest", "",
        "_An auto-generated radar of newly published research — fetched, digested, "
        "and trend-analyzed daily._", "",
        f"`{grand_total} papers`  ·  `{len(cfg.topics)} topics`  ·  "
        f"`{grand_today} new today`  ·  _updated {today}_", "",
        '<div class="grid cards" markdown>', "",
    ] + home_cards + ["</div>"]
    (docs / "index.md").write_text("\n".join(home_lines) + "\n", encoding="utf-8")

    # Tags index page (Material tags plugin populates it) + custom theme assets.
    (docs / "tags.md").write_text(
        "---\nhide:\n  - navigation\n  - toc\n---\n"
        "# 🏷️ Tags\n\nBrowse digested papers by tag.\n", encoding="utf-8")
    (docs / "stylesheets").mkdir(parents=True, exist_ok=True)
    (docs / "stylesheets" / "extra.css").write_text(SITE_CSS, encoding="utf-8")
    (docs / "javascripts").mkdir(parents=True, exist_ok=True)
    (docs / "javascripts" / "newtab.js").write_text(SITE_JS, encoding="utf-8")
    (docs / "javascripts" / "mathjax.js").write_text(SITE_MATHJAX, encoding="utf-8")

    # Cross-link pass: append "Related in this collection" to each paper page for
    # every other corpus paper whose *name* it mentions. Built fresh from the live
    # corpus each publish, so links to compacted/dropped papers vanish automatically.
    names = sorted((n for n in name_loc if n not in ambiguous), key=len, reverse=True)
    if names:
        pat = re.compile(r"(?<![\w-])(" + "|".join(re.escape(n) for n in names) + r")(?![\w-])")
        for path, self_name, body_lower in written_pages:
            hits = {m.group(1) for m in pat.finditer(body_lower)} - {self_name}
            if hits:
                links = [f"- [{_esc(name_loc[n][0])}]"
                         f"(../../../{name_loc[n][1]}/{name_loc[n][2]}/papers/{name_loc[n][3]}.md)"
                         for n in sorted(hits)]
                with open(path, "a", encoding="utf-8") as f:
                    f.write("\n\n## 🔗 Related in this collection\n\n"
                            + "\n".join(links[:12]) + "\n")

    mkdocs_cfg = {
        "site_name": "Paper Digest",
        "site_description": "Daily auto-generated research paper digests and trend analysis",
        "theme": {
            "name": "material",
            "font": {"text": "Inter", "code": "JetBrains Mono"},
            "features": ["navigation.tabs", "navigation.tabs.sticky", "navigation.indexes",
                         "navigation.top", "navigation.tracking", "toc.follow",
                         "content.code.copy", "search.suggest", "search.highlight"],
            "palette": [
                {"media": "(prefers-color-scheme: light)", "scheme": "default",
                 "primary": "indigo", "accent": "teal",
                 "toggle": {"icon": "material/weather-night", "name": "Dark mode"}},
                {"media": "(prefers-color-scheme: dark)", "scheme": "slate",
                 "primary": "indigo", "accent": "teal",
                 "toggle": {"icon": "material/weather-sunny", "name": "Light mode"}},
            ],
        },
        "extra_css": ["stylesheets/extra.css"],
        "extra_javascript": [
            "javascripts/mathjax.js",
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js",
            "javascripts/newtab.js",
        ],
        "markdown_extensions": [
            "admonition", "attr_list", "md_in_html", "tables",
            "pymdownx.details", "pymdownx.superfences", "pymdownx.tasklist",
            {"pymdownx.arithmatex": {"generic": True}},
            {"toc": {"permalink": True}},
        ],
        "plugins": ["callouts", "search", {"tags": {"tags_file": "tags.md"}}],
        "nav": nav,
    }
    (config.SITE_DIR / "mkdocs.yml").write_text(
        yaml.safe_dump(mkdocs_cfg, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    log.info("site built: %d topics", len(cfg.topics))


def deploy_site(cfg: Config) -> bool:
    """Force-deploy site/ to the gh-pages branch of origin."""
    mkdocs_yml = config.SITE_DIR / "mkdocs.yml"
    if not mkdocs_yml.exists():
        log.warning("no mkdocs.yml; skipping deploy")
        return False
    venv_mkdocs = config.ROOT / ".venv" / "bin" / "mkdocs"
    mkdocs_bin = str(venv_mkdocs) if venv_mkdocs.exists() else "mkdocs"
    try:
        subprocess.run(
            [mkdocs_bin, "gh-deploy", "--force", "-f", str(mkdocs_yml),
             "--remote-branch", "gh-pages"],
            cwd=config.ROOT, check=True, capture_output=True, text=True, timeout=300,
        )
        log.info("site deployed to gh-pages")
        return True
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        detail = getattr(e, "stderr", "") or str(e)
        log.warning("gh-deploy failed (push code + enable Pages first): %s", str(detail)[:300])
        return False


# ----------------------------------------------------------------------------- #
# Obsidian vault sync
# ----------------------------------------------------------------------------- #
def _md_link(display: str, target: str) -> str:
    # Angle-bracket destination keeps spaces/brackets valid in CommonMark/Obsidian.
    return f"[{display}](<{target}>)"


# --- Obsidian beautification ------------------------------------------------- #
# Generated notes are rewritten into an Obsidian-native style: YAML properties
# (incl. extracted tags), callouts for TL;DR / Overview / Predictions, and
# emoji section headers.

_HEADING_EMOJI = [
    ("key contribution", "⭐"), ("problem", "🎯"), ("method", "🧩"),
    ("result", "📊"), ("limitation", "⚠️"), ("relevance", "🔗"), ("tag", "🏷️"),
    ("timeline", "🕒"), ("how the field", "📈"), ("current state", "🗺️"),
    ("open problem", "❓"), ("key paper", "📌"), ("overview", "🔭"),
]


def _split_fm(md: str):
    if md.startswith("---"):
        parts = md.split("---", 2)
        if len(parts) == 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                fm = {}
            return fm, parts[2].lstrip("\n")
    return {}, md


def _quote(text: str) -> str:
    """Prefix every line with '> ' so it renders inside an Obsidian callout."""
    return "\n".join((">" if not ln.strip() else f"> {ln}")
                     for ln in text.rstrip().split("\n"))


def _sections(body: str):
    """Return (head_before_first_h2, [(title, content), ...])."""
    chunks = re.split(r"(?m)^##[ \t]+", body)
    head = chunks[0].strip()
    secs = []
    for chunk in chunks[1:]:
        nl = chunk.find("\n")
        if nl == -1:
            secs.append((chunk.strip(), ""))
        else:
            secs.append((chunk[:nl].strip(), chunk[nl + 1:].strip()))
    return head, secs


def _emoji_heading(title: str) -> str:
    low = title.lower()
    for key, em in _HEADING_EMOJI:
        if key in low:
            return f"## {em} {title}"
    return f"## {title}"


def _dump_fm(fm: dict) -> str:
    return yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()


def beautify_digest(md: str) -> str:
    fm, content = _split_fm(md)
    _, secs = _sections(content)
    title = fm.get("title") or "Untitled"

    tldr, tags, body_secs = None, [], []
    for stitle, sbody in secs:
        low = stitle.lower()
        if low.startswith(("tl;dr", "tldr")):
            tldr = sbody
        elif low.startswith("tag"):
            tags = re.findall(r"#([\w/-]+)", sbody)
        else:
            body_secs.append((stitle, sbody))

    if tags:
        fm["tags"] = tags
    fm.setdefault("cssclasses", ["paper-digest"])

    meta = []
    authors = fm.get("authors") or []
    if authors:
        shown = ", ".join(authors[:8]) + (" et al." if len(authors) > 8 else "")
        meta.append(f"> **Authors:** {shown}")
    pub_disp = _fmt_ts(fm["published_time"]) if fm.get("published_time") else (fm.get("published") or "")
    line2 = []
    if fm.get("venue"):
        line2.append(f"**Venue:** {fm['venue']}")
    if pub_disp:
        line2.append(f"**Published (v1):** {pub_disp}")
    if fm.get("source"):
        line2.append(f"**Source:** {fm['source']}")
    if line2:
        meta.append("> " + "  ·  ".join(line2))
    if fm.get("url"):
        meta.append(f"> **Link:** [{fm.get('source', 'open')}]({fm['url']})")

    out = [f"---\n{_dump_fm(fm)}\n---", f"# {title}"]
    if meta:
        out.append("> [!info]- Metadata\n" + "\n".join(meta))
    if tldr:
        out.append("> [!abstract] TL;DR\n" + _quote(tldr))
    for stitle, sbody in body_secs:
        out.append(_emoji_heading(stitle))
        if sbody:
            out.append(sbody)
    if tags:
        out.append("\n".join(["---", " ".join(f"#{t}" for t in tags)]))
    return "\n\n".join(out) + "\n"


def beautify_trend(md: str) -> str:
    fm, content = _split_fm(md)
    head, secs = _sections(content)

    overview, nextsteps, body_secs = None, None, []
    for stitle, sbody in secs:
        low = stitle.lower()
        if low.startswith("overview"):
            overview = sbody
        elif low.startswith("predicted next"):
            nextsteps = sbody
        else:
            body_secs.append((stitle, sbody))

    if fm.get("topic_slug"):
        fm["tags"] = [f"trend/{fm['topic_slug']}"]
    fm.setdefault("cssclasses", ["paper-trend"])

    out = [f"---\n{_dump_fm(fm)}\n---", head or f"# {fm.get('title', 'Trend Analysis')}"]
    if overview:
        out.append("> [!abstract] Overview\n" + _quote(overview))
    for stitle, sbody in body_secs:
        out.append(_emoji_heading(stitle))
        if sbody:
            out.append(sbody)
    if nextsteps:
        out.append("> [!tip]+ 🔮 Predicted next steps\n" + _quote(nextsteps))
    return "\n\n".join(out) + "\n"


def _esc(text: str) -> str:
    return text.replace("|", "\\|")


def sync_obsidian(conn, cfg: Config) -> None:
    vault = cfg.obsidian_vault
    vault.mkdir(parents=True, exist_ok=True)
    obs = vault / ".obsidian"
    obs.mkdir(exist_ok=True)  # mark as a vault
    # Install + enable the styling snippet (merge, don't clobber user settings).
    (obs / "snippets").mkdir(exist_ok=True)
    (obs / "snippets" / "paper-digest.css").write_text(OBSIDIAN_CSS, encoding="utf-8")
    appearance = obs / "appearance.json"
    try:
        data = json.loads(appearance.read_text(encoding="utf-8")) if appearance.exists() else {}
    except (json.JSONDecodeError, OSError):
        data = {}
    snips = set(data.get("enabledCssSnippets", []))
    snips.add("paper-digest")
    data["enabledCssSnippets"] = sorted(snips)
    appearance.write_text(json.dumps(data, indent=2), encoding="utf-8")

    today = dt.date.today().isoformat()
    cur_year = dt.date.today().year
    home = [
        "---", "title: Paper Digest", "cssclasses: [paper-home]", "---",
        "# 📚 Paper Digest", "",
        f"> [!note] Daily research radar across {len(cfg.topics)} topics",
        f"> _Last updated: {today}._", "",
        "## Topics", "",
    ]

    for topic in cfg.topics:
        folder = naming.sanitize_title(topic.name)  # '/' etc. are illegal in paths
        tdir = vault / folder
        # Wipe + regenerate so notes for dropped/compacted-away papers don't linger.
        if tdir.exists():
            shutil.rmtree(tdir)
        tdir.mkdir(parents=True, exist_ok=True)
        years = state.years_for_topic(conn, topic.slug)
        topic_total = topic_today = 0
        year_links = []  # (year, n, rel_from_topic)

        for year in years:
            rows = state.digested_for_topic_year(conn, topic.slug, year)
            topic_total += len(rows)
            ydir = tdir / str(year)
            ydir.mkdir(parents=True, exist_ok=True)

            tr_src = config.TREND_DIR / topic.slug / f"{year}.md"
            has_trend = tr_src.exists()
            trend_md = tr_src.read_text(encoding="utf-8") if has_trend else None
            trend_name = f"_Trend {year}.md"
            if has_trend:
                (ydir / trend_name).write_text(beautify_trend(trend_md), encoding="utf-8")

            paper_table, today_rows = [], []
            for row in rows:
                src = config.ROOT / (row["digest_path"] or "")
                if not src.exists():
                    continue
                fname = src.name
                (ydir / fname).write_text(
                    beautify_digest(src.read_text(encoding="utf-8")), encoding="utf-8")
                date = row["published"] or "—"
                venue = _esc(row["venue"] or "—")
                tr = f"| {date} | {_md_link(_esc(row['title']), fname)} | {venue} |"
                paper_table.append(tr)
                if (row["fetched_at"] or "").startswith(today):
                    today_rows.append(tr)

            # Digest note: Today (current year) or Year-in-Review (passed year).
            if year == cur_year:
                topic_today += len(today_rows)
                dig_name = f"_Today {year}.md"
                dig_md = (["---", f"title: {json.dumps(f'Today — {topic.name} ({year})')}",
                           "cssclasses: [paper-today]", "---"]
                          + _today_page_lines(f"{topic.name} ({year})", today, today_rows))
                dig_label = f"🆕 Today's Digest ({len(today_rows)} new)"
            else:
                dig_name = f"_{year} in Review.md"
                dig_md = (["---", f"title: {json.dumps(f'{year} in Review — {topic.name}')}",
                           "cssclasses: [paper-today]", "---"]
                          + _yearly_digest_lines(topic.name, year, trend_md, len(rows)))
                dig_label = f"🗓️ {year} in Review"
            (ydir / dig_name).write_text("\n".join(dig_md) + "\n", encoding="utf-8")

            # Year index note.
            yindex = ["---", f"title: {json.dumps(f'{topic.name} ({year})')}",
                      "cssclasses: [paper-index]", "---", f"# {topic.name} — {year}", "",
                      "➡️ " + _md_link(dig_label, dig_name), ""]
            yindex += _timeline_section(trend_md, rows)
            trend_link = _md_link("Read the full trend analysis", trend_name) if has_trend else None
            yindex += _trend_digest_section(trend_md, trend_link)
            yindex.append(f"## 📄 Papers ({len(paper_table)})")
            yindex.append("")
            yindex += (["| Date | Paper | Venue |", "| --- | --- | --- |"] + paper_table
                       if paper_table else ["_No digests yet._"])
            yindex_name = f"_Index {year}.md"
            (ydir / yindex_name).write_text("\n".join(yindex) + "\n", encoding="utf-8")
            year_links.append((year, len(rows), f"{year}/{yindex_name}"))

        # Topic landing: intro + by-year list.
        tindex = (["---", f"title: {json.dumps(topic.name)}", "cssclasses: [paper-index]",
                   "---", f"# {topic.name}", ""] + _intro_section(topic)
                  + ["## 🗓️ By year", ""])
        for (year, n, rel) in year_links:
            tindex.append("- " + _md_link(f"{year} — {n} papers", rel))
        if not year_links:
            tindex.append("_No papers yet._")
        tindex_name = f"_Index - {folder}.md"
        (tdir / tindex_name).write_text("\n".join(tindex) + "\n", encoding="utf-8")

        # Home entry: topic → year sub-links.
        home.append(f"- **{_md_link(topic.name, f'{folder}/{tindex_name}')}** — "
                    f"{topic_total} papers · {topic_today} new today")
        for (year, n, rel) in year_links:
            home.append("    - " + _md_link(f"{year} ({n})", f"{folder}/{rel}"))

    (vault / "Home.md").write_text("\n".join(home) + "\n", encoding="utf-8")
    log.info("obsidian vault synced (beautified): %s", vault)


def publish(conn, cfg: Config, deploy: bool = True) -> None:
    build_site(conn, cfg)
    sync_obsidian(conn, cfg)
    if deploy:
        deploy_site(cfg)
