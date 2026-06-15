---
title: "Learning Coordinated Preference for Multi-Objective Multi-Agent Reinforcement Learning"
authors: ["Pengxin Wang", "Lihao Guo", "Yi Xie", "Bo Liu", "Siyang Cao", "Jingdi Chen"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14693"
url: "http://arxiv.org/abs/2606.14693v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Learning Coordinated Preference for Multi-Objective Multi-Agent Reinforcement Learning.pdf"
---

# Learning Coordinated Preference for Multi-Objective Multi-Agent Reinforcement Learning

## TL;DR
PCMA (Preference Coordinated Multi-agent Policy Optimization) addresses cooperative multi-objective multi-agent RL by letting each agent learn a distinct, observation-conditioned preference vector over objectives rather than forcing all agents to share one. Theoretically, preference diversity yields a provable first-order improvement in the team objective. Empirically, PCMA outperforms MADDPG, IPPO, and MAPPO across MPE, SMAC, MOMAland, and a CARLA autonomous-driving scenario.

## Problem
In cooperative MOMARL, assigning the same scalarization weight to every agent conflates two distinct conflict structures: objectives competing within an agent, and agents competing under the same objective. Existing approaches (linear scalarization via MAPPO, value decomposition via MoMix) either require retraining per new preference or rely on the IGM assumption incompatible with continuous actions. No prior method learns coordinated, agent-specific trade-offs that collectively cover the team-beneficial region of the Pareto front.

## Method
PCMA treats each agent's preference vector `p_i ∈ Δ^{K-1}` as a latent coordination variable under the CTDE framework.

- **Stochastic preference planner**: each agent `i` has a planner `ϕ_ψ(o_i)` that outputs Dirichlet concentration parameters `α_i`; preferences are sampled `p_i ~ Dir(α_i)` at each step.
- **Preference-conditioned actor**: actions `a_i ~ π_θ(· | o_i, p_i)` via simple concatenation; utility advantage `A^{U_i} = A^{team} + λ p_i^⊤ A^{ind}_i` blends sparse team signal with dense per-objective signal.
- **Dual critics**: a centralized team critic and per-agent vector critics estimate `A^{team}` and `A^{ind}_i` respectively.
- **Diversity regularizer**: the planner loss `L_{plan}` includes a PPO term (encouraging team-improving preferences) minus `λ_1 D_α`, the expected pairwise preference distance, preventing all agents from collapsing to the same direction.
- **Theoretical grounding**: Theorem 4.2 decomposes first-order team improvement into a direct gradient term, an average alignment term, and a diversity-induced term `ηκN D_p > 0`; Theorem 4.6 (equilibrium tracking) shows that slow preference updates keep policies near the moving equilibrium with bounded error `C/(1-ρ) · δ`.

## Key Contributions
- Formulation of cooperative MOMARL as a *team-optimal equilibrium* problem—finding the preference profile whose induced Nash equilibrium maximizes the team objective.
- Theorem 4.2: preference diversity `D_p` contributes a provably positive additive term to the first-order team improvement, under a preference-improvement alignment assumption.
- Lemma 4.3 + Theorem 4.6: local continuity of preference-conditioned equilibria and bounded equilibrium-tracking error under slow preference drift.
- PCMA algorithm: stochastic Dirichlet preference planners + preference-conditioned PPO actors + diversity regularization, applicable to continuous and discrete action spaces.
- Empirical validation across 9 cooperative tasks (MPE, SMAC, MOMAland drone/walker) and a high-fidelity CARLA intersection simulation via OpenCDA-MARL.

## Results
- **Cooperative Spread**: PCMA 1.00 success rate vs. MAPPO 0.80, MADDPG 0.38, IPPO 0.27.
- **Safe Predator-Prey**: PCMA 0.96 vs. MAPPO 0.91, MADDPG 0.68.
- **Catch**: PCMA 0.94 success / 14.21 avg. reward vs. MAPPO 0.53 / 11.33.
- **MOMAWalker**: PCMA 93.64 forward distance vs. MADDPG 75.04, MAPPO 70.52 (IPPO 6.69).
- **SMAC-8m**: PCMA 0.87 success vs. MAPPO 0.80, MADDPG 0.23, IPPO 0.00.
- **OpenCDA-MARL (cooperative)**: PCMA utility −2072.9 vs. SAC −4776.9 and MAPPO −16793.3; PCMA 69.6% success, SAC 68.6%.
- Ablations confirm that learned planners outperform both random-preference (RAND) and shared-preference (SAME) variants; moderate `λ_1 = 0.1–0.2` improves over `λ_1 = 0` without the instability of `λ_1 = 0.5`.

## Limitations
- Assumes explicit reward decomposition into a scalar team reward plus per-agent vector rewards; this decomposition must be provided by the environment designer, not learned.
- Evaluation is on controlled cooperative benchmarks; the paper acknowledges open-ended real-world settings with emergent objectives are out of scope.
- Theoretical guarantees (Assumption 4.1 preference-improvement alignment, Assumption 4.4 attraction near equilibrium) are local and may not hold globally or in non-stationary environments.
- CARLA validation uses a narrow one-dimensional action (target speed); broader behavioral validation with richer action spaces is left to future work.
- The off-policy PCMA variant (SAC backbone) is only partially explored; on-policy PPO is the primary instantiation.

## Relevance to Agentic AI / LLM Agents
This paper addresses a core challenge in multi-agent systems: how a team of agents with different roles and observations should coordinate when objectives are heterogeneous and potentially conflicting—a structural problem that directly arises in LLM-based multi-agent pipelines (e.g., a planning agent trading off thoroughness vs. speed while a tool-use agent trades off accuracy vs. latency). The preference-as-latent-coordination-variable idea is broadly applicable: in agentic frameworks where subagents are specialized for different objectives, learning to coordinate trade-off directions rather than centralizing a single objective could improve team-level task completion. The equilibrium-tracking result is particularly relevant to dynamic agentic settings where roles and task demands shift over an episode, suggesting that gradually adapting agent objectives can remain stable without full re-optimization. Future LLM agent systems that expose utility signals per agent (e.g., cost, quality, safety) could directly incorporate PCMA's preference-coordination mechanism.

## Tags
#multi-agent #reinforcement-learning #multi-objective #pareto #coordination #marl #preference-learning #cooperative-ai
