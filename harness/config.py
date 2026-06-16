"""Configuration loading for the paper digest harness."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Project root = parent of the harness/ package.
ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.yaml"

# Derived directories (created on demand).
PAPER_DIR = ROOT / "paper"
DIGEST_DIR = ROOT / "digests"
TREND_DIR = ROOT / "trends"
STATE_DIR = ROOT / "state"
TEXT_DIR = STATE_DIR / "text"
SITE_DIR = ROOT / "site"
LOG_DIR = ROOT / "logs"
DB_PATH = STATE_DIR / "papers.db"


@dataclass
class Topic:
    name: str
    slug: str
    earliest_date: dt.date
    arxiv_categories: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    huggingface: bool = True
    conferences: list[str] = field(default_factory=list)
    intro: str = ""   # fixed human-written topic description for the overview page


@dataclass
class Config:
    obsidian_vault: Path
    github_repo: str
    digest_model: str
    trend_model: str
    rank_model: str
    llm_rank: bool
    max_papers_per_topic_per_run: int
    claude_bin: str
    claude_timeout_sec: int
    digest_concurrency: int
    digest_max_chars: int
    digest_window_start: int
    digest_window_end: int
    monthly_keep: int
    yearly_keep: int
    topics: list[Topic]

    def topic(self, slug: str) -> Topic | None:
        return next((t for t in self.topics if t.slug == slug), None)


def _parse_date(value) -> dt.date:
    if isinstance(value, dt.date):
        return value
    if isinstance(value, dt.datetime):
        return value.date()
    return dt.date.fromisoformat(str(value))


def load_config(path: Path | str = CONFIG_PATH) -> Config:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    g = data.get("global", {})
    topics = [
        Topic(
            name=t["name"],
            slug=t["slug"],
            earliest_date=_parse_date(t["earliest_date"]),
            arxiv_categories=list(t.get("arxiv_categories", [])),
            keywords=list(t.get("keywords", [])),
            huggingface=bool(t.get("huggingface", True)),
            conferences=list(t.get("conferences", [])),
            intro=str(t.get("intro", "")).strip(),
        )
        for t in data.get("topics", [])
    ]
    return Config(
        obsidian_vault=Path(g["obsidian_vault"]).expanduser(),
        github_repo=g["github_repo"],
        digest_model=g.get("digest_model", "claude-sonnet-4-6"),
        trend_model=g.get("trend_model", "claude-opus-4-8"),
        rank_model=g.get("rank_model", g.get("digest_model", "claude-sonnet-4-6")),
        llm_rank=bool(g.get("llm_rank", True)),
        max_papers_per_topic_per_run=int(g.get("max_papers_per_topic_per_run", 30)),
        claude_bin=g.get("claude_bin", "claude"),
        claude_timeout_sec=int(g.get("claude_timeout_sec", 600)),
        digest_concurrency=int(g.get("digest_concurrency", 4)),
        digest_max_chars=int(g.get("digest_max_chars", 30000)),
        digest_window_start=int(g.get("digest_window_start", 21)),
        digest_window_end=int(g.get("digest_window_end", 6)),
        monthly_keep=int(g.get("monthly_keep", 100)),
        yearly_keep=int(g.get("yearly_keep", 400)),
        topics=topics,
    )


def ensure_dirs() -> None:
    for d in (PAPER_DIR, DIGEST_DIR, TREND_DIR, STATE_DIR, TEXT_DIR, SITE_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)
