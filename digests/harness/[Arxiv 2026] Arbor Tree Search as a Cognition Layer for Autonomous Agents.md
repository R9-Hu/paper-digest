---
title: "Arbor: Tree Search as a Cognition Layer for Autonomous Agents"
authors: ["Neha Prakriya", "Chaojun Hou", "Zheng Gong", "Huasha Zhao", "Xi Zhao", "Mou Li", "Zhenyu Gu", "Emad Barsoum"]
source: "Arxiv"
venue: ""
published: "2026-06-10"
published_time: "2026-06-10T18:14:56+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12563"
url: "http://arxiv.org/abs/2606.12563v1"
pdf: "paper/harness/[Arxiv 2026] Arbor Tree Search as a Cognition Layer for Autonomous Agents.pdf"
---

# Arbor: Tree Search as a Cognition Layer for Autonomous Agents

*🕒 **Published (v1):** 2026-06-10 18:14 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.12563v1)*

## TL;DR
Arbor is a multi-agent framework that reformulates full-stack LLM inference optimization as heuristic-scored stateful tree search, using an Orchestrator–Critic checks-and-balances architecture with dynamically-constructed Domain Specialists. A shared search tree serves as working memory across agents, propagating failures as constraints and expanding dynamically as bottlenecks shift. On six production models on AMD MI355X GPUs, Arbor achieves +40%–+193% throughput over vendor-optimized baselines in multi-day autonomous campaigns.

## Problem
Existing autonomous optimization agents (AlphaEvolve, AVO, KernelSkill, Astra) operate on isolated, stateless targets within a single stack layer. Cross-layer performance optimization—where a kernel change can expose a framework bug that regresses serving throughput—requires navigating a stateful, dynamically expanding action space where failures at one layer invalidate progress at another, and no prior system tolerates or extracts signal from cascading cross-layer failures.

## Method
Arbor formulates optimization as heuristic tree search over T = (V, E). Each node encodes an action and its outcome (kept/reverted/crashed); the path root→node is the cumulative intervention sequence. The search state S_t tracks the tree, a scored candidate queue, outcome history with diagnostic annotations, and current agent assignments.

**Scoring heuristic:**
```
h(a) = [g(a)/c(a)] · (1 − r_acc) · (1 − r_crash) · m_gap + C√(ln N / (1 + n_cat))
```
where g(a) is expected gain (profiled GPU time share × category speedup prior), c(a) is wall-clock cost, r_acc/r_crash are empirical failure rates updated online, m_gap is an urgency multiplier [1.0–2.0], and the UCB-style term encourages exploration of under-sampled categories. All terms update after every action.

The **Orchestrator** drives depth-first search: profile → score → dispatch → gate (accuracy + e2e benchmark) → update tree → re-score. It does not implement optimizations; it constructs Domain Specialist agents dynamically per task by composing prompts from hardware context, Knowledge Base entries, and prior failure history. Multiple specialists run in parallel with GPU-aware scheduling.

The **Critic** operates over the full trajectory with four sub-capabilities: guardrails (measurement integrity), root-cause analysis (crash/regression diagnosis enabling constrained retries), introspection (evaluating whether a reverted idea warrants a refined sub-action), and stability monitoring (long-horizon health tracking, publishing constraints that prune branches).

A **persistent Knowledge Base** accumulates validated techniques, failure modes, and parameter-level findings across campaigns. KB entries initialize scoring priors (r_acc, r_crash, g(a)) and are directly composed into specialist prompts, enabling warm-start transfer.

## Key Contributions
- Formulation of cross-layer performance optimization as stateful tree search with dynamic expansion: profiling after kept actions reveals new bottlenecks, spawning branches that did not exist at initialization.
- Checks-and-balances multi-agent architecture: Orchestrator pursues aggressive gains; Critic enforces stability constraints; neither can act unilaterally.
- Hard/soft skill decomposition: hard skills = domain expertise; soft skills = coordination protocols (resource arbitration, expertise-boundary delegation, cross-agent finding integration).
- Persistent KB that makes each campaign start from strictly stronger priors than the last, with KB entries composed directly into dynamically-constructed specialist prompts.
- Demonstrated hardware-agnostic reproducibility: cross-generation validation on MI300X, run-to-run variance ≤2 percentage points.

## Results
- **gpt-oss-120b** (MoE 120B, MXFP4, MI355X): +48% throughput (4405 → 6515 tok/s/GPU); 9/30 actions kept, 16 reverted with diagnostic insight, 3 crash with recovery.
- **DeepSeek-R1-0528** (FP8, MI355X): +90% throughput; compound of MTP speculative decoding, CK GEMM rewrites, fused allreduce, config tuning.
- **MiniMax-M2.5** (FP8, MI355X): +50%.
- **GLM-5-FP8** (MI355X): +193% via cross-layer interaction (TP=8→TP=4 + NSA attention kernel + MoE dispatch co-optimization).
- **Qwen3.5-397B-A17B** (FP8, MI355X): +40%.
- **Kimi-K2.5** (MXFP4, MI355X): +60%.
- Cross-generation on MI300X: +62–99% across models (Appendix B).
- **Ablation on gpt-oss-120b**: single agent (no tree search) → +33%, crashes irrecoverably at hour 4; no Domain Specialists → +30%, exhausts at hour 6; no Critic → +12.9%/+16.5% valid, with catastrophic correctness failure (GSM8K accuracy → 0%) or benchmark inflation.
- 39% of kernel-level improvements regress end-to-end throughput when deployed into the serving pipeline, motivating the gating requirement.
- Baselines: InferenceX vendor-optimized configurations (SemiAnalysis 2026) representing extensive manual engineering team effort.

## Limitations
- Agent quality is tied to the underlying LLM backend capability tier; no systematic comparison across model families performed.
- All primary experiments on AMD Instinct GPUs (MI355X, MI300X); not yet evaluated on NVIDIA GPUs.
- Scoring constants (prior multipliers, m_gap, exploration coefficient C) chosen from early development experience, not systematically tuned; no formal sensitivity analysis.
- Evaluation domain restricted to LLM inference serving; extensions to training or single-operator optimization are not demonstrated.
- KB maturity is a prerequisite for learned value-model extensions; the system is not yet at the scale where a learned prior can replace the hand-crafted scoring heuristic.

## Relevance to Harnesses / Meta-Harnesses
Arbor is a canonical example of a **meta-harness**: rather than writing an optimizer for a specific target, it constructs a general orchestration layer that dynamically assembles specialist sub-agents at runtime and routes work through a structured search process—precisely the "harness over harnesses" pattern. The tree as shared working memory, with failures propagating upward as branch constraints and successes triggering re-profiling that expands the frontier, is a concrete instantiation of stateful meta-level control that goes beyond simple agent-loop wrappers. The Orchestrator–Critic checks-and-balances design addresses a key open problem in harness research: preventing individual agents from corrupting shared state (measurement integrity, accuracy gating) while sustaining long-horizon campaigns. The persistent Knowledge Base enabling warm-start transfer across campaigns is directly applicable to any meta-harness that must generalize across tasks or environments.

## Tags
#multi-agent #tree-search #meta-harness #orchestration #llm-inference-optimization #persistent-knowledge-base #agentic-systems #checks-and-balances
