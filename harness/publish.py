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
:root {
  --md-primary-fg-color: #2f3e6e;
  --md-primary-fg-color--light: #4356a0;
  --md-primary-fg-color--dark: #1e2a52;
  --md-accent-fg-color: #00a99d;
}
[data-md-color-scheme="slate"] {
  --md-primary-fg-color: #3a4a86;
  --md-accent-fg-color: #2dd4bf;
  --md-default-bg-color: #0f1424;
}
.md-typeset h1, .md-typeset h2 { font-weight: 800; letter-spacing: -.02em; }
.md-typeset h2 { margin-top: 2rem; padding-bottom: .2rem;
  border-bottom: 2px solid var(--md-default-fg-color--lightest); }

/* Grid cards on the home page */
.md-typeset .grid.cards > ul > li {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 14px; padding: 1rem 1.2rem;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.md-typeset .grid.cards > ul > li:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 26px rgba(0,0,0,.12);
  border-color: var(--md-accent-fg-color);
}

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
  display: inline-block; padding: .05rem .55rem; border-radius: 999px;
  background: var(--md-accent-fg-color); color: #fff; font-size: .68rem; font-weight: 700;
}
.md-typeset .new-badge {
  display: inline-block; padding: .05rem .5rem; border-radius: 999px;
  background: #e8590c; color: #fff; font-size: .68rem; font-weight: 700;
}
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


