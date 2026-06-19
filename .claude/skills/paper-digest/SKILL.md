---
name: paper-digest
description: Run or inspect the paper digest meta-harness — fetch new papers (arXiv/HuggingFace/conferences), digest them, analyze research trends, and publish to GitHub Pages + Obsidian. Use when the user asks to "run the paper digest", "check for new papers", "update the digest", "add/track a topic", or "regenerate the trends/site".
---

# Paper Digest Meta-Harness

This project (`/home/renjiu/Research/code/paperDigest`) is a daily research radar.
Pipeline: **Collector** (Python, arXiv+HF+conferences) → **Digester** (`claude -p`)
→ **Analyst** (`claude -p`) → **Publisher** (GitHub Pages + Obsidian).

The control surface is `config.yaml` (topics, `earliest_date`, keywords, sources,
models). State/dedup lives in `state/papers.db`.

## Common actions

Run from the project root using the project venv.

- **Full daily run:** `./run.sh`
- **Preview matches (no download):** `.venv/bin/python -m harness.orchestrate --stage fetch --dry-run`
- **One topic, full chain:** `.venv/bin/python -m harness.orchestrate --topic <slug>`
- **Single stage:** `.venv/bin/python -m harness.orchestrate --stage {fetch|digest|trends|publish}`
- **Override backfill date:** `... --stage fetch --since 2025-06-01`
- **Build/sync without deploying:** `.venv/bin/python -m harness.orchestrate --stage publish --no-deploy`
- **Weekly review/复盘 (E):** `.venv/bin/python -m harness.orchestrate --review` — one LLM call
  synthesizing the week (themes, gaps, suggested keywords/skills); writes `reviews/<ISO-week>.md`
  + the site's **Review** dashboard. Otherwise fires automatically once per ISO week.
- **Check model availability:** `.venv/bin/python -m harness.orchestrate --check-models`
  (probes the pinned models via `claude -p`; reports + auto-falls-back to the family
  alias if an ID was retired). Daily runs do this pre-flight automatically;
  `--skip-model-check` opts out.

## Adding / editing a topic
Edit `config.yaml` → append (or modify) a block under `topics` with `name`, `slug`,
`earliest_date`, `arxiv_categories`, `keywords`, `huggingface`, `conferences`.
Then run a fetch (optionally `--topic <slug>`).

## Skills, profile, review (self-growing cycle)
- **Prompt methodology lives in `skills/<name>.md`** (editable, not in Python). To change
  how papers are selected/digested/analyzed/reviewed, edit the skill file — a missing file
  falls back to the in-code default. This is distinct from *this* Claude-Code skill (which
  documents commands).
- **User identity/needs live in `profile.md`** (injected into selection/relevance/trends/
  review/ask). Edit it to retune what's surfaced.
- **Review (E)** keyword suggestions: read them on the Review page / `reviews/`. Apply
  them with `.venv/bin/python -m harness.orchestrate --apply-suggestions` (merges into
  `config.yaml`, deduped, comments preserved), or copy chosen ones in by hand.
- **Ask panel** (`harness.ask_server`) also has a "What to read next" button → `/recommend`
  (profile-aware reading list for the current topic via the `what-to-read-next` skill).

## Notes for the agent
- Always use `.venv/bin/python`, not system python.
- The digest/trend stages call `claude -p` headless; they cost tokens and take time.
  Prefer `--topic` / `--stage` to scope work when the user asks for something specific.
- Never hand-edit files under `paper/`, `digests/`, `trends/`, or `state/` — they are
  generated. Change behavior via `config.yaml` or the `harness/` code.
- Publishing deploys to the `gh-pages` branch of the repo in `config.yaml`
  (`github_repo`) and writes Markdown into the Obsidian vault (`obsidian_vault`).
