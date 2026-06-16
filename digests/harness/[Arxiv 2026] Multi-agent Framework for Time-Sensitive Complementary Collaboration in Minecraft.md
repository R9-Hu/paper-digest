---
title: "Multi-agent Framework for Time-Sensitive Complementary Collaboration in Minecraft"
authors: ["Juheon Yi", "Jinglu Wang", "Xiaoyi Zhang", "Yan Lu"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T09:02:33+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.15684"
url: "http://arxiv.org/abs/2606.15684v1"
pdf: "paper/harness/[Arxiv 2026] Multi-agent Framework for Time-Sensitive Complementary Collaboration in Minecraft.pdf"
---

# Multi-agent Framework for Time-Sensitive Complementary Collaboration in Minecraft

*🕒 **Published (v1):** 2026-06-14 09:02 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15684v1)*

## TL;DR
TickingCollabBench is a Minecraft-based benchmark for evaluating LLM agents on time-sensitive complementary collaboration: tasks where heterogeneous agents with partial observability must coordinate under strict real-time deadlines and failure risks. The authors also release TickingCollab, a declarative YAML-driven orchestration framework with an automated, LLM-assisted, feasibility-filtered benchmark generation pipeline. Evaluations show current LLMs fail catastrophically under real-time async conditions, with ~20 s API latency alone driving most failures.

## Problem
Existing Minecraft multi-agent benchmarks (TeamCraft, MineCollab, MineLand, etc.) feature static environments, homogeneous agents, individually-solvable tasks, and no real-time failure risk — making genuine mandatory collaboration optional. Constructing truly dynamic collaborative scenarios with heterogeneous agents required writing low-level Minecraft server plugins from scratch, creating high development overhead and limiting benchmark diversity.

## Method
The paper introduces three components:

1. **TickingCollab framework**: A declarative YAML task specification interface that abstracts Minecraft's primitive APIs. A Fabric server plugin translates YAML event definitions (e.g., `progressive_fill` for lava waves, monster spawn/despawn schedules) into runtime dynamics without custom plugin development. Mineflayer bots serve as the agent–environment bridge.

2. **Feasibility-aware automated benchmark generation**: A user provides a task metadata template with a variable parameter space. GPT-5.1 drafts structurally diverse YAML configurations; a feasibility verifier applies approximate constraint checks (tool tier sufficiency, block spawn counts, survival block quantities, agent DPS vs. enemy HP with margins α, β, γ) to filter out unsolvable configurations. This yielded 634 valid tasks from 750 generated (250 per task type).

3. **TickingCollabAgent baselines** with two coordination policies: (a) **Centralized** — a master agent aggregates all peer observations and dispatches actions; (b) **Distributed** — agents plan in parallel via a propose–wait–act negotiation protocol with selective multi-agent broadcasting. Both are evaluated in **synchronous** (simulation paused during LLM inference, isolating planning accuracy) and **asynchronous** (real-time, latency counts) modes.

Four quantitative difficulty metrics are defined: agent heterogeneity H (pairwise normalized attribute distance), collaboration necessity N (total workload / max single-agent throughput; N>1 guarantees mandatory collaboration), environment dynamicity D (state changes per timestep), and time-to-failure τ (seconds until irreversible failure).

## Key Contributions
- TickingCollabBench: 634-task benchmark suite across three task types (crisis preparation, vanishing block mining, boss raid) with quantifiably higher H, N, D, and lower τ than all prior Minecraft multi-agent benchmarks
- TickingCollab framework: declarative YAML dynamic event manager, communication manager, dual-mode evaluator (sync/async), and parallel simulation with fine-grained cost logging
- Feasibility-aware LLM-driven benchmark generation pipeline that navigates an NP-hard configuration space
- Quantitative comparison framework with four collaboration difficulty metrics applied to nine existing benchmarks

## Results
- **Centralized vs. distributed (sync mode, GPT-5.1)**: Centralized outperforms distributed across all tasks; distributed spends most timesteps in planning/negotiation, leaving insufficient time for action
- **Async mode collapses performance**: GPT-5.1 centralized sync → async drops from 0.42→0.15 (crisis), 0.62→0.05 (mine), 0.28→0.06 (raid); ~20 s mean API latency frequently exceeds τ
- **Oracle gap (centralized sync, GPT-5.1 vs. oracle)**: 0.42 vs. 0.91 (crisis), 0.62 vs. 0.80 (mine), 0.28 vs. 0.59 (raid)
- **DeepSeek-R1 centralized sync**: 0.26 (crisis), 0.65 (mine), 0.37 (raid) — comparable to GPT-5.1 on mine, weaker elsewhere
- **Scaling**: More agents improves success on mine/raid (throughput gain) but hurts crisis (more agents require more shelter blocks, increasing workload superlinearly)
- **Communication cost (distributed)**: Message volume and inference calls scale rapidly with team size, frequently hitting the 40-minute simulation timeout

## Limitations
- Only structured semantic sensors; no first-person video/audio — VLM evaluation deferred to future work
- Oracle still uses hand-crafted heuristics for NP-hard scheduling; optimal oracle performance is not guaranteed, especially for raid (moving enemies complicate planning)
- Feasibility verification uses approximate constraints with tunable margins, so some filtered-in configurations may remain practically unsolvable under runtime stochasticity
- Evaluated only two LLMs (GPT-5.1, DeepSeek-R1); no smaller/open-weight model diversity
- The ~20 s API latency bottleneck is a property of current cloud LLM APIs, not inherent to agent architecture

## Relevance to Harnesses / Meta-Harnesses
TickingCollab is directly a multi-agent orchestration harness: it abstracts environment APIs into a declarative YAML spec, manages dynamic event injection, bridges agent runtimes to simulation, and provides dual execution modes to isolate reasoning accuracy from system latency — all canonical harness-layer concerns. The automated benchmark generation pipeline is a meta-harness pattern: an LLM generates configuration instances over a parameter space, and a programmatic verifier filters them for validity before they are consumed by evaluation agents. The dual sync/async execution modes provide a reusable technique for decoupling correctness evaluation from latency evaluation in any time-sensitive agentic harness. The communication manager abstraction (mapping high-level actions to low-level API calls, returning structured observations) mirrors the tool-call/observation loop used in production agentic harnesses, making the coordination overhead findings directly applicable to real harness design.

## Tags
#multi-agent #benchmark #orchestration-framework #minecraft #llm-agents #harness #automated-benchmark-generation #real-time-constraints