# ----------------------------------------------------------------------------- #
# GitHub Pages (MkDocs Material)
# ----------------------------------------------------------------------------- #
def build_site(conn, cfg: Config) -> None:
    docs = config.SITE_DIR / "docs"
    if docs.exists():
        shutil.rmtree(docs)
    docs.mkdir(parents=True, exist_ok=True)

    today = dt.date.today().isoformat()
    nav = [{"Home": "index.md"}]
    home_lines = [
        "# 📚 Paper Digest",
        "",
        f"_An auto-generated radar of newly published research — digested and "
        f"trend-analyzed daily. Updated {today}._",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]

    for topic in cfg.topics:
        rows = _topic_rows(conn, topic.slug)
        tdir = docs / topic.slug
        (tdir / "papers").mkdir(parents=True, exist_ok=True)

        # Trend file (raw) — source for the timeline + trend-digest sections.
        trend_src = config.TREND_DIR / f"{topic.slug}.md"
        has_trend = trend_src.exists()
        trend_md = trend_src.read_text(encoding="utf-8") if has_trend else None
        if has_trend:
            (tdir / "trend.md").write_text(trend_md, encoding="utf-8")

        # Per-paper pages (slugified filenames for clean URLs) + table rows.
        paper_nav = []
        paper_rows = []
        today_rows = []
        used_slugs: set[str] = set()
        for row in rows:
            src = config.ROOT / (row["digest_path"] or "")
            if not src.exists():
                continue
            pslug = naming.slugify(row["title"])
            base = pslug
            i = 2
            while pslug in used_slugs:
                pslug = f"{base}-{i}"
                i += 1
            used_slugs.add(pslug)
            (tdir / "papers" / f"{pslug}.md").write_text(
                src.read_text(encoding="utf-8"), encoding="utf-8"
            )
            paper_nav.append({row["title"]: f"{topic.slug}/papers/{pslug}.md"})
            date = row["published"] or "—"
            v = row["venue"] or ""
            venue_cell = f'<span class="venue">{_esc(v)}</span>' if v else "—"
            tr = f"| {date} | [{_esc(row['title'])}](papers/{pslug}.md) | {venue_cell} |"
            paper_rows.append(tr)
            if (row["fetched_at"] or "").startswith(today):
                today_rows.append(tr)

        # Dedicated "Today's Digest" page (sibling to Trend analysis).
        (tdir / "today.md").write_text(
            "\n".join(_today_page_lines(topic.name, today, today_rows)) + "\n",
            encoding="utf-8")

        # Topic overview page: intro -> today link -> timeline -> trend digest -> papers.
        trend_link = "[Read the full trend analysis](trend.md)" if has_trend else None
        page = [f"# {topic.name}", ""]
        page += _intro_section(topic)
        page += [f"🆕 **[Today's Digest](today.md)** — {len(today_rows)} new today", ""]
        page += _timeline_section(trend_md, rows)
        page += _trend_digest_section(trend_md, trend_link)
        page.append(f"## 📄 Papers ({len(paper_rows)})")
        page.append("")
        if paper_rows:
            page += ["| Date | Paper | Venue |", "| --- | --- | --- |"] + paper_rows
        else:
            page.append("_No digests yet._")
        (tdir / "index.md").write_text("\n".join(page) + "\n", encoding="utf-8")

        # Nav: bare index path first => clickable section header (navigation.indexes).
        topic_children = [f"{topic.slug}/index.md"]
        if has_trend:
            topic_children.append({"Trend analysis": f"{topic.slug}/trend.md"})
        topic_children.append({"Today's Digest": f"{topic.slug}/today.md"})
        if paper_nav:
            topic_children.append({"Papers": paper_nav})
        nav.append({topic.name: topic_children})

        # Home grid card per topic.
        links = [f"[Overview]({topic.slug}/index.md){{ .md-button }}"]
        if has_trend:
            links.append(f"[Trend]({topic.slug}/trend.md){{ .md-button }}")
        links.append(f"[Today]({topic.slug}/today.md){{ .md-button }}")
        home_lines += [
            f"-   {_emoji(topic.slug)} **[{topic.name}]({topic.slug}/index.md)**",
            "",
            "    ---",
            "",
            f"    **{len(paper_rows)}** papers · <span class=\"new-badge\">{len(today_rows)} new today</span>",
            "",
            "    " + " ".join(links),
            "",
        ]

    home_lines.append("</div>")
    (docs / "index.md").write_text("\n".join(home_lines) + "\n", encoding="utf-8")

    # Custom theme assets.
    (docs / "stylesheets").mkdir(parents=True, exist_ok=True)
    (docs / "stylesheets" / "extra.css").write_text(SITE_CSS, encoding="utf-8")

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
        "markdown_extensions": [
            "admonition", "attr_list", "md_in_html", "tables",
            "pymdownx.details", "pymdownx.superfences", "pymdownx.tasklist",
            {"toc": {"permalink": True}},
        ],
        "plugins": ["callouts", "search"],
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
    total_papers = 0
    home_rows = []

    for topic in cfg.topics:
        rows = _topic_rows(conn, topic.slug)
        total_papers += len(rows)
        folder = naming.sanitize_title(topic.name)  # '/' etc. are illegal in paths
        tdir = vault / folder
        tdir.mkdir(parents=True, exist_ok=True)

        trend_src = config.TREND_DIR / f"{topic.slug}.md"
        trend_name = f"_Trend - {folder}.md"
        has_trend = trend_src.exists()
        trend_md = trend_src.read_text(encoding="utf-8") if has_trend else None
        if has_trend:
            (tdir / trend_name).write_text(beautify_trend(trend_md), encoding="utf-8")

        # Paper notes + table rows (full + today's).
        paper_table = []
        today_rows = []
        for row in rows:
            src = config.ROOT / (row["digest_path"] or "")
            if not src.exists():
                continue
            fname = src.name
            (tdir / fname).write_text(
                beautify_digest(src.read_text(encoding="utf-8")), encoding="utf-8")
            date = row["published"] or "—"
            venue = _esc(row["venue"] or "—")
            tr = f"| {date} | {_md_link(_esc(row['title']), fname)} | {venue} |"
            paper_table.append(tr)
            if (row["fetched_at"] or "").startswith(today):
                today_rows.append(tr)

        # Dedicated "Today's Digest" note (sibling to the trend note).
        today_name = f"_Today - {folder}.md"
        today_md = ["---", f"title: {json.dumps('Today — ' + topic.name)}",
                    "cssclasses: [paper-today]", "---"] + \
            _today_page_lines(topic.name, today, today_rows)
        (tdir / today_name).write_text("\n".join(today_md) + "\n", encoding="utf-8")

        # Overview note: intro -> today link -> timeline -> trend digest -> papers.
        index = [
            "---", f"title: {json.dumps(topic.name)}", "cssclasses: [paper-index]", "---",
            f"# {topic.name}", "",
        ]
        index += _intro_section(topic)
        index += ["🆕 " + _md_link(f"Today's Digest ({len(today_rows)} new)", today_name), ""]
        index += _timeline_section(trend_md, rows)
        trend_link = _md_link("Read the full trend analysis", trend_name) if has_trend else None
        index += _trend_digest_section(trend_md, trend_link)

        index.append(f"## 📄 Papers ({len(paper_table)})")
        index.append("")
        index += (["| Date | Paper | Venue |", "| --- | --- | --- |"] + paper_table) \
            if paper_table else ["_No digests yet._"]

        index_name = f"_Index - {folder}.md"
        (tdir / index_name).write_text("\n".join(index) + "\n", encoding="utf-8")
        home_rows.append((topic.name, len(paper_table), has_trend, len(today_rows),
                          f"{folder}/{index_name}", f"{folder}/{trend_name}",
                          f"{folder}/{today_name}"))

    home = [
        "---", "title: Paper Digest", "cssclasses: [paper-home]", "---",
        "# 📚 Paper Digest", "",
        f"> [!note] Daily research radar — {total_papers} papers across {len(cfg.topics)} topics",
        f"> _Last updated: {today}._", "",
        "## Topics", "",
    ]
    # Indented tree — nesting shows the level relations.
    for name, n, has_trend, n_today, idx_path, trend_path, today_path in home_rows:
        home.append(f"- **{_md_link(name, idx_path)}** — {n} papers")
        if has_trend:
            home.append("    - " + _md_link("📈 Trend analysis", trend_path))
        home.append("    - " + _md_link(f"🆕 Today's Digest ({n_today})", today_path))
        home.append("    - " + _md_link("📄 Papers & overview", idx_path))
    (vault / "Home.md").write_text("\n".join(home) + "\n", encoding="utf-8")
    log.info("obsidian vault synced (beautified): %s", vault)


def publish(conn, cfg: Config, deploy: bool = True) -> None:
    build_site(conn, cfg)
    sync_obsidian(conn, cfg)
    if deploy:
        deploy_site(cfg)
