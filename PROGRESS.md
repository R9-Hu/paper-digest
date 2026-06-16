# Build Progress — Paper Digest Meta-Harness

Living checklist. See [PLAN.md](PLAN.md) for the full design.
**Updated every ~500K tokens of work and at each milestone.**

Legend: ✅ done · 🔄 in progress · ⬜ todo · ⚠️ blocked

Last updated: 2026-06-15 (✅ COMPLETE — end-to-end verified)

## Milestones
- ✅ **0. Scaffold + tracking** — git init, dirs, `config.yaml`, `requirements.txt`,
  `.gitignore`, `PLAN.md`, `PROGRESS.md`, `README.md`, venv + deps installed.
- ✅ **1. Foundations** — `harness/config.py`, `harness/models.py`,
  `harness/naming.py`, `harness/state.py` (sqlite). Tested.
- ✅ **2. Collector (Agent 1)** — `harness/fetch.py` + `sources/{arxiv,hf,conf}_source.py`.
  Verified live: arXiv + HF return results, venue detection works, PDF download +
  `[Place Year] Title.pdf` rename confirmed.
- ✅ **3. Digester (Agent 2)** — `harness/digest.py` + `harness/llm.py`
  (pdftotext + `claude -p`). Verified: produced a faithful structured digest.
- ✅ **4. Analyst (Agent 3)** — `harness/trends.py`. Verified: produced a grounded
  trend report.
- ✅ **5. Publish + orchestrate** — `harness/publish.py`, `harness/orchestrate.py`,
  `run.sh`, `.claude/skills/paper-digest/SKILL.md`. MkDocs build + Obsidian sync verified.
- ✅ **6. Provision + verify** — GitHub repo `R9-Hu/paper-digest` created + pushed;
  Pages **live (HTTP 200)** at https://r9-hu.github.io/paper-digest/; Obsidian vault
  created; crontab @ 08:00 installed. Bounded full-chain run across all 4 topics:
  8 downloaded, 8 digested, 4 trend reports, deployed. Idempotency confirmed.

## Status: LIVE
- ✅ **Full backfill complete** (2026-06-15): 128 papers fetched + digested across
  all 4 topics (vlm 33, med-foundation 31, agentic-ai 32, harness 32), 0 failures,
  4 trend reports. Site redeployed (HTTP 200), Obsidian vault populated (137 notes).
- ✅ **Obsidian beautification** shipped: YAML props + extracted tags, callouts
  (TL;DR/Overview/Predictions), emoji headings, table indexes + Home.
- ✅ Incremental per-paper DB commits (durable dedup; safe concurrent access).
- From here the 08:00 cron runs incrementally (only new papers each day).

## Notes / decisions
- Hybrid pipeline; local cron @ 08:00; new Obsidian vault `~/Obsidian/PaperDigest`;
  new repo `R9-Hu/paper-digest`.
- Seed topics: vlm, med-foundation, agentic-ai, harness. Backfill since 2025-01-01.
- Digests → Sonnet, trends → Opus (configurable in `config.yaml`).

## Add-ons (post-launch)
- ✅ **Obsidian beautification** — callouts, property tags, emoji headings, table indexes.
- ✅ **Overview page restructure** (site + Obsidian) — fixed intro callout → concise
  timestamped **Timeline** (from Analyst's new `## Timeline` section; falls back to
  per-month counts) → **Trend digest** (overview teaser + link to full analysis) →
  Papers table. Per-topic `intro` added to config.yaml. Home page is an indented
  tree; website left nav uses `navigation.indexes` for clickable hierarchy.
- ✅ **Model checking + auto-fallback** (`harness/modelcheck.py`) — pre-flight probes
  pinned models via `claude -p`; falls back to the family alias (opus/sonnet/haiku)
  if an ID is retired. Flags: `--check-models`, `--skip-model-check`. Verified
  (OK path + simulated-retirement fallback).

- ✅ **Per-topic Today's Digest** — dedicated page (site `today.md` / Obsidian
  `_Today - <topic>.md`) listing papers collected today (by `fetched_at`); nav
  sibling to Trend analysis, subtitle link on overview, home-tree sibling.
- ✅ **systemd user timer** (replaces cron) — `systemd/paper-digest.{service,timer}`
  with `Persistent=true` (catches up missed runs) + linger. cron entry removed.
- ✅ **Earliest-version publish time in every digest** — `published_ts` captured
  from arXiv v1 (`arxiv_source`), stored in DB (migration), shown in digest
  front matter (`published_time`) + a visible "🕒 Published (v1)" line + Obsidian
  metadata callout. Backfilled 130/137 existing digests via `harness.backfill_published`
  (re-queried arXiv, rate-limit resilient).

## Blockers
- _none yet_

## Verification status
- ⬜ fetch dry-run · ⬜ 1-paper full chain · ⬜ idempotency · ⬜ site live · ⬜ Obsidian · ⬜ cron
