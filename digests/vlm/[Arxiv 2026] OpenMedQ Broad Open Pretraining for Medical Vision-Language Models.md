---
title: "OpenMedQ: Broad Open Pretraining for Medical Vision-Language Models"
authors: ["Ibrahim Gulluk", "Max Van Puyvelde", "Olivier Gevaert"]
source: "Arxiv"
venue: "MIDL"
published: "2026-06-11"
published_time: "2026-06-11T06:24:44+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.12953"
url: "http://arxiv.org/abs/2606.12953v1"
pdf: "paper/vlm/[Arxiv 2026] OpenMedQ Broad Open Pretraining for Medical Vision-Language Models.pdf"
---

# OpenMedQ: Broad Open Pretraining for Medical Vision-Language Models

*🕒 **Published (v1):** 2026-06-11 06:24 UTC  ·  **Source:** Arxiv  ·  **Venue:** MIDL  ·  [link](http://arxiv.org/abs/2606.12953v1)*

## TL;DR
OpenMedQ is a fully-open medical VLM (ViT-base + LLaMA-7B with LoRA) pretrained on the broadest publicly available medical mix to date: 14 datasets totaling ~3.35M samples spanning pathology, radiology, microscopy, and text-only clinical QA. It achieves state-of-the-art BLEU-1 on PathVQA (75.9), outperforming Med-PaLM M variants up to 562B parameters, while its vision encoder leads three strong contrastive baselines on average classification transfer across 8 unseen benchmarks.

## Problem
Most medical VLMs either use narrow pretraining mixes (single-corpus contrastive encoders like BiomedCLIP, PMC-CLIP) or withhold weights and data (BiomedGPT, Med-PaLM M), leaving the community without a fully-open, broadly-pretrained baseline that practitioners can inspect, reproduce, and extend.

## Method
OpenMedQ follows the LLaVA architecture: a ViT-base-patch16-224 vision encoder initialized from BiomedCLIP is connected via a linear projection to a LLaMA-7B language model initialized from PMC-LLaMA. Image and text tokens are concatenated and decoded left-to-right with next-token cross-entropy loss; image and prefix tokens are masked during loss computation. Fine-tuning uses LoRA (rank r=8) applied to LLaMA-7B. Training runs on a single A100 with AdamW, batch size 64, lr 5×10⁻⁵, up to 15 epochs. For classification transfer evaluation, the vision encoder is detached and a linear head (R^{2d×m}) is attached; both encoder and head are fine-tuned for 100 epochs under a fixed downstream recipe identical across all baselines.

## Key Contributions
- Broadest fully-open medical pretraining mix to date: 14 datasets, ~3.35M samples across pathology, radiology, microscopy, and text-only clinical QA.
- State-of-the-art BLEU-1 on PathVQA (75.9) at 7B parameters, beating Med-PaLM M up to 562B (~80× larger).
- Highest mean macro-F1 (0.757) on 8 unseen medical classification benchmarks under a fixed evaluation recipe, surpassing BiomedCLIP, PMC-CLIP, and PubMedCLIP (all ~0.745–0.746).
- Full release of weights, dataset recipes, and an interactive demo for community use.

## Results
- **PathVQA BLEU-1**: 75.9 (vs. prefix tuning 70.3, Med-PaLM M up to 562B: 72.27)
- **VQA-MED BLEU-1**: 64.5 (matches 2019 challenge best of 64.4)
- **Mean macro-F1 across 8 classification benchmarks**: OpenMedQ 0.757 vs. PubMedCLIP 0.746, PMC-CLIP 0.745, BiomedCLIP 0.745, from-scratch 0.616
- Wins outright on MedFMC-chest and MedFMC-endo; ties PMC-CLIP on CXR8
- Trails best encoder by ≤0.02 on four benchmarks; notable gap on Breast-Ultrasound (0.876 vs. 0.915)

## Limitations
- BLEU-1 captures only surface-level token overlap, not clinical correctness or reasoning quality.
- Med-PaLM M's larger variants still lead on VQA-RAD and Slake benchmarks.
- Narrow-modality contrastive encoders can outperform OpenMedQ on specific tasks (e.g., Breast-Ultrasound).
- Vision encoder is ViT-base (small capacity); no ablation on larger vision backbones.
- Pretraining data breadth is bounded to publicly available datasets; proprietary clinical data is excluded by design.

## Relevance to Vision-Language Models
OpenMedQ directly advances the open-source medical VLM ecosystem by demonstrating that broad data diversity—not proprietary scale—is a reproducible lever for competitive performance. The LLaVA-style architecture with domain-initialized components (BiomedCLIP encoder + PMC-LLaMA backbone) and LoRA fine-tuning provides a practical, resource-efficient template for domain-specialized VLMs. The finding that a 7B-parameter model pretrained on open data beats closed 562B-parameter models on PathVQA challenges assumptions about parameter count as the primary driver of medical VLM capability. This work is directly relevant to researchers studying data-efficient VLM pretraining, medical multimodal grounding, and open-science reproducibility in clinical AI.

## Tags
#vlm #medical-vqa #open-source #pretraining #image-text #lora #classification-transfer #medical-imaging
