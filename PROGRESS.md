# Build Progress — Paper Digest Meta-Harness

Living checklist. See [PLAN.md](PLAN.md) for the full design.
**Updated every ~500K tokens of work and at each milestone.**

Legend: ✅ done · 🔄 in progress · ⬜ todo · ⚠️ blocked

Last updated: 2026-06-15 (infra provisioned; verification running)

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
- 🔄 **6. Provision + verify** — ✅ GitHub repo `R9-Hu/paper-digest` created + pushed,
  ✅ Pages live at https://r9-hu.github.io/paper-digest/, ✅ Obsidian vault created,
  ✅ crontab @ 08:00 installed. 🔄 bounded full-chain verification across all 4 topics
  running (`--max-papers 2 --since 2026-05-20`).

## Notes / decisions
- Hybrid pipeline; local cron @ 08:00; new Obsidian vault `~/Obsidian/PaperDigest`;
  new repo `R9-Hu/paper-digest`.
- Seed topics: vlm, med-foundation, agentic-ai, harness. Backfill since 2025-01-01.
- Digests → Sonnet, trends → Opus (configurable in `config.yaml`).

## Blockers
- _none yet_

## Verification status
- ⬜ fetch dry-run · ⬜ 1-paper full chain · ⬜ idempotency · ⬜ site live · ⬜ Obsidian · ⬜ cron
