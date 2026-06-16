---
title: "VisualClaw: A Real-Time, Personalized Agent for the Physical World"
authors: ["Haoqin Tu", "Jianwen Chen", "Zijun Wang", "Siwei Han", "Juncheng Wu", "Hardy Chen", "Haonian Ji", "Kaiwen Xiong", "Jiaqi Liu", "Peng Xia", "Jieru Mei", "Hongliang Fei", "Jason Eshraghian", "Zeyu Zheng", "Yuyin Zhou", "Huaxiu Yao", "Cihang Xie"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T06:58:22+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16295"
url: "http://arxiv.org/abs/2606.16295v1"
pdf: "paper/harness/[Arxiv 2026] VisualClaw A Real-Time, Personalized Agent for the Physical World.pdf"
---

# VisualClaw: A Real-Time, Personalized Agent for the Physical World

*🕒 **Published (v1):** 2026-06-15 06:58 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16295v1)*

## TL;DR
VisualClaw is a self-evolving multimodal agent that addresses three VLM deployment gaps—dense video upload cost, static scaffolds, and missing agentic evaluation—through a three-timescale harness: a CPU-only cascaded frame gate, a hot/cold skill injector, and a memory-augmented offline evolver. It cuts per-question API cost by −98.1% on average versus full-frame upload while improving accuracy on video-QA benchmarks, and transfers the same self-evolution stack to a new 200-scenario agentic benchmark (VisualClawArena) where it outperforms non-evolving baselines by up to +8.2 macro accuracy points.

## Problem
Deploying VLMs for real-time, streaming video tasks faces three unsolved gaps simultaneously: (1) dense frame upload makes API cost prohibitive at scale (e.g., a 30-min clip at 1 fps costs ~1.93M input tokens per question); (2) the agent scaffold is fixed at deployment and cannot adapt from its own failures without weight updates; (3) standard video-QA benchmarks test one-shot answer selection rather than whether agents can use visual evidence inside tool-using workspaces with file manipulation and executable checks.

## Method
VisualClaw is a three-timescale scaffold wrapped around frozen cloud VLM weights:

**Per-frame (~10 µs, edge):** A cascaded gate G processes streaming frames with three CPU-only stages—perceptual hash (dHash) for near-duplicate rejection, a 128-dim encoder (HSV histogram, luminance, edge density, texture), and an adaptive change gate with temporally-decaying thresholds—emitting MAJOR/MINOR/SKIP verdicts online without buffering the full clip. Only MAJOR frames are forwarded to the cloud.

**Per-question (~10 ms, cloud):** A hot/cold skill injector embeds each question with a sentence-transformer, inlines the top-k skills ("hot tier") as full markdown cards into the system prompt, and exposes remaining skills as a compact name+description catalogue ("cold tier"), decoupling per-question prompt cost from bank size.

**Per-session (offline):** After every Nevo=15 failures, an LLM evolver E updates the skill bank S using retrieved failure trajectories and confidence-gated episodic memories. Two variants: **Cat.** appends raw retrieved memories to the evolution prompt; **Guide** prepends an instruction prefix telling the evolver to abstract reusable skills rather than echo scenario specifics. Two bank-hygiene filters maintain quality: F1 rejects near-duplicate entries via token-Jaccard overlap at evolve-time; F2 prunes skills whose per-skill hit rate lags the bank mean.

VisualClawArena (200 scenarios, 3,106 total steps) is curated via a five-stage pipeline—candidate generation, timestamped workspace construction, paired text-only/with-clip leakage filtering, multimodal criteria selection, and health checks—averaging 24.4 steps and 18.1 visual-required steps per scenario, scored by executable checkers rather than bare answer matching.

