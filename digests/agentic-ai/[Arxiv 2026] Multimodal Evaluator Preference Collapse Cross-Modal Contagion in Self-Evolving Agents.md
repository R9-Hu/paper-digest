---
title: "Multimodal Evaluator Preference Collapse: Cross-Modal Contagion in Self-Evolving Agents"
authors: ["Zewen Liu"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T13:18:20+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16682"
url: "http://arxiv.org/abs/2606.16682v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Multimodal Evaluator Preference Collapse Cross-Modal Contagion in Self-Evolving Agents.pdf"
---

# Multimodal Evaluator Preference Collapse: Cross-Modal Contagion in Self-Evolving Agents

*🕒 **Published (v1):** 2026-06-15 13:18 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16682v1)*

## TL;DR
When LLM agents use a separate (cross-model) evaluator in a test-time reinforcement learning feedback loop, evaluator preference collapse is amplified 3.2× in multimodal settings compared to same-model self-evaluation. A newly identified phenomenon—cross-modal contagion—causes evaluator biases acquired on one modality (text, visual) to corrupt strategy selection on the other. Self-evaluation provides near-complete immunity (97% zero-contagion rate).

## Problem
Test-time reinforcement learning (TTRL) loops that rely on an LLM-as-judge can cause agents to converge on strategies preferred by the evaluator rather than strategies optimal for the task (Evaluator Preference Collapse, EPC). Prior work established EPC only in text-only, same-model settings. This paper asks whether EPC is worse in multimodal cross-model settings, and whether biases acquired on one modality corrupt evaluation on another—a previously uncharacterized failure mode for multimodal self-improving agents.

## Method
The authors formalize TTRL as a multiplicative-weights stochastic bandit over 11 strategies (8 text-domain, 3 visual-domain), using asymmetric weight updates (αwin=0.08, αlose=0.04) and a fixed baseline strategy (step_by_step) as the pairwise comparator. Executor: DeepSeek-chat. Evaluators tested: GPT-4o, Qwen-plus, DashScope gui-plus, DeepSeek-chat (self-eval).

**Cross-modal contagion** is measured via a four-phase isolation paradigm:
- Phase 1: Train on text only → wT
- Phase 2: Train on visual only → wV
- Phase 3: Start from wT, train on visual → wT→V
- Phase 4: Start from wV, train on text → wV→T

Contagion coefficient γA→B = ‖wA→B − wB‖₂ / ‖wB‖₂ measures deviation of the post-contagion distribution from the pure-modality baseline. The full contagion matrix Γ(J) is indexed by evaluator identity J. Collapse severity is quantified via PCI (coefficient of variation of strategy weights); multimodal PCI (MPCI) aggregates per-modality PCI and cross-modal divergence (CPCI).

## Key Contributions
- **Multimodal EPC quantified**: GPT-4o cross-model evaluation yields PCI=1.464—3.2× self-evaluation (0.461) and 2.0× a random evaluator (0.716); visual tasks collapse more than text (1.464 vs. 1.348); visual strategies receive only 9.1% combined weight.
- **Cross-modal contagion discovered**: Evaluator preferences learned on one modality transfer to and corrupt strategy selection on the other; strategy inversion observed (text-optimal synthesis ↔ visual-optimal step_by_step swap after cross-modal exposure).
- **Contagion matrix Γ(J) formalized**: Provides a modality×modality framework for quantifying evaluator-conditional preference transfer.
- **Evaluator-conditional contagion hierarchy established**: Cross-model evaluators (GPT-4o, Qwen-plus) produce strong bidirectional contagion (γ̄ ≈ 1.0–1.2); high round counts collapse the contagion channel (DashScope, 50 rounds: 70% zero rate); self-evaluation yields near-complete immunity (DeepSeek self-eval, N=30: 97% zero contagion, d=0.07).
- **MM-EPC experimental framework released** with bootstrap analysis pipeline and machine-readable results.

## Results
- GPT-4o evaluating DeepSeek-chat: PCI=1.464 (overall), PCI_text=1.348, PCI_visual=1.464; step_by_step absorbs 48.4% of weight; visual strategies (visual_grounding, spatial_decompose, aesthetic_frame) total 9.1%.
- Self-evaluation (DeepSeek): PCI=0.461; ground-truth PCI (correctness oracle) = 0.251.
- GPT-4o contagion (N=8, 30 rounds): γ̄T→V=1.176, γ̄V→T=1.089, ∆γ=−0.088, p=0.575—strong but symmetric; directional asymmetry not significant.
- Qwen-plus (N=5, 30 rounds): γ̄T→V=1.119, γ̄V→T=0.988; T→V dominant in 4/5 reps; direction reversed vs. GPT-4o.
- DashScope gui-plus (N=10, 50 rounds): γ̄T→V=0.273, γ̄V→T=0.341; 7/10 reps collapse to γ=0.
- DeepSeek self-eval (N=30, 30 rounds): γ̄T→V=0.033, γ̄V→T=0.023; 29/30 reps yield exactly zero contagion; Cohen's d=0.07.
- Total experiment: 3,932 TTRL rounds, ~13,000 API calls across four evaluator configurations.

## Limitations
- Phase 1–2 experiments use only N=1 (GPT-4o, 30 rounds) for the initial contagion measurement; directional asymmetry claims from that run were not replicated at N=8.
- "Visual" tasks are text-proxied—no real images provided to executor or evaluator; visual strategies are semantically underdetermined, making PCI estimates for visual tasks a lower bound.
- Strategy set imbalance (8 text, 3 visual) biases weight distribution toward text strategies independently of evaluator effects.
- Qwen-plus condition interrupted at 7/30 planned repetitions due to API billing issues; only 5 valid runs used.
- Fixed baseline strategy (step_by_step) is also a candidate strategy, introducing structural drift that favors it via asymmetric updates; mitigated but not eliminated.
- Contagion metric γ is unbounded and geometrically sensitive to simplex concentration; bounded alternatives (JS divergence, Hellinger distance) recommended for future work.
- All experiments use a single executor (DeepSeek-chat); generalization to other executor families untested.

## Relevance to Agentic AI / LLM Agents
This paper directly targets a core risk in LLM-as-judge-driven self-improving agents: the evaluator shapes the agent's behavior in ways that are invisible to standard task metrics. The cross-modal contagion finding is particularly critical for multimodal agentic pipelines (e.g., vision-language agents using GPT-4o for self-improvement), where a shared evaluator across modalities can silently suppress modality-appropriate strategies. The practical hierarchy—cross-model evaluation is high-risk, self-evaluation is near-immune—provides actionable design guidance for agent system architects: either use same-model evaluation or deploy multi-evaluator ensembles and monitor PCI/Γ alongside task performance. The strategy inversion phenomenon (optimal strategies flip after cross-modal training exposure) also flags a subtle path-dependency failure mode in multi-task agent training curricula.

## Tags
#llm-as-judge #self-improvement #reward-hacking #multimodal-agents #evaluator-bias #test-time-training #goodharts-law #agentic-ai
