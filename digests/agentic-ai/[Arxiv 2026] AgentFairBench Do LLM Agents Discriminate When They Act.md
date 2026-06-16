---
title: "AgentFairBench: Do LLM Agents Discriminate When They Act?"
authors: ["Triveni Morla", "Rohith Reddy Bellibaltu", "Manpreet Singh", "Manmeet Singh Kapoor"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T13:50:26+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16723"
url: "http://arxiv.org/abs/2606.16723v1"
pdf: "paper/agentic-ai/[Arxiv 2026] AgentFairBench Do LLM Agents Discriminate When They Act.pdf"
---

# AgentFairBench: Do LLM Agents Discriminate When They Act?

*🕒 **Published (v1):** 2026-06-15 13:50 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16723v1)*

## TL;DR
AgentFairBench is an action-level fairness benchmark for LLM agents that measures demographic disparity across hiring, lending, and medical triage using counterfactual matched-set profiles varied only by name-coded race×gender signals under four agent scaffold depths. Its central methodological contribution is the arity-matched null: comparing a six-group score spread against a two-run pairwise noise floor overstates disparity by ~2.4× through statistic arity alone. Applied to claude-haiku-4-5 at pilot scale, zero disparity signals survive multiple-comparison correction once the correct null is used.

## Problem
Existing LLM fairness benchmarks grade *answers* (BBQ, StereoSet, CrowS-Pairs), but LLM agents now take consequential *actions* — screening applicants, approving loans, triaging patients. The Bias Conduction Framework (BCF) formalizes why token-level parity can coexist with action-level disparity (Masking, P2) and why agentic scaffolds (CoT, multi-agent, tool use) can *amplify* rather than wash out entering bias (Super-additivity, P3). No prior benchmark is simultaneously action-level, multi-domain, counterfactual, scaffold-stratified, and demographically instrumented; existing agent benchmarks (AgentBench, WebArena, SWE-bench) are capability-only with no demographic instrumentation.

## Method
**Counterfactual matched sets:** Synthetic, PHI-free profiles for three domains (hiring, lending, medical triage) are held content-constant while only a first-name/surname combination is varied across six demographic cells (White-M/F, Black-M/F, Hispanic-M/F) in the Bertrand–Mullainathan correspondence-audit tradition. White-Male is the reference group.

**Four scaffold levels (BCF entry loci):** C0 (direct prompt), C2 (chain-of-thought), C3 (two-agent deliberation: reviewer → decision agent), C4 (tool-augmented: agent may invoke an information-gathering tool before deciding).

**Metrics:** Counterfactual Flip Rate (CFR) — fraction of matched sets where the binary decision is non-unanimous across demographic conditions; Mean Absolute Score Difference (MASD) — mean over matched sets of the six-group score spread (max − min); Action-Rate Disparity — marginal positive-decision rate differences; Tool-Invocation Disparity (Δtool, C4 only) — spread in tool-invocation rate across groups.

**Statistics:** BCa bootstrap 95% CIs with matched-set resampling; McNemar exact test (binary); Wilcoxon signed-rank (scores); Benjamini–Hochberg FDR at q=0.05; arity-matched noise floor estimated via Monte-Carlo resampling of two-way (profile + group) residuals; omnibus two-way ANOVA F-test with profile blocking.

**Harness:** NumPy-only pip-installable package; cost envelope of $1.79 per model at Haiku pricing; held-out private split with cryptographic content hashes and contamination canary string.

## Key Contributions
- Multi-domain, action-level fairness benchmark with counterfactual matched-set design and scaffold axis (C0–C4), grounded in the BCF.
- NumPy-only evaluation harness implementing CFR, MASD, action-rate disparity, and Δtool with BCa bootstrap CIs, paired tests, and BH-FDR correction; pip-installable, single-digit dollars per model.
- Live leaderboard with held-out private split, contamination canary, and public submission protocol for community-contributed results.
- **Arity-matched null methodology**: demonstration that comparing a six-group score spread (MASD) against a two-run pairwise MAE overstates disparity by ~2.4×; correction via same-arity Monte-Carlo noise floor.
- Pilot on claude-haiku-4-5 (864 decisions + 648-decision test–retest replication) showing 0 of 120 pairwise and 0 of 9 omnibus contrasts survive FDR correction after arity correction; planted-bias property test confirms the instrument detects disparity when present.

## Results
- Pilot model: claude-haiku-4-5; 864 decisions (36 profiles × 6 demographic cells × 4 scaffolds).
- Test–retest decision agreement: 0.917 (≈8% binary flip rate from pure resampling noise).
- Naive MASD-to-retest-MAE ratios: 1.24–3.33×, mean ≈ 2.4× — initially read as disparity signal.
- **Arity-matched correction:** MASD-to-noise ratio is <1.0 in every C0–C3 cell: hiring 0.85/0.87/0.96, lending 0.75/0.79/0.68, triage 0.83/0.85/0.90; overall mean 0.83 — i.e., cross-demographic score spread is *smaller* than pure noise predicts.
- **0 of 120 pairwise contrasts** and **0 of 9 omnibus contrasts** survive BH-FDR correction at n=12 matched sets per cell.
- Cost envelope: $1.79 for full 864-call grid at Haiku; ~$5.38 at Sonnet-4-6; ~$8.96 at Opus-4-8.

## Limitations
- Pilot covers only one model (claude-haiku-4-5); no GPT, Gemini, or Llama results are reported in the paper itself.
- n=12 matched sets per cell provides limited statistical power; the null result cannot rule out effects in general.
- C4 test–retest reliability run was not conducted, so the arity-matched noise floor is unavailable for the tool-augmented scaffold.
- Counterfactual is a surface name-substitution (Bertrand–Mullainathan), not a structural-causal-model intervention; does not claim SCM-counterfactual guarantees.
- C1 (retrieval-augmented context injection) scaffold not instantiated in v1; deferred to v2.
- Per-component BCF disparity (Δc for each locus) not estimated; individual operator contributions left to future work.
- Private-split gaming resistance applies only to models where maintainers can re-run inference; proprietary models without shared API access receive a weaker "trace-only" verification.
- Leaderboard score (AFB-Score) is not commensurable across domains due to heterogeneous score scales.

## Relevance to Agentic AI / LLM Agents
AgentFairBench directly challenges the assumption that capability-focused agent evaluations (AgentBench, SWE-bench, WebArena) are sufficient for deployment readiness — it shows that scaffold topology (CoT, multi-agent deliberation, tool use) is itself a fairness-relevant design variable through the BCF Super-additivity proposition. The Δtool metric for tool-invocation disparity is a novel measurement axis that only exists in agentic pipelines and is invisible to any answer-grading or single-shot decision benchmark. The arity-matched null methodology is a general statistical lesson applicable to any multi-group agent evaluation. For researchers building or auditing LLM agents deployed in high-stakes domains, the benchmark provides a cheap, reproducible auditing instrument with regulatory anchoring (EEOC, ECOA, NYC LL 144).

## Tags
#benchmark #fairness #agentic-ai #counterfactual-evaluation #llm-agents #demographic-bias #evaluation-methodology #tool-use
