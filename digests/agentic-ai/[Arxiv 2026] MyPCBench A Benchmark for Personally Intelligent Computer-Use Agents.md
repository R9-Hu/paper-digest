---
title: "MyPCBench: A Benchmark for Personally Intelligent Computer-Use Agents"
authors: ["Lawrence Keunho Jang", "Andrew Keunwoo Jang", "Jing Yu Koh", "Ruslan Salakhutdinov"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T14:08:09+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16748"
url: "http://arxiv.org/abs/2606.16748v1"
pdf: "paper/agentic-ai/[Arxiv 2026] MyPCBench A Benchmark for Personally Intelligent Computer-Use Agents.pdf"
---

# MyPCBench: A Benchmark for Personally Intelligent Computer-Use Agents

*🕒 **Published (v1):** 2026-06-15 14:08 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16748v1)*

## TL;DR
MyPCBench is a reproducible Linux-desktop benchmark that evaluates computer-use agents as personal assistants operating over a single coherent user identity (Michael Scott from The Office) seeded across 17 simulated web applications. It reveals that even the best current model (Claude Opus 4.6) solves only 55.4% of 184 tasks fully, with performance collapsing on cross-application and long-horizon tasks.

## Problem
Existing computer-use and desktop agent benchmarks run against impersonal, minimally-seeded environments where tasks are scoped to whatever data the current task literally requires. This excludes the majority of real personal-assistant use cases—those requiring login-gated accounts, cross-app consistent history, and user-specific context (e.g., "which restaurant do I order from every Friday?"). No prior benchmark seeds a coherent user identity at the scale of a full personal computer.

## Method
The authors construct a Docker-packaged Ubuntu 24.04 VM (QEMU/KVM + GNOME Shell) populated deterministically from a single JSON persona spec for Michael Scott. A Python pipeline seeds 17 custom Next.js web-app clones (analogues of Gmail, Chase, DoorDash, Delta, etc.) with cross-consistent records: 1,812 bank transactions, 2,398 emails, 679 calendar events, 402 food-delivery orders, 10,746 browser history entries, etc., such that any real-world event (e.g., a trip) leaves correlated records across every plausibly relevant app. Tasks (184 total) are derived by manually sifting 2,749 real OpenClaw community requests and rewriting them to reference Michael's seeded data. Each task carries a natural-language rubric (mean 6.5 criteria; 1,191 total). Agents are evaluated via a ReAct CUA loop with a uniform `computer+bash` tool surface; grading uses an LLM-as-a-judge (Gemini 3.1 Flash-Lite) over full trajectories per rubric item.

## Key Contributions
- Reproducible, cross-app-consistent Linux desktop environment: 17 pre-logged-in web apps + LibreOffice + Firefox profile, seeded end-to-end from one persona spec, packaged as a Docker/QEMU image with deterministic snapshot reset.
- 184 tasks across 6 behavioral types (bounded action, multi-step orchestration, cross-source reconciliation, aggregation & reporting, personal lookup, pattern inference), 68% multi-application, derived from real personal-assistant requests.
- Benchmarking of 6 models (Claude Opus 4.6/Sonnet 4.6, GPT-5.5/GPT-5.4 mini, Qwen 3.5 35B-A3B/9B) with failure taxonomy across trajectory length, app count, and task type.

## Results
- **Claude Opus 4.6**: 55.4% perfect / 81.8% rubric score / 3.61% trajectory efficiency — only model above 50% perfect.
- **Claude Sonnet 4.6**: 39.1% perfect / 65.4% rubric score.
- **GPT-5.5**: 29.3% perfect / 54.1% rubric score.
- **GPT-5.4 mini**: 19.0% perfect / 48.8% rubric score.
- **Qwen 3.5 35B-A3B**: 7.6% perfect / 42.5% rubric score.
- **Qwen 3.5 9B**: 2.7% perfect / 7.0% rubric score (collapses under dual-tool surface).
- At 7+ apps per task: Opus drops to 36%, Sonnet to 14%, GPT-5.5 to 4.5%, all others to 0%.
- Failure modes cluster by family: GPT premature DONE (235/354 hits), Qwen persona-data hallucination (13/31 hits), Claude bash-shortcut (bypassing UI).
- Opus trajectory efficiency is >5× Qwen 9B (3.61 vs. 0.65 rubric points/step).

## Limitations
- Single persona (Michael Scott) limits generalizability; persona-specific quirks from The Office canon may not reflect realistic diversity of user identities.
- Only 184 tasks; coverage of the 17-app space is necessarily sparse (some task types have as few as 11 instances).
- 100-turn hard cap may artificially disadvantage models still climbing at the ceiling (Opus performance was still rising at the cap).
- Grading relies on a single LLM judge (Gemini 3.1 Flash-Lite); inter-annotator reliability on edge cases is not fully characterized.
- Tasks sourced from one community (OpenClaw Discord) may skew toward power-user request types.

## Relevance to Agentic AI / LLM Agents
MyPCBench directly benchmarks the hardest regime for LLM agents—long-horizon, cross-application, identity-grounded computer use—which is the core challenge for personal assistant deployment. Its failure taxonomy (premature termination, persona hallucination, tool-surface misuse) provides actionable diagnostics for agent architecture work, particularly around context management across many apps and tool-use policy. The sharp performance cliff at 7+ apps (Opus: 36%, all others ≤4.5%) quantifies a concrete frontier problem for multi-step agent planning and state tracking. The benchmark's real-world-derived task suite and cross-consistent identity seeding make it a more ecologically valid test of personalization than prior retrieval-augmented or profile-injection approaches.

## Tags
#benchmark #computer-use #personal-assistant #desktop-agent #multi-app #long-horizon #evaluation #llm-agent
