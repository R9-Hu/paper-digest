---
title: "Zero-Shot Captioning for Cultural Heritage: Automated Image Analysis of Traditional Indonesian Clothing"
authors: ["Anugrah Aidin Yotolembah", "Novanto Yudistira", "Gembong Edhi Setyawan"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13275"
url: "http://arxiv.org/abs/2606.13275v1"
pdf: "paper/vlm/[Arxiv 2026] Zero-Shot Captioning for Cultural Heritage Automated Image Analysis of Traditional Indonesian Clothing.pdf"
---

# Zero-Shot Captioning for Cultural Heritage: Automated Image Analysis of Traditional Indonesian Clothing

## TL;DR
Custom ZeroCLIP is a retrieval-augmented vision-language framework for inductive zero-shot captioning of traditional Indonesian garments across all 38 provinces. It combines frozen CLIP encoders with a trainable BERT–LSTM decoder that conditions generation on cosine-retrieved captions from seen provinces. On 8 fully unseen provinces it achieves CLIPScore 0.8536, BLEU-4 0.3342, and METEOR 0.4859, outperforming off-the-shelf VLM baselines.

## Problem
General-purpose VLMs (CLIP, BLIP, InstructBLIP) fail to generate province-specific cultural terminology for Indonesian traditional garments because their Western-centric pretraining data lacks fine-grained heritage vocabulary. No prior dataset covers all 38 Indonesian provinces, and existing approaches treat this as recognition rather than cultural-meaning reconstruction under a strict inductive zero-shot constraint.

## Method
The system uses a frozen CLIP ViT-B/32 image encoder to embed test images and a frozen CLIP text encoder to pre-encode all training-split captions into a retrieval bank. At inference, cosine similarity retrieves the top-K=5 culturally proximate captions from the seen-province bank. A trainable BERT encoder mean-pools the K retrieved caption embeddings into a context vector, which is fused with the frozen CLIP visual embedding via learnable projection layers (z = W_v·v + W_t·ē). An LSTM autoregressive decoder then generates the caption conditioned on z. Only BERT, projection layers, and LSTM are trained (AdamW, lr=2×10⁻⁵, 100 epochs); CLIP is frozen throughout to prevent catastrophic forgetting. The province-level inductive protocol strictly excludes all images, labels, and captions from the 8 unseen test provinces during training, validation, and retrieval-bank construction.

## Key Contributions
- **Custom ZeroCLIP**: a RAG-based BERT–LSTM decoder architecture grafted onto frozen CLIP for culturally grounded caption generation.
- **Indonesian Traditional Attire Dataset**: 3,800 expert-annotated images (100/province × 38 provinces), covering ceremonial attributes, ethnic affiliation, garment categories, and image types (male/female/couple/isolated); publicly released.
- **Province-level inductive zero-shot protocol**: strict split ensuring 8 held-out provinces are invisible at every stage, with near-duplicate filtering (CLIP similarity threshold 0.95) to prevent leakage.
- **Ablation demonstrating retrieval necessity**: disabling retrieval causes −19.3% METEOR, confirming retrieval drives cultural vocabulary recovery rather than the decoder alone.

## Results
- **Custom ZeroCLIP vs. best per-metric baseline on 8 unseen provinces:**
  - CLIPScore: 0.8536 vs. InstructBLIP 0.8371 (+1.97%)
  - BLEU-4: 0.3342 vs. CLIP Baseline 0.2817 (+18.64%)
  - METEOR: 0.4859 vs. InstructBLIP 0.4410 (+10.18%)
- **Ablation (Table V):**
  - ZeroCLIP w/o retrieval: CLIPScore 0.8214 / BLEU-4 0.2743 / METEOR 0.3921
  - Retrieval-only Top-1 (no LSTM): 0.8104 / 0.3187 / 0.4201
  - Custom ZeroCLIP: 0.8536 / 0.3342 / 0.4859
- **Human evaluation (80 images, 5 annotators, 1–5 Likert):**
  - Cultural accuracy: 4.4±0.5 (vs. BLIP 3.1±0.8, InstructBLIP 3.6±0.9)
  - Fluency: 4.3±0.4 (vs. BLIP 3.8±0.6, InstructBLIP 4.1±0.5)
  - Fleiss' κ=0.68 (substantial agreement)
- n-gram overlap with top-1 retrieved caption: 23% unigram, 8% bigram — confirms non-trivial generation beyond retrieval copying.

## Limitations
- Zero-shot is province-level, not token-level; cultural term recovery depends on whether synonymous terminology exists in seen-province captions, not on genuinely unseen-vocabulary generalization.
- Retrieval can propagate visually similar but culturally incorrect terminology from seen provinces.
- Comparison is asymmetric: Custom ZeroCLIP is domain-adapted while baselines (BLIP, InstructBLIP, MSGIT) are evaluated off-the-shelf; no fine-tuned baseline variants are included.
- Dataset is small (100 images/province); image diversity may be insufficient for some garment categories.
- Generated captions are stated to be assistive rather than authoritative, requiring expert validation before deployment in museum or ceremonial contexts.

## Relevance to Vision-Language Models
This work directly probes a well-known failure mode of large pretrained VLMs: their cultural and geographic bias toward Western training distributions, which suppresses fine-grained non-Western vocabulary at inference. The retrieval-augmented adaptation strategy — freezing CLIP and training only a lightweight BERT–LSTM head conditioned on retrieved text — is a practical recipe for domain-specializing VLMs in low-resource settings without full fine-tuning. For researchers tracking VLMs, this paper provides evidence that RAG-style retrieval over domain-specific text corpora is a strong complement to frozen CLIP features when cultural or specialized vocabulary recovery is the target task, and introduces a benchmark (province-level inductive zero-shot) that is stricter and more ecologically valid than standard ZSL splits.

## Tags
#vlm #zero-shot #image-captioning #retrieval-augmented-generation #cultural-heritage #clip #low-resource #multimodal
