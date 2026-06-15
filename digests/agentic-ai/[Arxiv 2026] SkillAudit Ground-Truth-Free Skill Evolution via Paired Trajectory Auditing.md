---
title: "SkillAudit: Ground-Truth-Free Skill Evolution via Paired Trajectory Auditing"
authors: ["Haowen Gao", "Haoran Chen", "Can Wang", "Shasha Guo", "Liang Pang", "Zhaoyang Liu", "Huawei Shen", "Xueqi Cheng"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14239"
url: "http://arxiv.org/abs/2606.14239v1"
pdf: "paper/agentic-ai/[Arxiv 2026] SkillAudit Ground-Truth-Free Skill Evolution via Paired Trajectory Auditing.pdf"
---

# SkillAudit: Ground-Truth-Free Skill Evolution via Paired Trajectory Auditing

## TL;DR
SkillAudit is a framework for evolving LLM agent "skills" (structured procedural instruction packages) without any ground-truth feedback—no hidden tests, reference solutions, or oracle signals. It works by running the same task twice (with and without the candidate skill) and using the behavioral divergence between those two trajectories as a self-contained optimization signal. On 89 containerized professional tasks, it achieves 73.9% average task reward vs. 56.7% for static expert-authored skills and 40.9% for no skill at all.

## Problem
Agent skills degrade after deployment as edge cases, API changes, and task-specific constraints surface through use. Existing skill evolution methods rely on privileged feedback—held-out validation scores, oracle pass/fail signals, environment rewards, or enterprise logs—that practitioners typically do not have. The gap is: how to improve skills when the only available inputs are a task description (T), workspace data (W), and an initial skill (S₀).

## Method
**Paired Trajectory Auditing:** At each iteration, the agent executes the task twice in parallel—once with the candidate skill (τ_w) and once without (τ_wo). Behavioral divergences between the two trajectories are the primary signal, isolating the skill's effect from task difficulty.

**PACE (Process-Aligned Contrastive Evaluation):** A cluster of 12 LLM-based evaluator templates across four dimensions—Process Adherence, Artifact Evidence, Consistency, and Effectiveness Delta—that compare trajectory divergence points and produce *segment-anchored* diagnostic signals: each signal is tied to a verbatim quote from the skill document, specifying which passage caused which wrong action. A three-way verdict (helped / hurt / inert) gates commit, rollback, or deferral of each update.

**Anchor Verifier:** Compiled once from T and W at setup, then frozen. Encodes only constraints checkable without ground truth (file existence, format compliance, values recomputable from workspace). Acts as a drift guard: even if PACE reports improvement, an Anchor Verifier regression forces rollback.

**Dual-Strategy Pipelines:** A compatibility pre-assessment routes tasks to either:
- *Refine*: subtraction-first; removes noise/redundancy from broadly sound skills; halts on any hurt signal; protects segments PACE marks as helpful.
- *Repair*: diagnosis-driven replacement; swaps conflicting passages with verified alternatives extracted from τ_wo; may fill knowledge gaps post-removal.

The loop runs at most 5 iterations, terminating when no hurt in the last two rounds, Anchor Verifier passes, and no surgery targets remain.

## Key Contributions
- Formal definition of the ground-truth-free constraint C_gtf for skill evolution, ruling out all external oracle signals during optimization.
- Paired trajectory auditing as a label-free mechanism to isolate skill effect from task difficulty.
- PACE: segment-anchored, process-aligned contrastive evaluation across four dimensions with priority-ordered verdict aggregation (any "hurt" vetoes all other signals).
- Anchor Verifier: a deterministic, frozen structural check compiled once from the task specification, immune to LLM evaluator drift.
- Dual Refine/Repair pipelines with differentiated constraint gates.
- Identification of an *observability boundary*: evolution succeeds when skill knowledge leaves an observable structural trace; domain-procedural knowledge without observable traces resists ground-truth-free optimization.

## Results
- **Overall:** 73.9% average task reward on 89 SkillsBench tasks; +33.0 pp over no-skill baseline (40.9%); +17.2 pp over static expert-skill baseline (56.7%).
- Outperforms static skill in 7 of 8 domains; matches (not exceeds) in Finance & Economics.
- Largest gains: Software Engineering (+38.5 pp), Office & White Collar (+26.7 pp), Mathematics & OR (+21.9 pp).
- Skill-hurt recovery: 3 tasks where the expert skill was strictly worse than no skill (reward 0.0 vs. 1.0) are all restored to reward 1.0.
- High-quality skills (initial reward ≥ 0.5, n=59): 92% (54/59) preserved or improved.
- Low-quality skills (initial reward < 0.5, n=30): 43% (13/30) lifted to passing.
- By knowledge type: library-API (79.2%) and mathematical-methods (80.7%) skills evolve well; domain-procedure skills (69.2%) dominate the failure set (77% of tasks left at reward 0).
- By task type: formatting/generation/transformation reach ≥88.9%; search (25.0%), repair (45.0%), planning (57.5%) evolve worst.
- Model: Claude Opus 4.8 used for all agent runs, PACE evaluations, and Skill Iterator calls.

## Limitations
- Ground-truth-free evolution cannot synthesize domain-procedural knowledge the auditor cannot observe; ~57% of initially failing skills remain at reward 0 after evolution.
- Over-pruning on semantic tasks: without observable traces, subtraction can delete load-bearing domain knowledge the verifier cannot justify restoring.
- Under-pruning on already-passing tasks: bloated skills above 1,500 lines may be left untouched because Anchor Verifier passes under both conditions, providing no edit authorization signal.
- Falls back to single-trajectory evaluation when the without-skill run is too incoherent to serve as a reference, weakening the contrastive signal.
- Maximum 5 iterations; complex skills may need more refinement cycles.
- Evaluated on a single model (Claude Opus 4.8); generalization to other frozen agents is unverified.
- The Repair pipeline's "swap" mechanism relies on τ_wo containing a correct alternative fragment—absent when both runs fail.

## Relevance to Agentic AI / LLM Agents
SkillAudit directly addresses the practical lifecycle problem for tool-augmented agents deployed on long-horizon professional tasks: skills authored once become stale, and most production environments lack oracle feedback to drive improvement. The paired-trajectory auditing mechanism is a general principle—using contrastive self-execution as a gradient substitute—applicable whenever an agent can re-run a task without ground truth. The observability boundary finding has immediate design implications for anyone building agent skill libraries: it predicts exactly which skill types will resist automated refinement and require human or oracle intervention. The work also validates and empirically characterizes the Anthropic Agent Skills specification as a viable adaptation interface for frozen LLMs across professional domains.

## Tags
#skill-evolution #agent-skills #ground-truth-free #trajectory-auditing #process-reward #llm-agents #benchmark #self-improvement