## Key Contributions
- CPU-only cascaded frame gate that runs online (no full-clip access), no LLM in the selection loop, and no GPU—first such mechanism in this comparison set
- Hot/cold hybrid skill injection bounding prompt cost at O(k) regardless of bank size
- Memory-augmented meta-evolver with two instantiation modes (Cat., Guide) and self-healing bank hygiene (dedup + utility pruning)
- VisualClawArena: 200-scenario multimodal agentic benchmark with executable-check scoring, supporting both Codex and Claude Code backends via a staged-workspace bridge
- Demonstration that the same evolution stack transfers from single-call video-QA to multi-step agentic execution

## Results
- **Video-QA accuracy (streaming vs. Plain baseline, Gemini 3 Flash):** avg +3.85%, peak +15.80% on EgoSchema; EgoPlan-Bench +4.23%
- **FullEvo on offline Uniform-8 baseline (Gemini 3 Flash):** +13.00% EgoSchema (60.6%→73.6%), +12.15% EgoPlan-Bench, +5.34% V-MME long, +3.50% NextQA
- **EgoSchema leaderboard:** streaming FullEvo (Guide) 68.40% vs. VideoAgent 60.20%; offline Uniform-8+FullEvo 73.60% vs. Gemini 1.5 Pro 72.20% and LLoVi (GPT-4o) 67.60%
- **Cascade-fill at matched K=8 budget beats Uniform-8:** +1.80% NextQA, +3.58% EgoPlan-Bench (without evolution); compounds with FullEvo (+1.50%, +1.95%)
- **API cost reduction:** −98.1% avg vs. full-frame @1 fps; peak −99.3% on V-MME long (30-min clips); −25.9% vs. Uniform-8+FullEvo
- **VisualClawArena (Codex):** VisualClaw Cat. 54.27% macro; +2.92 over w/o FullEvo; +4.02 over Uniform-8 (50.25%)
- **VisualClawArena (Claude Code):** VisualClaw Cat. 52.16% macro; +3.16 over w/o FullEvo; +8.17 over Uniform-8 (43.99%); Cascade-8 costs −9.5% vs. Uniform-8
- **Difficulty stratification:** FullEvo gains concentrate on Hard scenarios (+5.4 Codex, +5.3 Claude Code over w/o FullEvo); slight regression on Easy (already-saturated) scenarios

## Limitations
- Evolution is triggered only after accumulating Nevo=15 failures; the scaffold is static until that threshold is crossed
- Guide variant (best for video-QA) underperforms Cat. in agentic settings—the two modes require different deployment decisions with no automatic selector
- FullEvo marginally hurts Easy scenarios by introducing prompt noise or over-correction in near-saturated regimes
- VisualClawArena contains only 200 scenarios; the VSI indoor split remains the hardest (~36–38% macro) and is underrepresented in easy tiers
- Offline evolver adds per-session latency (uses Claude Haiku 4.5); cost of evolution calls is not reported for video-QA experiments, only for VisualClawArena
- Cascade gate parameters (τmajor=0.30, 10 s silence ceiling) are fixed; sensitivity analysis is deferred to appendices not reproduced here

## Relevance to Harnesses / Meta-Harnesses
VisualClaw is architecturally a meta-harness: it wraps frozen VLM weights with an externally-evolving scaffold (skill bank + episodic memory) that updates itself between inference calls without gradient-based training—exactly the "scaffold-as-the-unit-of-adaptation" pattern central to meta-harness research. The three-timescale design (per-frame gate / per-question injection / per-session evolution) provides a concrete, implemented template for composing harness layers with qualitatively different update frequencies. VisualClawArena's staged-workspace bridge—which plugs both Codex and Claude Code as interchangeable backends behind a common scoring contract—is itself a harness abstraction demonstrating how to evaluate scaffold improvements independently of backend choice. For researchers building or benchmarking agentic harnesses, the Cat./Guide distinction and the bank-hygiene filters (dedup + utility pruning) are directly reusable design patterns for managing growing prompt-side knowledge stores without context saturation.

## Tags
#multimodal-agent #skill-evolution #memory-augmented #video-efficiency #agent-scaffold #meta-harness #benchmark #streaming-video
