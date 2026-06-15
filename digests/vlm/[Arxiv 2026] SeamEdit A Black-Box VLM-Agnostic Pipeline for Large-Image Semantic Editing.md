---
title: "SeamEdit: A Black-Box VLM-Agnostic Pipeline for Large-Image Semantic Editing"
authors: ["Xiangyu Lyu", "Dan Lei"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13041"
url: "http://arxiv.org/abs/2606.13041v1"
pdf: "paper/vlm/[Arxiv 2026] SeamEdit A Black-Box VLM-Agnostic Pipeline for Large-Image Semantic Editing.pdf"
---

# SeamEdit: A Black-Box VLM-Agnostic Pipeline for Large-Image Semantic Editing

## TL;DR
SeamEdit is a training-free, model-agnostic pipeline that wraps any VLM with inpainting capability as a black-box oracle to perform semantic editing on large images that exceed a single VLM's input resolution. It addresses alignment drift and seam artifacts that appear when closed-source VLMs are naively applied to tiled editing via five post-hoc stages: overlay decomposition, multi-candidate VLM inpainting, Grid-SIFT geometric alignment + local color correction, seam-risk-based candidate ranking, and dynamic-programming curved seam fusion.

## Problem
Existing tile-based high-resolution editing methods (MultiDiffusion, MobilePicasso, HiPrompt, Tiled Diffusion) require white-box access to internal diffusion states (latent variables, attention maps, denoising trajectories) and cannot be applied to closed-source VLMs exposed only as APIs. Direct application of black-box VLMs to tiled editing produces two systematic failure modes: (1) canvas-level alignment drift (translation, rotation, scale deviations between generated tile and original canvas) and (2) visible seam artifacts at tile boundaries due to absence of cross-tile context during generation.

## Method
SeamEdit operates in five stages without modifying or fine-tuning any VLM:

1. **Overlay tile decomposition**: The input image is divided into an R×C grid; each core tile Cr,c is expanded by δ pixels on all sides to form Tr,c, providing boundary context to the VLM and an overlap buffer for seam processing. A binary inpainting mask marks only the core region for repainting.

2. **Multi-candidate VLM inpainting**: Each tile (image + mask + text instruction) is submitted K times to the black-box VLM G, exploiting its stochastic sampling to generate K candidates per tile, decoupling generation from selection.

3. **Grid-SIFT geometric alignment**: SIFT features are extracted in a Gr×Gc spatial grid over each tile to ensure uniform spatial coverage, then matched between the reference tile and each candidate. RANSAC estimates an affine transform Ak with validity constraints on inlier count, spatial coverage, RMSE, translation, rotation, scale, and shear. Candidates failing validity use the identity transform.

4. **Local color-consistency correction**: Per-channel mean/std statistics are computed in the overlap region; a clipped linear gain-bias transform moves the candidate's color distribution toward the reference (strength η). A Gaussian low-pass residual Δ compensates residual low-frequency color drift (strength γ, magnitude-clipped by ε).

5. **Seam-risk candidate ranking + DP curved seam fusion**: Each candidate is scored via a composite quality metric Q combining PSNR, SSIM, seam risk (max over directions of color + gradient MAE in the boundary band), geometric penalty, valid-pixel coverage, and overall color difference. The best candidate k* per tile is selected. At fusion, overlapping regions between adjacent tiles undergo minimum-cost curved seam search via 1D dynamic programming (cost = color L1 + λ·gradient L1 difference), followed by feathered alpha blending of width f pixels around the optimal seam path Γ*.

## Key Contributions
- Training-free, VLM-agnostic tiled editing pipeline treating any inpainting-capable VLM as a pure black-box API, with no access to model internals.
- Overlay-based tile decomposition providing boundary context to the VLM and an overlap buffer for post-hoc correction and fusion.
- Grid-SIFT geometric alignment correcting affine drift in black-box VLM outputs, with geometric validity constraints to prevent degenerate corrections.
- Local color-consistency correction combining per-channel linear normalization with Gaussian low-frequency residual compensation.
- Seam-risk-based multi-candidate ranking that jointly scores boundary color/gradient continuity, geometric reliability, valid-pixel coverage, and PSNR/SSIM in overlay regions.
- Dynamic-programming curved seam fusion adapting seam-carving-style minimum-energy path search to the tiled VLM editing context, combined with feathered blending.

## Results
- Automatic candidate ranking (selecting 12 of 15 usable candidates from a 3×4 grid experiment using GPT-Image-2 as backend) versus the full candidate pool:
  - Composite score: 33.18 ± 25.37 vs. 26.54 ± 26.35 (↑)
  - Color Δ: 10.38 ± 5.66 vs. 24.09 ± 28.84 (↓)
  - Max seam MAE: 36.20 ± 20.11 vs. 67.23 ± 66.66 (↓)
  - PSNR: 19.98 ± 2.27 vs. 17.30 ± 5.89 (↑)
  - SSIM: 0.884 ± 0.058 vs. 0.723 ± 0.336 (↑)
- Qualitative comparisons against FLUX.2-Dev, SUPIR, and online tools (Bigjpg/iLoveIMG/ImgLarger); SeamEdit shows better boundary continuity and structure preservation across sky, building, vegetation, and road regions.
- No quantitative full-pipeline numbers against baselines are reported; comparisons are qualitative only.

## Limitations
- Generation quality is fully dependent on the backend VLM; API changes or service discontinuation break reproducibility.
- Composite scoring weights (αi, βi) are empirically tuned; no systematic sensitivity analysis is provided.
- Multi-candidate generation scales linearly in K API calls per tile, which is costly for time-sensitive applications.
- Extreme semantic edits where the new tile content conflicts sharply with surrounding context can cause residual boundary artifacts that cannot be fully resolved by geometric/seam correction.
- Evaluation is limited to a single backend (GPT-Image-2) on one scene; broader evaluation across backends and scene types is not included.
- No user studies or perceptual metrics (e.g., LPIPS) are reported in the main experiment.

## Relevance to Vision-Language Models
SeamEdit directly addresses a practical deployment gap for closed-source VLMs: how to leverage their strong inpainting generation quality on images larger than their native resolution, without white-box access. It positions VLMs as interchangeable generation oracles, meaning improvements in frontier VLMs (better instruction following, higher fidelity inpainting) automatically benefit the pipeline without any retraining — a model-agnostic scaling property that is directly relevant to practitioners using commercial VLMs. The paper also highlights an underexplored failure mode of VLMs in structured spatial tasks (alignment drift under tiled processing), complementing the broader literature on VLM spatial reasoning limitations. For researchers tracking VLMs, SeamEdit exemplifies an increasingly common pattern: wrapping closed-source VLMs with classical computer vision post-processing (SIFT, DP seam carving, color normalization) to compensate for weaknesses that cannot be addressed via prompting alone.

## Tags
#vlm #image-editing #tiled-generation #inpainting #high-resolution #black-box #seam-artifacts #training-free
