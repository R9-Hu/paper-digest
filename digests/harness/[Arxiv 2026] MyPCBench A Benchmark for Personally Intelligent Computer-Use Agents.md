---
title: "MyPCBench: A Benchmark for Personally Intelligent Computer-Use Agents"
authors: ["Lawrence Keunho Jang", "Andrew Keunwoo Jang", "Jing Yu Koh", "Ruslan Salakhutdinov"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T14:08:09+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16748"
url: "http://arxiv.org/abs/2606.16748v1"
pdf: "paper/harness/[Arxiv 2026] MyPCBench A Benchmark for Personally Intelligent Computer-Use Agents.pdf"
---

# MyPCBench: A Benchmark for Personally Intelligent Computer-Use Agents

*🕒 **Published (v1):** 2026-06-15 14:08 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16748v1)*

## TL;DR
MyPCBench is a reproducible Linux-desktop benchmark that evaluates computer-use agents as personal assistants against a fully seeded persona (Michael Scott), spanning 17 logged-in web apps and 184 tasks sourced from real OpenClaw community requests. It exposes a large gap between current frontier capabilities and genuine personal-assistant use: the best model (Claude Opus 4.6) fully solves only 55.4% of tasks, with steep degradation on cross-application and long-horizon work.

## Problem
Existing computer-use benchmarks run against empty or minimally seeded desktops, excluding tasks that require logged-in accounts, personal history, or cross-app consistency — precisely the tasks a real personal assistant must handle. No prior benchmark seeds a coherent, deep user identity across a full desktop stack, leaving evaluation misaligned with deployment.

## Method
The benchmark is packaged as a Docker-hosted QEMU/KVM Ubuntu 24.04 VM with GNOME Shell. A deterministic Python pipeline generates all user data (1,812 bank transactions, 2,398 emails, 679 calendar events, 10,746 browser history entries, etc.) from a single JSON persona spec, writing cross-consistent SQLite databases for 17 Next.js web-app clones plus a populated Firefox profile and home directory. Tasks are derived from 2,749 real OpenClaw Discord requests, filtered and rewritten to reference Michael Scott's seeded data, then assigned natural-language rubrics in the Odysseys format. Evaluation uses a CUA ReAct loop (OSWorld-compatible HTTP Control API) with a shared `computer+bash` tool surface across all models, graded by an LLM-as-a-judge (Gemini 3.1 Flash-Lite) that scores each rubric criterion against the full screenshot trajectory.

## Key Contributions
- A reproducible, persona-seeded Linux desktop (Docker + QEMU, base snapshot reset between tasks) with 17 pre-logged-in consumer web-app clones and ~42,000 rows of cross-consistent user-facing state.
- 184 tasks across 6 behavioral types (bounded action, multi-step orchestration, cross-source reconciliation, aggregation & reporting, personal lookup, pattern inference) with weighted rubrics totaling 1,191 criteria.
- A uniform agent harness extending OSWorld with per-provider CUA translation layers and a shared `computer+bash` action surface; supports 100-turn budgets and snapshot-based task isolation.
- Benchmarking of 6 models (Claude Opus 4.6 / Sonnet 4.6, GPT-5.5 / GPT-5.4 mini, Qwen 3.5 35B-A3B / 9B) with a failure taxonomy identifying 5 distinct failure modes per model family.

## Results
- Claude Opus 4.6: 55.4% perfect, 81.8% rubric score, 3.61 trajectory efficiency — only model above 50%.
- Claude Sonnet 4.6: 39.1% perfect, 65.4% rubric score.
- GPT-5.5: 29.3% perfect, 54.1% rubric score.
- GPT-5.4 mini: 19.0% perfect, 48.8% rubric score.
- Qwen 3.5 35B-A3B: 7.6% perfect, 42.5% rubric score.
- Qwen 3.5 9B: 2.7% perfect, 7.0% rubric score.
- At 7+ apps per task: Opus drops to 36% perfect; GPT-5.5 reaches only 4.5%; GPT-5.4 mini, Qwen 35B, and Qwen 9B reach 0%.
- Failure modes cluster by family: GPT → premature DONE (235/354 hits), Qwen → persona-data hallucination (13/31), Claude → bash shortcutting past the UI.

## Limitations
- Single canonical persona (Michael Scott); no multi-user or adversarial persona coverage.
- 17 apps represent six SimilarWeb categories, omitting many real-world app classes (healthcare, government, IoT).
- 100-turn hard cap may penalize deliberate agents; Opus trajectory curves are still rising at the cap.
- LLM-as-a-judge grading (Gemini 3.1 Flash-Lite) introduces judge-model variance not fully quantified.
- Task set reflects one community's (OpenClaw Discord) request distribution, which may skew toward power-user workflows.
- No evaluation of multi-session memory or persistent state changes across tasks.

## Relevance to Harnesses / Meta-Harnesses
MyPCBench ships a full agent harness as a first-class artifact: it extends the OSWorld HTTP Control API runner with per-provider CUA translation layers, snapshot-based task isolation, a shared tool-surface normalization layer, and an LLM-as-a-judge evaluation pipeline — precisely the components a meta-harness must coordinate. The per-provider action-translation layer (mapping Claude's `computer.click` → OSWorld `click`, adding vendor-specific bash tool equivalents) is a concrete example of provider-agnostic harness abstraction. The rubric-graded, trajectory-level evaluation format (inherited from Odysseys) demonstrates how a meta-harness can decouple task specification from grading logic, enabling reuse across benchmark environments.

## Tags
#benchmark #computer-use-agents #agent-harness #personalization #desktop-automation #llm-as-judge #multi-app #evaluation
