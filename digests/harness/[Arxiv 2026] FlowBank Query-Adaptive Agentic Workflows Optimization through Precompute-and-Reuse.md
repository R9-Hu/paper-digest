---
title: "FlowBank: Query-Adaptive Agentic Workflows Optimization through Precompute-and-Reuse"
authors: ["Lingzhi Yuan", "Chenghao Deng", "Fangxu Yu", "Souradip Chakraborty", "Mohammad Rostami", "Furong Huang"]
source: "Arxiv"
venue: ""
published: "2026-06-09"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.11290"
url: "http://arxiv.org/abs/2606.11290v1"
pdf: "paper/harness/[Arxiv 2026] FlowBank Query-Adaptive Agentic Workflows Optimization through Precompute-and-Reuse.pdf"
---

# FlowBank: Query-Adaptive Agentic Workflows Optimization through Precompute-and-Reuse

## TL;DR
FlowBank reframes agentic workflow optimization as portfolio construction: rather than deploying one static workflow or generating a fresh workflow per query, it precomputes a compact bank of complementary workflows offline and routes each query to the best member at inference time. Across five benchmarks, this precompute-and-reuse strategy outperforms both the best automated baseline (AFlow, +4.26% relative) and the best handcrafted baseline (+14.92% relative) while remaining cost-competitive.

## Problem
Existing automated workflow optimization methods make a false dichotomy: task-level methods spend substantial offline compute but deploy only one universal workflow, discarding complementary candidates; query-level methods adapt per query but push expensive generation cost into inference. Neither exploits the observation that workflows discovered during task-level search already solve *different* query subsets, and that a meaningful fraction of queries served by costly query-level generation can be answered by cheaper precomputed workflows.

## Method
FlowBank is a three-stage pipeline.

**Stage 1 – Diversifying (DiverseFlow):** Extends MCTS-based workflow search (built on AFlow) with a two-phase sampling strategy. A performance-oriented warm-up phase seeds the pool with individually strong workflows using accuracy-weighted parent sampling. A complementarity-oriented expansion phase then re-weights queries by difficulty `μ(q) = 1 / (1 + Σ e(ω_i, q))`, steering search toward queries not yet covered by any discovered workflow. The final candidate pool also incorporates a query-level workflow generator (ScoreFlow) as a dynamic workflow member.

**Stage 2 – Curating (CuraFlow):** Solves a coverage-maximizing combinatorial subset selection: for each cardinality k, find the size-k subset of the raw pool that maximizes `Coverage(Ω) = (1/|D|) Σ_q max_{ω∈Ω} e(ω,q)`. The optimal portfolio size k* is the minimum k such that coverage exceeds τ·Coverage(Ω_raw) (τ=0.96). Ties in coverage favor the subset with lowest mean pairwise performance-vector correlation.

**Stage 3 – Matching:** Casts workflow selection as edge-value prediction on a query–workflow bipartite graph G = (D ∪ Ω*, E). Query nodes are initialized from query text embeddings; workflow nodes from workflow-description embeddings. A heterogeneous 2-layer GNN + MLP decoder is trained with masked edge-value regression, where the supervision target is a performance–cost composite: `v_{q,ω} = (1−λ)·ẽ_{q,ω} + λ·(1−c̃_{q,ω})`. At inference, a single GNN forward pass predicts utilities for all portfolio members and selects the argmax.

## Key Contributions
- Empirical demonstration that task-level discarded workflows retain set-level reuse value, and that per-query generation cost is partially redundant (motivating observations on workflow complementarity).
- DiverseFlow: query-difficulty-weighted MCTS that steers search toward uncovered queries to build a coverage-diverse candidate pool.
- CuraFlow: submodularity-aware combinatorial portfolio distillation that compresses the pool to a compact, deployable subset.
- Bipartite GNN matching: pairwise edge-value formulation that exploits query–workflow relational structure and handles utility ties gracefully.
- State-of-the-art average performance across MATH, AMC, MBPP, MMLU Pro, and DROP while remaining on the Pareto frontier for performance–cost trade-off.

## Results
- FlowBank average performance: **73.40** across 5 benchmarks vs. best automated baseline AFlow (GPT-4o) at 70.40 (+3.00 absolute, **+4.26% relative**) and best handcrafted baseline MultiPersona at 63.87 (**+14.92% relative**).
- Per-benchmark scores: MATH 69.34, AMC 67.94, MBPP 84.26, DROP 83.49, MMLU Pro 67.40 — first on all five.
- Average inference cost: **1.65 ×10⁻³ $/1K tokens** vs. AFlow (GPT-4o) at 1.95 and ScoreFlow at 2.37; FlowBank sits on the Pareto frontier (no compared method achieves both higher performance and lower cost).
- FlowBank uses Qwen3-8B as optimizer vs. AFlow's GPT-4o optimizer, yet still outperforms it.
- Ablation: replacing DiverseFlow with AFlow drops average −1.65pts; replacing CuraFlow with top-k accuracy selection drops −1.44pts; skipping curation and matching the full pool degrades performance; GNN selector outperforms flat MLP classifier.

## Limitations
- Coverage-maximizing portfolio search via exhaustive enumeration is tractable only for moderate pool sizes and small k; scalability to very large candidate pools is not analyzed.
- The GNN selector requires training on workflow execution results over D_train for each new benchmark/task distribution, adding offline overhead.
- Portfolio size k* determination depends on τ, a hyperparameter that may need tuning per benchmark; when τ falls on the coverage plateau, an extra portfolio size must be evaluated.
- Incorporating query-level (ScoreFlow) workflows into the pool adds those generation costs during training-time evaluation; the interaction between dynamic workflow generation cost and portfolio curation is not deeply analyzed.
- Generalization to out-of-distribution queries at deployment (inductively, new query types unseen during GNN training) is not evaluated.

## Relevance to Harnesses / Meta-Harnesses
FlowBank is directly relevant as a **meta-harness for workflow management**: it sits above individual agent workflows and orchestrates *which* pre-built workflow is dispatched for each query, making it a query-adaptive execution harness. The three-stage architecture (diversified search → curated portfolio → learned dispatch) mirrors the concerns of meta-harness design—coverage, redundancy elimination, and routing—translated into the agentic workflow domain. The GNN-based matching component is a learned routing layer functionally analogous to orchestrators in multi-agent harnesses, but grounded in graph-relational structure over query–workflow pairs. For researchers tracking harnesses, FlowBank demonstrates that precomputed workflow portfolios with lightweight learned selectors can serve as a practically efficient alternative to heavyweight online meta-agents that generate structure on the fly.

## Tags
#multi-agent #workflow-optimization #portfolio-methods #mcts #graph-neural-network #meta-harness #query-routing #agentic-systems
