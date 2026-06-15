---
title: "HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry"
authors: ["Tingyang Chen", "Shuo Lu", "Kang Zhao", "Weicheng Meng", "Hanlin Teng", "Tianhao Li", "Chao Li", "Xule Liu", "Jian Liang", "Zhizhong Zhang", "Yuan Xie", "Heng Qu", "Kun Shao", "Jian Luan"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14249"
url: "http://arxiv.org/abs/2606.14249v1"
pdf: "paper/agentic-ai/[Arxiv 2026] HarnessX A Composable, Adaptive, and Evolvable Agent Harness Foundry.pdf"
---

# HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry

## TL;DR
HarnessX is a foundry that treats the agent runtime harness (prompts, tools, memory, control flow) as a first-class typed object that can be automatically composed, adapted, and co-evolved with the model. Its AEGIS engine formalizes harness adaptation as an MDP over symbolic artifacts, running a four-stage trace-driven pipeline (Digester → Planner → Evolver → Critic) with deterministic acceptance gates. Across five benchmarks and three model families, it delivers an average +14.5% absolute gain (up to +44.0%) without any model weight updates in the harness-only setting.

## Problem
Agent harnesses are hand-crafted, static, and architecturally entangled: any model or task change requires bespoke modification, components are conflated in single codepaths preventing principled reuse, and the rich execution traces produced during operation are discarded rather than cycled back into improvement. Neither harness design nor model training benefits from the other's progress.

## Method
**Harness Composition.** The harness is formalized as `H = (M, C)`, where `C = (P, S)` decomposes into a hook-indexed processor list `P : Hook → List[Processor]` and shared slot resources `S`. Processors implement `async process(event) -> AsyncIterator[Event]` and attach to one of eight typed lifecycle hooks (`task_start`, `before_model`, `after_model`, `before_tool`, etc.). A nine-dimensional taxonomy (model selection, context assembly, memory management, tool ecosystem, execution environment, evaluation/reward, control/safety, observability, training bridge) covers the full behavioral space; a substitution algebra enables type-safe per-task insertion and removal of processors via `_singleton_group` mutual exclusion and `_order` hints.

**AEGIS (Harness Adaptation).** Harness evolution is framed as an MDP: configurations are states, typed code-level edits are actions, and execution traces plus verifier scores are feedback. This *operational mirror* maps three known RL pathologies—reward hacking, catastrophic forgetting, under-exploration—to concrete design risks addressed by four dedicated stages:
- *Digester*: compresses raw traces (~10M tokens/iteration on GAIA) into structured per-task summaries with failure categories and cross-iteration history.
- *Planner*: constructs a full adaptation landscape covering both incremental and structural changes, guarding against convergence to local edits.
- *Evolver*: generates candidate harnesses as typed builder operations with change manifests and smoke tests.
- *Critic + Deterministic Gate*: the Critic checks manifest consistency and reward-hacking risk; the deterministic gate enforces build validity and a *seesaw constraint* (no regression on previously passing tasks). LLMs explore and propose; deterministic checks govern what ships.

**Variant Isolation.** On heterogeneous task sets, a single harness stagnates due to conflicting behavioral requirements. Up to K variants are maintained; each task is routed to its highest-performing variant. Seesaw constraints are scoped per-variant, allowing an edit that improves one cluster to fork a new variant rather than be rejected.

**Harness-Model Co-Evolution.** A shared replay buffer accumulates reward-annotated trajectories across harness versions. Cross-harness GRPO computes group-relative advantages per task across harness versions, enabling off-policy model training at no additional rollout cost. Both AEGIS (non-parametric) and GRPO (parametric) operate over the same buffer each iteration.

## Key Contributions
- Formalization of the harness as a serializable, composable, typed first-class object with a nine-dimensional behavioral taxonomy and substitution algebra
- AEGIS: a multi-agent, trace-driven harness evolution engine grounded in an *operational mirror* between RL and symbolic adaptation, with principled defenses against all three canonical RL pathologies
- Variant isolation via ensemble routing, enabling stable multi-task evolution without cross-task interference
- Harness-model co-evolution via cross-harness GRPO over a shared replay buffer, breaking both the scaffolding ceiling and the training-signal ceiling
- Empirical validation across five benchmarks (ALFWorld, GAIA, WebShop, τ³-Bench, SWE-bench Verified) and three model families (Claude Sonnet 4.6, GPT-5.4, Qwen3.5-9B)

## Results
- Average absolute gain of **+14.5%** across 15 model–benchmark configurations (14/15 improving)
- Up to **+44.0%** on ALFWorld with Qwen3.5-9B (weakest model, weakest baseline)
- Minimum gain among improving configs: **+1.1%** on τ³-Bench (near-ceiling baseline)
- Inverse-scaling pattern: weakest model benefits most (Qwen3.5-9B +44.0% vs. Sonnet 4.6 +11.2% on ALFWorld)
- Variant isolation on GAIA: **+13.6%** gain, non-degrading over 15 rounds (vs. stagnation without it)
- Co-evolution yields additional **+4.7%** over harness-only evolution
- Up to 15 evolution rounds evaluated per configuration

## Limitations
- Codebase not yet open-sourced at submission time (deferred to future release)
- Single-harness evolution stagnates on heterogeneous task sets without variant isolation; variant isolation adds routing overhead and variant management complexity
- Scaffolding ceiling: harness evolution is eventually bottlenecked by fixed model reasoning capacity; co-evolution addresses this but at the cost of model training infrastructure
- AEGIS meta-agent is itself an LLM; its failure modes (hallucinated manifests, poor diagnosis) propagate into proposed edits, mitigated but not eliminated by deterministic gating
- Adaptation batch costs are substantial (~10M tokens/iteration for GAIA); cost-performance tradeoffs are acknowledged but not fully characterized
- Operational mirror analogy to RL has limits (noted in §7.3): symbolic edit spaces are open-ended and non-stationary in ways that MDP theory does not fully cover

## Relevance to Agentic AI / LLM Agents
HarnessX directly addresses the meta-level problem of agent infrastructure engineering: rather than treating scaffolding as fixed boilerplate, it makes the harness itself a learnable, evolvable artifact—a shift with broad implications for any system that deploys LLM agents at scale. The operational mirror is theoretically significant because it converts the informal folk wisdom of harness tuning into a principled framework with concrete failure-mode predictions and defenses. The inverse-scaling finding—that weaker models benefit most from evolved harnesses—suggests harness optimization is a high-ROI complementary lever to model scaling, particularly relevant for deployment on smaller, cheaper models. The co-evolution result (harness and model improve in a shared loop) sets a new target for agent training pipelines, challenging the convention of treating scaffold design and model fine-tuning as separate engineering concerns.

## Tags
#harness-engineering #agent-infrastructure #self-evolving-agents #scaffold-optimization #rl-for-agents #co-evolution #multi-agent #benchmark
