---
title: "Bayesian-Agent: Posterior-Guided Skill Evolution for LLM Agent Harnesses"
authors: ["Xiaojun Wu", "Cehao Yang", "Honghao Liu", "Xueyuan Lin", "Wenjie Zhang", "Zhichao Shi", "Xuhui Jiang", "Chengjin Xu", "Jia Li", "Jian Guo"]
source: "HuggingFace"
venue: ""
published: "2026-06-06"
published_time: "2026-06-06T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.08348"
url: "https://huggingface.co/papers/2606.08348"
pdf: "paper/harness/[HuggingFace 2026] Bayesian-Agent Posterior-Guided Skill Evolution for LLM Agent Harnesses.pdf"
---

# Bayesian-Agent: Posterior-Guided Skill Evolution for LLM Agent Harnesses

*🕒 **Published (v1):** 2026-06-06 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.08348)*

## TL;DR
Bayesian-Agent wraps LLM agent harnesses with a probabilistic evidence layer that treats reusable skills and SOPs as Bayesian hypotheses rather than heuristically edited text. By recording verified trajectory outcomes and maintaining feature-conditioned posteriors per skill, it drives five auditable rewrite actions (explore, patch, split, compress, retire) that evolve the harness substrate without touching model weights. On deepseek-v4-flash in incremental repair mode it lifts SOP-Bench from 80%→95%, Lifelong AgentBench from 90%→100%, and RealFin-Bench from 45%→65%.

## Problem
Existing self-evolving agent harnesses revise skills and SOPs through heuristic LLM reflection or by admitting raw success/failure counts as if trajectories were i.i.d. — neither approach separates observation strength from belief strength, leading to noisy edits that corrupt working skills or fail to fix recurring failure modes. Concurrently, skills accumulated without principled pruning bloat context budgets and surface stale assumptions to downstream runs.

## Method
Bayesian-Agent introduces a **categorical Bayesian evidence model** layered over a frozen execution harness. Each reusable skill `hk` accumulates a dataset `Dk,t` of verified (externally graded) binary-outcome trajectories. Feature vectors `zt` discretize runtime signals — benchmark context, failure-mode label, token-count bucket, turn-count bucket, latency bucket — into a fixed schema. The posterior is a factorized Naïve-Bayes classifier with Laplace smoothing (λ=1): class priors `πk,t(ℓ)` and per-feature likelihoods `θk,j,t(v|ℓ)` are updated online; the success posterior `sk,t(z)` normalizes the ratio of smoothed class scores (Eq. 10). A conjugate Beta-Bernoulli summary is also maintained for audit and conservative failure-dominance checks.

An ordered decision rule (Eq. 12) maps posterior state to one of five harness interventions:
- **Explore** — no observations yet, or posterior still uncertain
- **Patch** — a failure mode `r` has appeared ≥2 times → inject guardrail into model-facing prompt
- **Split** — ≥3 contexts and ≥4 observations suggest heterogeneous cases covered by one SOP
- **Compress** — ≥3 observations and success probability ≥0.72 → trim reliable skill text
- **Retire** — `β ≥ 4` and success probability <0.45 → mark skill unreliable

The framework operates in two modes: **full mode** (registry starts empty, updates online throughout a benchmark run) and **incremental mode** (ingest a completed baseline run's verified traces, then rerun only failed tasks with posterior-guided patches). Model-facing prompts receive executable guardrails and failure-mode patches; raw posterior numbers are kept in a separate audit log rather than exposed to the LLM. Adapter contracts allow GenericAgent, mini-swe-agent, and Claude Code to serve as drop-in execution backends that emit trajectory schemas and accept skill text.

## Key Contributions
- Formal casting of harness skills/SOPs as Bayesian evidence objects: `P(success | frozen model, inference environment, skill, feature vector)` replaces heuristic self-critique
- Efficient feature-conditioned categorical posterior (factorized Naïve-Bayes + Laplace smoothing) designed for sparse, expensive, context-dependent agent trajectories
- Five-action posterior-guided rewrite policy (explore / patch / split / compress / retire) with inspectable audit trail and before/after skill-evolution snapshots
- Adapter boundary enabling the same evidence loop across four execution backends (native, GenericAgent, mini-swe-agent, Claude Code) without harness-specific modifications
- Incremental repair mode: plug-in posterior layer that targets only failed tasks from a prior baseline run, spending tokens proportionally to repair need

## Results
All figures below are task-completion accuracy; BA-Inc token counts cover repair attempts only.

- **SOP-Bench (deepseek-v4-flash):** GA 80% → BA-Full 95% / BA-Inc 95%; 3/4 GA failures repaired; BA-Inc uses 153k repair tokens vs. 1.39M GA total
- **Lifelong AgentBench (deepseek-v4-flash):** GA 90% → BA-Inc 100%; 2/2 failures repaired with 84k repair tokens; BA-Full regresses to 85% (sparse-evidence ordering effect)
- **RealFin-Bench (deepseek-v4-flash):** GA 45% → BA-Full 52% → BA-Inc 65%; 8/22 failures converted
- **deepseek-v4-pro (saturated settings):** SOP-Bench and Lifelong both at 100% GA baseline, leaving BA-Inc inactive; RealFin: GA 60% → BA-Inc 68% (3/16 failures)
- **Backend ablation (deepseek-v4-flash):**
  - Native backend: SOP 95%→100%, Lifelong 95%→100%, RealFin 62.5%→72.5%
  - mini-swe-agent: Lifelong 85%→100%, RealFin 60%→70%
  - Claude Code: SOP 90%→100%, RealFin 77.5%→87.5%
  - Claude Code (pro-1m): SOP 65%→95%→100%, RealFin 65%→75%
- Baselines in main table include OpenClaw and Claude Sonnet 4.6 (GA 100%, OpenClaw 70%, Claude Code 75% on Lifelong AgentBench)

## Limitations
- Factorized categorical Naïve-Bayes is not full Bayesian structure learning or model selection; feature independence assumption may miss interaction effects
- Full online mode is not monotonically beneficial: BA-Full underperforms GA on Lifelong AgentBench with deepseek-v4-flash (85% vs. 90%), attributable to sparse-evidence ordering effects
- Backend coverage limited: main accuracy table centers on GenericAgent; broad plug-and-play generality across many independent harness/model pairs is future work
- Incremental mode presupposes a completed baseline run with verified outcomes; one-off tasks, subjective labels, nonstationary environments, and missing-tool failures yield little benefit
- Thresholds in the decision rule (Eq. 12) are engineering defaults, not tuned optima; sensitivity analysis absent
- No repeated-trial error bars; all reported figures are single consolidated benchmark runs

## Relevance to Harnesses / Meta-Harnesses
Bayesian-Agent directly operationalizes the meta-harness concept: it sits above execution harnesses (GenericAgent, mini-swe-agent, Claude Code) as a portable evidence-and-policy layer that governs how the harness substrate — prompts, SOPs, skill registries — evolves across runs. The adapter boundary (trajectory schema in, skill text out) is a concrete interface specification for meta-harness interoperability, showing how a principled optimization layer can be decoupled from any particular runtime. The posterior-guided action vocabulary (patch, split, compress, retire, explore) offers a transferable taxonomy for harness asset lifecycle management beyond this system. For researchers building or studying meta-harnesses, the incremental repair mode illustrates a practical deployment pattern: augment an existing harness's outputs with belief-calibrated repair rather than replacing the harness wholesale.

## Tags
#meta-harness #skill-evolution #bayesian-optimization #sop #agent-harness #self-evolving-agents #posterior-inference #harness-engineering
