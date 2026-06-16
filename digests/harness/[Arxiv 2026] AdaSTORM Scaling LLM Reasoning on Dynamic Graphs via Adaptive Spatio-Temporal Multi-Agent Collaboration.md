---
title: "AdaSTORM: Scaling LLM Reasoning on Dynamic Graphs via Adaptive Spatio-Temporal Multi-Agent Collaboration"
authors: ["Bing Hao", "Ruijie Wang", "Haodong Qian", "Yunlong Chu", "Yuhang Liu", "Yumeng Lin", "Minglai Shao", "Jianxin Li"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T07:32:44+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16328"
url: "http://arxiv.org/abs/2606.16328v1"
pdf: "paper/harness/[Arxiv 2026] AdaSTORM Scaling LLM Reasoning on Dynamic Graphs via Adaptive Spatio-Temporal Multi-Agent Collaboration.pdf"
---

# AdaSTORM: Scaling LLM Reasoning on Dynamic Graphs via Adaptive Spatio-Temporal Multi-Agent Collaboration

*🕒 **Published (v1):** 2026-06-15 07:32 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16328v1)*

## TL;DR

AdaSTORM is a two-stage multi-agent framework that scales LLM reasoning over dynamic graphs from tens of nodes to thousands, using RL-driven adaptive graph partitioning followed by spatio-temporally decoupled agent collaboration. It is the first MAS framework specifically designed for dynamic graph reasoning. On graphs of 500–1000 nodes, it achieves >90% accuracy on several tasks where all baselines score 0%.

## Problem

LLMs reasoning over dynamic graphs are bottlenecked by exponential context growth and finite context windows, limiting practical handling to graphs with tens of nodes. Standard multi-agent paradigms (chain, debate) operate globally on full graph topology and fail under combinatorial explosion at scale. No prior MAS framework addresses dynamic graph partitioning or spatio-temporal agent coordination.

## Method

AdaSTORM operates in two sequential stages:

**Adaptive Partitioning:** A multimodal Capacity Estimator fuses LM-encoded queries, LM-encoded model profiles, GNN-based structural encodings, and a learnable latent vector into a joint embedding, then uses an MLP to predict per-region reasoning feasibility ϕᵢ. A Cost Estimator programmatically traces agent invocations to compute inference cost C(P). An RL-based Adaptive Partitioner (trained via policy-gradient optimization) refines a METIS warm-start partitioning through two actions—region splitting and node migration—maximizing a reward that balances feasibility improvement and cost reduction while penalizing over-segmentation.

**Collaborative Reasoning:** Resulting partitions are mapped to a LangGraph-maintained shared global state. Spatial Agents handle static local topology and cut-edge communication; Temporal Agents enforce chronological constraints on event quadruples (u, v, s, t), operating either as pre-filters or post-validators. Agents execute in parallel with message passing across boundary cut-edges.

## Key Contributions

- First multi-agent framework tailored for large-scale dynamic graph reasoning.
- RL-based adaptive partitioner with a capacity-feasibility constraint and cost minimization objective; objective-agnostic design generalizes across task types.
- Dynamic graph lifecycle quadruple (u, v, s, t) representation that maximizes temporal information density with minimal token overhead.
- Spatio-temporal decoupled agent architecture integrating with LangGraph for parallel execution.
- Empirical demonstration of scaling dynamic graph LLM reasoning to 1,000-node graphs.

## Results

- **Large-scale (N=500/800/1000, Table 1):** All baselines (DeepSeek-Distill-7/14/32B standalone, GPT-4o mini, DeepSeek-V4-Flash, chain-MAS, debate-MAS) score 0% on Community Detection, Connected Components, and Temporal Motif Counting at all scales. AdaSTORM-32B achieves 71%/52%/26% (Community Detection), 90%/77%/63% (Connected Components), 90%/88%/72% (Reachability), 100%/91%/83% (Temporal Motif Counting) at N=500/800/1000.
- **Temporal Motif Counting at N=500:** 100% accuracy (AdaSTORM-32B).
- **Capacity Estimator ablation (Table 3):** Removing the estimator (random feasibility score) drops Connected Components accuracy from 90%→61% at N=500 and raises token cost from 16,723→33,756.
- **Adaptive Partitioner ablation (Fig. 6):** AdaSTORM-32B outperforms METIS-STORM, GAP-STORM, KaHIP-STORM, and Random-STORM on both accuracy and token cost at all scales.
- **Existing small-to-medium benchmarks (Fig. 5):** AdaSTORM achieves SOTA on GraphWiz, GraphArena, GraphInstruct, NLGraph, GPC, LLM4DyG.
- **Real-world datasets (Table 2):** Evaluated on Wikipedia (9,227 nodes), Reddit (10,984 nodes), Enron (184 nodes), Flights (13,169 nodes), UNTrade (255 nodes); generalizes robustly with variable per-task performance.

## Limitations

- Framework assumes global reasoning can be decomposed into subregion sub-tasks; less applicable to problems requiring rich semantic attributes, external domain knowledge, or highly ambiguous NL objectives.
- LLM backbone treated as a black box—local reasoning errors, unstable intermediate outputs, and imperfect capacity estimation propagate to final results.
- Partition count k scales with graph size (e.g., 162 regions for N=1000 with 32B backbone), adding coordination overhead.
- Performance on real-world datasets is inconsistent (e.g., Temporal Motif Counting: 100% on Reddit/Wiki but 5–10% on UNTrade/Flight), suggesting sensitivity to graph density and temporal structure.

## Relevance to Harnesses / Meta-Harnesses

AdaSTORM is a concrete example of a task-decomposition meta-harness: it does not modify the base LLM but wraps it in an orchestration layer (RL-based partitioner + LangGraph coordinator) that dynamically determines how many agents to spawn and how to route sub-tasks—analogous to how a meta-harness decides which sub-agents to invoke and with what scope. The capacity estimator functions as a load-balancer for cognitive load, a pattern directly relevant to meta-harness design where estimating per-agent feasibility before delegation avoids catastrophic failure. The framework's objective-agnostic partitioner and LangGraph-based shared-state communication demonstrate composable, topology-aware orchestration patterns that translate naturally to general multi-agent harness architectures managing heterogeneous sub-agents across structured problem spaces.

## Tags

#multi-agent #dynamic-graphs #llm-reasoning #graph-partitioning #reinforcement-learning #orchestration #spatio-temporal #scalability
