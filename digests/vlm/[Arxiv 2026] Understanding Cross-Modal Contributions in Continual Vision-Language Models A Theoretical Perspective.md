---
title: "Understanding Cross-Modal Contributions in Continual Vision-Language Models: A Theoretical Perspective"
authors: ["Salimeh Sekeh", "Mary Wisell"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T18:41:36+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14883"
url: "http://arxiv.org/abs/2606.14883v1"
pdf: "paper/vlm/[Arxiv 2026] Understanding Cross-Modal Contributions in Continual Vision-Language Models A Theoretical Perspective.pdf"
---

# Understanding Cross-Modal Contributions in Continual Vision-Language Models: A Theoretical Perspective

*🕒 **Published (v1):** 2026-06-12 18:41 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14883v1)*

## TL;DR
This paper introduces a formal theoretical framework for understanding how vision and language modality contributions drive catastrophic forgetting in continual VLMs. Four pairwise cosine-expectation scores (two cross-modal, two intra-modal) computed from a single frozen forward pass are shown to predict loss drift, gradient alignment masks, and forgetting magnitude. Contribution-guided environment ordering achieves up to 1.74× forgetting reduction on MS-COCO without any architectural change.

## Problem
Prior continual VLM methods (prompt tuning, adapters, weight interpolation) suppress catastrophic forgetting empirically but none formally characterize which property of the joint image-text embedding space determines how much forgetting occurs, nor how modality-specific alignment varies across a sequence of environments.

## Method
The paper defines four scalar contribution scores as pairwise cosine expectations between environments Et and Et′: cross-modal (ConI→T, ConT→I) and intra-modal (ConI→I, ConT→T), each parameterized by a σ value (0 = identical, 1 = orthogonal). Three theoretical analyses use these scores:

- **T1 (Loss decomposition):** Proves under the Environment Smooth Transition assumption that total loss drift ∆LOSS(t→t′) = β₁·ConI→T + β₂·ConT→I + α, decomposing linearly for both CE and CLIP loss components. The CLIP term has zero cross-seed variance under a frozen encoder but can reverse the sign of ∆CE.
- **T2 (Contribution Balance Factor, CBF):** Defines CBF as an optimal binary mask P* on the gradient that maximizes gradient alignment. Proves P* is achieved by scaling cross-modal similarity scores, and that the CLIP weight λ monotonically controls within-environment alignment CLV(t) under adaptive fine-tuning (null under frozen encoder).
- **T3 (Forgetting bound and ordering):** Derives a closed-form bound on forgetting Ft as a function of intra-environment Hessian curvature, and bounds the forgetting difference Ft1−Ft2 across two environments by the Hessian of cross-modal contributions. Ordering environments to minimize cumulative contribution cost ΣConIT minimizes total forgetting Fπ.

Experiments use CLIP (RN50, ViT-B/32, ViT-B/16) on MS-COCO 2017 (5 semantic environments, high cross-modal variance: σI=0.138) and CUB-200-2011 (5 taxonomic environments, low variance: σI=0.063), under both frozen and adaptive protocols, 3 seeds, 120-permutation ordering sweeps.

## Key Contributions
- **T1 (Loss decomposition theorem):** ∆LOSS linearly decomposes into ConI→T and ConT→I; both terms required to predict transition direction; CLIP term is zero-variance under frozen encoder.
- **T2 (CBF theorem):** CBF objective reduces analytically to p² under a contribution-normalized mask (verified to machine precision); λ monotonically controls CLV(t) only under adaptive fine-tuning.
- **T3 (Forgetting bound + ordering):** Closed-form bound; contribution-guided ordering yields up to 1.74× forgetting reduction on COCO across all 120 permutations and three architectures.
- **OOD robustness:** Lower ConIT predicts higher pairwise MCM AUROC on COCO (Pearson ≈ −0.42 to −0.55); T3 ordering simultaneously improves cumulative OOD AUROC (0.715→0.757 on COCO).
- **Empirical validation boundary:** CUB's near-uniform contributions (σI=0.063) collapse the predictor range (1.16× ratio, positive Pearson), defining when the framework loses discriminative power.

## Results
- **T1 (COCO, ViT-B/16, frozen, λ=1):** ∆CLIP std=0 across all seeds/epochs; ∆CLIP reverses sign of ∆LOSS on E4→E5; OLS R² rises from ≈0 (frozen) to +0.12 (COCO) and +0.16 (CUB) at epoch 10 under adaptive encoding.
- **T2 (CLV(t) sweep, adaptive ViT-B/16):** CLV(t) increases from ≈0.04 (λ=0) to ≈0.50 (λ=5) on CUB; COCO saturates lower (≈0.27–0.36); frozen encoder shows exactly zero sensitivity to λ.
- **T3 (120-ordering sweep, frozen):**
  - COCO RN50: best 3.52 vs worst 5.96 Fπ (1.69×, Pearson −0.082)
  - COCO ViT-B/32: 2.98 vs 5.35 (1.79×, Pearson −0.138)
  - COCO ViT-B/16: 3.12 vs 5.41 (1.73×, Pearson −0.125)
  - CUB all models: ≈1.16× ratio, Pearson positive (+0.156 to +0.247)
- **Sequential BT (ViT-B/16, frozen):** Best ordering reduces BT from 2.011 to 1.806 on COCO (≈10%); zero benefit on CUB.
- **Pairwise OOD (frozen):** COCO mean AUROC ≈0.89–0.90; CUB ≈0.65–0.70; adaptive fine-tuning degrades COCO to 0.61 and CUB to 0.50.
- **Cumulative OOD (ViT-B/16):** T3 ordering: COCO 0.757 vs 0.715 neutral; CUB 0.506 vs 0.488.

## Limitations
- Theoretical results rely on the Environment Smooth Transition assumption (Assumption 4.3), which holds approximately only at conservative adaptive encoder learning rates.
- T3 ordering benefit requires substantial cross-modal variation (σI≈0.138 on COCO); near-uniform regimes (CUB σI=0.063) render the predictor uninformative.
- Experiments use a single shared linear head, which caps accuracy (≈0.17–0.21 on CUB); multi-head architectures are not evaluated.
- Adaptive encoder results on CUB show Fπ ≈ 16–17 (14× over frozen), with positive Pearson, indicating the framework degrades under aggressive fine-tuning in low-variance settings.
- OOD robustness analysis is empirical only; no theoretical guarantees connect contribution scores to OOD AUROC.
- Only CLIP-based architectures are tested; generalization to other VLM families (e.g., BLIP, LLaVA) is unverified.

## Relevance to Vision-Language Models
This work provides the first formal characterization of how CLIP's joint image-text embedding geometry governs catastrophic forgetting in sequential fine-tuning, a practical regime for adapting VLMs to new domains. The cross-modal contribution scores are computable from a single frozen forward pass and require no additional supervision, making them a lightweight diagnostic tool directly applicable to any CLIP-derived VLM. The finding that the CLIP loss component can reverse the direction of CE loss drift—and that λ monotonically controls intra-environment alignment—has direct implications for hyperparameter selection in continual CLIP adaptation methods such as ZSCL and prompt tuning. The unification of forgetting reduction and OOD discriminability under a single contribution-guided ordering criterion opens a theoretically grounded avenue for principled continual VLM algorithm design.

## Tags
#continual-learning #catastrophic-forgetting #clip #vision-language-models #cross-modal-alignment #ood-detection #theoretical-analysis #environment-ordering
