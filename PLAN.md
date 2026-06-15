# Paper Digest Meta-Harness — Implementation Plan

## Context

You want a personal research radar that, **every day at 8am**, surfaces newly
published papers/posts on the topics you care about, downloads them, digests
each one, and tracks how each topic is evolving (with a prediction of likely
next steps). Output goes to two places: a **GitHub Pages website** and your
**Obsidian vault**. The harness must be *configurable*: you add/remove topics
and set how far back the first search reaches.

Today `/home/renjiu/Research/code/paperDigest` is an **empty, non-git folder**.
We build the whole thing from scratch.

### Decisions locked in (from your answers)
- **Pipeline:** Hybrid — Python does the deterministic fetch/download/rename/dedup
  via the arXiv & HuggingFace APIs; **Claude agents** (`claude -p` headless) do
  the digest + trend analysis. Subagents are spawned by those agents when useful.
- **Scheduling:** Local `cron` at 08:00 → `run.sh`. (Machine must be on/online.)
- **Obsidian:** create a **new vault** at `~/Obsidian/PaperDigest`.
- **GitHub Pages:** **new dedicated public repo** `R9-Hu/paper-digest`.
- **Topics (seed):** Vision-Language Models, Foundation Models in Medicine,
  Agentic AI / LLM Agents, Harnesses / Meta-Harnesses.
- **First-run backfill:** since `2025-01-01`; daily runs are incremental.
- Auth already present: `gh` logged in as **R9-Hu** (repo scope); Claude Code
  credentials exist (so `claude -p` headless needs no API key). `pdftotext`
  available for PDF→text.

### The three agents (mapped to your description)
1. **Collector** (`harness/fetch.py`, deterministic Python) — finds & downloads
   new papers, renames them, dedups. May call a Claude subagent only for fuzzy
   conference discovery.
2. **Digester** (`claude -p` per paper) — reads the PDF text, writes a structured
   digest note. May spawn subagents (e.g. to look up related work).
3. **Analyst** (`claude -p` per topic) — reads all digests for a topic, writes the
   trend timeline + current-state + predicted-next-step analysis.

A Python **orchestrator** wires them together so the unattended cron run is
deterministic, logged, and resumable; each LLM step is an isolated `claude -p`
call that fails soft (one bad paper never breaks the run).

---

## Project layout

```
paperDigest/
├── config.yaml                # topics, dates, sources, paths, models  ← user-edited
├── requirements.txt
├── .venv/                     # python venv (arxiv, feedparser, requests, pyyaml, mkdocs-material)
├── README.md
├── run.sh                     # cron entry: activate venv → python -m harness.orchestrate
├── harness/
│   ├── __init__.py
│   ├── orchestrate.py         # MAIN: fetch → digest → trends → publish; logging, --topic/--stage flags
│   ├── fetch.py               # AGENT 1: query, download, rename, dedup
│   ├── sources/
│   │   ├── arxiv_source.py    # arXiv API (category + keyword + date window)
│   │   ├── hf_source.py       # HuggingFace daily-papers API → arxiv PDF
│   │   └── conf_source.py     # OpenReview (ICLR/NeurIPS) + conf tags from arxiv comments (best-effort)
│   ├── digest.py              # AGENT 2 driver: pdftotext → claude -p → digest .md
│   ├── trends.py              # AGENT 3 driver: claude -p over a topic's digests → trend .md
│   ├── publish.py             # build MkDocs site + gh-deploy; sync markdown to Obsidian
│   ├── state.py               # sqlite dedup/state store
│   └── naming.py              # filename builder + sanitizer
├── paper/<topic-slug>/        # downloaded PDFs:  "[Arxiv 2025] Title.pdf"
├── digests/<topic-slug>/      # per-paper digest markdown
├── trends/<topic-slug>.md     # per-topic trend analysis
├── state/papers.db            # sqlite: seen ids, status, per-topic last_run
├── site/ (mkdocs docs)        # generated website source
├── logs/                      # cron.log, per-run logs
└── .claude/
    ├── settings.json          # permissions for headless agents
    └── skills/paper-digest/SKILL.md   # lets you also run it interactively ("run the paper digest")
```

---

## Component details

