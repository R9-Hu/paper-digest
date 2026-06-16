---
title: "daVinci-kernel: Co-Evolving Skill Selection, Summarization, and Utilization via RL for GPU Kernel Optimization"
authors: ["Dayuan Fu", "Mohan Jiang", "Tongyu Wang", "Dian Yang", "Jiarui Hu", "Liming Liu", "Jinlong Hou", "Pengfei Li"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T09:58:21+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16497"
url: "http://arxiv.org/abs/2606.16497v1"
pdf: "paper/agentic-ai/[Arxiv 2026] daVinci-kernel Co-Evolving Skill Selection, Summarization, and Utilization via RL for GPU Kernel Optimization.pdf"
---

# daVinci-kernel: Co-Evolving Skill Selection, Summarization, and Utilization via RL for GPU Kernel Optimization

*🕒 **Published (v1):** 2026-06-15 09:58 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16497v1)*

## TL;DR
daVinci-kernel is a reinforcement learning framework for GPU kernel optimization that jointly trains three agents—Skill Selection, Policy, and Skill Summary—sharing one LLM backbone over a dynamically evolving skill library. Candidate skills are admitted only after execution-based verification confirms reproducible speedups, ensuring the library stays aligned with the policy's advancing capability frontier. On KernelBench, daVinci-kernel-14B outperforms the prior best RL-trained model (Dr. Kernel-14B) by up to 46% on the hardest level.

## Problem
Existing LLM-based kernel optimization agents improve the generator for the current task but do not maintain a skill library that co-evolves with training. As the policy improves, early-stage optimization knowledge becomes stale or already internalized, and the remaining performance gap requires subtler, more coordinated transformations. Static skill banks or retrieval-only approaches therefore fail to sustain high-quality speedups over long training horizons.

## Method
Three agents share a single Qwen3 backbone and are initialized via diversity-filtered SFT (HDBSCAN-clustered downsampling to reduce generic skill dominance), then jointly optimized end-to-end with REINFORCE:

- **Skill Selection Agent**: Two-stage retrieval—BM25 pre-filters to top-20 candidates; LLM reranker selects up to 3 skills via a `select_skills` tool call with chain-of-thought reasoning.
- **Policy Agent**: Multi-turn CUDA/Triton kernel generation conditioned on injected skill content; uses TRLOO with bottleneck-aware rewards (correctness × speedup × profiling ratio) and mismatch-ratio sampling (MRS/PRS).
- **Skill Summary Agent**: Triggered when a rollout exceeds relative (α=1.2×) and absolute (β=1.2×) speedup thresholds; distills the trajectory into structured skills (name/description/scope/tags/content) via `update_skill_library` tool call; each candidate is execution-verified before library admission.

Joint RL uses per-agent advantage estimation: policy uses cross-scheme TRLOO over (k+1)×n=16 trajectories; selection advantage compares mean returns across k=3 skill schemes via LOO; summary advantage compares verified speedup across s=2 parallel summary calls via LOO. The library is updated atomically at each training step.

## Key Contributions
- A closed-loop RL framework coupling skill discovery (Summary Agent) and skill exploitation (Policy Agent) through a dynamically evolving, execution-verified skill library.
- Per-agent advantage estimation enabling joint end-to-end optimization of three heterogeneous agents sharing one backbone.
- Diversity-filtered SFT cold start using Qwen3-Embedding-8B + HDBSCAN to prevent skill mode collapse from generic patterns.
- Empirical demonstration that frontier-aware skill evolution is the key driver of gains on hard tasks, not backbone scale.

## Results
- **daVinci-kernel-14B on KernelBench** (Fast1 threshold): Level 1: 37.2%, Level 2: 70.6%, Level 3: 32.2% — vs. Dr. Kernel-14B (reproduce): 30.4% / 58.5% / 22.1%.
- **Level 3 improvement**: up to 46% over Dr. Kernel-14B on Fast1; Level 3 Fast1.2: 7.3% vs. 2.8%.
- **daVinci-kernel-8B**: Level 2 Fast1.2 improves from 9.4% (Dr. Kernel-8B reproduce) to 22.1%.
- **Best-turn (TTS) performance** — 14B: Level 2 Fast1.2 reaches 63.2%, Level 3 Fast1 reaches 68.5%.
- **Ablation 1 (no inference-time skill injection)**: Level 2 Fast1 drops from 44.8% to 20.6% (8B); Level 3 from 10.1% to 2.0% — largest single-component degradation.
- **Ablation 5 (no skills at all)**: Level 2 Fast1 reaches 51.6% (8B) but Level 2 Fast2 collapses to 2.1% and Level 3 Fast1.5 to 0.0%, confirming skills are necessary for deep speedups.
- **Ablation 4 (BM25-only selection)**: Level 3 Fast1 can match or exceed full model but collapses at Fast1.5 (0.2% vs. 2.0%), showing LLM reranking is required for high-precision optimization.

## Limitations
- Evaluation confined to KernelBench; generalization to other GPU programming domains (e.g., custom hardware backends, non-CUDA targets) is not demonstrated.
- Skill library growth is conservative (one skill per task per step) — aggressive growth strategies are unexplored.
- The three-agent joint training adds orchestration complexity; training cost and wall-clock overhead relative to single-agent RL are not quantified.
- Skill verification requires re-executing the policy, introducing additional compute per training step.
- Performance at the strictest thresholds (Fast2) remains low even for the best model (Level 3 Fast2: 1.3%), indicating hard limits on very-high-speedup tasks.

## Relevance to Agentic AI / LLM Agents
daVinci-kernel is a concrete instantiation of *frontier-aware skill evolution*: it treats the knowledge library not as a static retrieval index but as a co-training participant that must continuously update to match the agent's shifting competence boundary — a pattern directly applicable to any long-horizon agentic task where early-learned behaviors become irrelevant as the agent improves. The three-agent architecture with per-agent advantage estimation demonstrates how to joint-optimize heterogeneous roles (retriever, executor, distiller) sharing one backbone, which is a reusable design primitive for multi-role LLM agent systems. The execution-gated skill admission mechanism provides a template for grounding skill accumulation in verifiable outcome signals rather than plausibility — critical for reliability in tool-using agents. This work extends the Voyager/ExpeL/SkillRL lineage by showing that co-evolution of skill generation, selection, and policy through RL is strictly necessary for sustained improvement beyond what retrieval augmentation or RL alone can achieve.

## Tags
#gpu-kernels #skill-learning #multi-agent #reinforcement-learning #code-generation #benchmark #tool-use #knowledge-evolution
