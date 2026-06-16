---
title: "AgentFairBench: Do LLM Agents Discriminate When They Act?"
authors: ["Triveni Morla", "Rohith Reddy Bellibaltu", "Manpreet Singh", "Manmeet Singh Kapoor"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T13:50:26+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16723"
url: "http://arxiv.org/abs/2606.16723v1"
pdf: "paper/harness/[Arxiv 2026] AgentFairBench Do LLM Agents Discriminate When They Act.pdf"
---

# AgentFairBench: Do LLM Agents Discriminate When They Act?

*🕒 **Published (v1):** 2026-06-15 13:50 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16723v1)*

## TL;DR
AgentFairBench is a reproducible, multi-domain benchmark and evaluation harness that measures demographic disparity in the *actions* of LLM agents (not their text outputs) across hiring, lending, and medical triage. It introduces a scaffold axis (direct → chain-of-thought → multi-agent → tool-augmented) to test whether agentic complexity amplifies bias, and a critical methodological correction: naive MASD-to-noise comparisons overstate disparity by ~2.4× due to statistic arity mismatch. A pilot on claude-haiku-4-5 finds no demographic effect above the arity-matched noise floor.

## Problem
Existing fairness benchmarks grade model *answers* (BBQ, StereoSet, CrowS-Pairs), not model *actions*. This misses the structural gap formalized as "Masking" (BCF P2): token-level parity can coexist with action-level disparity when language is mapped to executable decisions, tool calls, and multi-step trajectories. Additionally, agentic scaffolds (CoT, multi-agent deliberation, tool use) may *amplify* entering bias (BCF P3 Super-additivity) — a phenomenon no prior benchmark instruments.

## Method
**Counterfactual matched-set design** following Bertrand–Mullainathan: synthetic, demographic-neutral profiles (hiring résumés, loan applications, clinical intakes) are evaluated in sets of six variants that differ only in a name-coded race×gender signal (White/Black/Hispanic × Male/Female). Each profile is run under four agent scaffolds — C0 (direct prompt), C2 (chain-of-thought), C3 (two-agent deliberation), C4 (tool-augmented) — so scaffold depth is a first-class measurement axis.

The **evaluation harness** (`agentfairbench`, pip-installable, NumPy-only) computes:
- **CFR** (counterfactual flip rate): fraction of matched sets where the binary decision is not unanimous across demographic conditions
- **MASD** (mean absolute score difference): mean of per-set max–min score spread across six groups
- **Action-rate disparity**: group-level proportion of positive decisions
- **∆tool** (C4 only): spread in tool-invocation rate across groups

All estimates use BCa bootstrap CIs, McNemar/Wilcoxon paired tests, and Benjamini–Hochberg FDR correction at q=0.05. The key methodological contribution is an **arity-matched noise floor**: MASD is a six-group range statistic and must be compared against a Monte Carlo six-group noise spread (from within-cell residuals after removing group main effects), not against a two-run pairwise retest MAE.

## Key Contributions
- Multi-domain, action-level fairness benchmark (hiring/lending/triage) with counterfactual matched sets and a scaffold stratification axis — no prior benchmark combines all five properties simultaneously
- Pip-installable, NumPy-only evaluation harness implementing CFR, MASD, action-rate disparity, ∆tool, with full statistical rigor (BCa bootstrap, FDR control); cost ~$1.79 for 864 calls at Haiku tier
- Live leaderboard with held-out private test split, contamination canary (`AGENTFAIRBENCH-CANARY-2f9c1a`), and SHA-256 content hashes per profile to prevent benchmark gaming
- **Arity-matched null methodology**: demonstration that comparing a six-group spread to a two-run pairwise difference mechanically overstates disparity by ~2.4× under pure noise; correction reduces apparent MASD-to-noise ratio from 2.4× to 0.83× (mean)
- Novel tool-invocation disparity metric ∆tool measuring procedurally disparate scrutiny in C4 scaffold

## Results
- **Pilot**: 864 decisions (36 profiles × 6 demographic conditions × 4 scaffolds) on claude-haiku-4-5, plus a 648-decision test–retest run (C0–C3)
- Test–retest decision agreement: **0.917** (≈8% binary flip rate from pure resampling noise)
- Per-cell retest MAE: **0.15–5.75** score points
- Naive MASD-to-noise ratio: **1.24–3.33×** (mean ~2.4×) — flagged as artifactual
- Arity-matched MASD-to-noise ratio: **0.75–0.96** across all C0–C3 domain-scaffold cells (mean **0.83**) — below 1.0 everywhere, indicating observed score spread is *smaller* than noise expectation
- **0 of 120** pairwise contrasts and **0 of 9** omnibus contrasts survive FDR correction → no demographic effect distinguishable from sampling noise at n=12 matched sets per cell
- Planted-bias property test confirms the harness *does* recover known disparity when injected, validating instrument sensitivity

## Limitations
- Pilot covers only one model (claude-haiku-4-5) at modest scale (n=12 matched sets per domain-scaffold cell); insufficient power to draw general conclusions about LLM fairness
- C4 scaffold not included in the test–retest reliability run, so ∆tool results lack a noise floor comparison
- Counterfactual design is a correspondence-audit (name substitution), not a structural-causal-model counterfactual; does not intervene on a protected-attribute node in a causal graph, so the stronger SCM-counterfactual guarantee does not apply
- C1 scaffold (retrieval-augmented context injection) deferred to v2; scaffold ladder is incomplete
- Leaderboard's held-out gaming resistance applies only to models where maintainers can re-run inference; proprietary models without shared API access receive only trace-reproducibility verification
- Domain score scales (0–100 / 1–5 / 1–5) are not commensurable in harm, so cross-domain aggregation is intentionally avoided but limits single-number comparison
- Genuine k-replicate noise floor (using multiple independent runs rather than within-cell residuals) deferred to v1.1

## Relevance to Harnesses / Meta-Harnesses
AgentFairBench is itself a **meta-harness**: a pip-installable orchestration layer that wraps arbitrary LLM agents in counterfactual evaluation loops, implements multiple scaffold topologies (C0–C4) as pluggable entry loci, and computes a battery of statistical metrics from structured action traces — exactly the pattern of a meta-harness that instruments underlying agent systems. The **replay adapter** (re-scoring frozen JSONL trace archives without re-issuing API calls) and the **mock adapter** (deterministic canned responses for CI) are canonical meta-harness engineering patterns for reproducibility and cost control. The cost-envelope design ($1.79/model at Haiku) and the CLI `agentfairbench run/score/cost` structure offer a concrete template for how evaluation harnesses should expose pre-flight estimation alongside execution. The arity-matched null methodology is a transferable statistical lesson for any harness that computes spread statistics over multi-condition evaluation grids.

## Tags
#benchmark #evaluation-harness #llm-agents #algorithmic-fairness #counterfactual-evaluation #multi-agent #statistical-methodology #agentic-scaffolds