### `config.yaml` (the meta-harness control surface)
```yaml
global:
  obsidian_vault: /home/renjiu/Obsidian/PaperDigest
  github_repo: R9-Hu/paper-digest
  digest_model: claude-sonnet-4-6      # cheap & good for summarization
  trend_model:  claude-opus-4-8        # deeper reasoning for synthesis
  max_papers_per_topic_per_run: 30     # safety cap (esp. first backfill)
topics:
  - {name: "Vision-Language Models",         slug: vlm,            earliest_date: 2025-01-01,
     arxiv_categories: [cs.CV, cs.CL, cs.LG], keywords: ["vision-language","VLM","multimodal LLM"],
     huggingface: true,  conferences: [CVPR, ICCV, NeurIPS, ICLR]}
  - {name: "Foundation Models in Medicine",  slug: med-foundation, earliest_date: 2025-01-01,
     arxiv_categories: [eess.IV, cs.CV, cs.LG], keywords: ["medical foundation model","clinical LLM","generalist medical"],
     huggingface: true,  conferences: [MICCAI, CVPR, NeurIPS]}
  - {name: "Agentic AI / LLM Agents",        slug: agentic-ai,     earliest_date: 2025-01-01,
     arxiv_categories: [cs.AI, cs.CL, cs.LG], keywords: ["LLM agent","multi-agent","tool use","agentic"],
     huggingface: true,  conferences: [NeurIPS, ICLR, ICML]}
  - {name: "Harnesses / Meta-Harnesses",     slug: harness,        earliest_date: 2025-01-01,
     arxiv_categories: [cs.AI, cs.CL, cs.SE], keywords: ["agent harness","scaffolding","orchestration","agent framework"],
     huggingface: true,  conferences: [NeurIPS, ICLR]}
```
Adding a topic = append a block. Changing reach = edit `earliest_date`.

### Agent 1 — Collector (`fetch.py` + `sources/`)
- **arXiv** (`arxiv_source.py`): query `cat:(...) AND (all:"kw1" OR all:"kw2" ...)`,
  `sort=submittedDate desc`, page until older than `earliest_date`. Use the `arxiv`
  pip package (built on the export API; respects rate limits). Capture title,
  authors, year, abstract, pdf_url, arxiv_id, and the `comment` field (often
  reveals "Accepted to CVPR 2025" → venue).
- **HuggingFace** (`hf_source.py`): pull `https://huggingface.co/api/daily_papers`
  windowed by date, keyword-filter, map each to its arXiv id, download that PDF.
- **Conferences** (`conf_source.py`, best-effort): OpenReview API for ICLR/NeurIPS
  accepted lists; otherwise derive venue from the arXiv `comment` field. Document
  limits in README; never block the run on conference scraping.
- **Dedup/state** (`state.py`): sqlite keyed on canonical id (arxiv id or HF id);
  skip already-seen; record `status` (fetched/digested/failed) and per-topic
  `last_run`. Daily runs therefore fetch only genuinely new items.
- **Download + naming** (`naming.py`): save PDF to `paper/<slug>/`, filename
  `"[<Place> <Year>] <Title>.pdf"` where Place ∈ {Arxiv, HuggingFace, MICCAI, …}.
  Sanitizer strips `<>:"/\|?*`, control chars, collapses whitespace, trims to
  ~150 chars — exactly your "ignore symbols that aren't valid in a filename".

### Agent 2 — Digester (`digest.py`)
- `pdftotext` the PDF → `state/text/<id>.txt`.
- Call `claude -p --model <digest_model> --output-format json` headless with a
  digest prompt that points the agent at the text file (it reads it via the Read
  tool) and **permits spawning subagents** for related-work lookups when useful.
- Output a digest note `digests/<slug>/<same-name>.md` with front matter +
  sections: TL;DR · Problem · Method · Key contributions · Results/numbers ·
  Limitations · Relation to this topic · Tags · Links. Mark `digested` in sqlite.
- Fail-soft: a paper that errors is logged and retried next run; the batch continues.

### Agent 3 — Analyst (`trends.py`)
- Per topic, feed the agent the set of digest notes (new + a rolling window of
  prior ones) via `claude -p --model <trend_model>`.
- Produces `trends/<slug>.md`: how the topic developed → current clusters/SOTA →
  open problems → **predicted next steps**, citing the key papers. May spawn
  subagents per sub-theme. Overwrites the topic's trend file each run (history
  kept in git).

