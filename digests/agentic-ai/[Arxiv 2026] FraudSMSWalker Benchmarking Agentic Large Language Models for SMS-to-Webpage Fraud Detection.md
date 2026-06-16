---
title: "FraudSMSWalker: Benchmarking Agentic Large Language Models for SMS-to-Webpage Fraud Detection"
authors: ["Y. H. Zhou", "Z. M. Ma", "Y. J. Zhou", "Y. T. Li", "H. X. Xiang", "Y. M. Cheng", "T. L. Chen", "K. J. Zhang", "Z. H. Nan", "J. H. Ni", "Z. Wu", "Q. Y. Pan", "S. Zhang", "S. Cheng", "M. Y. Luo"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T12:53:55+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16659"
url: "http://arxiv.org/abs/2606.16659v1"
pdf: "paper/agentic-ai/[Arxiv 2026] FraudSMSWalker Benchmarking Agentic Large Language Models for SMS-to-Webpage Fraud Detection.pdf"
---

# FraudSMSWalker: Benchmarking Agentic Large Language Models for SMS-to-Webpage Fraud Detection

*🕒 **Published (v1):** 2026-06-15 12:53 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16659v1)*

## TL;DR
FraudSMSWalker is a controlled benchmark of 699 bilingual SMS-to-webpage chains for evaluating whether LLM web agents can detect fraud from content evidence alone, without URL or domain reputation shortcuts. Evaluation of nine agents reveals a universal failure mode: high fraud recall but catastrophically low benign recall, plus weak evidential grounding of positive predictions.

## Problem
Existing smishing benchmarks test message classification in isolation; phishing/web-agent benchmarks expose raw URLs or domains, allowing models to shortcut on reputation signals rather than reasoning over the SMS–webpage evidence chain. No prior benchmark isolates whether agents can make sound fraud judgments from visible content when all location and reputation cues are withheld.

## Method
Each instance pairs a real-world SMS message (URL replaced with a fixed placeholder) with sanitized webpage evidence (title, visible text, form signals—no raw URLs, hosts, IPs, redirects, or reputation metadata). The task is binary chain-level fraud judgment: does the combined SMS claim + webpage interaction constitute a deceptive flow? Hard benign cases are explicitly included—pages with login forms, payment widgets, and verification steps that are legitimate within the stated service context but visually resemble scam flows. Nine web agents are run under a masked browser-agent protocol (live-page access, URL-masked observations). Evaluation uses: (1) binary accuracy/precision/recall; (2) an LLM-as-Judge evidence-support audit that checks whether the agent's interaction trajectory actually supports its conclusion (not whether the label is correct). A 2×2 ablation (agent vs. text-only × URL-masked vs. URL-visible) disentangles browser interaction from URL shortcutting.

## Key Contributions
- Formulates URL-masked SMS-to-webpage fraud judgment as a distinct benchmark task separating visible content evidence from reputation shortcuts.
- Constructs FraudSMSWalker: 699 bilingual (381 Chinese, 318 English) chains across 10 service scenarios with hard benign cases; human audit achieves 96% inter-annotator agreement and κ=0.92.
- Introduces an LLM-as-Judge evidence-support audit (validated against human reviewers at 91% agreement, κ=0.82) that distinguishes correct-and-supported from correct-but-unsupported predictions.
- Evaluates 9 frontier web agents (Qwen3.6-Plus, GPT-5.5, DeepSeek-V4-Pro, Claude Sonnet 4.6 Thinking, Gemini 3.1 Flash Lite, etc.) under masked conditions with URL-visibility ablations.

## Results
- **Overall accuracy**: All nine agents cluster near the 52.5% always-benign baseline; best is Qwen3.6-Plus at 50.93%, worst is Claude Sonnet 4.6 Thinking at 42.06%.
- **Fraud recall vs. benign recall**: Fraud recall ranges 64–90%; benign recall ranges 12.81%–30.25%—a near-total collapse in false-positive control.
- **Evidence support rate**: 9.59%–32.19% of predictions pass the full evidence-support audit; even the best (GPT-5.5 at 32.19%) fails on >2/3 of cases.
- **Unsupported-YES rate**: 8 of 9 agents exceed 63% unsupported positive predictions; Doubao-Seed-2.0-pro peaks at 85.26%.
- **Forbidden URL-style reasoning persists** even under masking: most agents 42–55%; Gemini and GPT-5.5 lower at ~26–29%.
- **URL-visibility ablation (Qwen3.6-Plus, snapshot setting)**: Revealing URLs raises fraud recall from 29.82% → 75.90% but collapses benign recall from 83.11% → 26.16%, confirming that URL cues drive the fraud–benign operating point rather than genuine reasoning.

## Limitations
- Benchmark is controlled (not a natural SMS traffic sample); SMS redaction may reduce linguistic diversity relative to verbatim corpora.
- Live-page mode introduces temporal drift as pages disappear or redirect.
- Residual stylistic cues may survive URL masking.
- Evidence-support audit is judge-based; human validation covers a stratified subset but is not a full replacement for expert security review.

## Relevance to Agentic AI / LLM Agents
This benchmark directly stress-tests the safety-critical judgment capacity of web agents by removing the reputation shortcuts on which deployed systems rely—forcing agents to reason over cross-modal, multi-step evidence chains. The finding that correct labels are overwhelmingly unsupported by trajectory evidence (correct-but-unsupported dominating every agent) is a sharp diagnostic for a known failure mode of agentic systems: achieving correct outputs through brittle heuristics rather than grounded reasoning. For the broader agentic-AI community, FraudSMSWalker establishes that benign recall and evidence-grounded decision-making—not raw task accuracy—should be the primary evaluation axes for agents operating in adversarial real-world environments.

## Tags
#benchmark #web-agents #fraud-detection #safety #evidence-grounding #evaluation #llm-judge #multimodal
