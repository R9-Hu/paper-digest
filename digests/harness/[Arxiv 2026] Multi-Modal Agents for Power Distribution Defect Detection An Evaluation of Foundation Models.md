---
title: "Multi-Modal Agents for Power Distribution Defect Detection: An Evaluation of Foundation Models"
authors: ["Quan Quan"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T06:57:01+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12969"
url: "http://arxiv.org/abs/2606.12969v1"
pdf: "paper/harness/[Arxiv 2026] Multi-Modal Agents for Power Distribution Defect Detection An Evaluation of Foundation Models.pdf"
---

# Multi-Modal Agents for Power Distribution Defect Detection: An Evaluation of Foundation Models

*🕒 **Published (v1):** 2026-06-11 06:57 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.12969v1)*

## TL;DR
This paper proposes a multi-modal agent framework for autonomous power distribution inspection and systematically benchmarks foundation models across three capability tiers: perception (defect identification and description), reasoning (RAG-augmented severity grading and maintenance planning), and tool usage (closed-loop work-order generation via ReAct). On a private 26,803-image dataset covering 10 equipment and 31 defect categories, zero-shot accuracy is below 10% for all tested models, with RAG and few-shot exemplars substantially closing the gap.

## Problem
General-purpose VLMs lack fine-grained recognition of domain-specific industrial equipment, cannot generalize to rare defect categories in long-tail distributions, and cannot autonomously trigger maintenance workflows (the "information silo" problem). No prior benchmark existed to evaluate foundation models jointly across perception, reasoning, and executable tool use in high-stakes power infrastructure inspection.

## Method
A single foundation model serves as the unified cognitive engine for all three stages. **Perception** uses vision-language alignment to produce semantic defect descriptions rather than discrete labels. **Reasoning** is augmented via RAG over two domain knowledge bases ("Power Equipment Defect Rating Standards" and a "Historical Defect Case Library"), retrieved at inference time to ground severity grading in regulatory standards. **Tool usage** is implemented via the ReAct architecture, with the model selecting from four fixed APIs (`get_camera_image`, `search_knowledgebase`, `write_report`, `send_alert`) and generating JSON arguments. Prompt engineering includes role specification, a closed vocabulary of valid equipment/defect labels (to reduce hallucination), and optional few-shot image-text exemplars retrieved by cosine similarity. Evaluated models: GLM-4.5V (with and without thinking), Qwen2.5-VL-32B, Qwen3-VL-30B, LLaVA-1.5, DeepSeek-VL2, Gemma3-4B/12B/27B, and Step3.

## Key Contributions
- Three-dimensional evaluation framework (perception / reasoning / tool use) for multimodal agents in industrial inspection
- Domain-specific benchmark: 26,803 annotated drone/field images, 10 equipment categories, 31 defect categories, long-tail distribution deliberately preserved
- Empirical comparison of 9 foundation models under 0-shot, 1-shot, and 5-shot RAG with text-only vs. multimodal exemplars
- Failure taxonomy for agent tool-chain execution (hallucinated sub-tasks, duplicated actions, cascading failures, invalid arguments)

## Results
- **Zero-shot recognition**: All models below 10% accuracy for both equipment and defects; model scale alone shows no significant improvement without domain knowledge.
- **5-shot RAG (best model, GLM-4.5V)**: Equipment Acc 54.39%, Defect Acc 37.52%; F1 ~53–55% equipment, ~55–56% defect.
- **Text-only vs. multimodal exemplars (5-shot, DeepSeek-VL2)**: Adding images raises equipment Acc by +2.05% but drops equipment Recall/F1/Prec; for defects, Recall +5% and F1 +6.5% but Acc −0.64% — no uniformly dominant modality.
- **Conditional grading accuracy** (given correct defect): GLM-4.5V-thinking 93.02%, Qwen3-VL-30B 91.68%, Step3 91.02%; unconditional grading 31–43%.
- **Tool use (function-call-supported models)**: Step3 — tool accuracy 70.83%, argument accuracy 80.42%, task success 42.92%; GLM-4.5V — 79.58% tool, 78.75% arg, 30% task success.
- **Tool use (no function-call support)**: Gemma3-12b task success 3.4%; Qwen2.5-VL-32B 10%.

## Limitations
- Dataset is private and not released; results are not reproducible externally.
- No frontier proprietary models (GPT-4V, Claude, Gemini) tested due to data-security constraints.
- Cascading tool-chain failures are a systemic bottleneck with no mitigation beyond better base models.
- Task decomposition hallucinations (invented sub-areas) are frequent and unaddressed at the architectural level.
- RAG exemplar pool capped at 10 per category; gains plateau before this limit, leaving rare-category performance unresolved.
- No instruction tuning; full reliance on prompt engineering and retrieval for domain adaptation.

## Relevance to Harnesses / Meta-Harnesses
This paper instantiates a domain-specific agent harness with a fixed three-stage pipeline (input parsing → task decomposition → tool invocation) and a standardized API surface, which is precisely the scaffolding structure meta-harness research seeks to generalize. The failure taxonomy — hallucinated sub-tasks, duplicate actions, cascading dependency failures, argument mismatches — provides concrete empirical evidence for where harness scaffolding must compensate for foundation model weaknesses rather than deferring to the model. The RAG module embedded within the reasoning stage illustrates how harnesses compose retrieval sub-systems to augment model cognition, a pattern directly relevant to recursive or modular harness design. The evaluation protocol itself (per-capability metric decomposition, LLM-as-judge for toolchain coherence) demonstrates reproducible harness evaluation methodology applicable to meta-harness benchmarking.

## Tags
#multimodal-agent #vlm #tool-use #rag #industrial-inspection #benchmark #react #evaluation
