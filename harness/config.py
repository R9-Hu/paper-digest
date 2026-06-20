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
SKILLS_DIR = ROOT / "skills"        # C: editable prompt/methodology library
REVIEW_DIR = ROOT / "reviews"       # E: weekly review (复盘) notes
DB_PATH = STATE_DIR / "papers.db"
PROFILE_PATH = ROOT / "profile.md"  # user identity/needs profile


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
class Profile:
    """User identity/needs — injected into selection, digestion, trends, review, and
    the ask panel so the knowledge base reflects *who it serves*. Loaded from
    profile.md; absent file → cfg.profile is None and nothing is injected."""
    identity: str = ""
    values: list[str] = field(default_factory=list)
    reading_pace: str = ""
    avoid: list[str] = field(default_factory=list)
    notes: str = ""

    def as_context(self, max_chars: int = 1200) -> str:
        bits = []
        if self.identity:
            bits.append(f"Identity: {self.identity}")
        if self.values:
            bits.append("Values: " + "; ".join(self.values))
        if self.reading_pace:
            bits.append(f"Reading pace: {self.reading_pace}")
        if self.avoid:
            bits.append("Avoid: " + "; ".join(self.avoid))
        if self.notes:
            bits.append(self.notes.strip())
        return "\n".join(bits)[:max_chars].strip()


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
    wait_for_token_reset: bool
    rate_limit_max_wait_sec: int
    weekly_digest_budget: int
    weekly_conserve_threshold: float
    weekly_reset_weekday: int
    weekly_reset_hour: int
    monthly_keep: int
    yearly_keep: int
    topics: list[Topic]
    profile: "Profile | None" = None

    def topic(self, slug: str) -> Topic | None:
        return next((t for t in self.topics if t.slug == slug), None)


def load_profile(path: Path | str = PROFILE_PATH) -> "Profile | None":
    """Parse profile.md (YAML frontmatter + free-text notes body). None if absent."""
    p = Path(path)
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    fm, notes = {}, text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                fm = {}
            notes = parts[2].strip()
    if not isinstance(fm, dict):
        fm = {}
    return Profile(
        identity=str(fm.get("identity", "")).strip(),
        values=[str(v) for v in (fm.get("values") or [])],
        reading_pace=str(fm.get("reading_pace", "")).strip(),
        avoid=[str(v) for v in (fm.get("avoid") or [])],
        notes=notes,
    )


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
        wait_for_token_reset=bool(g.get("wait_for_token_reset", True)),
        rate_limit_max_wait_sec=int(float(g.get("rate_limit_max_wait_hours", 6)) * 3600),
        weekly_digest_budget=int(g.get("weekly_digest_budget", 2500)),
        weekly_conserve_threshold=float(g.get("weekly_conserve_threshold", 0.8)),
        weekly_reset_weekday=int(g.get("weekly_reset_weekday", 0)),
        weekly_reset_hour=int(g.get("weekly_reset_hour", 0)),
        monthly_keep=int(g.get("monthly_keep", 100)),
        yearly_keep=int(g.get("yearly_keep", 400)),
        topics=topics,
        profile=load_profile(),
    )


def ensure_dirs() -> None:
    for d in (PAPER_DIR, DIGEST_DIR, TREND_DIR, STATE_DIR, TEXT_DIR, SITE_DIR, LOG_DIR,
              SKILLS_DIR, REVIEW_DIR):
        d.mkdir(parents=True, exist_ok=True)
