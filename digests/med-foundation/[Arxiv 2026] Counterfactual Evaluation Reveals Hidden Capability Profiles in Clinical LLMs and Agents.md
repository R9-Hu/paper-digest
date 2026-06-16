---
title: "Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents"
authors: ["Matt Turk"]
source: "Arxiv"
venue: ""
published: "2026-05-28"
published_time: "2026-05-28T21:37:06+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2605.30590"
url: "http://arxiv.org/abs/2605.30590v1"
pdf: "paper/med-foundation/[Arxiv 2026] Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents.pdf"
---

# Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents

*🕒 **Published (v1):** 2026-05-28 21:37 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2605.30590v1)*

## TL;DR
Standard coverage-based evaluation of clinical LLMs (checking whether outputs overlap with reference recommendations) cannot detect whether a model actually responds to changed patient facts. This paper introduces the Causal Sensitivity Score (CSS), a pre-registered counterfactual metric that mutates oncology tumor-board cases along five clinically meaningful dimensions and scores whether model recommendations update in the correct direction. Benchmarking six frontier models reveals that CSS and coverage-based rankings are nearly opposite, exposing a universal surgery-status blind spot invisible to coverage metrics.

## Problem
Coverage-based metrics (e.g., weighted recall against expert-consensus treatment lists) measure output overlap with reference answers but cannot distinguish a model that reasons from patient facts from one that produces the same recommendation regardless of input. This "look-right vs. be-right" gap is sharpened in tool-using agents, which can retrieve correct information yet still ignore it. No prior clinical LLM evaluation framework measures input responsiveness as a first-class property.

## Method
The authors define the **Causal Sensitivity Score (CSS)**: for each (model, case, intervention) triple, a baseline recommendation is generated from the unmodified patient packet, then an intervened recommendation from a mutated packet. A judge LLM (gpt-5.4 by default, claude-opus-4-7 for self-judging avoidance) scores the pair `{0.0, 0.5, 1.0}` — no change / acknowledged-but-unchanged / updated correctly — per a **pre-registered** scoring rule committed before any model is evaluated.

Interventions span five families pre-registered in a YAML catalog:
- **A** — biomarker flip (HER2/ER/PD-L1 status swap; *n*=129 eligible)
- **B** — prior treatment failure injection (*n*=269)
- **C** — biomarker strip (delete mentions; *n*=153, 80 after no-op removal)
- **D** — surgery-status toggle (resection history added/removed; *n*=306)
- **E** — stage perturbation (*n*=5, underpowered)

The cohort is 224 oncology tumor-board cases (median ~80k chars each) with expert-consensus ground-truth labels. Six frontier models are evaluated in single-shot inference and, for Family D, in a ReAct tool-using agent setting where interventions propagate through tool returns rather than the prompt. CSS is compared against the published **Consensus Match Score (CMS)**, a weighted recall: `CMS = 0.6R_strong + 0.2R_tacit + 0.15(1−V_refusal) + 0.05P_extra`.

## Key Contributions
- Pre-registered interventional metric (CSS) for clinical LLMs that measures input responsiveness rather than output coverage, with a YAML catalog committed before evaluation.
- Empirical demonstration of near-rank-reversal between CSS and CMS across six frontier models (Spearman ρ = −0.49; all six models change rank).
- Discovery of a universal Family D (surgery-status) blind spot: every frontier model scores ≤17.2% CSS on surgery-status interventions, a safety-critical failure CMS does not surface.
- Direct transfer of CSS to tool-using ReAct agents without metric modification, showing tool use lifts five of six models (+2.5 to +20.3pp) while gpt-5.4 is unchanged despite identical retrieval patterns.
- Cross-judge replication (uniform claude-opus-4-7) preserving rank order (ρ = +1.00) and three-rater medical-professional validation confirming aggregate family failure rates (Family D: LLM mean 0.10 vs. human mean 0.09).
- CSS framed as a candidate dense reward signal for future agentic RL in clinical AI.

