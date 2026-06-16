---
title: "VeriGraph: Towards Verifiable Data-Analytic Agents"
authors: ["Jiajie Jin", "Zhao Yang", "Wenle Liao", "Yuyang Hu", "Guanting Dong", "Xiaoxi Li", "Yutao Zhu", "Zhicheng Dou"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T11:50:56+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16603"
url: "http://arxiv.org/abs/2606.16603v1"
pdf: "paper/agentic-ai/[Arxiv 2026] VeriGraph Towards Verifiable Data-Analytic Agents.pdf"
---

# VeriGraph: Towards Verifiable Data-Analytic Agents

*🕒 **Published (v1):** 2026-06-15 11:50 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16603v1)*

## TL;DR
VeriGraph recasts LLM data-analytic agent execution as the incremental construction of a heterogeneous evidence DAG, making every numerical and qualitative conclusion traceable back to raw data through typed graph edges. An 8B model trained with graph-aware composite rewards achieves the highest Overall score across four data-intensive benchmarks while attaining 87.61% Grounding Rate — the fraction of final claims recoverable from the agent's exposed evidence artifact.

## Problem
Prevailing ReAct/CodeAct data agents produce flat linear transcripts that entangle deterministic code execution with semantic deduction; intermediate computational artifacts are transient observations, and qualitative reasoning steps are free-form text. This makes numerical conclusions non-reproducible and qualitative judgments indistinguishable from confabulation, with no mechanism to localize failures to a specific computation, grounding step, or inference.

## Method
VeriGraph maintains a heterogeneous DAG G=(V,E) where V = Vdata ∪ Vclaim and E = Ecomp ∪ Eground ∪ Ederive. At each agent step, three primitives expand the graph:

- **Computational expansion**: automatically extracts new interpreter variables and their dependencies via pre/post namespace snapshots and static AST walks, adding data→data edges without sys.settrace overhead.
- **Grounding expansion (`bind`)**: anchors an existing runtime variable to an atomic natural-language claim node, creating a data→claim edge; structurally enforced to reference only existing artifacts.
- **Derivational expansion (`infer`)**: records how a higher-level conclusion follows from a set of established claim premises with an explicit reasoning annotation, creating claim→claim edges.

Terminal extraction (`submit_answer`) designates terminal claim nodes; the ancestor subgraph G* is the compact auditable evidence chain. Traceability reduces to graph reachability: a claim is verifiable iff it has a path to raw data sources.

Training uses a two-stage curriculum: (1) cold-start SFT on ~36K distilled trajectories at both atomic (single-primitive) and full-trajectory granularity; (2) DAPO RL with a composite reward R = R_process (mean per-step execution success rate) + R_infer (per-derivation LLM verifier, ∈{−0.5, +1}) + R_outcome (rubric-based LLM judge on the terminal subgraph). No separate grounding reward is needed — `bind` validity is structurally enforced by the runtime.

## Key Contributions
- Heterogeneous evidence DAG formalism with three typed expansion primitives embedded directly in the code action space, unifying deterministic computation and semantic deduction.
- Graph-based policy optimization (DAPO variant) with a hierarchical composite reward aligned to the DAG's construction order: computational integrity → derivational validity → terminal subgraph quality.
- Grounding Rate (GR) metric: decomposes each answer into atomic claims and measures what fraction can be recovered from the evidence artifact exposed by the method.
- Empirical demonstration that evidence structure must be a primary training objective, not a post-hoc explanation; outcome-only RL degrades both accuracy and grounding.

## Results
- **VeriGraph-8B Overall: 73.68** — highest among all evaluated baselines including GPT-5.2/5.4 ReAct, Claude-4.5-Opus ReAct, and specialized agents DataMind/DeepAnalyze.
- **Grounding Rate: 87.61%**, +14.04 points over the strongest ReAct baseline (GPT-5.4 at 78.52%).
- Matches Claude-4.5-Opus ReAct (73.22 Overall) under a strictly stronger evidence contract (only entry exposing both computational and derivational provenance).
- VeriGraph-14B: 75.74 Overall, 88.67 GR; VeriGraph-4B: 68.44 Overall, 68.28 GR — 4B already surpasses vanilla Qwen3-8B ReAct.
- Ablation: removing trajectory SFT collapses Overall by 35.90 points; outcome-only RL degrades to 65.35 Overall and 76.46 GR vs. full model's 73.68/87.61.
- Prompted graph structure (Prompt-Veri @ Qwen3-32B) improves over flat CodeAct but trails trained VeriGraph, showing the policy must *learn* when to materialize evidence.

## Limitations
- DAB-Step Research Content/Format scores (3.31/3.56) substantially trail proprietary direct-inference baselines (≥4.6) because answers are serialized from the terminal subgraph rather than written as free-form prose, incurring a stylistic penalty from LLM judges — a presentation artifact also visible in all ReAct agents.
- GR measures structural recoverability, not semantic truth; a `bind` with a misleading description of an existing artifact passes structural checks and requires a downstream human auditor or judge to catch.
- 8B→14B scaling yields diminishing returns (+1.84 Overall) versus 4B→8B (+5.40), suggesting the graph interface saturates quickly for report-style tasks.
- Backbone evaluation limited to the Qwen3 family; generalization to other model families is untested.
- Verifier overhead is ~1.3× outcome-only rollout cost; scales with |I| (number of infer calls per trajectory).

## Relevance to Agentic AI / LLM Agents
VeriGraph directly addresses the trustworthiness gap that limits deployment of data-analytic agents in high-stakes settings (finance, science), showing that making evidence structure a first-class training objective simultaneously improves task accuracy and auditability — these need not trade off. The graph-based policy optimization extends GRPO/DAPO-style RL with structured process rewards, complementing broader work on reward shaping for multi-step agents and providing a concrete alternative to outcome-only RL for agents whose intermediate reasoning steps matter. The DAG interface is a reusable architectural primitive: its separation of code-space computation from semantic-space derivation applies broadly to any agent that mixes tool use with natural-language reasoning.

## Tags
#data-analytic-agents #verifiability #evidence-graph #neuro-symbolic #reinforcement-learning #process-reward #grounding #dag
