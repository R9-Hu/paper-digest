---
title: "WISE: A Long-Horizon Agent in Minecraft with Why-Which Reasoning"
authors: ["Renmin Cheng", "Changhao Chen"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T03:35:02+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12852"
url: "http://arxiv.org/abs/2606.12852v1"
pdf: "paper/harness/[Arxiv 2026] WISE A Long-Horizon Agent in Minecraft with Why-Which Reasoning.pdf"
---

# WISE: A Long-Horizon Agent in Minecraft with Why-Which Reasoning

*🕒 **Published (v1):** 2026-06-11 03:35 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.12852v1)*

## TL;DR
WISE is a long-horizon embodied agent for Minecraft that closes the loop between exploration, episodic memory, and planning by augmenting conventional what-where-when memory with explicit causal structure via a VLM-built Causal Event Graph. A companion Opportunistic Task Scheduler dynamically reorders pending subtasks when causally relevant entities are encountered, and a three-tier multi-scale exploration strategy ensures spatially comprehensive coverage. Together these components yield a 30-point success-rate gain and 26% faster completion over the prior SOTA low-level controller MrSteve on sequential sparse tasks, and a 44-point gain with 42.5% less time on adaptive non-sequential tasks.

## Problem
Hierarchical LLM-augmented Minecraft agents concentrate research effort on high-level planners while the low-level controller remains the dominant bottleneck. Existing controllers (e.g., MrSteve/PEM) store episodic observations keyed only by visual similarity (cosine distance on MineCLIP embeddings), which breaks under viewpoint changes and occlusion, and cannot infer *why* a past observation is relevant to a new task. Additionally, controllers execute subgoals in a rigid fixed order, missing opportunities when task-relevant entities appear out of sequence. Exploration strategies are similarly greedy and leave large unexplored regions.

## Method
WISE has three tightly integrated modules:

**Causal Event Graph (CEG):** A two-level memory system sits on top of the existing Place Event Memory (PEM). Short-term geometric memory (identical to PEM) retains MineCLIP embeddings clustered by DP-Means for fast visual retrieval. Asynchronously, a VLM (GPT-4o) processes hybrid keyframes selected by both cluster centroids and image entropy. For each keyframe the VLM extracts entity nodes, infers `CAN_OBTAIN` causal edges (e.g., `cow → beef`), and adds `CO_OCCURS_WITH` spatial co-occurrence edges. Retrieval at query time combines cosine visual similarity with a binary causal-match term: `Score(x,τ) = λ·sim(eₓ, Enc(τ)) + (1−λ)·CausalMatch(x,τ)`.

**Opportunistic Task Scheduler (OTS):** At each decision step, every pending subtask receives a priority score `Priority(τᵢ,t) = 0.3·Urgency + 0.5·CausalRel + 0.2·(1−NavCost)`. CausalRel goes high when an active causal path in the CEG links current observations to the subtask. If the highest-priority task differs from the current one, execution is preempted and the queue is reordered.

**Multi-Scale Progressive Exploration:** Three hierarchical tiers: (1) Global — quadtree partitioning with utility = coverage gain − distance penalty, O(log n) region selection; (2) Regional — frontier-based, evaluating coverage gain, novelty, and navigation cost; (3) Local — Voronoi decomposition fills interior coverage gaps every 40 steps.

The three modules form a closed loop: exploration feeds observations → CEG converts them to causal knowledge → OTS consumes that knowledge for adaptive planning.

## Key Contributions
- Identification of the causal-memory disconnect as the primary low-level controller bottleneck (beyond mere memory capacity).
- Causal Event Graph: VLM-driven semantic graph over episodic memory encoding `why` and `which`, enabling viewpoint-invariant and causally grounded retrieval.
- Opportunistic Task Scheduler: priority-weighted dynamic subtask reordering driven by live causal relevance scores.
- Three-tier multi-scale exploration (quadtree global + frontier regional + Voronoi local) achieving O(log n) global efficiency with local completeness guarantees.
- Ablation evidence of synergy: full WISE exceeds the sum of individual module gains.

## Results
All experiments use MineRL on Minecraft Java Edition 1.11.2; baselines are Steve-1 and MrSteve (PEM).

- **Exploration (128×128 simulated, 6k steps):** WISE 99% vs. MrSteve 59% map coverage; rate 0.097 vs. 0.067 coverage/1k steps.
- **Exploration (384×384 simulated, 20k steps):** WISE 98% vs. MrSteve 83%.
- **Exploration (128×128 real Minecraft, 10k steps):** WISE 97% vs. MrSteve 67% vs. Steve-1 19%.
- **ABA-Sparse sequential task (50 episodes, 12k step budget):** WISE 62% success / 5,981 avg. steps vs. MrSteve 32% / 8,123 steps vs. Steve-1 0%; return localization 2,341 steps vs. 4,253 (MrSteve).
- **ABC-Sparse non-sequential task:** WISE 77% success / 4,620 avg. steps vs. MrSteve 33% / 8,040 steps vs. Steve-1 0%.
- **VLM cost:** ~16 GPT-4o calls/episode, ~$0.48/episode; inference runs asynchronously off the control loop.
- Ablation (PEM+Graph only, no OTS or multi-scale exploration): 47% / 42% success on ABA/ABC, confirming each module adds independent gains.

## Limitations
- VLM graph construction (GPT-4o) costs ~$0.48/episode, limiting scalability and reproducibility without API access.
- Causal edges are VLM-generated and may be incorrect or incomplete; no explicit error-correction mechanism is described.
- Opportunistic scheduler weights (`wu`, `wr`, `wn`) are hand-tuned empirically and may not generalize to domains beyond Minecraft.
- Evaluation is restricted to two task types (ABA-Sparse, ABC-Sparse) in Minecraft; generalization to other open-world environments is unvalidated.
- Only 50 episodes per condition reported; confidence intervals and statistical significance are not provided.
- API-privileged agents (Voyager, JARVIS-1, GITM) are excluded from comparison, leaving open questions about how WISE compares to the broader SOTA.

## Relevance to Harnesses / Meta-Harnesses
WISE exemplifies a *closed-loop meta-harness* pattern: instead of a flat sequence of tool calls, its three modules (exploration, causal memory, opportunistic scheduler) form a harness-level control loop in which each component's outputs gate and redirect the others. The Causal Event Graph functions as a structured, queryable knowledge layer—analogous to a harness maintaining typed context across agent steps—while the Opportunistic Task Scheduler acts as a meta-level dispatcher that preempts and reorders subtask execution at runtime based on accumulated semantic state. For researchers building general meta-harnesses, WISE's two-level retrieval (fast visual + slow causal) and its weight-parameterized priority formula offer concrete design patterns for combining immediate perceptual signals with longer-horizon structured knowledge. The asynchronous VLM graph-construction thread also illustrates how expensive reasoning can be decoupled from a real-time control harness without blocking the main execution loop.

## Tags
#embodied-agent #minecraft #episodic-memory #causal-reasoning #task-scheduling #vlm #hierarchical-planning #long-horizon