## Results
- **CMS vs. CSS rank reversal**: grok-4.20-reasoning ranks 6th on CMS (0.480) but 1st on CSS (0.473); gpt-5 ranks 1st on CMS (0.610) but 4th on CSS (0.427); gpt-5.4 ranks 4th on CMS (0.575) but last on CSS (0.309).
- **Family D universal failure**: all six models score ≤17.2% CSS on surgery-status interventions (grok-4.20: 17.2%; gpt-5.4: 3.9%; claude-opus-4-7: 11.9%; claude-sonnet-4-6: 8.3%; gpt-5: 8.2%; gpt-5.4-mini: 14.2%).
- **Per-family capability profiles**: claude-opus-4-7 wins Family A (biomarker flip, 0.523); grok-4.20 wins Family B (prior treatment, 0.868) and Family D; gpt-5 wins Family C (biomarker strip, 0.406).
- **Agent transfer (Family D, n=100)**: tool-using CSS gains — claude-sonnet-4-6: +20.3pp (0.070→0.273, rank 4→1); gpt-5: +17.0pp; claude-opus-4-7: +12.0pp; grok-4.20: +6.0pp; gpt-5.4-mini: +2.5pp; gpt-5.4: 0.0pp (0.050→0.050). Best tool-using model still only 27.3% on Family D.
- **Score distribution (gpt-5.4)**: 59.6% wrong-direction, 21.3% correct — worst wrong-direction rate among all six models.
- **Judge robustness**: uniform-Opus replication yields identical rank order (ρ = +1.00); inter-judge κ = 0.61–0.69 on {0, 0.5, 1.0}; Opus is 4–7pp stricter, so gpt-5.4's last-place finish (already Opus-judged by default) is conservative.
- **Human validation**: LLM-vs-majority κ = 0.46 (69/100 exact agreement); per-family aggregate CSS rates agree closely (Family D LLM 0.10 vs. human 0.09).

## Limitations
- With only six models, the rank-correlation test is underpowered (permutation *p* = 0.36); rank reversal is descriptive, not inferential.
- Regex-based mutations admit three failure modes scored 0.0 under the pre-registered rule: semantic no-ops, incomplete propagation across chart sections, and medical incoherence (59% of Family D human-annotated rows flagged as incoherent, e.g., curative resection inserted into a metastatic case).
- Per-row LLM-human κ is moderate-to-low for Families C (0.07) and D (0.16); headline claims are population-level, not per-case.
- Intervention catalog authored by a single researcher; no independent clinical vetting of scoring rules at the time of publication.
- Scope limited to oncology tumor-board cases; generalization to other clinical domains requires domain-specific catalogs.
- Agent setting conflates tool-use structure, ReAct prompting, and sectioned retrieval; gpt-5.4 persistence is consistent with structural responsiveness but not proven causal.
- Family E has only *n*=5 eligible cases; no conclusions drawn.

## Relevance to Foundation Models in Medicine
CSS directly addresses the reliability gap in clinical foundation-model evaluation: that a model which memorizes treatment patterns can pass coverage benchmarks without actually processing patient-specific information, which is a critical safety concern for oncology decision support. The finding that all six frontier models — including the current strongest general-purpose LLMs — fail surgery-status interventions at near-floor rates underscores that clinical deployment readiness cannot be inferred from standard benchmarks alone. The metric's transfer to tool-using agents is particularly relevant as clinical AI increasingly adopts agentic architectures (EHR retrieval, multi-step reasoning), where the "retrieval-without-update" failure mode identified here has direct patient-safety implications. CSS's formulation as a candidate dense reward signal also connects to the emerging agenda of using RL to fine-tune clinical foundation models for reliable reasoning under patient-state change.

## Tags
#clinical-ai #evaluation-metric #counterfactual-probing #llm-agents #oncology #benchmark #causal-sensitivity #reward-signal
