---
title: "Contract-Based Compositional Shielding for Safe Multi-Agent Reinforcement Learning"
authors: ["Omar Adalat", "Edwin Hamel-De le Court", "Francesco Belardinelli"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14130"
url: "http://arxiv.org/abs/2606.14130v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Contract-Based Compositional Shielding for Safe Multi-Agent Reinforcement Learning.pdf"
---

# Contract-Based Compositional Shielding for Safe Multi-Agent Reinforcement Learning

## TL;DR
Purely factorized (unilateral) runtime shields in multi-agent RL are overly conservative: they exclude joint actions that are safe only through coordination. This paper certifies tuples of local LTLsafe obligations via a circular assume-guarantee fixed point, projecting them into decentralized action masks that recover team-optimal coordinated safe behavior without central control at runtime.

## Problem
Decentralized shields in safe MARL typically compute each agent's permitted actions by assuming worst-case teammate behavior — the Cartesian product of per-agent safe sets. This discards jointly safe actions that are safe only when teammates commit to specific behaviors, making decentralized shields strictly more conservative than a centralized shield and sacrificing team-optimal return. No prior approach admits circular coordination assumptions (where A relies on B and B relies on A) without imposing an acyclic dependency order between agents.

## Method
**Contract definition**: A contract C = (φ₁,...,φₙ) is a tuple of local LTLsafe obligations, one per agent over local sub-alphabets Apᵢ ⊆ Ap, whose conjunction must semantically entail the shared global safety formula Φsafe.

**Certification via contract-product fixed point**: Each φᵢ is compiled into a finite deterministic safety automaton. Their product with the environment forms the contract product state space X^C. A monotone assume-guarantee predecessor operator TC is iterated to compute the greatest fixed point Win□_C — the largest locally safe region admitting non-empty Cartesian action interfaces closed under all successors. A contract is certified iff the initial state lies in Win□_C. This circular fixed point avoids acyclic training orders used by prior work.

**Library construction**: Candidate contracts up to formula depth D=2 are enumerated offline, each certified or discarded; the retained set is the certified library L_cert.

**Runtime masks**: For each product state, the winning rectangles project to per-agent action masks. Agent i receives only its local mask; no inter-agent communication is required at runtime.

**Learning-time selection**: A non-stationary multi-armed bandit (discounted UCB) treats each certified contract as an arm, switching contracts at episode boundaries based on observed team return — separating safety (static, offline-certified) from reward adaptation (online bandit).

## Key Contributions
- Decomposition of a single global LTLsafe specification into local obligations compiled into contract safety automata.
- Circular compositional soundness theorem (Theorem 1): any execution admitted by certified local masks satisfies Φsafe, without acyclicity constraints.
- Optimal safe recovery theorem (Theorem 2): if the globally optimal safe policy is representable by some contract in L_cert, the combined max over contracts and policies achieves it.
- Safety under bandit contract selection (Theorem 3): switching certified contracts only at episode resets preserves Φsafe every episode.
- Empirical evaluation over 6 MARL benchmarks and 15 algorithmic variants.

## Results
- **6 environments**: Flatland, Connector, Level-Based Foraging, RWARE, Pressure Plate, Car Platoon.
- **15 variants**: IPPO, IQL, MAPPO, Joint-PPO, PQN-VDN, Lagrangian-IPPO/IQL, ICPO, shielded variants, Contract-IPPO, Contract-IQL.
- Where factorized shields are viable, Contract-IPPO/IQL improves reward over shielded baselines and converges toward Shielded-Joint-PPO (the centralized upper bound).
- For RWARE, Pressure Plate, and Connector, the global specifications admit no factorized shield at all; contract shielding is the only decentralized approach that produces safe policies.
- Largest instances: up to 12,001 candidate profiles searched; up to 390 certified.
- No aggregate scalar summary reported; results are presented as learning curves with ±95% CI (Figure 4).

## Limitations
- Offline contract enumeration scales exponentially with formula depth D and number of agents; D=2 used throughout experiments.
- No convergence guarantee for the bandit selector; performance is bounded by library representability.
- Mask identifiability requires each agent to maintain an augmented local contract-product state, not just raw environment observations.
- Only deterministic, qualitative (LTLsafe) safety properties; quantitative and probabilistic obligations are left for future work.
- The certified library must be constructed for each new environment and safety specification from scratch.

## Relevance to Agentic AI / LLM Agents
This work directly addresses the formal safety coordination problem that arises when multiple autonomous agents must collectively satisfy a shared constraint without a central enforcer — a core challenge for multi-agent LLM pipelines and tool-using agent networks. The circular assume-guarantee framework is a principled alternative to the typical approach of either centralizing control or using uncertified heuristics, and the contract-as-commitment abstraction maps naturally onto structured agent communication. The runtime/offline separation (certify safety offline, optimize reward online) is an architectural pattern applicable to agentic systems where LLM policies must be constrained by verifiable safety envelopes. Results demonstrating that factorized shields fail on coordination-dependent safety tasks highlight why naive decomposition of safety checks in multi-agent LLM systems is insufficient.

## Tags
#multi-agent #safe-rl #shielding #formal-methods #ltl #assume-guarantee #marl #cooperative-agents
