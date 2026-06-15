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
        "# Paper Digest",
        "",
        f"_Last updated: {today}._",
        "",
        "An auto-generated radar of newly published research, digested and trend-analyzed daily.",
        "",
    ]

    for topic in cfg.topics:
        rows = _topic_rows(conn, topic.slug)
        tdir = docs / topic.slug
        (tdir / "papers").mkdir(parents=True, exist_ok=True)

        # Per-paper pages (slugified filenames for clean URLs).
        paper_nav = []
        paper_index_lines = []
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
            meta = []
            if row["published"]:
                meta.append(row["published"])
            if row["venue"]:
                meta.append(row["venue"])
            suffix = f" — {' · '.join(meta)}" if meta else ""
            paper_index_lines.append(
                f"- [{row['title']}](papers/{pslug}.md){suffix}"
            )

        # Trend page.
        trend_src = config.TREND_DIR / f"{topic.slug}.md"
        has_trend = trend_src.exists()
        if has_trend:
            (tdir / "trend.md").write_text(
                trend_src.read_text(encoding="utf-8"), encoding="utf-8"
            )

        # Topic landing page.
        landing = [f"# {topic.name}", ""]
        if has_trend:
            landing.append("➡️ **[Trend analysis](trend.md)**")
            landing.append("")
        landing.append(f"## Papers ({len(paper_index_lines)})")
        landing.append("")
        landing += paper_index_lines or ["_No digests yet._"]
        (tdir / "index.md").write_text("\n".join(landing) + "\n", encoding="utf-8")

        # Nav for this topic.
        topic_children = [{"Overview": f"{topic.slug}/index.md"}]
        if has_trend:
            topic_children.append({"Trend analysis": f"{topic.slug}/trend.md"})
        if paper_nav:
            topic_children.append({"Papers": paper_nav})
        nav.append({topic.name: topic_children})

        home_lines.append(
            f"- **[{topic.name}]({topic.slug}/index.md)** — {len(paper_index_lines)} papers"
            + ("  ·  [trend](" + f"{topic.slug}/trend.md)" if has_trend else "")
        )

    (docs / "index.md").write_text("\n".join(home_lines) + "\n", encoding="utf-8")

    mkdocs_cfg = {
        "site_name": "Paper Digest",
        "site_description": "Daily auto-generated research paper digests and trend analysis",
        "theme": {
            "name": "material",
            "features": ["navigation.sections", "navigation.top", "content.code.copy", "search.suggest"],
            "palette": [
                {"scheme": "default", "primary": "indigo", "accent": "indigo",
                 "toggle": {"icon": "material/weather-night", "name": "Dark mode"}},
                {"scheme": "slate", "primary": "indigo", "accent": "indigo",
                 "toggle": {"icon": "material/weather-sunny", "name": "Light mode"}},
            ],
        },
        "markdown_extensions": ["admonition", "pymdownx.details", "pymdownx.superfences",
                                "toc", "tables"],
        "plugins": ["search"],
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
    ("how the field", "📈"), ("current state", "🗺️"), ("open problem", "❓"),
    ("key paper", "📌"), ("overview", "🔭"),
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
    line2 = [f"**{k}:** {fm[v]}" for k, v in
             (("Venue", "venue"), ("Published", "published"), ("Source", "source"))
             if fm.get(v)]
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
    (vault / ".obsidian").mkdir(exist_ok=True)  # mark as a vault

    today = dt.date.today().isoformat()
    total_papers = 0
    home_rows = []

    for topic in cfg.topics:
        rows = _topic_rows(conn, topic.slug)
        total_papers += len(rows)
        folder = naming.sanitize_title(topic.name)  # '/' etc. are illegal in paths
        tdir = vault / folder
        tdir.mkdir(parents=True, exist_ok=True)

        index = [
            "---", f"title: {json.dumps(topic.name)}", "cssclasses: [paper-index]", "---",
            f"# {topic.name}", "",
        ]

        trend_src = config.TREND_DIR / f"{topic.slug}.md"
        trend_name = f"_Trend - {folder}.md"
        has_trend = trend_src.exists()
        if has_trend:
            (tdir / trend_name).write_text(
                beautify_trend(trend_src.read_text(encoding="utf-8")), encoding="utf-8")
            index.append("> [!abstract] Trend analysis")
            index.append("> ➡️ " + _md_link("Read the trend analysis", trend_name))
            index.append("")

        index.append(f"## 📄 Papers ({len(rows)})")
        index.append("")
        if rows:
            index.append("| Date | Paper | Venue |")
            index.append("| --- | --- | --- |")
            for row in rows:
                src = config.ROOT / (row["digest_path"] or "")
                if not src.exists():
                    continue
                fname = src.name
                (tdir / fname).write_text(
                    beautify_digest(src.read_text(encoding="utf-8")), encoding="utf-8")
                date = row["published"] or "—"
                venue = _esc(row["venue"] or "—")
                link = _md_link(_esc(row["title"]), fname)
                index.append(f"| {date} | {link} | {venue} |")
        else:
            index.append("_No digests yet._")

        index_name = f"_Index - {folder}.md"
        (tdir / index_name).write_text("\n".join(index) + "\n", encoding="utf-8")
        home_rows.append((topic.name, len(rows), has_trend,
                          f"{folder}/{index_name}", f"{folder}/{trend_name}"))

    home = [
        "---", "title: Paper Digest", "cssclasses: [paper-home]", "---",
        "# 📚 Paper Digest", "",
        f"> [!note] Daily research radar — {total_papers} papers across {len(cfg.topics)} topics",
        f"> _Last updated: {today}._", "",
        "## Topics", "",
        "| Topic | Papers | Trend |",
        "| --- | --- | --- |",
    ]
    for name, n, has_trend, idx_path, trend_path in home_rows:
        trend_cell = _md_link("📈 trend", trend_path) if has_trend else "—"
        home.append(f"| {_md_link(_esc(name), idx_path)} | {n} | {trend_cell} |")
    (vault / "Home.md").write_text("\n".join(home) + "\n", encoding="utf-8")
    log.info("obsidian vault synced (beautified): %s", vault)


def publish(conn, cfg: Config, deploy: bool = True) -> None:
    build_site(conn, cfg)
    sync_obsidian(conn, cfg)
    if deploy:
        deploy_site(cfg)
