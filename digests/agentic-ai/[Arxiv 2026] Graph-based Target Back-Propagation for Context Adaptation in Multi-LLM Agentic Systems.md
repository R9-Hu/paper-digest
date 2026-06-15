---
title: "Graph-based Target Back-Propagation for Context Adaptation in Multi-LLM Agentic Systems"
authors: ["Tan Zhu", "Tong Yao", "Kananart Kuwaranancharoen", "Amit Singh", "Yushang Lai", "Deepa Mohan", "Shankara Bhargava"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14155"
url: "http://arxiv.org/abs/2606.14155v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Graph-based Target Back-Propagation for Context Adaptation in Multi-LLM Agentic Systems.pdf"
---

# Graph-based Target Back-Propagation for Context Adaptation in Multi-LLM Agentic Systems

## TL;DR
GTBP adapts the Difference Target Propagation idea from neural networks to multi-LLM agentic workflows modeled as DAGs: it propagates local target outputs backward through the graph so each module receives a localized credit signal rather than relying on global trajectory reflection. Prompt updates are performed stage-wise with frozen model weights, eliminating gradient access requirements. Theoretical stability guarantees and empirical gains over GEPA/zero-shot/few-shot baselines are provided across three benchmarks.

## Problem
Existing context-adaptation methods for multi-LLM agentic systems (e.g., GEPA, TextGrad) suffer from **attribution ambiguity**: credit for final-output errors is assigned implicitly through whole-trajectory LLM reflection, making it non-deterministic which module's prompt should change and in what direction. These methods also lack convergence guarantees for their prompt-update dynamics.

## Method
GTBP models the agentic workflow as a directed acyclic graph G = (V, E) where each node is a frozen LLM sub-module with a tunable prompt. After a forward pass caches all node inputs/outputs, GTBP runs a backward pass in reverse topological order: for each downstream node v with inferred target Ôv, an LLM is prompted (via template Pback) to infer a target input Iˆv that would have caused v to produce Ôv — effectively approximating the intractable inverse of Mv. This yields a local target Ôu for each predecessor u. Each module then receives a module-level update set {(Iv, Ov, Ôv)} and an LLM optimizer (template Poptimize) revises the prompt's structured claim list using target–output discrepancies. Prompt complexity is controlled by a stage-wise schedule: an initial edit budget m0, a claim-addition interval m+ (add one claim every m+ iterations), and an edit-budget decay interval m− (reduce editable claims over time). Theoretical analysis uses an implicit-weight theorem to show the induced weight perturbation is O(t⁻¹), bounding the local objective change and establishing stability; a sufficiently capable LLM optimizer produces an overall loss gap of O(t⁻¹).

## Key Contributions
- **GTBP framework**: graph-structured, backward target-propagation for credit assignment in multi-LLM agentic workflows, with no gradient access required.
- **Explicit credit pipeline**: local targets are inferred deterministically by graph traversal, avoiding the attribution ambiguity of global-reflection methods.
- **Convergence theory**: stage-wise prompt updates are shown to become stable (|ΔFv| = O(t⁻¹)) and the overall task loss gap is O(t⁻¹) under stated assumptions.
- **Stage-wise scheduling**: structured budget control (m0, m+, m−) over prompt-claim edits enables monotonically growing but increasingly stable prompts.
- **Empirical validation**: consistent outperformance of GEPA on three heterogeneous benchmarks at comparable or lower training cost.

## Results
- **HotpotQA F1**: GTBP 0.800 vs. GEPA 0.7697 (+4.0%), zero-shot 0.7535, few-shot 0.7659.
- **LiveBench-Math accuracy**: GTBP 0.669 vs. GEPA 0.641 (+4.4%), zero-shot 0.611, few-shot 0.556.
- **SubPOP Wasserstein distance (↓)**: GTBP 0.1072 vs. GEPA 0.1160 (−7.8%), zero-shot 0.1261, few-shot 0.1212.
- **Training efficiency**: On LiveBench-Math, GTBP uses 1,807 LLM calls vs. GEPA's 1,594 — comparable; on SubPOP GTBP uses 1,730 calls vs. GEPA's 12,700 (7.3× fewer).
- **Convergence curve (SubPOP)**: WD decreases and rank-match accuracy increases rapidly in early iterations, stabilizing as prompt update ratio shrinks, consistent with O(t⁻¹) bound.

## Limitations
- Theoretical analysis requires strong assumptions: bounded prompt edits, single-token setting, single-block LLM approximation, and a "sufficiently capable" LLM optimizer; extension to weaker assumptions is open.
- Evaluated only on a **one-hidden-layer** workflow (≤4 intermediate modules + output node); scalability to deeper graphs, dynamic routing, and tool-calling nodes is untested.
- **Prompt length grows monotonically** over training (Figure 4c); no pruning or budget-aware compression is performed, increasing per-call inference cost.
- Multi-target ambiguity (a node branching to multiple successors) is explicitly sidestepped by the one-hidden-layer constraint; the general DAG case is unresolved.
- GTBP underperforms fine-tuned open-weight models (e.g., Llama-3-70B on SubPOP) — it targets the frozen-weight regime, not fine-tuning.

## Relevance to Agentic AI / LLM Agents
GTBP directly addresses one of the most fundamental open problems in compound LLM systems: how to assign credit and optimize individual module behavior without touching model weights or requiring differentiable execution. It provides the first theoretically grounded alternative to heuristic textual backpropagation (TextGrad, Agentic Neural Networks) and whole-trajectory reflection (GEPA, ACE) for prompt optimization in multi-agent DAG workflows. The work is immediately relevant to practitioners building DSPy-style multi-module pipelines, and the stage-wise scheduling mechanism offers a practical template for automatic prompt engineering at production scale. The convergence analysis is also a rare theoretical foothold in a field where most prompt-optimization methods lack any formal guarantees.

## Tags
#prompt-optimization #multi-agent #credit-assignment #context-adaptation #agentic-workflow #automatic-prompt-engineering #dag #convergence-theory
