# Paper Digest — a self-growing knowledge base

A personal research radar built as a **self-growing knowledge-base loop**
(Claude + Obsidian + a webpage):

- **A · 收集 Collect** — newly published papers per tracked topic from **arXiv**,
  **HuggingFace** daily papers, and (best-effort) **top conferences**; deduped and
  ranked, the highest-impact ones downloaded to `paper/<topic>/`.
- **B · 处理 Digest** — each paper reduced by a Claude agent to a structured note.
- **C · 技能/方法库 Skill library** — the reusable *methodologies* behind every step
  (selection, digest, trends, review) live as **editable files in `skills/`**, not
  buried in code. Edit them, add new ones; the library accrues. See [`skills/README.md`](skills/README.md).
- **D · 沉淀+输出 Precipitate & output** — per-topic/per-year **trend** maps, a hybrid
  **RAG card cache**, and publishing to a **GitHub Pages** site + your **Obsidian** vault.
- **E · 回流/复盘 Review & flow back** — a weekly **review** synthesizes the week, spots
  gaps, and **suggests next focus / keywords / new skills**, surfaced on the site's
  **Review** dashboard so the base keeps improving.

Who the base serves is set once in [`profile.md`](profile.md) (identity + what you
value); it's injected into selection, relevance, trends, review, and the ask panel.
The pipeline runs as Python (**Collect**) → `claude -p` agents (**Digest/Trends/Review**)
→ **Publisher**; each LLM step's prompt comes from the editable skill library.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Requirements already present on the host: `pdftotext` (poppler), `gh` (authenticated),
and Claude Code CLI logged in (so `claude -p` headless needs no API key).

## Configure

Edit [`config.yaml`](config.yaml):
- Add/remove **topics** (each with `slug`, `earliest_date`, `arxiv_categories`,
  `keywords`, `huggingface`, `conferences`).
- `earliest_date` controls how far back the **first** run reaches; later runs are
  incremental (only genuinely new papers, deduped via `state/papers.db`).
- Pick `digest_model` / `trend_model` and `max_papers_per_topic_per_run`.

## Run

```bash
# Full daily pipeline (all topics):
./run.sh

# Granular control:
.venv/bin/python -m harness.orchestrate --stage fetch --dry-run     # preview matches
.venv/bin/python -m harness.orchestrate --topic vlm                 # one topic, full chain
.venv/bin/python -m harness.orchestrate --stage digest              # only the digest stage
.venv/bin/python -m harness.orchestrate --since 2025-06-01          # override earliest date
.venv/bin/python -m harness.orchestrate --review                    # run the weekly review/复盘 now, then publish
```

Stages: `fetch` · `digest` · `trends` · `publish` (default: all in order). The weekly
review (E) also fires automatically once per ISO week on the first in-window run.

## Skill library (C) & profile

- **`skills/<name>.md`** — each step's prompt/methodology, editable without touching
  Python (`digest`, `impact-ranking`, `relevance`, `trend-synthesis`, `daily-brief`,
  `followup-qa`, `review`, …). Missing/old file → built-in default is used, so nothing
  breaks. Format + list: [`skills/README.md`](skills/README.md).
- **`profile.md`** — your identity/needs (YAML frontmatter + notes). Layered onto each
  skill's system prompt at runtime so collection/digests/trends reflect *you*. Absent
  file → no injection (original behavior).
- **Weekly window** — `week_usage` (the conserve gate) measures usage since the
  current session reset. The reset **auto-learns** itself: when `claude` reports a
  usage limit, the harness captures the reset time (a weekly reset is >24h out, vs
  the 5-hour one) into `meta['session_reset_at']` and rolls it weekly — re-checked
  every run, no manual input. `weekly_reset_weekday/hour` in `config.yaml` is just
  the fallback until that's learned.
- **Review** — `harness.review` writes `reviews/<ISO-week>.md`, stores it in the
  `meta` table, and renders the **Review** dashboard page (site + Obsidian `_Review.md`).
  Keyword suggestions default to **suggest-only**; opt in to apply them with
  `--apply-suggestions` (merges them into `config.yaml`, deduped, comments preserved).
- **Ask panel** (local, `harness.ask_server`) — besides per-paper Q&A, a
  **"What to read next"** button calls `/recommend` to get a profile-aware, ranked
  reading list for the current topic (via the `what-to-read-next` skill).

### Model checking

The digest/trend stages call pinned Anthropic models (`digest_model` / `trend_model`
in `config.yaml`). Before each LLM run the harness **probes** those models via
`claude -p`; if a pinned ID has been retired/updated, it **auto-falls back** to the
family alias (`opus`/`sonnet`/`haiku`, always the latest) so the run still succeeds,
and logs a note to update `config.yaml`. Check manually anytime:

```bash
.venv/bin/python -m harness.orchestrate --check-models   # report (and exit)
# add --skip-model-check to any run to bypass the pre-flight
```

If `ANTHROPIC_API_KEY` is set, the report also lists currently available model IDs
from the Models API to help you pick a new pin.

## Schedule (08:00 daily)

Scheduling uses a **systemd user timer** with `Persistent=true`, so a run missed
while the machine was asleep/off is **caught up** on the next boot (cron would
silently skip it). See [`systemd/README.md`](systemd/README.md) for install/operate.

```bash
systemctl --user list-timers paper-digest.timer   # next/last run
systemctl --user start paper-digest.service       # trigger a run now
```

The machine still needs to be on at some point each day for the run to happen.

## Layout

| Path | What |
|------|------|
| `config.yaml` | topics + settings (the control surface) |
| `harness/` | the pipeline (fetch / digest / trends / publish / orchestrate) |
| `paper/<slug>/` | downloaded PDFs |
| `digests/<slug>/` | per-paper digest notes |
| `trends/<slug>.md` | per-topic trend analysis |
| `state/papers.db` | sqlite dedup + run state |
| `site/` | MkDocs site source (published to GitHub Pages) |
| `PLAN.md` / `PROGRESS.md` | design + build tracking |

## Notes
- Conference coverage is **best-effort** (OpenReview for ICLR/NeurIPS + venue tags
  parsed from arXiv `comment` fields); arXiv + HuggingFace are the reliable backbone.
- Everything is plain Markdown, so output is portable across web + Obsidian.
