---
title: "Diffusion-Refined Segmentation and Vision-Language Interpretation for Pediatric Brain Tumor MRI"
authors: ["Wentao Ke", "Jianche Liu"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T03:38:40+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14072"
url: "http://arxiv.org/abs/2606.14072v1"
pdf: "paper/vlm/[Arxiv 2026] Diffusion-Refined Segmentation and Vision-Language Interpretation for Pediatric Brain Tumor MRI.pdf"
---

# Diffusion-Refined Segmentation and Vision-Language Interpretation for Pediatric Brain Tumor MRI

*🕒 **Published (v1):** 2026-06-12 03:38 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14072v1)*

## TL;DR
This paper presents a two-stage pipeline for pediatric brain tumor segmentation on BraTS-PEDs 2023 data: a Swin-UNETR baseline generates coarse masks that condition diffusion-based refiners (3D DDPM and MedSegDiff), yielding improved boundary delineation. Conditioned MedSegDiff achieves the best HD95 (9.35 voxels) across all models. Segmentation outputs are then passed to Gemini 2.5 Pro for automated radiology report generation.

## Problem
Pediatric brain tumor segmentation is substantially harder than adult: tumors have diffuse, infiltrative boundaries with high inter-observer variability, the BraTS-PEDs dataset is small (99 subjects), and severe class imbalance makes the enhancing tumor (ET) subregion—sometimes <1% of total volume—extremely difficult to delineate. Diffusion models had not been systematically evaluated on pediatric cohorts, and their gains over strong CNN/Transformer baselines were unestablished.

## Method
**Stage 1 — Coarse segmentation:** Two 3D baselines trained on BraTS-PEDs 2023 (69/15/15 split, four mpMRI modalities—T1, T1CE, T2, T2-FLAIR):
- **3D Res U-Net** (MONAI): residual encoder-decoder optimized with Soft Dice Loss.
- **Swin-UNETR**: shifted-window self-attention transformer encoder + CNN decoder, fine-tuned from pretrained weights on adult glioma data, optimized with Soft Dice.

**Stage 2 — Diffusion refinement:** Two DDPM-family models conditioned on the coarse Swin-UNETR prediction C:
- **3D U-Net DDPM refiner**: operates on 96³ patches; noises the 3D label map Y₀ with cosine schedule (T=1000); conditions by appending C as 4 extra channels (12-ch input); trained with Dice-CE + boundary-weighted MSE (w=3 on class edges); inference via DPM-Solver. The conditional variant injects the prior as `Y_t' = √ᾱ_t C + √(1−ᾱ_t) ε` and runs DDIM refinement steps rather than full generation from noise.
- **MedSegDiff**: operates on 128² 2D axial slices; separates a diffusion branch (noise prediction) from a parallel highway U-Net (direct mask prediction); skip features fused via FF-Parser (learnable Fourier-domain spectral attention); conditioning appends C to both branches; loss combines noise MSE + γ·DiceCE (γ=10); DPM-Solver sampling.

**Stage 3 — MLLM reporting:** Volumetric metrics per subregion (NC, ED, ET) computed from Swin-UNETR predictions, concatenated with 2D axial MRI+overlay images, and zero-shot prompted to Gemini 2.5 Pro via Vertex AI to produce structured radiology reports.

## Key Contributions
- Systematic comparison of coarse-to-refined segmentation on the pediatric-specific BraTS-PEDs 2023 benchmark, covering CNNs, Transformers, and two DDPM families.
- Demonstration that **coarse conditioning is critical** for diffusion model stability and performance on pediatric data; unconditioned variants collapse or plateau far below baselines.
- Conditioned MedSegDiff achieves the best boundary accuracy (HD95 = 9.35), surpassing even the pretrained Swin-UNETR prior it refines (HD95 = 9.85), showing the diffusion reverse process tightens contours beyond the coarse prediction.
- End-to-end integration of segmentation with an MLLM (Gemini 2.5 Pro) for automated, clinically structured diagnostic report generation from raw MRI volumes.

## Results
All metrics on the internal 15-subject test set; four mpMRI modalities; three subregions: TC (tumor core), WT (whole tumor), ET (enhancing tumor).

| Model | Dice Avg | Dice ET | HD95 ↓ | Sensitivity | Precision |
|---|---|---|---|---|---|
| 3D Res U-Net | 0.48 | 0.19 | 38.35 | 0.93 | 0.34 |
| Swin-UNETR | 0.77 | 0.60 | 13.02 | 0.84 | 0.88 |
| Swin-UNETR (pretrained) | 0.77 | 0.63 | 9.85 | 0.89 | 0.85 |
| DDPM (scratch) | 0.39 | 0.08 | 102.76 | 0.49 | 0.37 |
| DDPM (conditioned) | 0.73 | 0.63 | 33.54 | 0.87 | 0.74 |
| MedSegDiff (scratch) | 0.62 | 0.48 | 49.67 | 0.77 | 0.67 |
| **MedSegDiff (conditioned)** | **0.75** | **0.61** | **9.35** | **0.83** | **0.80** |

- BraTS-PEDs 2023 challenge top teams reported WT Dice 0.81–0.84, TC 0.77–0.81, ET 0.53–0.65; MedSegDiff (conditioned) matches the ET and boundary range without ensembling.
- Conditioning lifts DDPM's ET Dice from 0.08 → 0.63; MedSegDiff from 0.48 → 0.61.

## Limitations
- Dataset is very small (99 subjects; 69 training); no k-fold cross-validation used due to compute constraints; metrics reported on an internal split rather than the challenge's held-out test set, making direct comparison indicative only.
- Diffusion inference requires hundreds of reverse steps (T=1000), making real-time clinical deployment prohibitively slow; DDIM acceleration not yet applied in experiments.
- Batch sizes restricted to 2 (Swin-UNETR, 3D DDPM) on a single 24 GB L4 GPU, limiting gradient stability.
- MLLM reporting pipeline inherits any upstream segmentation errors and carries zero-shot hallucination risk; reports lack RAG grounding or clinician-in-the-loop verification.
- MedSegDiff operates on 2D axial slices, potentially missing 3D spatial context.

## Relevance to Vision-Language Models
This work is directly relevant to VLM researchers interested in **medical multimodal understanding**: it uses Gemini 2.5 Pro as a zero-shot multimodal reasoner that jointly interprets 2D MRI images and structured volumetric text to synthesize clinical radiology reports, demonstrating a practical VLM-as-downstream-interpreter pattern. The pipeline exemplifies how strong VLMs can bridge the gap between pixel-level model outputs and human-interpretable clinical language without task-specific fine-tuning. It also highlights a key failure mode for VLMs in high-stakes domains—hallucination risk when grounding in verified medical knowledge is absent—motivating RAG-augmented or fine-tuned medical VLMs as future work.

## Tags
#vlm #medical-imaging #segmentation #diffusion-models #radiology-report-generation #pediatric-mri #mllm #brain-tumor
