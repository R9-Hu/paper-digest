---
title: "Orchestra-o1: Omnimodal Agent Orchestration"
authors: ["Fan Zhang", "Vireo Zhang", "Shengju Qian", "Haoxuan Li", "Hao Wu", "Jinyang Wu", "Donghao Zhou", "Zhihong Zhu", "Zheng Lian", "Xin Wang", "Pheng-Ann Heng"]
source: "Arxiv"
venue: ""
published: "2026-06-10"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13707"
url: "http://arxiv.org/abs/2606.13707v1"
pdf: "paper/harness/[Arxiv 2026] Orchestra-o1 Omnimodal Agent Orchestration.pdf"
---

# Orchestra-o1: Omnimodal Agent Orchestration

## TL;DR
Orchestra-o1 is an omnimodal multi-agent orchestration framework that decouples high-level planning from modality-specialized sub-agent execution, supporting text, image, audio, and video tasks within a unified dependency-aware parallel scheduling loop. It introduces DA-GRPO, an offline RL algorithm that trains a compact 8B open-source orchestrator by aligning step-level orchestration decisions with expert trajectories. On the OmniGAIA benchmark, it achieves 72.8% accuracy (proprietary setting), outperforming Gemini-3-Pro by 10.3%.

## Problem
Existing LLM agent orchestration frameworks are either restricted to text/vision-language tasks or use rigid linear sub-agent pipelines, making them ill-suited for omnimodal tasks where text, image, audio, and video must coexist and interact. Native omnimodal LLMs handle all modalities in a single context and underperform on tasks requiring long-horizon reasoning or fine-grained cross-modal understanding (e.g., Gemini-3-Pro achieves only 62.5% on OmniGAIA under a ReAct wrapper).

## Method
Orchestra-o1 is structured as a three-level hierarchical policy:

**Scaffold layer**: A main agent maintains a latent dependency graph G_t over sub-goals. At each round it selects a parallel-ready batch P_t ⊆ R_t (nodes whose predecessors are complete), respecting cost budget B_t and a parallelism cap K_max. Independent sub-tasks are dispatched asynchronously; dependent ones wait.

**Backend/tool selection**: Each sub-agent backend b is described by a skill vector φ(b) over five capability dimensions (text, image, audio, video, code) plus cost/latency profiles. The main agent matches sub-task requirement vectors r(u) to backends via a cost-aware dot-product objective (Eq. 5). Tool subsets T*(u) are selected similarly via sparse coverage (Eq. 7).

**Context memory**: After each delegation round, results are summarized into structured history H_t. A compressed context C_t+1 is maintained within a token budget L_ctx by maximising information relevance to the query (Eq. 20). The loop terminates when a learned stopping probability exceeds τ_stop.

**DA-GRPO training**: Standard GRPO is adapted for orchestration by scoring each sampled decision offline from reconstructed states without re-executing sub-agents. A four-component rubric reward covers format correctness (binary), action validity (binary), tool reasonableness (0–3), and decision quality (0–3), with weights α=(0.1, 0.1, 0.2, 0.6). Claude-Haiku-4.5 serves as the reward model. 300 seed examples yield ~1,200 verified training samples after cascade quality-gate filtering (anchor coverage, deduplication, modal-bypass test, numerical sandbox check, LLM judge). Orchestra-o1-8B is fine-tuned from Qwen3-8B on 8×H20 GPUs.

## Key Contributions
- **Orchestra-o1 framework**: dependency-aware parallel orchestration for heterogeneous omnimodal tasks, with modality-aware task decomposition, online sub-agent specialization, flexible model/tool backends.
- **DA-GRPO**: offline RL training objective that provides dense step-level supervision over delegation, tool assignment, backend selection, parallel scheduling, and stopping decisions — avoiding costly live sub-agent rollouts during training.
- **Seed-based data curation pipeline**: five rewrite strategies (pivot swapping, temporal shifting, numerical recombination, entity-sibling querying, multi-hop reordering) with cascade verification gates to generate diverse omnimodal training examples.
- **Theoretical grounding**: Proposition 1 (round-level latency advantage of parallel vs. linear orchestration, speedup ≤ K_t); Proposition 2 (information-theoretic justification that specialized orchestration has strictly lower Bayes risk than a native omnidmodal agent under mild assumptions).

## Results
- **Orchestra-o1-GPT-5**: 72.8% overall on OmniGAIA vs. Gemini-3-Pro 62.5% (+10.3%) and AOrchestra-GPT-5 40.0% (+32.8%).
- **Difficulty breakdown (proprietary)**: 80.3% easy / 75.0% medium / 56.4% hard; vs. AOrchestra 45.1% / 40.0% / 32.1% (absolute gains of ~35%, 35%, 24%).
- **Orchestra-o1-8B (open-source)**: 30.0% overall, up from OmniAtlas-Qwen3-30B-A3B at 20.8% — with a 4× smaller main-agent backbone.
- **Efficiency**: Orchestra-o1-GPT-5 achieves 72.8% at aggregate cost 341.6 vs. AOrchestra's 40.0% at cost 565.7 — simultaneously higher accuracy and lower cost.
- **Category gains**: consistent improvements across geography, technology, history, sport, art, movie, science, food on OmniGAIA.

## Limitations
- OmniGAIA is the sole benchmark; generalization to other omnimodal settings (e.g., real-time interactive tasks, streaming modalities) is undemonstrated.
- DA-GRPO training data covers only 1,200 verified examples derived from 300 seeds — limited diversity and scale.
- The cost-aware backend matching (Eq. 5) and tool coverage (Eq. 7) rely on manually specified skill vectors φ(b) and ψ(g); these may not transfer out-of-box to novel models or tools.
- Parallel sub-task latency advantage (Proposition 1) assumes conditionally independent sub-tasks with no shared mutable state — a condition that may not hold in tasks with tight inter-modal dependencies.
- The information-theoretic proof (Proposition 2) relies on the assumption that the main agent aggregates sub-agent evidence without information loss, which is not guaranteed in practice.
- Proprietary backbone (GPT-5) required for SOTA performance; the open-source 8B model lags by 42.8 percentage points.

## Relevance to Harnesses / Meta-Harnesses
Orchestra-o1 is a concrete, formally specified multi-agent harness in which the orchestrator layer itself is a learnable policy — precisely the meta-harness paradigm where the harness logic (decomposition, routing, scheduling, stopping) is not hand-coded but trained end-to-end. DA-GRPO is notable as a training recipe that operates on reconstructed harness states offline, making it cost-efficient to improve the harness controller without re-executing the full pipeline. The dependency-graph representation of sub-task relationships formalizes the scheduling semantics that most meta-harness frameworks leave implicit, offering a blueprint for how harness coordination logic can be made both parallelism-aware and verifiably optimal in latency. This paper connects directly to work on recursive agent harnesses and reward modeling for orchestration by providing an end-to-end trained example of both.

## Tags
#multi-agent #orchestration #omnimodal #reinforcement-learning #grpo #agent-scheduling #meta-harness #benchmark
