---
title: "Trust but Verify: Mitigating Medical Hallucinations via Post-Hoc Adversarial Auditing and Multi-Agent Feedback Loops"
authors: ["Muhammad Osama", "Maheera Amjad", "Zartasha Mustansar", "Arslan Shaukat", "Muhammad U. S. Khan"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T06:21:19+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14149"
url: "http://arxiv.org/abs/2606.14149v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Trust but Verify Mitigating Medical Hallucinations via Post-Hoc Adversarial Auditing and Multi-Agent Feedback Loops.pdf"
---

# Trust but Verify: Mitigating Medical Hallucinations via Post-Hoc Adversarial Auditing and Multi-Agent Feedback Loops

*🕒 **Published (v1):** 2026-06-12 06:21 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14149v1)*

## TL;DR
This paper proposes "Trust but Verify," a five-agent pipeline that performs post-hoc adversarial auditing against real-time regulatory databases to prevent LLMs from recommending banned or withdrawn pharmaceuticals. Using a 103-question adversarial MCQ benchmark (BannedDrug-Bench), the system reduces Hallucination Error Rate (HER) by ~53% across five open-access models compared to vanilla single-shot inference. The key insight is that even SOTA models with native RAG fail this task because parametric knowledge overrides retrieved safety signals.

## Problem
LLMs trained on historical data systematically recommend pharmaceuticals that have since been withdrawn or banned (e.g., rofecoxib, valdecoxib), a failure mode called *regulatory knowledge obsolescence*. Existing mitigations—RAG, self-reflection, and semantic guardrails—are insufficient: SOTA proprietary models (GPT-5.1, GPT-5.3, Gemini 3 Flash, Gemini 3.1 Pro) with native browsing still select banned drugs because parametric memory overrides retrieved withdrawal notices.

## Method
A five-agent pipeline built on a **single LLM backbone** with prompt-based persona redirection:

1. **Router Agent** — classifies queries as MEDICAL or GENERAL; bypasses the audit loop for non-clinical queries.
2. **Medical Clinical Agent** — generates a candidate drug recommendation; on retry, receives a list of banned entities from the auditor and must exclude them.
3. **Entity Extractor Agent** — parses the clinical recommendation into structured JSON `{treatment, condition}`.
4. **Safety Auditor Agent** — performs real-time web search (Tavily API, targeting FDA/NIH/DrugBank) on the extracted entities; emits a `{status: SAFE|UNSAFE, reason}` verdict.
5. **General Chat Agent** — handles non-medical queries.

The feedback loop allows up to **three retry attempts**: if the auditor flags a drug as BANNED, the clinical agent must select a different option or issue a safe refusal ("no safe option exists"). Safety is treated as a deterministic state machine—output is authorized only when auditor verdict is SAFE.

**Dataset:** 103 adversarial MCQs from DrugBank where the clinically plausible correct answer is always a withdrawn/banned substance (97 unique drugs). Temperature = 0.1 for all inferences via NVIDIA NIM API.

**Metrics:** Accuracy (label match), Pointwise Score (PS; +1 correct, 0 refusal, −0.25 hallucination), Hallucination Error Rate (HER), Component Fidelity (CF; ratio of successful agent invocations).

## Key Contributions
- Introduces **BannedDrug-Bench**: 103 adversarial clinical MCQs specifically targeting regulatory knowledge obsolescence (publicly released on HuggingFace).
- Proposes a **model-agnostic, single-backbone** five-agent adversarial audit architecture requiring no retraining or parameter expansion.
- Demonstrates that **SOTA proprietary models with native RAG** (GPT-5.1/5.3, Gemini 3/3.1 Pro) still fail to suppress banned-drug recommendations, establishing the inadequacy of retrieval alone.
- Introduces the **Component Fidelity (CF) score** as a structural reliability metric for multi-agent pipeline evaluation.
- Separates high-stakes clinical routing from general queries to control inference latency and token cost.

## Results
All figures from Table II and text:

- **Vanilla HER:** 90.29%–99.03% across all five models (near-maximum penalty).
- **Vanilla Pointwise Score:** ~−0.24 to −0.22 (approaching maximum penalty of −0.25) for all models.
- **Agentic HER:** 35.92%–40.78%; reduction of ~53–61 percentage points per model.
  - meta/llama3-70b-instruct: 99.03% → 37.86% (−61.17 pp)
  - tiiuae/falcon3-7b-instruct: 99.03% → 35.92%
  - openai/gpt-oss-120b: 94.17% → 40.78%
  - openai/gpt-oss-20b: 90.29% → 35.92%
  - meta/llama3-8b-instruct: 98.06% → 38.83%
- **Agentic Pointwise Score:** −0.08 to −0.10 (shifted toward safe-refusal baseline of 0.0).
- **Component Fidelity:** 73.82%–85.71% across agentic models (openai/gpt-oss-120b highest at 85.71%).
- **Accuracy drop** in agentic mode is intentional: dangerous correct-label selections converted to refusals (e.g., llama3-70b: 97.09% → 33.98%).
- SOTA proprietary models (Experiment III) all selected banned drugs despite having real-time search enabled.

## Limitations
- Dataset is small (103 MCQs) and structured (MCQ format only); does not capture free-text patient queries or multi-morbid scenarios.
- Proprietary models (GPT-5.x, Gemini 3.x) not evaluated on the full 103-question benchmark due to resource/access constraints; only qualitative Experiment III observations provided.
- DrugBank-derived expert-validated dataset does not substitute for real clinical field testing.
- Sequential feedback loop introduces inference latency; not benchmarked quantitatively.
- CF scores of 73–85% indicate non-trivial agent invocation failures, but failure modes are not analyzed in detail.
- Single LLM backbone means persona redirection via prompts; no true heterogeneous agent diversity.

## Relevance to Agentic AI / LLM Agents
This work is a concrete instantiation of the post-hoc adversarial verification pattern for safety-critical agentic systems: rather than relying on a model's parametric knowledge or passive RAG retrieval, it inserts an independent auditor agent that can veto and trigger correction loops. The finding that SOTA models with native RAG still fail the task is important for anyone designing medical or compliance-sensitive agents—it shows that retrieval integration at the generation level is insufficient without a separate, deterministic verification step. The five-agent decomposition with a router, a clinical reasoner, an extractor, an auditor, and a fallback handler is a reusable architectural pattern for any domain where regulatory or factual currency matters. The CF score also offers a practical metric for evaluating structural reliability in multi-agent pipelines beyond task-level accuracy.

## Tags
#multi-agent #hallucination-mitigation #healthcare-ai #adversarial-auditing #rag #safety #regulatory-compliance #clinical-decision-support
