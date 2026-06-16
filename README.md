# Paper Digest Meta-Harness

A personal research radar. Every day at **08:00** it:

1. **Collects** newly published papers for each topic you track — from **arXiv**,
   **HuggingFace** daily papers, and (best-effort) **top conferences** — downloads
   the PDFs into `paper/<topic>/` named `[<Place> <Year>] <Title>.pdf`.
2. **Digests** each new paper with a Claude agent into a structured note.
3. **Analyzes** the research trend per topic (how it developed → current state →
   predicted next steps).
4. **Publishes** to a **GitHub Pages** website and your **Obsidian** vault.

Three agents map to the pipeline: **Collector** (Python) → **Digester** (`claude -p`)
→ **Analyst** (`claude -p`). Agents spawn subagents when useful.

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
```

Stages: `fetch` · `digest` · `trends` · `publish` (default: all in order).

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
