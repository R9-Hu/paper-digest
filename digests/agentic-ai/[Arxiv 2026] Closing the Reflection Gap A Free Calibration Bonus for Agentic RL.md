---
title: "Closing the Reflection Gap: A Free Calibration Bonus for Agentic RL"
authors: ["Yinglun Zhu"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14211"
url: "http://arxiv.org/abs/2606.14211v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Closing the Reflection Gap A Free Calibration Bonus for Agentic RL.pdf"
---

# Closing the Reflection Gap: A Free Calibration Bonus for Agentic RL

## TL;DR
LLM agents persistently mis-assess their own correctness even after observing concrete environment feedback (execution results, error messages)—a "reflection gap" that standard outcome-only RL barely closes due to a credit-assignment mismatch. RefGRPO fixes this by augmenting the GRPO reward with a cost-free calibration bonus (the indicator that the agent's binary self-assessment matches the actual outcome) and a two-stage decaying coefficient schedule. The result is simultaneous gains in reflection calibration and task accuracy, enabling verifier-free self-improvement and better test-time selective prediction.

## Problem
Standard RL (e.g., GRPO) trains LLM agents purely on outcome rewards, so gradients are agnostic to whether the agent's post-feedback self-assessment is correct. This creates two pathological gradient signals: (1) honest error flags on failed rollouts receive negative advantage, suppressing genuine error detection; (2) underconfident flags on successful rollouts receive positive advantage, reinforcing erroneous self-doubt. Consequently, underconfidence rates remain above 44% even after GRPO training, and reflection accuracy lags far behind task accuracy.

## Method
RefGRPO augments GRPO+ with two components:

1. **Free calibration bonus**: For each rollout k, compute `c_k = 𝟙(s^ref_{k,H} = r_k)`, where `s^ref ∈ {0,1}` is the agent's binary post-feedback reflection score and `r_k ∈ {0,1}` is the outcome reward. Augment the reward: `r̃_k = r_k + α(t)·c_k`. This gives well-calibrated rollouts higher relative advantage regardless of task outcome—no separate reward model, LLM judge, or human annotation required.

2. **Dynamic coefficient schedule**: Two-stage schedule `α(t) = α₀` for the first `γ·T` steps (default α₀=0.1, γ=2/3), then `α(t) = α₁ < α₀` (default α₁=0) for the remainder. Front-loading calibration early then tapering allows the model to retain calibration gains while recovering any task-accuracy cost of the fixed-coefficient variant.

The augmented advantages are computed over group-normalized `r̃_k` values, and the GRPO+ clipped-surrogate objective (asymmetric clipping, token-mean normalization, no KL penalty) is otherwise unchanged.

## Key Contributions
- Identifies and formally characterizes the **reflection gap**: persistent post-feedback miscalibration in RL-trained LLM agents, diagnosed as a credit-assignment mismatch in outcome-only RL.
- Introduces **RefGRPO**: a drop-in augmentation to GRPO-style algorithms using a free, annotation-free calibration bonus derived from the reflection–outcome contrast.
- Proposes the **ChowScore** (adapted from Chow 1957/1970) as a unified metric combining task accuracy and reflection calibration, with a tunable credit β for honest error detection.
- Demonstrates **verifier-free self-improvement**: calibrated reflection scores serve as informative pseudo-rewards for continued RL without outcome supervision (+2.8 accuracy points vs. +0.5 for GRPO+).
- Demonstrates **test-time selective prediction**: calibrated reflections used to filter rollouts improve selective accuracy lift from +0.6 (GRPO+) to +1.6 (RefGRPO) in single-turn.

## Results
- **Multi-turn, Qwen2.5-Coder-7B**: underconfidence rate 44.4% → 7.7%; task accuracy 75.1% → 76.5%; ChowScore 73.0% → 76.5% (vs. GRPO+ baseline).
- **Single-turn, Qwen2.5-Coder-3B**: underconfidence rate 23.7% → 1.3%; reflection accuracy 76.6% → 79.7%; ChowScore 68.5% → 71.1%.
- **Single-turn, Llama-3.2-3B**: underconfidence 30.9% → 23.5%; ChowScore 58.4% → 62.2%.
- **Calibration delta (Acc_ref − Acc)** vs. 7B specialists: RefGRPO-7B +1.3, SQL-R1-7B +0.2, OmniSQL-7B −1.0; RefGRPO is the only model whose reflection is meaningfully informative.
- **Self-improvement**: from RefGRPO checkpoint, +2.8 accuracy (67.1→69.9) vs. +0.5 from GRPO+ checkpoint despite lower starting accuracy.
- **Selective prediction lift (Acc_sel@8 − Avg@8)**: single-turn GRPO+ +0.6 → RefGRPO +1.6; multi-turn GRPO+ +0.9 → RefGRPO +1.1.
- Evaluated across five text-to-SQL benchmarks: Spider-Dev, Spider-DK, Spider-Realistic, Spider-Test, Bird-Dev.

## Limitations
- Experiments capped at 7B parameter scale; generalization to larger models is unverified.
- Binary reflection score `s^ref ∈ {0,1}` only; extension to real-valued confidence in [0,1] is left for future work.
- Evaluated exclusively on text-to-SQL with verifiable binary outcomes; applicability to domains with non-binary or noisier feedback signals is untested.
- The calibration bonus still requires access to the ground-truth outcome `r_k` at training time; it does not address settings where outcome supervision is entirely unavailable.

## Relevance to Agentic AI / LLM Agents
Post-feedback self-assessment is a core capability for autonomous agents that must decide when to retry, commit, or escalate—making the reflection gap a practically significant failure mode rather than a theoretical curiosity. RefGRPO's "free calibration" framing is directly actionable: it requires no auxiliary verifier, which has been a persistent bottleneck in scaling agent training. The downstream applications—verifier-free self-improvement and selective prediction—address two open problems in agentic RL: reducing dependence on external outcome oracles and improving test-time compute efficiency. This work connects to the broader line of agentic RL research (SkyRL, Search-R1, SWE-RL) by adding a calibration dimension that existing outcome-only methods ignore.

## Tags
#agentic-rl #reflection-calibration #grpo #self-improvement #selective-prediction #reinforcement-learning #text-to-sql #llm-agents
