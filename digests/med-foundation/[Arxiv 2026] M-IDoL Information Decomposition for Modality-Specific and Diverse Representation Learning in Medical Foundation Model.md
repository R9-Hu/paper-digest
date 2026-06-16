---
title: "M-IDoL: Information Decomposition for Modality-Specific and Diverse Representation Learning in Medical Foundation Model"
authors: ["Yihang Liu", "Longzhen Yang", "Jiaxiong Yang", "Ying Wen", "Lianghua He", "Heng Tao Shen"]
source: "Arxiv"
venue: ""
published: "2026-04-10"
published_time: "2026-04-10T04:06:11+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2604.08936"
url: "http://arxiv.org/abs/2604.08936v2"
pdf: "paper/med-foundation/[Arxiv 2026] M-IDoL Information Decomposition for Modality-Specific and Diverse Representation Learning in Medical Foundation Model.pdf"
---

# M-IDoL: Information Decomposition for Modality-Specific and Diverse Representation Learning in Medical Foundation Model

*🕒 **Published (v1):** 2026-04-10 04:06 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2604.08936v2)*

## TL;DR
M-IDoL is a self-supervised medical foundation model that addresses "information ambiguity" in multimodal pre-training by decomposing the contrastive objective into two entropy-based terms: one that maximizes inter-modality separation and one that minimizes intra-modality uncertainty. Pre-trained on 1.15M unlabeled images across five imaging modalities, it outperforms 20 existing foundation and modality-specific models on 21 downstream clinical tasks.

## Problem
Existing unified medical foundation models (MFMs) apply a single contrastive learning (CL) objective across heterogeneous modalities (X-ray, fundus, OCT, dermoscopy, pathology). This uniformly maximizes mutual information including modality-shared redundancy, collapsing all modalities into one embedding space. The result is *information ambiguity*: degraded inter-modality specificity (modalities are not separable) and degraded intra-modality diversity (fine-grained semantic discrimination within a modality is suppressed).

## Method
M-IDoL reformulates the standard contrastive objective by explicitly subtracting the trivariate mutual information term that captures cross-modality redundancy. Because direct estimation of trivariate MI is unstable at scale, the objective is decomposed into two tractable entropy terms:

**max H(X|Z) − H(X|Y,Z)**

- **Inter-modality entropy maximization** `H(X|Z)`: encourages representation X to be statistically independent of representations Z from other modalities, implemented via a *routing-consistency loss* `L_route`. A Mixture-of-Experts (MoE) projector with top-1 routing (one expert per modality, N=5) is trained with Sinkhorn–Knopp balancing to assign each unlabeled image to a latent modality subspace. The loss enforces that all augmented views of the same image route to the same expert, while images from other modalities route to different experts.

- **Intra-modality uncertainty minimization** `H(X|Y,Z)`: within each MoE subspace, an InfoNCE-based *intra-modality contrastive loss* `L_cst` pulls augmented views of the same image together and pushes views from other samples apart, reducing augmentation noise without conflating cross-modality semantic variance.

The two losses are summed: `L_M-IDoL = L_route + L_cst`. A DINO-style siamese network (student/teacher with EMA) using Swin-B backbone is pre-trained for 100 epochs on 2× NVIDIA A6000 GPUs. At inference, only the teacher encoder is retained; the MoE projector is discarded.

## Key Contributions
- Formal identification of *information ambiguity* in unified multimodal CL pre-training as excessive modality-shared redundancy.
- Information decomposition framework that reformulates trivariate MI removal into two tractable entropy-based objectives without requiring explicit multivariate MI estimation.
- MoE projector that achieves unsupervised modality routing (no modality labels used during pre-training) via routing-consistency loss with Sinkhorn–Knopp balancing.
- Intra-modality contrastive loss that operates within modality-separated MoE subspaces, improving fine-grained semantic diversity per modality.
- State-of-the-art results across 21 downstream datasets spanning 5 modalities, outperforming 20 baselines including both modality-specific and unified MFMs.

## Results
- **vs. unified MFMs** (LVM-Med, UniMed, Unimiss+, MedCoss, CoSMIC): M-IDoL achieves statistically significant improvement (p < 0.05) on most of 21 datasets; average gain >6% over Unimiss+, LVM-Med, and UniMed; >4% over continual-learning MFMs (MedCoss, CoSMIC) on OCT and pathology tasks.
- **vs. modality-specific models**:
  - Fundus: 95.19% AUC on APTOS vs. 94.36% (RETFound, pre-trained on 1.6M fundus images)
  - OCT: 99.34% AUC on OCTID vs. 98.84% (MIRAGE, pre-trained on 260K OCT images)
  - Pathology (Mitosis): 95.62% ACC vs. 93.64% (Virchow); competitive on MHIST (no significant difference vs. Virchow, p = n.s.)
  - X-ray (RSNA): 93.23% AUC vs. 91.68% (AFiRe)
  - Dermoscopy: slightly below Panderm on ISIC2016/2017 but competitive (p < 0.05 on HAM10000 AUC: 97.96% vs. 97.13%)
- **Ablation** (Table 2, five datasets): Baseline → +MoE only → +L_route → +L_cst yields monotone improvement; e.g., on RSNA AUC: 87.42 → 88.31 → 91.45 → 93.23%.
- **Expert count**: one expert per modality (N=5) chosen; additional experts yield marginal gains.

## Limitations
- Pre-training covers only five imaging modalities; generalization to modalities absent from pre-training (e.g., MRI, ultrasound, endoscopy) is untested.
- Requires specifying expert count N equal to the number of modalities; performance sensitivity to N mismatch or unknown modality count is not evaluated.
- Backbone is Swin-B (vision-only); no text or report modality included, limiting applicability to vision-language MFM settings.
- Modality labels are not used during pre-training, but the method implicitly assumes modalities are distinct enough to be separable by unsupervised routing — not validated for modalities with high visual overlap.
- Evaluation uses linear probing for pathology but full fine-tuning for other modalities, making cross-modality performance comparisons not strictly apples-to-apples.

## Relevance to Foundation Models in Medicine
M-IDoL directly targets a core failure mode of unified medical foundation models — the collapse of heterogeneous imaging modalities into a shared representation space — and provides a principled information-theoretic remedy applicable to any MoE-augmented self-supervised architecture. For researchers tracking MFMs, this establishes a new benchmark across 21 datasets and five modalities while demonstrating that modality-aware pre-training objectives can match or exceed modality-specific specialists without sacrificing generality. The routing-consistency + intra-modality contrastive approach complements ongoing work on continual learning (MedCoss, CoSMIC) and vision-language alignment (UniMed) by offering a single-stage, label-free alternative. The MoE projector design also offers a reusable plug-in for existing MFM backbones.

## Tags
#medical-foundation-model #multimodal-representation #mixture-of-experts #contrastive-learning #information-theory #modality-specificity #self-supervised #medical-imaging
