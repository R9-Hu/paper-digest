---
title: "A First-Principles Derivation of LLM Policy Optimization: From Expected Reward to GRPO and Its Structural Extensions"
authors: ["Jianghan Shen", "Siqi Luo", "Yue Li", "Jiyao Liu", "Wanying Qu", "Yi Zhang", "Ziyan Huang", "Tianbin Li", "Ming Hu", "Xiaohong Liu", "Yirong Chen", "Junjun He"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T13:55:23+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16733"
url: "http://arxiv.org/abs/2606.16733v1"
pdf: "paper/agentic-ai/[Arxiv 2026] A First-Principles Derivation of LLM Policy Optimization From Expected Reward to GRPO and Its Structural Extensions.pdf"
---

# A First-Principles Derivation of LLM Policy Optimization: From Expected Reward to GRPO and Its Structural Extensions

*🕒 **Published (v1):** 2026-06-15 13:55 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16733v1)*

## TL;DR
This survey re-derives all LLM policy-gradient algorithms from the single objective J(θ) = E_τ[R(τ)] and organizes them along two axes: the **trajectory side** (how pθ(τ) governs sample collection, reuse, and constraints) and the **reward side** (how R(τ) is assigned, normalized, and converted to per-token advantages). The resulting framework is diagnostic: each method is located by which factor it modifies, what failure motivated the change, and what residual instability remains.

## Problem
Existing LLM RL surveys organize methods by domain, pipeline stage, or chronology, which obscures *why* each design choice was made and *which factor* of J(θ) it intervenes on. Practitioners facing a concrete training failure (high variance, instability, reward hacking) lack a principled map from failure to minimal corrective intervention, and the rapid post-GRPO expansion makes navigation increasingly difficult without such a framework.

## Method
Starting from J(θ) = E_τ[R(τ)], the survey derives the full chain: log-derivative trick (trajectory side, making the gradient tractable) → reward-to-go + advantage + GAE (reward side, per-token credit assignment) → importance sampling + PPO-Clip (trajectory side, data reuse + trust region) → LLM–MDP mapping (confirming deterministic transitions and differentiable log-probs) → GRPO (reward-side substitution: group-relative normalization Âᵢ = (Rᵢ − µ_G)/σ_G replaces the learned critic while the trajectory side is unchanged). Post-GRPO methods are then classified as: **trajectory-side** (collection, compression/reuse, diversity, repair, clipping granularity), **reward-side** (density, source, shaping, multi-objective, statistical bias correction, credit assignment), or **both-side** (compound instabilities where one-sided fixes leave residual failures). The framework extends to Agentic RL (multi-turn trajectory expansion) and the GRPO-OPD hybrid (teacher signal incorporated into the reward side while retaining J(θ)).

## Key Contributions
- Two-axis diagnostic decomposition of J(θ) unifying all policy-gradient methods under a single framework
- Formal proof that GRPO is a purely reward-side substitution; trajectory side (importance ratio, clipping, KL) is identical to PPO
- Classification of 40+ post-GRPO methods (DAPO, PRIME, Dr.GRPO, SCoRe, TreeRPO, VAPO, etc.) into trajectory-side, reward-side, and both-side categories with explicit failure→intervention mappings
- Extension of the two axes to Agentic RL (multi-turn, tool-using settings) and GRPO-OPD hybrid (on-policy distillation within the policy-gradient frame)
- Identification of "compound failures" requiring joint trajectory+reward design as the frontier for next-generation algorithms
- DPO and divergence-minimization distillation formally characterized as boundary cases that exit the policy-gradient frame

## Results
Survey paper; no novel empirical benchmarks. Analytical claims:
- The two-axis map subsumes all reviewed online policy-gradient methods within a unified derivation from J(θ)
- Compound failures (e.g., clip–variance coupling in DAPO, granularity coupling in HT-GRPO/GTPO) are shown to require joint both-side intervention—no single-side fix is sufficient
- DPO and f-divergence distillation are confirmed to require separate treatment as they replace rather than modify J(θ)

## Limitations
- No empirical experiments; the diagnostic utility of the framework is not validated on real training runs
- Coverage restricted to online policy-gradient methods; offline/preference-based methods (DPO, IPO) are explicitly out of scope
- The post-GRPO landscape is rapidly evolving; some methods may postdate or be missed by this snapshot
- The full Agentic RL (§7) and GRPO-OPD (§8) sections are truncated in the provided text, limiting assessment of their depth

## Relevance to Agentic AI / LLM Agents
Section 7 of this survey is explicitly dedicated to Agentic RL, framing multi-turn tool-using agents as a trajectory-side extension: single-step generation expands to multi-turn environment interaction, which simultaneously introduces reward-side challenges (delayed feedback, temporal credit assignment across turns). This directly addresses how to train LLM agents using RL—methods like WebRL, AgentRL, SkyRL, Search-R1, DeepResearcher, and ZeroSearch all appear in the framework's taxonomy. The two-axis diagnostic map provides a shared vocabulary for understanding why agent training is harder than single-turn RLVR: the trajectory and reward sides must be co-designed, not fixed independently.

## Tags
#reinforcement-learning #policy-gradient #grpo #llm-training #agentic-rl #rlhf #reward-modeling #survey
