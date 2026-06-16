---
title: "Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts"
authors: ["Wenbo Pan", "Shujie Liu", "Chin-Yew Lin", "Jingying Zeng", "Xianfeng Tang", "Xiangyang Zhou", "Yan Lu", "Xiaohua Jia"]
source: "HuggingFace"
venue: ""
published: "2026-06-04"
published_time: "2026-06-04T09:26:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.05922"
url: "https://huggingface.co/papers/2606.05922"
pdf: "paper/harness/[HuggingFace 2026] Retrospective Harness Optimization Improving LLM Agents via Self-Preference over Trajectory Rollouts.pdf"
---

# Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts

*🕒 **Published (v1):** 2026-06-04 09:26 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.05922)*

## TL;DR
RHO (Retrospective Harness Optimization) is a self-supervised method that improves a full agent harness—tools, skills, and instructions—using only unlabeled past trajectories, with no validation set or ground-truth labels. It selects a diversity-weighted challenging coreset via a Determinantal Point Process, re-solves tasks in parallel groups, extracts self-validation and self-consistency signals, then proposes and self-ranks N candidate harnesses. A single RHO round lifts SWE-Bench Pro pass rate from 59% to 78%.

## Problem
All prior harness optimization methods (DSPy, TextGrad, GEPA, ADAS, Meta-Harness) require a labeled validation set to score candidates, which is difficult to obtain in deployment. Experience-based self-improvement methods (Dynamic Cheatsheet, ReasoningBank, Sleep-time Compute) avoid labels but only update memory/skills, leaving executable tools and core instructions untouched. No existing method is simultaneously label-free, edits the full harness (including executable tools), and operates in a single offline retrospective pass.

## Method
RHO operates in three stages over a corpus of past trajectories D = {(t_i, τ_i)}:

1. **Coreset Selection**: A language-model judge scores each trajectory for difficulty and produces a textual description of failure modes. Embeddings of descriptions form a similarity matrix S; combined with difficulty scores r, a DPP kernel K = diag(ẽr) S diag(ẽr) with θ=0.7 selects k=10 tasks that jointly maximize difficulty and embedding diversity via greedy DPP.

2. **Group Rollout**: Each coreset task is re-solved G=3 times in parallel with the current harness h₀. Two diagnostic signals are extracted per task:
   - *Self-validation* (rankval): the agent inspects each trajectory against task requirements, flagging incorrect tool calls, false assumptions, and premature stops.
   - *Self-consistency* (rankcon): the agent compares divergent trajectories to identify contradictory plans, tool sequences, or answers.
   Per-task instructions I_t = rankval ∪ rankcon are merged into a global improvement instruction set I.

3. **Best-of-N Harness Proposal**: N=3 candidate harnesses are generated in parallel via optimize(h₀, I). Each candidate is re-run on all k coreset tasks; a pairwise self-preference ranker scores each candidate trajectory against the original baseline trajectory. The candidate with maximum aggregate relative-advantage score S_j is accepted if S_j > 0, else h₀ is retained.

The harness is materialized as a directory: markdown files for instructions/skills, executable scripts for tools.

## Key Contributions
- RHO: first self-supervised method to optimize the *full* agent harness (tools + skills + instructions) using only unlabeled past trajectories in a single retrospective pass.
- DPP-based coreset selection that balances difficulty and diversity; ablations show either alone is insufficient.
- Two-dimensional diagnostic extraction (self-validation + self-consistency) that isolates improvement signals more reliably than raw-trajectory single-pass analysis.
- Best-of-N harness proposal with self-preference selection to guard against stochastic optimization failures.
- Evaluation across three domains (SWE-Bench Pro, Terminal-Bench 2, GAIA-2) with analysis of behavior shift and action-mix change.

## Results
- **SWE-Bench Pro**: Vanilla Codex 0.59 → RHO 0.78 (+0.19 absolute); vs. feedback-free baselines (Dynamic Cheatsheet +0.03, ReasoningBank +0.02, Sleep-time Compute +0.05); vs. Meta-Harness 1-round (0.62, requires labels, 0.4× agent calls) and Meta-Harness 10-round (0.80, requires labels, 3.1× agent calls).
- **Terminal-Bench 2**: 0.71 → 0.76 (+0.05); baselines all +0.02.
- **GAIA-2**: 0.29 → 0.37 (+0.08); baselines +0.01/−0.01/+0.03.
- **Coreset ablation** (SWE-Bench Pro): difficulty-only 0.62, coverage-only 0.58, random 0.64, DPP 0.78.
- **Diagnosis ablation** (SWE-Bench Pro): full 0.78, −self-consistency 0.56, −self-validation 0.70, raw trajectory 0.60.
- **Best-of-N consistency**: across N=3 candidates, the chosen harness avoids the worst candidate in all benchmarks; lowest candidate on SWE-Bench Pro still reaches 0.73 vs. 0.59 baseline.
- Behavior analysis: RHO shifts action mix toward verification (+61% verify) on SWE-Bench Pro and toward execution on Terminal-Bench 2/GAIA-2; gains concentrate on long-horizon tasks.

## Limitations
- Requires environments that reset cleanly and tolerate repeated rollout attempts; one-shot or irreversible tasks are explicitly out of scope.
- Assumes agent competence is substantially mediated by an editable harness; domains where this doesn't hold are unaddressed.
- Generalization to harness surfaces, task fingerprints, and rollout budgets beyond the three tested domains is future work.
- Self-preference ranking is not guaranteed to select the highest held-out test performer—it consistently avoids the worst candidate but the chosen harness does not always match the top-scoring one.
- Trajectories used as optimization input may contain adversarially injected content (e.g., mid-task browser hijacking), which could entrench malicious behavior in the optimized harness.
- Single retrospective pass; if the trajectory corpus is small or unrepresentative, signal quality degrades.

## Relevance to Harnesses / Meta-Harnesses
RHO directly advances the meta-harness research agenda—the automatic improvement of the full agent harness (prompts, skills, executable tools) without human curation—by removing the labeled-validation prerequisite that every prior meta-harness optimizer (ADAS, Meta-Harness) depends on. The DPP-coreset + group-rollout + self-preference pipeline provides a concrete architecture for deployment-time harness evolution, filling the gap between static harnesses and validation-gated iterative search. For practitioners building self-improving agents, the ablations quantify exactly which components of retrospective analysis carry the signal (self-consistency is the dominant contributor on SWE-Bench Pro), and the comparison table (Table 5) provides a clean taxonomy of the design space. The work also establishes that full-harness edits (tools + skills) outperform memory-only approaches by a large margin, reinforcing the importance of treating the harness as a first-class optimization target.

## Tags
#harness-optimization #meta-harness #self-supervised #agent-self-improvement #determinantal-point-process #swe-bench #tool-use #llm-agents
