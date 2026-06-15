"""Publishing — build the MkDocs site and sync Markdown into the Obsidian vault.

Both outputs are regenerated from the digests/ + trends/ + sqlite state, so they
always reflect the current corpus. The site is force-deployed to the gh-pages
branch via `mkdocs gh-deploy`.
"""
from __future__ import annotations

import datetime as dt
import logging
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


def sync_obsidian(conn, cfg: Config) -> None:
    vault = cfg.obsidian_vault
    vault.mkdir(parents=True, exist_ok=True)
    (vault / ".obsidian").mkdir(exist_ok=True)  # mark as a vault

    today = dt.date.today().isoformat()
    home = ["# 📚 Paper Digest", "", f"_Last updated: {today}._", "", "## Topics", ""]

    for topic in cfg.topics:
        rows = _topic_rows(conn, topic.slug)
        folder = naming.sanitize_title(topic.name)  # '/' etc. are illegal in paths
        tdir = vault / folder
        tdir.mkdir(parents=True, exist_ok=True)

        index_lines = [f"# {topic.name}", ""]

        trend_src = config.TREND_DIR / f"{topic.slug}.md"
        trend_name = f"_Trend - {folder}.md"
        if trend_src.exists():
            (tdir / trend_name).write_text(trend_src.read_text(encoding="utf-8"), encoding="utf-8")
            index_lines.append("➡️ " + _md_link("Trend analysis", trend_name))
            index_lines.append("")

        index_lines.append(f"## Papers ({len(rows)})")
        index_lines.append("")
        for row in rows:
            src = config.ROOT / (row["digest_path"] or "")
            if not src.exists():
                continue
            fname = src.name
            (tdir / fname).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            meta = " · ".join(x for x in (row["published"], row["venue"]) if x)
            line = "- " + _md_link(row["title"], fname)
            if meta:
                line += f"  — {meta}"
            index_lines.append(line)
        if not rows:
            index_lines.append("_No digests yet._")

        index_name = f"_Index - {folder}.md"
        (tdir / index_name).write_text("\n".join(index_lines) + "\n", encoding="utf-8")
        home.append("- " + _md_link(topic.name, f"{folder}/{index_name}")
                    + f"  ({len(rows)} papers)")

    (vault / "Home.md").write_text("\n".join(home) + "\n", encoding="utf-8")
    log.info("obsidian vault synced: %s", vault)


def publish(conn, cfg: Config, deploy: bool = True) -> None:
    build_site(conn, cfg)
    sync_obsidian(conn, cfg)
    if deploy:
        deploy_site(cfg)