### Publishing (`publish.py`)
- **GitHub Pages:** MkDocs + Material theme. `publish.py` regenerates `site/`
  nav (Home → per-topic: Trend page + list of digest notes), then
  `mkdocs gh-deploy` pushes the built site to the `gh-pages` branch of
  `R9-Hu/paper-digest`. One-time setup: create repo via `gh repo create`, enable
  Pages on `gh-pages`. Final URL: `https://r9-hu.github.io/paper-digest/`.
- **Obsidian:** copy the same digest/trend markdown into
  `~/Obsidian/PaperDigest/<Topic>/`, rewrite links to `[[wikilinks]]`, generate a
  per-topic index note and a vault `Home.md`. Create the vault's `.obsidian/`
  on first run so it opens cleanly. (Plain markdown — no build step.)

### Orchestrator + scheduling
- `orchestrate.py`: loop topics → fetch → digest new → trends → publish; structured
  logging to `logs/`; flags `--topic <slug>`, `--stage fetch|digest|trends|publish`,
  `--dry-run`, `--since <date>` for manual/partial runs.
- `run.sh`: `cd` project, activate `.venv`, `exec python -m harness.orchestrate`.
- **Cron** (added at implementation time): `0 8 * * * /home/renjiu/Research/code/paperDigest/run.sh >> /home/renjiu/Research/code/paperDigest/logs/cron.log 2>&1`.

---

## Progress tracking (user request)
- On approval, copy this plan into the project as `paperDigest/PLAN.md` and create
  `paperDigest/PROGRESS.md` — a living checklist of build steps with status
  (todo / in-progress / done), notes, and blockers.
- **Update `PROGRESS.md` every ~500K tokens of work** (and at each milestone), so
  progress is trackable across sessions. Both files are committed to git, so
  history is preserved.

## Build steps (implementation order)
0. Copy `PLAN.md` + create `PROGRESS.md` in the project folder (tracking).
1. Scaffold project: `git init`, venv, `requirements.txt`
   (`arxiv`, `feedparser`, `requests`, `pyyaml`, `mkdocs-material`), `config.yaml`, `README.md`.
2. `naming.py` + `state.py` (sqlite schema) — the shared foundations.
3. `sources/arxiv_source.py` → `fetch.py` (arXiv path first, end-to-end).
4. Add `sources/hf_source.py`, then best-effort `sources/conf_source.py`.
5. `digest.py` (pdftotext + `claude -p` + digest template).
6. `trends.py` (per-topic synthesis).
7. `publish.py` (MkDocs site + Obsidian sync); create GitHub repo + vault.
8. `orchestrate.py` glue + `run.sh`; `.claude/settings.json` + `paper-digest` skill.
9. Install the 8am crontab entry.

---

## Verification (end-to-end)
- **Dry run:** `python -m harness.orchestrate --stage fetch --dry-run` — confirm
  each topic lists sane, on-topic papers since 2025-01-01 with correct
  `[Place Year] Title` names, no duplicates.
- **One real paper, full chain:** `python -m harness.orchestrate --topic vlm`
  with `max_papers_per_topic_per_run: 1`; verify a PDF in `paper/vlm/`, a digest
  in `digests/vlm/`, a `trends/vlm.md`, the MkDocs site builds, and the note
  appears in `~/Obsidian/PaperDigest/`.
- **Idempotency:** run again immediately → 0 new downloads/digests (sqlite dedup).
- **Web output:** open `https://r9-hu.github.io/paper-digest/` and check nav/search.
- **Obsidian:** open the vault, confirm wikilinks resolve and trend notes render.
- **Schedule:** test `run.sh` standalone, then a throwaway cron a few minutes out
  before relying on the 08:00 entry; check `logs/cron.log`.

## Notes / open items
- Cost: digests default to Sonnet, trends to Opus (configurable in `config.yaml`).
- The machine must be powered on & online at 08:00 (local cron). If it's often
  off, a follow-up could add a `systemd` timer with `Persistent=true` to catch up
  on next boot.
- Conference coverage is best-effort in v1 (OpenReview + arXiv comment tags);
  arXiv + HuggingFace are the reliable backbone.
