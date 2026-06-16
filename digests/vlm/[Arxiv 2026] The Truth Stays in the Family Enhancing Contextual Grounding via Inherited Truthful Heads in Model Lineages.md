---
title: "The Truth Stays in the Family: Enhancing Contextual Grounding via Inherited Truthful Heads in Model Lineages"
authors: ["Miso Choi", "Seonga Choi", "Mincheol Kwon", "Woosung Joung", "Jinkyu Kim", "Jungbeom Lee"]
source: "Arxiv"
venue: "ICML 2026"
published: "2026-06-14"
published_time: "2026-06-14T13:39:09+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15821"
url: "http://arxiv.org/abs/2606.15821v1"
pdf: "paper/vlm/[Arxiv 2026] The Truth Stays in the Family Enhancing Contextual Grounding via Inherited Truthful Heads in Model Lineages.pdf"
---

# The Truth Stays in the Family: Enhancing Contextual Grounding via Inherited Truthful Heads in Model Lineages

*🕒 **Published (v1):** 2026-06-14 13:39 UTC  ·  **Source:** Arxiv  ·  **Venue:** ICML 2026  ·  [link](http://arxiv.org/abs/2606.15821v1)*

## TL;DR
This paper discovers that attention heads specialized for context-grounded truthfulness ("Truth Scores") are strongly inherited from base LLMs to their fine-tuned multimodal descendants, explained by minimal parameter drift during fine-tuning. Building on this, the authors propose TruthProbe, a soft-gating mechanism that reweights head contributions proportional to their Truth Scores, reducing hallucination across both LLMs and MLLMs without any architectural changes or retraining.

## Problem
Existing hallucination-mitigation methods treat each model in isolation, ignoring that most deployed MLLMs (e.g., LLaVA variants, Qwen2.5-VL) share a foundational base LLM. Whether base-model behavioral properties—specifically, which attention heads faithfully ground responses in the provided context—persist through fine-tuning and multimodal adaptation is unknown. This gap prevents systemic, family-level reliability improvements.

## Method
**Truth Score measurement:** For each attention head, a linear binary probe is trained on activations at the final answer token to classify whether the head output reflects context-faithful (truthful) vs. hallucinated responses, given input structured as {context, question, answer}. Validation accuracy of this probe is the head's Truth Score.

**Inheritance analysis:** Truth Score distributions are compared across model families (Vicuna-7B → LLaVA-1.5/LLaVA-NeXT; Qwen2.5 → Qwen2.5-VL-Instruct/Qwen2.5-VL-Omni) using Pearson correlation, both with matched and mismatched probing datasets/modalities. Layer-wise Frobenius norm of weight differences quantifies parameter drift.

**TruthProbe soft gating:** At each Transformer layer $l$, the output of each attention head $h$ is scaled before the residual addition:
$$x^{l+1} = x^l + \text{Concat}_{h=1}^{H}(g_h^l \cdot o_h^l), \quad g_h^l = 1 + \lambda \cdot \text{norm}(S)$$
where $S$ is the head's Truth Score. This amplifies high-truthfulness heads while preserving all heads' contributions. Truth Scores from the base LLM are applied directly ("plug-and-play") to downstream MLLMs without re-probing.

## Key Contributions
- Defines head-level Context-Truthfulness Scores (Truth Scores) via linear probing on final-token activations.
- Demonstrates strong within-family correlation of Truth Scores (0.77–0.98 single-dataset; 0.51–0.64 cross-dataset) versus near-zero cross-family correlation (0.04–0.08 for Vicuna vs. Mistral).
- Provides mechanistic evidence: within-family attention-head weight drift (Frobenius norm ≈ 0.03) is ~34× smaller than cross-family drift (≈ 1.01), explaining score inheritance.
- Shows that high-Truth-Score heads attend to query-relevant image regions (query-dependent, spatially selective), while low-Truth-Score heads exhibit positional/structural attention patterns.
- Proposes TruthProbe, a lightweight inference-time soft gate transferable from base LLM to all family descendants.

## Results
**HaluEval (LLM validation):**
- Vicuna-7B: F1 13.37 → 29.15 (+TruthProbe on itself)
- Qwen2.5: Acc 27.65 → 35.04, F1 36.69 → 46.54
- Vicuna-7B with LLaMA2-7B base scores (transfer): Acc 38.89 → 48.47, F1 13.37 → 57.17 (surpasses self-probing)

**POPE (multimodal object-presence, MLLM transfer):**
- LLaVA-1.5 A-OKVQA Acc: 87.8 → 90.1 (TruthProbeLLM), 89.0 (TruthProbeMLLM)
- LLaVA-NeXT A-OKVQA Acc: 86.8 → 89.7 (TruthProbeLLM), 89.5 (TruthProbeMLLM)
- Qwen2.5-VL-Omni A-OKVQA Acc: 84.7 → 87.1 (TruthProbeLLM)

**CHAIR (image captioning hallucination, lower is better):**
- LLaVA-1.5: CHAIR_I 6.99 → 5.36, CHAIR_S 23.00 → 17.40 (TruthProbeLLM)
- LLaVA-NeXT: CHAIR_I 6.91 → 4.94, CHAIR_S 13.40 → 11.20 (TruthProbeLLM)
- TruthProbeLLM generally matches or outperforms TruthProbeMLLM, confirming transferability.

## Limitations
- Does not fully eliminate hallucinations; cautions against high-stakes deployment without human oversight.
- Normalization method for $\lambda$ must be tuned per benchmark (centered normalization for HaluEval/CHAIR, min-max for POPE), introducing a hyperparameter dependency.
- Small regression observed in some configurations (e.g., LLaVA-1.5 POPE COCO Acc: 86.9 → 86.7 with TruthProbeLLM; Qwen2.5-VL-Omni CHAIR_I slightly worsens with TruthProbeLLM).
- Probing requires a labeled subset of truthfulness data (292 samples for LLMs, 2,726 for MLLMs), though modest.
- Evaluated on a limited set of benchmarks; broader generalization (e.g., to open-ended VQA or dense captioning) is not demonstrated in the main text.
- Analysis focused on 7B-scale models; scalability to larger models is deferred to the Appendix.

## Relevance to Vision-Language Models
This paper directly addresses multimodal hallucination in VLMs by revealing that the truthfulness structure of a base LLM's attention heads is preserved after visual instruction tuning—a finding with practical consequence: one need only probe the base LLM (cheaper, text-only) to obtain soft gates that improve MLLM reliability. The attention-overlay analysis provides mechanistic grounding for *why* certain heads matter in VLMs—they attend to query-relevant image regions rather than exhibiting positional artifacts—connecting to the broader interpretability literature on visual grounding in cross-modal attention. For researchers tracking VLMs, TruthProbe offers a training-free, plug-and-play complement to training-based debiasing methods (DPO, RLHF), and the lineage-based transfer paradigm suggests that base-model quality is a persistent determinant of downstream MLLM reliability.

## Tags
#hallucination #attention-heads #vlm #mllm #mechanistic-interpretability #inference-time-intervention #truthfulness #model-lineage
