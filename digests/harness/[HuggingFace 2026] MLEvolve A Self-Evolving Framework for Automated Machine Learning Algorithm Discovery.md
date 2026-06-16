---
title: "MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery"
authors: ["Shangheng Du", "Xiangchao Yan", "Jinxin Shi", "Zongsheng Cao", "Shiyang Feng", "Zichen Liang", "Boyuan Sun", "Tianshuo Peng", "Yifan Zhou", "Xin Li", "Jie Zhou", "Liang He", "Bo Zhang", "Lei Bai"]
source: "HuggingFace"
venue: ""
published: "2026-06-04"
published_time: "2026-06-04T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.06473"
url: "https://huggingface.co/papers/2606.06473"
pdf: "paper/harness/[HuggingFace 2026] MLEvolve A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery.pdf"
---

# MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery

*🕒 **Published (v1):** 2026-06-04 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.06473)*

## TL;DR
MLEvolve is a self-evolving multi-agent LLM framework for automated ML algorithm discovery that replaces tree-based MCTS with a graph-structured search (Progressive MCGS), adds retrospective memory for experience accumulation, and decouples planning from code generation. It achieves 65.3% average medal rate on MLE-Bench (75 Kaggle tasks) under a 12-hour budget—state-of-the-art among all compared MLE agents—and generalizes to mathematical optimization, outperforming AlphaEvolve on 11/15 tasks.

## Problem
Existing LLM-based MLE agents suffer three compounding failures during long-horizon optimization: (1) inter-branch information isolation in tree-based search prevents transfer of successful strategies across trajectories; (2) memoryless search propagates only scalar rewards, discarding rich experiential context from prior iterations; (3) one-shot planner-coder coupling makes iterative refinement unstable and leads to full rewrites at every step.

## Method
MLEvolve integrates three components into a unified multi-agent loop:

**Progressive Monte Carlo Graph Search (MCGS):** Extends MCTS by organizing candidate solutions as a directed graph G=(V, E_T ∪ E_ref), where primary edges E_T preserve the parent-child tree backbone for selection/backpropagation, and reference edges E_ref encode cross-branch information flow without affecting credit assignment. Four expansion operators are defined: primary expansion (no reference), intra-branch evolution (local k-node trajectory), cross-branch reference (top-N nodes across stagnated branches), and multi-branch aggregation (new root drafted from multi-branch trajectory fusion). Selection uses a progressive soft-switch: UCT with time-decaying exploration constant c(t) is mixed with Elite-Guided exploitation (inverse-rank-weighted sampling from global top-K nodes), controlled by a schedule w(t)→w_min that empirically reduces branch-selection entropy from ~4.8 to ~2.8 effective active branches. Stagnation triggers (branch-level: τ_branch consecutive non-improving expansions; global-level: τ_global steps without global-best improvement) activate graph-based operators.

**Retrospective Memory:** A static domain knowledge base (task-type-indexed model + usage guidelines, used for cold-start initialization) combined with a dynamic global memory storing (plan, code, metric, analysis, feedback) records per executed node. Retrieval uses BM25 ⊕ FAISS vector search fused via Reciprocal Rank Fusion (RRF). Stage-aware queries: planning stage retrieves on the free-text plan; debugging stage queries on the error message.

**Hierarchical Planning with Adaptive Code Generation:** A Planner agent generates a module-level structured specification (what/why); a Coder agent selects among Base (full rewrite), Stepwise (module-by-module), or Diff (targeted patch edit) modes based on current search state.

Backbone LLM: Gemini-3.1-Pro-preview (temperature 1.0). Budget: 500 expansion steps, 12 hours, 21 vCPUs, 234 GB RAM, 1× H200.

## Key Contributions
- **Progressive MCGS**: graph-based extension of MCTS with reference edges enabling cross-branch information flow; entropy-inspired progressive exploration-to-exploitation scheduling.
- **Retrospective Memory**: hybrid BM25+FAISS retrieval with RRF fusion over accumulated search records; cold-start domain knowledge base; no additional LLM calls required for reflection.
- **Hierarchical Planner-Coder decoupling** with three adaptive code generation modes (Base/Stepwise/Diff).
- State-of-the-art on MLE-Bench full set (65.3% medal rate, 34.7% gold, 100% valid submission) at half the standard 24-hour budget.
- Cross-domain generalization: best result on 11/15 AlphaEvolve mathematical optimization tasks.

## Results
- **MLE-Bench (75 tasks, 12 h budget):**
  - Average medal rate: **65.3%** (vs. best prior proprietary MARS+: 62.7%, AIBuildAI: 63.1%, both at 24 h)
  - Gold medal rate: **34.7%** (vs. MARS+ 33.8%, AIBuildAI 25.8%)
  - Valid submission rate: **100%**
  - Above-median rate: **76.0%**
  - By complexity: Low 80.3%, Medium 64.0%, High 46.7%
- **MLE-Bench Lite ablation (22 tasks):**
  - Full MLEvolve: 81.82% medal, 54.55% gold, 88.39% beat ratio
  - w/o Progressive MCGS: 68.18% medal (largest single-component drop)
  - w/o Retrospective Memory: 68.18% medal (−13.64 pp)
  - w/o Adaptive Code Generation: 72.73% medal
- **AlphaEvolve math tasks (15 tasks):** Best on 11/15 vs. AlphaEvolve, AlphaEvolve-v2, SimpleTES, TTT-Discover, OpenEvolve.
- **Beat ratio over time:** MLEvolve reaches 98.2% vs. Vanilla MCTS plateau at ~70.7% on representative tasks.
- **Entropy dynamics:** Effective active branch count decays from 4.8 → 2.8 (MLEvolve) vs. static ~4.3 (Vanilla MCTS).

## Limitations
- Evaluated on a single backbone (Gemini-3.1-Pro-preview) for the main results; multi-LLM comparison is partial (image/NLP/audio subset only, no full-leaderboard numbers for other backbones).
- Requires substantial compute per task (21 vCPUs, 234 GB RAM, H200 GPU, 12 h); not feasible for resource-constrained settings.
- Domain knowledge base is manually curated and task-type-specific; coverage and quality depend on curation effort.
- Stagnation thresholds (τ_branch, τ_global) and schedule hyperparameters (c₀, c_min, w_min) require tuning; sensitivity not systematically reported beyond ablations.
- Generalization tested only on mathematical optimization as a second domain; broader AI-for-Science applicability is asserted but not yet demonstrated.

## Relevance to Harnesses / Meta-Harnesses
MLEvolve is itself a meta-harness: it orchestrates multiple specialized LLM agents (planner, coder, reviewer, debugger) through a structured iterative loop that governs when to call each agent, which context to inject (retrieved memory records, cross-branch references), and how to select code generation granularity—all decisions made programmatically by the framework rather than by any single model. The Progressive MCGS + Retrospective Memory design pattern—where the harness maintains persistent structured state across agent calls and uses that state to route future calls—is directly analogous to the orchestration layer concerns of multi-agent meta-harnesses tracking research pipelines. The finding that intra-branch evolution (trajectory-aware context injection) dominates the ablation gains (13.64 pp from memory alone) concretely quantifies the value of stateful context management in iterative agent harnesses, a key design axis for anyone building self-improving agentic pipelines.

## Tags
#agentic-ai #meta-harness #multi-agent #mcts #automated-ml #self-evolving #long-horizon #search-algorithm
