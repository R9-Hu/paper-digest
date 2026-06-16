---
title: "MoodAngels: A Retrieval-augmented Multi-agent Framework for Psychiatry Diagnosis"
authors: ["Mengxi Xiao", "Ben Liu", "He Li", "Jimin Huang", "Qianqian Xie", "Xiaofen Zong", "Mang Ye", "Min Peng"]
source: "NeurIPS"
venue: "NeurIPS 2025"
published: "2025-01-01"
year: 2025
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "openreview:AWU93F6Bup"
url: "https://openreview.net/forum?id=AWU93F6Bup"
pdf: "paper/harness/[NeurIPS 2025] MoodAngels A Retrieval-augmented Multi-agent Framework for Psychiatry Diagnosis.pdf"
---

# MoodAngels: A Retrieval-augmented Multi-agent Framework for Psychiatry Diagnosis

## TL;DR
MoodAngels is a retrieval-augmented multi-agent framework for mood disorder diagnosis that decomposes psychiatric scale assessments into item-level granular analysis and orchestrates three specialized diagnostic agents through a structured debate mechanism. It outperforms GPT-4o by 12.3% accuracy on 561 real-world clinical cases. The authors also release MoodSyn, a 1,173-case synthetic dataset generated via diffusion-based tabular synthesis to bypass patient-privacy constraints.

## Problem
Psychiatric diagnosis lacks objective biomarkers, suffers from symptom overlap across disorders, and depends on subjective self-reports that may conflict with clinician-evaluated scales. Existing LLM-based medical agents are trained on structured clinical evidence (lab results, imaging) unavailable in psychiatry, and clinical datasets cannot be shared publicly due to patient privacy.

## Method
MoodAngels wraps a backbone LLM (GPT-4o or DeepSeek-V3) in a three-layer pipeline:

1. **Granular-Scale Analysis** — Pearson correlation across 13 clinical scales selects the top-5% questions most predictive of mood disorder, grouping them into five symptom clusters (depressive mood, loss of interest, anxiety, insomnia, suicidal tendencies). Numeric scores are converted to narrative text for better agent interpretability.
2. **RAG Knowledge Base** — DSM-5 differential criteria are encoded with BGE-M3 embeddings and retrieved via dense similarity search; anonymized historical cases (2,243 total, 80% used as retrieval store) are also indexed for case-based reasoning.
3. **Three Diagnostic Agents + Debate Judge** — Angel.R (no case reference), Angel.D (retrieved cases displayed as context), and Angel.C (retrieved cases compared analytically) each produce independent diagnoses. If they disagree, Positive and Negative Debate Agents argue, and a Judge Agent terminates debate and renders a final verdict.

MoodSyn is built using TabSyn (VAE + score-based diffusion in latent space) with dynamic loss weighting to preserve intra-scale score consistency during synthesis.

## Key Contributions
- First multi-agent framework purpose-built for mood disorder (depression, bipolar) diagnosis, tackling symptom overlap and subjective scale reliability.
- Granular item-level scale analysis via Pearson-selected top-5% questions, replacing aggregate total-score inputs.
- Three-agent architecture with graduated reliance on historical cases, synthesized via a multi-round debate-and-judge mechanism.
- MoodSyn: open-source 1,173-case synthetic psychiatric dataset with verified statistical fidelity, ML utility, and privacy guarantees stronger than anonymization.

## Results
Real-world test set (561 cases):
- Angel.R (GPT-4o): ACC 0.920, MCC 0.829 — +12.3% ACC over bare GPT-4o (0.797)
- multi-Angels (GPT-4o): ACC 0.925, MCC 0.841 — best overall on real data
- multi-Angels (DeepSeek-V3): ACC 0.923, MCC 0.832
- Baseline GPT-4o (in-context only): ACC 0.797, MCC 0.792
- Baseline DeepSeek-V3: ACC 0.847, MCC 0.841

Ablation (Angel.R, real data):
- Using unfiltered total scores (13 scales) vs. 16 selected questions: ACC drops 6.8% (0.920 → 0.852), MCC drops 0.121
- Structured vs. narrative medical record format returned to agent: ACC drops 0.006 (0.920 → 0.914)

Synthetic data (MoodSyn, 140 cases, DeepSeek-V3 agents):
- multi-Angels: ACC 0.821, MCC 0.642 vs. DeepSeek-V3 baseline ACC 0.821, MCC 0.601

## Limitations
- Input restricted to scale scores and medical records; full clinical diagnosis involves ~1 hour of live patient interview plus real-time clinician judgments not capturable from records alone.
- Borderline cases (mild, sub-threshold symptoms) remain difficult; agents cannot reliably distinguish borderline-normal from mild disorder.
- Record-scale conflicts caused by remission or medication suppression of symptoms are flagged but not reliably resolved.
- Evaluation on a single hospital's dataset limits generalizability across clinical settings and demographics.

## Relevance to Harnesses / Meta-Harnesses
MoodAngels is a domain-specific instantiation of the multi-agent harness pattern: it coordinates heterogeneous specialist agents (Angel.R/D/C), a retrieval subsystem, and a judge/debate orchestrator within a fixed control flow. The structured debate-and-judge mechanism is a concrete implementation of adversarial verification — a harness-level construct that runs multiple agents, detects disagreement, and routes to a resolution sub-pipeline rather than trusting any single agent's output. The ablation design (isolating scale selection vs. record format vs. case retrieval) mirrors harness-level component analysis, making this a useful case study in how domain-specific orchestration choices (graduated RAG reliance, item-level feature engineering) interact with agent coordination quality.

## Tags
#multi-agent #rag #psychiatry #clinical-diagnosis #debate-mechanism #synthetic-data #llm-agent #domain-specific-harness
