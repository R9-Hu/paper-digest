---
title: "HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry"
authors: ["Tingyang Chen", "Shuo Lu", "Kang Zhao", "Weicheng Meng", "Hanlin Teng", "Tianhao Li", "Chao Li", "Xule Liu", "Jian Liang", "Zhizhong Zhang", "Yuan Xie", "Heng Qu", "Kun Shao", "Jian Luan"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T08:27:11+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.14249"
url: "http://arxiv.org/abs/2606.14249v1"
pdf: "paper/harness/[Arxiv 2026] HarnessX A Composable, Adaptive, and Evolvable Agent Harness Foundry.pdf"
---

# HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry

*🕒 **Published (v1):** 2026-06-12 08:27 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14249v1)*

## TL;DR
HarnessX formalizes the agent harness as a first-class typed object composed via a substitution algebra, then automatically evolves it through AEGIS—a trace-driven, four-stage multi-agent engine grounded in an operational mirror between symbolic harness adaptation and RL. Across five benchmarks and three model families, harness evolution yields an average absolute gain of +14.5% (up to +44.0%), with an additional +4.7% from closing the loop via harness–model co-evolution using cross-harness GRPO.

## Problem
Agent harnesses (prompts, tools, memory, control flow) remain hand-crafted and static: each new model or task requires bespoke scaffolding, harness components are architecturally entangled so changes silently break others, and trajectory data collected during execution is discarded rather than recycled into systematic improvement of either the harness or the model.

## Method
**Composition.** A harness `H = (M, C)` where `C = (P, S)`: `P` is a hook-indexed list of typed *processors* attached to eight lifecycle hooks (`task_start` through `task_end`); `S` is shared slot infrastructure (tool registry, tracer, sandbox). Processors expose a uniform `async process(event) → AsyncIterator[Event]` interface, carry singleton-group metadata preventing conflicting duplicates, and compose via sequential application at each hook. Nine orthogonal dimensions (model selection D1, context assembly D2, memory D3, tools D4, execution environment D5, evaluation D6, control/safety D7, observability D8, training bridge D9) span the full behavioral space.

**AEGIS (Adaptive Evolution via Grounded Iterative Synthesis).** Harness evolution is framed as an MDP over symbolic artifacts: configurations are states, typed builder edits are actions, and execution traces plus verifier scores are feedback (the *operational mirror*, Table 2). This mapping exposes three RL pathologies in symbolic form—reward hacking, catastrophic forgetting, under-exploration—each countered by a dedicated stage:
- *Digester*: compresses ~10M-token raw traces per iteration into structured per-task summaries with cross-iteration history.
- *Planner*: constructs an adaptation landscape spanning incremental and structural edit types to prevent local-repair bias (under-exploration defense).
- *Evolver*: generates typed builder operations with change manifests and smoke tests; each candidate must satisfy hook-type contracts and singleton-group exclusion.
- *Critic + deterministic gate*: Critic checks for reward hacking (manifest vs. trace evidence); gate enforces the *seesaw constraint* (reject any edit that regresses a previously solved task—catastrophic forgetting defense).

On heterogeneous benchmarks, *variant isolation* maintains up to K harness variants routed per task cluster; the seesaw constraint is scoped per-variant, allowing locally beneficial edits that would otherwise be rejected.

**Co-evolution.** A shared replay buffer accumulates scored traces tagged by harness version. AEGIS reads this buffer for harness edits; simultaneously, *cross-harness GRPO* partitions traces into per-task groups spanning harness versions, computes group-relative advantages, and updates model parameters off-policy—reusing cached log-probabilities so model RL costs no additional rollouts.

## Key Contributions
- **Typed harness substrate**: harness as independently serializable, hashable, substitutable first-class object; nine-dimensional processor taxonomy with substitution algebra.
- **AEGIS engine**: four-stage trace-driven evolution pipeline with operational mirror grounding RL pathologies as concrete design risks addressed by architectural defenses.
- **Variant isolation via ensemble routing**: fork-not-reject strategy for heterogeneous task sets, preventing cross-cluster interference while sustaining exploration.
- **Harness–model co-evolution**: shared replay buffer + cross-harness GRPO breaks the scaffolding ceiling (harness-only) and training-signal ceiling (model-only RL) simultaneously.

## Results
- **+14.5% average absolute gain** across 15 model–benchmark configurations (3 models × 5 benchmarks), up to **+44.0%**; 14 of 15 configurations improve.
- Inverse-scaling pattern: weakest agents benefit most (Qwen3.5-9B on ALFWorld: +44.0%; Sonnet 4.6 on ALFWorld: +11.2%).
- Near-ceiling benchmark (τ³-Bench): +1.1%.
- Variant-isolation ablation on GAIA: **+13.6%** non-degrading over 15 rounds vs. stagnation without isolation.
- Co-evolution yields **+4.7%** over harness-only evolution.
- Most frequent AEGIS edit targets: D2 (context assembly) and D4 (tool ecosystem).
- Baselines: initial hand-crafted static harnesses per model–benchmark pair.

## Limitations
- Codebase not yet released (promised in "a future release").
- Trace richness is a prerequisite: sparse signal causes early Digester short-circuit with no edit.
- Operational mirror analogy has limits (acknowledged in §7.3): the symbolic action space is open-ended and LLM-generated rather than enumerable, so RL convergence guarantees do not transfer.
- AEGIS is token-intensive: a single GAIA iteration generates ~10M tokens of raw traces before digestion.
- Scaffolding ceiling remains for capability-limited models under harness-only evolution; co-evolution mitigates but does not eliminate it.
- Evaluation covers three model families; generalization to other architectures (e.g., Gemini, Llama) not demonstrated.

## Relevance to Harnesses / Meta-Harnesses
HarnessX is the most comprehensive formalization of the meta-harness concept to date: it treats the harness as a typed, composable, first-class engineering artifact and closes the full loop from execution trace to harness edit to model training signal. The operational mirror (Table 2) provides a theoretical substrate that converts familiar RL failure modes into concrete architectural requirements, giving the field a principled vocabulary for harness evolution that prior work (Meta-Harness, SICA, Darwin Gödel Machine, AHE) lacked. The variant-isolation and co-evolution mechanisms directly address the two ceilings that bound meta-harness progress—cross-task interference and frozen-model capacity—making HarnessX the current reference architecture for anyone designing self-improving agentic infrastructure.

## Tags
#agent-harness #meta-harness #harness-evolution #aegis #composable-agents #reinforcement-learning #co-evolution #trace-driven-optimization #self-evolving-agents
