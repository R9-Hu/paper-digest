---
title: "Adapting Reinforcement Learning with Chain-of-Thought Supervision for Explainable Detection of Hateful and Propagandistic Memes"
authors: ["Mohamed Bayan Kmainasi", "Mucahid Kutlu", "Ali Ezzat Shahroor", "Abul Hasnat", "Firoj Alam"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T13:51:54+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15307"
url: "http://arxiv.org/abs/2606.15307v1"
pdf: "paper/vlm/[Arxiv 2026] Adapting Reinforcement Learning with Chain-of-Thought Supervision for Explainable Detection of Hateful and Propagandistic Memes.pdf"
---

# Adapting Reinforcement Learning with Chain-of-Thought Supervision for Explainable Detection of Hateful and Propagandistic Memes

*🕒 **Published (v1):** 2026-06-13 13:51 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15307v1)*

## TL;DR
This paper applies Group Relative Policy Optimization (GRPO)-based reinforcement learning to thinking-based multimodal LLMs for hateful and propagandistic meme detection, jointly optimizing classification accuracy, explanation quality, and CoT reasoning length. A multi-stage pipeline — SFT warm-up on distilled CoT rationales, supervised GRPO with a composite reward, and self-supervised GRPO on pseudo-labeled unlabeled memes — is evaluated on English (FHM) and Arabic (ArMeme) benchmarks. The method improves macro-F1 substantially while simultaneously generating natural-language explanations.

## Problem
Thinking-based MLLMs have not been systematically applied to subjective, culturally situated tasks like meme content moderation. Standard SFT provides no structured control over the balance between classification correctness, explanation faithfulness, and reasoning trace quality. Additionally, GRPO-based post-training for multimodal classification had not been studied across cross-lingual, fine-grained annotation, or self-supervised settings.

## Method
Three-stage post-training pipeline on Qwen3-VL-8B-Thinking:

1. **SFT warm-up**: Fine-tune on gold labels, GPT-4.1-distilled CoT traces (in `<think></think>` tags), and human-verified explanations. Three ablation variants: classification+explanation only; +fine-grained labels (protected categories/propaganda techniques); +distilled CoT.

2. **Supervised GRPO**: Composite reward R = α_fmt·R_fmt + α_lbl·R_lbl + α_exp·R_exp + α_think·R_think + α_met·R_met. R_think enforces a minimum CoT length (L_min=150 tokens) via a one-sided penalty to prevent reward hacking (empty thinking traces) without promoting verbosity. R_met uses METEOR against reference explanations. Weights set empirically: α_fmt=0.35, α_lbl=0.35, α_exp=0.08, α_met=0.12, α_think=0.10. K=16 candidates per input; group-relative advantage normalization.

3. **Self-supervised GRPO**: Initialized from the best supervised checkpoint; pseudo-labels derived via majority vote over K stochastic rollouts at five temperatures {0, 0.2, 0.4, 0.8, 1.0}. Only disagreement samples (3/5 or 4/5 agreement) are retained (2,000 per dataset), providing informative gradient signal. Consensus reward replaces R_lbl.

For ArMeme, fine-grained propaganda annotations (23 techniques) are generated via dual-annotator LLM pipeline (GPT-4.1 + Llama-4-Scout) consolidated by Gemini-3-Pro; human-LLM agreement Gwet's AC1 = 0.77.

## Key Contributions
- First systematic study of GRPO for multimodal meme detection across cross-lingual (English/Arabic), fine-grained, and self-supervised settings.
- Thinking-length reward R_think that penalizes empty/short CoT traces without rewarding verbosity, mitigating reward hacking.
- Multi-LLM dual-annotator pipeline to construct fine-grained Arabic propaganda labels (23 techniques) from scratch.
- Self-supervised GRPO via disagreement-based hard-sample selection and consensus pseudo-labeling, enabling RL without human annotations.
- Data/code/evaluation resources released publicly.

## Results
- **FHM (Hateful Memes)**: Supervised GRPO achieves 82.0% accuracy / 0.80 macro-F1, up from 79.9% (prior best [43]); +2.1pp accuracy. Self-supervised GRPO: 81.8% / 0.79 M-F1 (slight drop vs. supervised).
- **ArMeme**: Self-supervised GRPO achieves 0.612 macro-F1, up from 0.536 ([43]) and 0.551 ([5]), gains of +7.6 and +6.1 points respectively. Outperforms Qwen3-VL-8B-Instruct sequence-classifier (0.594 M-F1) while also generating explanations. Accuracy (72.8%) remains below seq-cls baselines (up to 76.6%).
- **Fine-grained SFT ablation**: Adding fine-grained labels lifts SFT macro-F1 from 0.43→0.51 on ArMeme (+8.0pp), 0.75→0.77 on FHM.
- **CoT distillation ablation**: Adds +0.01 M-F1 on FHM (0.77→0.78) and +0.03 on ArMeme (0.51→0.54) over fine-grained SFT.
- **GRPO over SFT**: Brings ArMeme to 0.597 from 0.54 (SFT+CoTD), FHM to 0.80 from 0.78.
- **Self-supervised GRPO on FHM**: Drops macro-F1 by 1.0 point vs. supervised, attributed to distribution mismatch in the unlabeled pool.

## Limitations
- Self-supervised GRPO degrades on FHM, likely due to unlabeled pool aggregated from heterogeneous English meme datasets with distributional mismatch.
- Sequence-classification baselines (no explanation) retain higher raw accuracy on ArMeme (76.6% vs. 72.8%), indicating a trade-off between generative explanation and peak accuracy.
- Arabic meme collection required semi-manual social media crawling due to absent APIs; coverage may be non-representative.
- Thinking-length reward is a proxy for reasoning quality; it cannot guarantee semantic validity of CoT traces.
- Results reported from a single random seed (42); variance across seeds is not characterized.
- Models trained with visual encoder frozen; joint fine-tuning may yield further gains.

## Relevance to Vision-Language Models
This work directly advances the application of thinking-based MLLMs (e.g., Qwen3-VL with explicit `<think>` traces) to subjective, cross-modal reasoning tasks where neither image nor text alone is sufficient. The GRPO-based composite reward framework — particularly the thinking-length regularizer preventing CoT collapse — is a transferable technique for any VLM task requiring joint classification and explanation. The finding that fine-grained annotation and CoT distillation stack additively with RL rewards informs multi-stage post-training recipes for VLMs in low-resource or culturally specific domains. The self-supervised extension via consensus pseudo-labeling offers a practical path for adapting VLMs to new moderation tasks without annotation.

## Tags
#vlm #multimodal-llm #reinforcement-learning #grpo #chain-of-thought #meme-detection #content-moderation #explainability
