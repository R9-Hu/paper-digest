---
title: "From Specialist to Generalist: Unlocking SAM's Learning Potential on Unlabeled Medical Images"
authors: ["Vi Vu", "Thanh-Huy Nguyen", "Tien-Thinh Nguyen", "Ba-Thinh Lam", "Hoang-Thien Nguyen", "Tianyang Wang", "Xingjian Li", "Min Xu"]
source: "Arxiv"
venue: "ISBI 2026"
published: "2026-01-25"
published_time: "2026-01-25T18:13:48+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2601.17934"
url: "http://arxiv.org/abs/2601.17934v2"
pdf: "paper/med-foundation/[Arxiv 2026] From Specialist to Generalist Unlocking SAM's Learning Potential on Unlabeled Medical Images.pdf"
---

# From Specialist to Generalist: Unlocking SAM's Learning Potential on Unlabeled Medical Images

*🕒 **Published (v1):** 2026-01-25 18:13 UTC  ·  **Source:** Arxiv  ·  **Venue:** ISBI 2026  ·  [link](http://arxiv.org/abs/2601.17934v2)*

## TL;DR
SC-SAM introduces a bidirectional co-training loop between U-Net (specialist) and SAM (generalist) to enable label-efficient medical image segmentation. U-Net generates point-based prompts and pseudo-labels to guide SAM's PEFT adaptation, while SAM's refined masks regularize U-Net. The framework outperforms existing semi-supervised SAM variants and medical foundation models like MedSAM on prostate MRI and polyp benchmarks.

## Problem
SAM cannot inherently exploit unlabeled data under PEFT—leaving abundant unannotated medical images unused. Existing semi-supervised SAM approaches either rely solely on SAM's own predictions (Dual-SAM, suffering from coupling/overconfidence) or use specialists only for prompting without closing the feedback loop (SP-SAM). Meanwhile, U-Net-style architectures excel at semi-supervised learning but lack SAM's semantic generalization.

## Method
SC-SAM pairs a U-Net specialist with a PEFT SAM (adapter layers in the image encoder; trainable prompt encoder and mask decoder). The co-training loop operates as follows:

1. **Specialist → Generalist**: U-Net predicts masks on both labeled and unlabeled images; five foreground/five background points are sampled from these predictions as prompts for SAM's PEFT fine-tuning, along with pseudo-label supervision.
2. **Generalist → Specialist**: SAM's refined mask predictions supervise U-Net as a high-level semantic regularizer.

A **sigmoid ramp-up** schedule weights the U-Net→SAM unsupervised loss as `ω(t) = exp(-(1 - t/T_max)²)` for `t ≤ T_max`, delaying noisy pseudo-label transfer until U-Net stabilizes. The total loss combines supervised Dice+CE on labeled data and cross-pseudo-label unsupervised losses on unlabeled data for both models.

## Key Contributions
- Bidirectional specialist–generalist co-training loop enabling SAM to leverage unlabeled data via PEFT without architectural duplication.
- Sigmoid ramp-up strategy that prevents early noisy pseudo-labels from corrupting SAM, addressing the convergence mismatch between U-Net (slow, domain-adaptive) and SAM (fast, prone to early overfitting).
- Demonstration that U-Net's pseudo-labels are superior to SAM's own predictions for breaking the dual-branch coupling problem seen in Dual-SAM variants.

## Results
**PROMISE12 (prostate MRI):**
- 5% labels: SC-SAM Dice 83.64, IoU 73.87, HD95 3.98 vs. KnowSAM (second best) Dice 78.49, IoU 67.16; outperforms MedSAM (Dice 63.00) and CPC-SAM (Dice 73.73)
- 10% labels: SC-SAM Dice 83.35, IoU 73.54 vs. KnowSAM 82.93, SAM 79.66

**COLON (polyp segmentation, 5 test sets):**
- 5% labels: SC-SAM achieves best Dice on CVC-300 (88.72), CVC-ClinicDB (79.54), CVC-ColonDB (67.77), ETIS-Larib (56.91), Kvasir (84.79)—consistently above KnowSAM and all PEFT-SAM baselines
- 10% labels: Similar pattern; SC-SAM leads on CVC-300 (88.17), CVC-ClinicDB (83.06), Kvasir (86.27); competitive on CVC-ColonDB (68.69) and ETIS-Larib (60.07)

**Ablation:** Removing the sigmoid ramp-up causes a 47% Dice drop (83.64 → 36.37) on PROMISE12 5%; UNet outperforms UNet++, ResUNet++, and Swin-UNet as specialist backbone.

## Limitations
- Evaluated only on 2D slice-based segmentation; volumetric consistency is not addressed despite prostate MRI being inherently 3D.
- Requires simultaneous training of two full model families (U-Net + SAM with adapters), increasing training complexity and memory relative to single-model approaches.
- Swin-UNet performs poorly as specialist due to ViT data hunger in semi-supervised regimes—generalizability of the framework to transformer-based specialists is limited.
- Tested on two anatomical domains (prostate, colon); broader generalization to other modalities (CT, fundus, pathology) is unverified.
- No evaluation at labeled fractions below 5%; behavior under extreme label scarcity is unknown.

## Relevance to Foundation Models in Medicine
SC-SAM directly addresses a practical barrier in deploying medical foundation models: SAM and its medical derivatives (MedSAM, SAM-Med2D) cannot exploit the large pool of unlabeled clinical images through standard PEFT. The finding that a vanilla U-Net can unlock this capability—outperforming purpose-built medical SAM variants—challenges the assumption that foundation model adaptation requires foundation-model-scale supervision. For researchers tracking medical FMs, this work establishes a reusable principle: pairing a domain-specialist semi-supervised learner with a generalist FM in a feedback loop is more effective than either model alone, and suggests that label efficiency gains from FM adaptation need not be sacrificed for unlabeled data utilization.

## Tags
#segmentation #sam #semi-supervised #peft #co-training #medical-image-segmentation #label-efficiency #unet
