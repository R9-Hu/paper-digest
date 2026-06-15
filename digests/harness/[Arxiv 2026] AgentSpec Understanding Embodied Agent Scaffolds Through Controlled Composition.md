---
title: "AgentSpec: Understanding Embodied Agent Scaffolds Through Controlled Composition"
authors: ["Jixuan Chen", "Jianzhi Shen", "Haoqiang Kang", "Zhi Hong", "Qingyi Jiang", "Soham Bose", "Yiming Zhang", "Leon Leng", "Amit Vyas", "Lingjun Mao", "Siru Ouyang", "Kun Zhou", "Lianhui Qin"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.14674"
url: "http://arxiv.org/abs/2606.14674v1"
pdf: "paper/harness/[Arxiv 2026] AgentSpec Understanding Embodied Agent Scaffolds Through Controlled Composition.pdf"
---

# AgentSpec: Understanding Embodied Agent Scaffolds Through Controlled Composition

## TL;DR
AgentSpec is a modular specification framework that decomposes embodied LLM agents into a typed Perception–Memory–Reasoning–Reflection–Action loop with standardized interfaces, enabling controlled swapping and ablation of components. Experiments across DeliveryBench, ALFRED, MiniGrid, and RoboTHOR demonstrate that scaffold compatibility and module interaction effects govern performance more than individual module strength or model scale.

## Problem
Existing embodied agent systems (Voyager, AgentGym, CoALA, AgentSquare) are tightly coupled pipelines where reasoning, memory, perception, and action are entangled with task-specific prompts and environment interfaces. This coupling makes it impossible to isolate component contributions, compare design alternatives, or understand how module interactions—constructive or destructive—shape agent behavior. The field lacks a principled, controlled platform for answering basic scaffold design questions.

## Method
AgentSpec wraps any Gym-compatible environment in a modular agent core that enforces typed intermediate objects at every interface boundary: Perception converts raw observations to a unified state `u_t`; Memory retrieves/updates episodic and semantic context `m_t`; Reasoning proposes a decision `r_t = R(u_t, m_t)`; Reflection critiques and refines it to `r̂_t`; Action grounds it to an executable `a_t`. Because every module receives and emits a fixed typed object, any single module can be swapped without rewriting the rest of the pipeline. Reasoning variants include CoT, ReAct, Plan-and-Solve, MAD, ToT; memory variants include flat buffers, DynamicCheatsheet, MemoryBank, OpenClaw, Zep, Mem0; reflection variants include Self-Refine, Reflexion, Retroformer. An optional RL module (GRPO, SUPO) can fine-tune the policy with or without scaffold-aligned training context.

## Key Contributions
- A typed, Gym-compatible modular specification (Perception–Memory–Reasoning–Reflection–Action + optional RL) with fixed interface contracts enabling controlled component ablation.
- Instantiation and systematic evaluation across four complementary embodied benchmarks (DeliveryBench, ALFRED, MiniGrid, RoboTHOR) and multiple open/closed-source backbones.
- Empirical identification of reusable design principles: memory helps only when its representation matches the downstream reasoner; multi-granularity memory is the robust default for long-horizon tasks; reflection is most valuable as a local error-repair layer; RL-trained policies must be co-optimized with their deployment-time scaffold structure (SUPO > GRPO for scaffold compatibility).
- Pareto analysis of performance vs. token cost showing that well-matched lightweight compositions beat heavier mismatched ones.

## Results
- DeliveryBench (GPT-5 mini): ReAct+MemoryBank reaches 30.67 hourly profit vs. ReAct+Base at 8.54; Plan-and-Solve+MemoryBank reaches 26.78 vs. Plan-and-Solve+Base at 6.18.
- DeliveryBench RL ablation: Base non-RL scores −3.07; GRPO raises it to 5.80; SUPO to 5.48. However, SUPO+DynamicCheatsheet achieves 8.27 vs. GRPO+DynamicCheatsheet at 5.02, showing SUPO composes better with structured memory.
- MAD (multi-agent debate) reasoning tolerates weaker memory more robustly than single-pass strategies, maintaining competitive performance even with low-level memory.
- Cross-benchmark: reasoning-centric configs dominate in short/symbolic MiniGrid; memory gains are more critical in ALFRED and DeliveryBench; RoboTHOR shows additional perception/navigation bottlenecks not resolved by reasoning or memory alone.
- Smaller models (Qwen-9B, Qwen-27B) with well-matched scaffolds approach closed-source model performance, demonstrating scaffold compensation for weaker base policies.

## Limitations
- All four benchmarks are embodied/navigation/delivery tasks; generalization to tool-use, web-agent, or code-agent scaffolds is untested.
- Module search space is fixed by human curation; no automated search over the full combinatorial space is performed.
- SUPO's improved scaffold compatibility is a partial solution; full joint optimization of policy and scaffold modules during RL training is left as future work.
- Pareto analysis covers token count and thinking time but not wall-clock latency under real deployment conditions or multi-GPU serving overhead.
- RoboTHOR results remain low overall, suggesting perception/visual grounding bottlenecks outside the framework's current scope.

## Relevance to Harnesses / Meta-Harnesses
AgentSpec is directly a meta-harness contribution: it operationalizes the idea that an agent scaffold is itself a composable, analyzable system rather than a fixed pipeline, and provides a controlled substrate for comparing harness design choices. Its typed interface contracts—analogous to the standardized I/O contracts in software meta-harnesses—formalize what it means to "plug in" a module, making the scaffold a first-class engineering artifact rather than glue code. The finding that post-hoc module attachment (adding memory/reflection to a bare RL policy) causes distribution shift unless co-optimized is a direct design principle for harness builders: scaffold structure must be incorporated at training time, not only inference time. For researchers tracking meta-harness methodology, AgentSpec demonstrates how controlled compositional ablation can surface interaction effects that are invisible when evaluating complete end-to-end systems.

## Tags
#agent-scaffold #meta-harness #modular-agents #embodied-ai #ablation-framework #memory-reasoning-interaction #reinforcement-learning #composition
