---
title: "A Causal Model of Theory of Mind in Conflict for Artificial Intelligence"
authors: ["Nikolos Gurney"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T16:44:42+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16944"
url: "http://arxiv.org/abs/2606.16944v1"
pdf: "paper/agentic-ai/[Arxiv 2026] A Causal Model of Theory of Mind in Conflict for Artificial Intelligence.pdf"
---

# A Causal Model of Theory of Mind in Conflict for Artificial Intelligence

*🕒 **Published (v1):** 2026-06-15 16:44 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16944v1)*

## TL;DR
This paper presents a structural causal model (formalized as a DAG) that answers *when* AI systems should engage Theory of Mind (ToM) reasoning in conflict, a question left unaddressed by existing mechanistic AI-ToM approaches. ToM is modeled as a conditionally activated mechanism triggered by situational and agent-level variables, with epistemic accuracy—not behavioral outcome—as the primary optimization target. The framework gives AI a resource-rational decision procedure for mentalizing that avoids wasted computation when social reasoning is causally unnecessary.

## Problem
Existing AI-ToM models answer *how* to mentalize (Bayesian inference, interactive POMDPs, inverse planning) but not *when*. ToM is computationally expensive and can be counterproductive: finite state machines achieve social behaviors without ToM; higher-order ToM degrades performance in low-complexity environments; DARPA ASIST deployments wasted ToM on tasks solvable without social reasoning. No prior work provides a causal account of the situational and agent-level conditions under which mentalizing is necessary, sufficient, or merely contributory.

## Method
The model is a directed acyclic graph (DAG) with structural equations, treating ToM as a mechanism node whose output is determined by upstream conditions rather than always-on:

**Exogenous variables (4):** Conflict Complexity (C ∈ [0,1]), Information Asymmetry (IA ∈ [0,1]), Objective Tractability (OT ∈ {0,1}), and Sophistication (S ∈ [0,1] — composite of recursive reasoning capacity, game frame recognition, and opponent modeling).

**Endogenous mediators (5):** Observable Signals (OS, mid-interaction update channel), Perceived Objective Tractability (POT), Perceived Opponent Sophistication (PS, anchored on self-projection with δ weight), Relative Sophistication (RS = S/PS, miscalibration ratio), and Accessible Tractability (AT, whether the agent can actually derive an analytical solution).

**ToM engagement** is a two-stage binary process yielding three states {0=not engaged, 1=engaged but rejected, 2=engaged and accepted}. Stage 1 fires when `λ₁·IA + λ₂(1−AT) + λ₃|RS−1| > θ_E` (three pathways: tractability, reasoning-depth, enabling-cause). Stage 2 conditions acceptance on signal strength, sophistication, and complexity.

**Epistemic Accuracy (EA)** is a mixture `w₁·f_analytical(AT) + w₂·f_ToM(RS) + w₃·f_intuitive` where mixture weights are determined by the ToM engagement state. Rejected mentalizing (ToM=1) leaves a trace in the intuitive mode. Conflict Behavior is downstream of EA and RS but outside the DAG proper.

## Key Contributions
- First structural causal model specifying *when* ToM engagement is necessary, sufficient, or contributory in conflict
- Formalization of three distinct causal pathways to ToM activation (tractability, reasoning-depth, enabling-cause)
- Separation of epistemic accuracy from behavioral policy, providing a clean optimization target for learning-based AI
- Principled resource-rational decision procedure for AI mentalizing with explicit fallback to analytical/heuristic modes
- DAG structure designed for modular generalization beyond conflict to coordination, cooperation, and other social phenomena

## Results
No empirical results reported; this is a theoretical paper. Simulation validation, empirical human-machine teaming studies, and functional form calibration are deferred to future work. The structural equations are specified directionally (e.g., POT increases with OS and S, decreases with C) but without committed functional forms or parameter estimates.

## Limitations
- Static, dyadic model of a single interaction; repeated-game extension is deferred
- Functional forms of OS (Eq. 1), the intuitive mode, and signal-to-sophistication mapping g(·) are intentionally unspecified, requiring future empirical calibration
- Sophistication S collapses recursive reasoning, game frame recognition, and opponent modeling into one scalar; the projection onto [0,1] is not formalized
- No empirical validation; simulation and HMI experiments are future work
- Additive treatment of IA in the engagement equation (Eq. 6) approximates rather than strictly formalizes the enabling-cause relationship
- Ethical analysis of conflict-optimized mentalizing, cross-cultural miscalibration, and selective withholding of social reasoning is explicitly deferred

## Relevance to Agentic AI / LLM Agents
This paper directly addresses a foundational design question for agentic systems that operate in multi-agent environments: when should an agent invest in modeling another agent's mental states rather than relying on analytical or heuristic reasoning? The decision procedure—assess C, IA, AT, RS; engage ToM only when the enabling cause and at least one triggering pathway are active—is implementable as a meta-controller over any existing mechanistic ToM module (PsychSim, interactive POMDP, Bayesian ToM). For LLM-based agents, which currently only mentalize when explicitly prompted and fail to generalize beyond canonical ToM tasks, this framework suggests a principled gating mechanism. The decoupling of epistemic accuracy from behavioral policy is particularly valuable for multi-agent RL systems, where separate optimization of the mental-state model and the action policy can prevent the behavioral-prediction conflation that plagues current approaches.

## Tags
#theory-of-mind #causal-model #multi-agent #human-machine-teaming #social-reasoning #epistemic-accuracy #resource-rationality #agentic-ai
