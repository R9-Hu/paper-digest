---
title: "CPS4: Class Prompt driven Semi-Supervised Spine Segmentation with Class-specific Consistency Constraint"
authors: ["Qingtao Pan", "Hongzan Sun", "Bing Ji", "Shuo Li"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T13:08:11+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15802"
url: "http://arxiv.org/abs/2606.15802v1"
pdf: "paper/vlm/[Arxiv 2026] CPS4 Class Prompt driven Semi-Supervised Spine Segmentation with Class-specific Consistency Constraint.pdf"
---

# CPS4: Class Prompt driven Semi-Supervised Spine Segmentation with Class-specific Consistency Constraint

*🕒 **Published (v1):** 2026-06-14 13:08 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15802v1)*

## TL;DR
CPS4 is the first text-guided semi-supervised spine segmentation framework that uses class-specific textual prompts to improve pseudo-label quality for MRI segmentation. It introduces token- and pixel-level attention losses during a VLM pretraining stage to enforce tight semantic alignment between each class prompt (e.g., "Lumbar Vertebra 1") and its corresponding spine unit. With only 5% labeled data, CPS4 achieves 80.44% mDice on MRSpineSeg, outperforming all SSL and VLM baselines.

## Problem
Existing semi-supervised segmentation methods suffer from low-quality pseudo labels. VLMs like CLIP and MedCLIP perform image-level cross-modal alignment and lack explicit constraints binding each class-specific text prompt to its corresponding spatial region, causing cross-class interference and unreliable class-prompt-guided segmentation maps for multi-class spine structures.

## Method
CPS4 operates in two stages:

**Stage 1 — Class-specific consistency constrained VLM pretraining:** A ViT vision encoder and BioClinicalBERT text encoder are pretrained on labeled data. For each class prompt *i*, two losses enforce per-class alignment:
- *Token-level attention loss* (Ltoken): concentrates the cross-modal attention map onto the target spine unit's binary mask region by maximizing the fraction of total attention mass falling within the foreground.
- *Pixel-level attention loss* (Lpixel): a pixel-wise binary cross-entropy between the upsampled attention map and the binary mask, preventing over-concentration on subregions.

**Stage 2 — Class prompt-driven semi-supervised segmentation:** The pretrained encoders generate a per-class attention map for each unlabeled image via dot-product between image patch tokens and class prompt tokens; OTSU thresholding converts each to a binary map, and all class maps are stacked into a unified multi-class pseudo label `y_text`. A Mean Teacher (student/teacher ResUNet) is then trained with three losses: supervised loss on labeled images, `L_text_semi` (student prediction vs. `y_text`), and `L_enhance_semi` (student prediction vs. combined teacher pseudo-label + `y_text`).

## Key Contributions
- First application of textual class prompts to semi-supervised spine segmentation.
- Token-level attention loss enforcing spatial concentration of cross-modal attention on target spine units.
- Pixel-level attention loss preventing subregion over-activation, complementing the token-level loss.
- Two-stage pipeline integrating VLM pretraining with a Mean Teacher SSL framework via class-prompt-guided pseudo-label enhancement.

## Results
- **5% labeled:** CPS4 80.44% mDice / 70.63% mIoU vs. best baseline GraphCL 78.21% / 67.89% (+2.23% / +2.42% mDice/mIoU).
- **10% labeled:** 81.67% mDice vs. GraphCL 78.64% (+3.03% mDice).
- **25% labeled:** 82.21% mDice vs. GraphCL 79.53%.
- **50% labeled:** 82.93% mDice / 73.55% mIoU (best across all ratios).
- Ablation (5% labeled): baseline MT 74.25% → +token loss → 79.41% → +pixel loss → 80.44%.
- Dataset: MRSpineSeg, 215 subjects, 20-class T2-weighted MR spine segmentation.

## Limitations
- Evaluated on a single public dataset (MRSpineSeg); generalizability to other anatomies or modalities is undemonstrated.
- Stage 1 pretraining uses only labeled data, so the quality of class-prompt alignment is bounded by labeled data size.
- Class prompts require knowing all possible class names at inference; unlabeled images must generate attention maps for all 20 classes regardless of which structures are present.
- The OTSU thresholding step for binarizing attention maps is a fixed heuristic; failure modes on atypical attention distributions are not analyzed.
- 2D ResUNet backbone; volumetric context is not exploited.

## Relevance to Vision-Language Models
This paper directly addresses a known weakness of contrastive VLMs (CLIP, MedCLIP): their image-level alignment fails to produce spatially localized, class-specific attention, which is critical for dense prediction tasks. The proposed token- and pixel-level attention losses are a principled, lightweight extension to VLM pretraining that enforces region-text grounding without requiring dense paired annotations beyond binary masks. For VLM researchers, this demonstrates a concrete path to adapting general-purpose vision-language encoders for fine-grained, multi-class medical segmentation, and the two-stage pretraining-then-SSL architecture is a reusable pattern for other anatomies or label-scarce domains.

## Tags
#vlm #semi-supervised-learning #medical-image-segmentation #spine-segmentation #pseudo-labels #cross-modal-alignment #clip #grounding
