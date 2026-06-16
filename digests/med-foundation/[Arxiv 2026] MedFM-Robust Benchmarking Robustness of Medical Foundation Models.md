---
title: "MedFM-Robust: Benchmarking Robustness of Medical Foundation Models"
authors: ["Xiangxiang Cui", "Tianjin Huang", "Yifang Wang", "Lijie Hu", "Lu Yin"]
source: "Arxiv"
venue: ""
published: "2026-05-18"
published_time: "2026-05-18T18:50:56+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2605.19027"
url: "http://arxiv.org/abs/2605.19027v3"
pdf: "paper/med-foundation/[Arxiv 2026] MedFM-Robust Benchmarking Robustness of Medical Foundation Models.pdf"
---

# MedFM-Robust: Benchmarking Robustness of Medical Foundation Models

*🕒 **Published (v1):** 2026-05-18 18:50 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2605.19027v3)*

## TL;DR
MedFM-Robust is the first systematic robustness benchmark for medical foundation models, covering 40 perturbation types (12 generic + 28 modality-specific) across 8 imaging modalities. It evaluates 5 VLMs and 2 SAM-based segmentation models on VQA, visual grounding, captioning, and segmentation. The central finding is that fine-tuning strategy—not model architecture—is the dominant determinant of robustness.

## Problem
Existing medical AI benchmarks evaluate models on clean, curated images, creating a gap between reported performance and real-world reliability. No prior work systematically assessed robustness of medical foundation models across diverse modalities, tasks (VQA, grounding, captioning, segmentation), and fine-tuning strategies under both generic and clinically realistic perturbations.

## Method
The authors build a modality-adaptive perturbation pipeline with 12 base corruptions (noise, degradation, geometric) and 28 modality-specific artifacts (e.g., CT metal streaks, MRI ghosting, ultrasound acoustic shadowing, OCT blink artifacts, endoscopy specular reflections). Severity is calibrated into 5 levels via SSIM-guided binary search (SSIM 0.90→0.50). Models evaluated:
- **VLMs**: LLaVA-Med, MedGemma, MedGemma-1.5, GPT-4o-mini, Gemini-2.5-flash — tested zero-shot on VQA (OmniMedVQA, accuracy) and captioning (ROCOv2, BLEU/ROUGE-L/CIDEr), and with LoRA fine-tuning on visual grounding (MeCoVQA, Acc@IoU≥0.5).
- **Segmentation**: MedSAM and SAM-Med2D tested across 5 strategies (full fine-tuning, encoder-only, decoder-only, LoRA, adapter) on ISIC 2016, Kvasir-SEG, Brain Tumor, Glaucoma Disc/Cup datasets.
Robustness is measured as absolute performance drop (Δ) averaged over perturbation types within each severity level.

## Key Contributions
- First benchmark combining generic + medical-specific perturbations across 8 modalities, calibrated with SSIM-guided severity levels.
- Unified evaluation spanning 3 VLM tasks (VQA, grounding, captioning) and dense segmentation under identical perturbation conditions.
- Empirical finding that fine-tuning strategy dominates robustness: LoRA degrades ~2× more than full fine-tuning for segmentation.
- Evidence that modality-specific perturbations are more damaging than generic ones (9 of top 15 hardest corruptions are domain-specific).
- Deployment guidelines: full fine-tuning most robust; SAM-Med2D adapter favorable efficiency-robustness trade-off; MedGemma most stable medical VLM.

## Results
**Segmentation:**
- Full fine-tuning: mean IoU drop 0.025; LoRA: 0.048 (~2× worse)
- SAM-Med2D LoRA IoU drop rises from 0.028 (low severity) to 0.065 (high severity)
- Most sensitive dataset: Kvasir endoscopy (IoU drop 0.050); most stable: Brain MRI (0.019)
- 9 of top 15 most damaging perturbations are modality-specific (Motion Artifacts OCT, Light Reflection, Specular Reflection dominate)

**VLMs — Visual Grounding (LoRA-tuned):**
- MedGemma: 65.4% → 22.3% (−43.1 pts); MedGemma-1.5: 69.2% → 29.0% (−40.2 pts)
- Compression artifacts: −32.9 pts; Gaussian Noise: −32.6 pts

**VLMs — Zero-shot VQA:**
- Gemini-2.5-flash: 67.0% clean → 30.9% perturbed (−36.1 pts, 54% relative drop)
- GPT-4o-mini: 50.0% clean, ~12% relative drop
- Medical VLMs (MedGemma): drop <20% relative; MedGemma smallest absolute drop (3.1 pts)

**VLMs — Zero-shot Captioning:**
- All models: BLEU drop <0.02 across all perturbation types and severity levels (<7% relative)

## Limitations
- Visual grounding evaluated only with LoRA fine-tuning; robustness under other adaptation strategies for grounding is not assessed.
- Benchmark covers 500 samples per VLM task—small sample size may limit statistical confidence.
- No evaluation of robustness under adversarial (non-corruption) perturbations or distribution shifts from scanner/site differences.
- SSIM-guided severity calibration may not align with perceived clinical significance of artifacts across modalities.
- Not every perturbation reaches severity level 5 (max iterations cap), introducing inconsistency at the high-severity end.

## Relevance to Foundation Models in Medicine
This paper directly addresses a critical deployment gap for medical foundation models: clean-benchmark accuracy does not predict robustness to clinically realistic image degradation. The finding that fine-tuning strategy—particularly LoRA—trades robustness for efficiency has immediate implications for how the community adapts large models (SAM, LLaVA, Gemini) to clinical settings. The result that general-purpose VLMs (Gemini-2.5-flash) achieve high zero-shot VQA accuracy but catastrophically fail on grounding challenges assumptions about their clinical readiness. For practitioners tracking foundation model deployment in medicine, this benchmark establishes that domain-specific robustness evaluation is non-negotiable and that task formulation (zero-shot vs. fine-tuned) is as consequential as model choice.

## Tags
#robustness #benchmark #medical-imaging #vlm #segmentation #fine-tuning #lora #foundation-models
