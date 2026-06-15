---
title: "When Should Agent Trust Be Conditional? Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms"
authors: ["Yihan Xia", "Taotao Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14200"
url: "http://arxiv.org/abs/2606.14200v1"
pdf: "paper/agentic-ai/[Arxiv 2026] When Should Agent Trust Be Conditional Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms.pdf"
---

# When Should Agent Trust Be Conditional? Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms

## TL;DR
This paper formalizes skill-conditional trust R(i|k) for heterogeneous LLM agent pools, derives when conditioning beats a global score, and shows the same cross-skill borrowing mechanism that buys data efficiency is a one-episode-cheap reputation-laundering attack vector. The key result is that on a CIVT-certified GREEN AppWorld pool, a zero-target attacker drives routing regret from 0 to 0.94 with a single fabricated farm episode.

## Problem
Standard reputation systems assign each agent one global trust scalar, which is wrong for skill-specialized LLM agents: the best agent per skill genuinely changes across skills, so routing to the globally highest-scored agent forfeits specialization value. Sparse per-skill evidence means naive per-skill estimates are too noisy to route on, motivating cross-skill evidence borrowing—but that borrowing channel has no prior adversarial characterization.

## Method
The authors define a unified coupling-weighted estimator:

τ̂ᵢ,ₖ(W) = Σₖ′ Wₖ,ₖ′ nᵢ,ₖ′ oᵢ,ₖ′ / Σₖ′ Wₖ,ₖ′ nᵢ,ₖ′

where W is a K×K coupling matrix; Global (W=11ᵀ), Independent (W=I), fixed-block Conditional (Wₖ,ₖ′=β for correlated pairs), and Adaptive (Wₖ,ₖ′=β·max(Rₖ,ₖ′,0) from data) are all special cases. Routing regret against oracle competence scores each estimator. The Conditional Information Value Test (CIVT) screens from existing logs—no model execution—whether a pool lies in the beneficial conditioning regime (Δsk≥0.03, Δor≥0.05, non-unique per-skill winner). A controlled phase-diagram sweep over heterogeneity H, evidence sparsity N, and skill correlation C characterizes when/how-much/whether to condition. Adversarial analysis runs four attacker profiles (launderer, whitewasher, Sybil, sleeper) at explicit budget B against β-parameterized defenses on a real AppWorld pair.

## Key Contributions
- Formal skill-conditional trust object R(i|k) with CIVT as a zero-cost deployability screen
- Phase diagram showing conditioning wins only under high H + sparse N + correlated C; coupling optimum β≈0.1 is a dual-use knob
- Real-data placement: 14-agent AppWorld pool lands GREEN (Δsk=+0.041/+0.054) with the per-skill winner genuinely changing across skills
- Budget degeneracy proof: B and β cancel algebraically in Eq.(1) for zero-target launderers, making the attack one-episode cheap regardless of rate limits
- Characterization of four defenses; only a structural zero-evidence gate reduces laundering benefit (0.9357→0), while adaptive coupling, capped borrowing, and detection-without-action all fail

## Results
- AppWorld pool (14 agents, 7 app-skills): πskill vs. πglobal: +0.041 score / +0.054 success; per-task headroom Δor=0.190/0.310; CIVT verdict GREEN
- Difficulty strata reduce C (0.56–0.68) and raise Δsk to +0.06–+0.09; test_challenge raises C to 0.82 and Δsk collapses to +0.01 (AMBER)
- Laundering attack (simple_note→phone, R=0.861, GREEN pair): routing regret 0→0.9357 at β≥0.05; attack is effective at β=0.1 (deployed default)
- Contaminated naive trust verdict: −0.0643 vs. honest +0.1922 (gap entirely caused by admitting zero-target agent into global baseline)
- Budget flat curve: B=1 and B=24 both yield regret=0.9357; rate limits are algebraically void
- Zero-evidence gate: cuts launderer/whitewasher benefit from 0.9357 to 0.0000, honest gain intact; sleeper (partial genuine target evidence) bypasses gate at an explicit residual cost

## Limitations
- Does not claim Sybil-resistance; zero-evidence gate is bypassable by a sleeper who plants even one genuine target episode
- Adaptive coupling's graceful degradation at low C inverts into vulnerability at high C (the exact regime where conditioning is most valuable)
- Analysis covers verifiable-outcome settings only; subjective peer-reported signals require transitive aggregation machinery not studied here
- AppWorld places in the shallow green regime (moderate H, large N, high C), so measured gains are small; deeper beneficial regimes exist but rely on more specialized, sparsely evidenced open-marketplace agents not yet available as a public benchmark
- Further conditioning on role r and query q is left to future work

## Relevance to Agentic AI / LLM Agents
Multi-agent orchestration systems must decide which agent to delegate each task to, and this paper provides the first quantitative framework for when skill-conditional trust actually beats global reputation—directly applicable to any orchestrator routing across heterogeneous agent pools (different models, scaffolds, or tool stacks). The budget-degeneracy result is immediately security-relevant: any open agent marketplace using empirical-Bayes-style cross-skill pooling is vulnerable to a one-episode laundering attack, a threat that attestation-based defenses (like provenance protocols) cannot address because the farm evidence is genuine. The CIVT test offers a practical zero-cost pre-deployment screen for whether skill conditioning is even worth the attack surface it opens.

## Tags
#multi-agent #trust-and-reputation #adversarial-robustness #task-routing #llm-agents #agent-security #reputation-laundering #benchmark
