---
title: "Weight Group-wise Post-Training Quantization for Medical Foundation Model"
authors: ["Yineng Chen", "Peng Huang", "Aozhong Zhang", "Hui Guo", "Penghang Yin", "Shu Hu", "Shao Lin", "Xin Li", "Tzu-Jen Kao", "Balakrishnan Prabhakaran", "MingChing Chang", "Xin Wang"]
source: "Arxiv"
venue: ""
published: "2026-04-09"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2604.07674"
url: "http://arxiv.org/abs/2604.07674v1"
pdf: "paper/med-foundation/[Arxiv 2026] Weight Group-wise Post-Training Quantization for Medical Foundation Model.pdf"
---

# Weight Group-wise Post-Training Quantization for Medical Foundation Model

## TL;DR
Permutation-COMQ is a post-training quantization (PTQ) method for medical foundation models (specifically MedSAM) that reorders weight matrix elements by magnitude before coordinate-wise minimization, mitigating the outlier-dominated scaling problem that degrades low-bit quantization. It requires no backpropagation, no Hessian inverse, and no hyperparameters. On CT abdominal segmentation, it outperforms RTN and COMQ baselines at 2-, 4-, and 8-bit precision.

## Problem
Large medical foundation models like MedSAM (ViT-B backbone, >1.5M mask training) are computationally prohibitive for deployment on resource-constrained clinical terminal devices. Existing PTQ methods (RTN, COMQ) suffer accuracy degradation at low bit-widths because per-channel scale factors are dominated by outlier weights, causing coarse quantization resolution for the majority of small-magnitude weights.

## Method
Permutation-COMQ extends COMQ (coordinate-wise minimization quantization) with a weight-aware permutation step:

1. **Permute**: Sort the weight matrix W ∈ ℝ^(m×n) by ascending magnitude within each quantization unit via a permutation matrix P, producing W_p = PW. This clusters similar-magnitude weights together, reducing intra-group variance and outlier influence on scale factors.
2. **Quantize**: Apply per-channel coordinate-wise minimization to W_p. Each column's scale factor δ_j and integer bit-code q_j are solved iteratively as closed-form univariate quadratic subproblems (dot products + rounding only; no gradient computation).
3. **Inverse permute**: Restore original weight ordering via W̃_q = P⁻¹W_q, preserving the layer's structural semantics.

Scale factors are initialized as δ_j⁰ = λ·(max(w_j)−min(w_j))/(2^b−1) with λ ∈ [0,1] to prevent collapse to zero. The algorithm iterates K times over all rows, updating bit-codes and scale factors alternately.

## Key Contributions
- PTQ algorithm (Permutation-COMQ) that eliminates backpropagation and Hessian inverse estimation, relying solely on dot products and rounding
- Weight-aware magnitude-sorted permutation that reduces intra-unit heterogeneity and mitigates outlier-dominated scale factor estimation
- Post-permutation inverse mapping that restores channel structure after quantization
- Demonstrated superiority over RTN and COMQ on MedSAM at 2-, 4-, and 8-bit precision on a real multi-center CT dataset

## Results
On AbdomenCT-1K (1000+ CT scans, 12 centers; organs: liver, kidney, spleen, pancreas); model: MedSAM (ViT-B); metrics: DSC / NSD:

- **2-bit**: Permutation-COMQ 86.94% DSC / 78.94% NSD vs. COMQ 71.80%/53.73%, RTN 29.79%/30.22%
- **4-bit**: 93.43% / 93.09% vs. COMQ 91.87%/90.01%, RTN 90.53%/86.76%
- **8-bit**: 93.62% / 93.20% vs. COMQ 93.49%/92.94%, RTN 93.50%/92.94%
- **FP32 baseline**: 93.51% DSC / 92.97% NSD
- Ablation (per-layer vs. per-channel weight-aware at 4-bit): per-layer drops to 55.44% DSC / 43.69% NSD vs. 93.43%/93.09% with per-channel — per-channel is critical

## Limitations
- Evaluated on a single model (MedSAM/ViT-B) and single dataset (AbdomenCT-1K); generalizability to other medical foundation model architectures (e.g., larger ViT variants, LLM-based medical models) is untested
- Only weight quantization is addressed; activation quantization is not considered, leaving full inference-time savings incomplete
- No reported wall-clock inference speedup or memory reduction measurements on actual terminal/edge devices — compression ratio benefits are implied, not empirically demonstrated
- Calibration data requirements are not fully characterized (size, domain sensitivity)
- Experiments are limited to segmentation; other tasks (classification, registration, report generation) are not evaluated

## Relevance to Foundation Models in Medicine
This work directly addresses a key barrier to clinical deployment of medical foundation models: the computational cost of large Vision Transformer-based models (MedSAM) on edge/terminal devices. By enabling near-lossless 4-bit and usable 2-bit quantization without fine-tuning data or backpropagation, it provides a practical compression pathway compatible with data-privacy constraints common in medical settings. The approach is positioned within the MedSAM ecosystem but is architecturally general to any linear-layer-heavy foundation model, making it relevant to the broader trend of adapting general-purpose foundation models (SAM, ViT) for medical imaging. It complements adapter/fine-tuning compression strategies (e.g., MobileSAM, FastSAM) with a post-hoc, data-free compression alternative.

## Tags
#quantization #post-training-quantization #medsam #medical-image-segmentation #model-compression #edge-deployment #ct-imaging #foundation-model-efficiency
