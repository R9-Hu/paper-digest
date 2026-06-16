---
title: "OpenClaw-Skill: Collective Skill Tree Search for Agentic Large Language Models"
authors: ["Tianyi Lin", "Chuanyu Sun", "Jingyi Zhang", "Changxu Wei", "Huanjin Yao", "Shunyu Liu", "Xikun Zhang", "Liu Liu", "Jiaxing Huang"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T14:20:50+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16774"
url: "http://arxiv.org/abs/2606.16774v1"
pdf: "paper/agentic-ai/[Arxiv 2026] OpenClaw-Skill Collective Skill Tree Search for Agentic Large Language Models.pdf"
---

# OpenClaw-Skill: Collective Skill Tree Search for Agentic Large Language Models

*🕒 **Published (v1):** 2026-06-15 14:20 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16774v1)*

## TL;DR
OpenClaw-Skill introduces Collective Skill Tree Search (CSTS), a framework that automatically constructs structured, diverse, and transferable skill trees for LLM agents by leveraging collective intelligence from multiple models. Combined with Collective Skill Reinforcement Learning (CSRL), it trains agents to select and exploit compositional skill paths for long-horizon agentic tasks. The resulting OpenClaw-Skill models consistently outperform their Qwen3/3.5 base models on real-world agent benchmarks.

## Problem
Existing automatic skill construction methods for LLM agents suffer from three compounding failures: (1) **skill fragmentation** — skills capture only local, unstructured procedures without orchestrating multi-step dependencies; (2) **limited diversity** — skills distilled from a single model's trajectories inherit that model's biases; (3) **poor transferability** — skills trained on one backbone LLM degrade significantly when applied to another backbone.

## Method
CSTS operates in two iterative phases over a decomposed task `T → (t₁, …, tₘ)`:

1. **Collective Skill Node Generation (CSN-Gen):** N heterogeneous models each attempt subtask `tₘ`, producing execution trajectories. A shared skill synthesizer `Φ_skill` condenses each trajectory into a candidate skill node `sₘ,ₙ`, yielding a diverse candidate set `Sₘ`.

2. **Collective Skill Node Assessment (CSN-Assess):** Each candidate is scored on two axes:
   - *Collective quality score* `Qₘ,ₙ`: average of J independent judge-model ratings (clarity, executability, completeness, relevance).
   - *Collective transferability score* `Tranₘ,ₙ`: average verification score when the skill synthesized from model Mₙ is applied to the *other* N−1 models. The final score `Score(sₘ,ₙ) = Qₘ,ₙ + Tranₘ,ₙ` selects the best node per subtask.

The selected nodes form a compositional **skill path** `S*_T = (s*₁, …, s*ₘ)`. These are used to build skill-augmented SFT data, followed by **Collective Skill RL (CSRL)**: for each subtask, G rollouts are sampled conditioned on each candidate skill; advantages are normalized *across the entire cross-skill group* (not per-skill), and a GRPO-style clipped objective updates the policy to favor higher-reward skill-conditioned strategies.

## Key Contributions
- **CSTS framework**: tree-search-based automatic skill construction using multi-model collective intelligence; addresses fragmentation via structured skill paths, diversity via multi-model generation, and transferability via explicit cross-model scoring.
- **Collective Skill RL (CSRL)**: extends GRPO to cross-skill rollout groups, enabling the policy to discriminate among skill-conditioned strategies rather than optimizing within a single skill.
- **OpenClaw-Skill model series**: trained on CSTS-generated SFT data and CSRL, evaluated on 4 Qwen3/3.5 backbones (4B–9B).
- **Skill-augmented training dataset**: 2K high-quality SFT examples built from collective skill paths and selected rollout trajectories.

## Results
**QwenClawBench (overall score):**
- OpenClaw-Skill 4B (Qwen3.5-4B base): 41.2 vs. 31.5 baseline (+9.7 pts)
- OpenClaw-Skill 9B (Qwen3.5-9B base): 44.9 vs. 34.5 baseline (+10.4 pts)
- Qwen3-4B: 12.8 vs. 7.0 (+5.8 pts); Qwen3-8B: 15.8 vs. 11.5 (+4.3 pts)
- Category-level highlights: SVM 33.2→70.9, CS 30.2→78.4 (9B); RIR 24.4→54.1 (4B)

**PinchBench (123-task expanded):**
- OpenClaw-Skill 9B: best 68.2 vs. 61.1, avg 53.6 vs. 47.1
- OpenClaw-Skill 4B: best 61.4 vs. 60.9, avg 47.6 vs. 45.9
- Qwen3-4B avg: 20.8 vs. 13.6; Qwen3-8B avg: 22.5 vs. 18.3

**Ablation (Qwen3.5-9B on QwenClawBench):**
- Base: 34.5 → +CSN-Gen: 39.8 → +CSN-Assess: 42.8 → +CSRL: 44.9

## Limitations
- Evaluated exclusively on OpenClaw-style real-world agent benchmarks; generalization to other agentic environments (web, OS, robotics) is not demonstrated.
- Skill construction requires running multiple heterogeneous models in parallel for both generation and transferability assessment, imposing substantial compute overhead at training time.
- Only 2K SFT examples are generated; the scalability and saturation behavior of CSTS under larger data budgets are not studied.
- Transferability scoring measures cross-backbone generalization at training time but does not guarantee robustness to models outside the training collective.
- The 4B models show much smaller gains on the 123-task PinchBench (best: +0.5 pts), suggesting limits at smaller scale.

## Relevance to Agentic AI / LLM Agents
CSTS directly tackles the skill-construction bottleneck that constrains LLM agent scalability in long-horizon, tool-use-heavy environments — a problem that has emerged as central to agentic AI as deployments move beyond toy sandboxes to persistent real-world systems like OpenClaw. The use of collective intelligence for both skill generation and transferability scoring addresses a key alignment mismatch where skills work for their source model but fail elsewhere, which is practically critical for model-agnostic skill reuse. CSRL's cross-skill advantage normalization is a technically interesting extension of GRPO that could generalize to other settings where multiple strategy candidates exist. This work fits squarely in the rapidly growing line on automatic skill acquisition alongside SkillRL, Trace2Skill, and CoEvoSkills, and the tree-structured compositional skill representation is a meaningful architectural advance over flat skill banks.

## Tags
#skill-learning #tool-use #reinforcement-learning #collective-intelligence #long-horizon-planning #grpo #agentic-benchmark #skill-transfer
