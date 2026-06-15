---
title: "Free Lunch in Medical Image Foundation Model Pre-training via Randomized Synthesis and Disentanglement"
authors: ["Yuhan Wei", "Yuting He", "Linshan Wu", "Fuxiang Huang", "Junlin Hou", "Hao Chen"]
source: "Arxiv"
venue: ""
published: "2026-02-12"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2602.12317"
url: "http://arxiv.org/abs/2602.12317v1"
pdf: "paper/med-foundation/[Arxiv 2026] Free Lunch in Medical Image Foundation Model Pre-training via Randomized Synthesis and Disentanglement.pdf"
---

# Free Lunch in Medical Image Foundation Model Pre-training via Randomized Synthesis and Disentanglement

## TL;DR
RaSD (Randomized Synthesis and Disentanglement) pre-trains medical image foundation models entirely on synthetic data generated from Gaussian distributions, requiring zero real images. Pre-trained at scale (1.2M 3D volumes, 9.6M 2D images), RaSD consistently outperforms scratch baselines and matches or exceeds real-data pre-trained models across 56 downstream tasks spanning 6 modalities and 48 datasets. The work establishes synthetic data as a viable, privacy-preserving substitute for real data in MIFM pre-training.

## Problem
MIFM pre-training is bottlenecked by the cost, scarcity, heterogeneity, and privacy constraints of large-scale annotated medical datasets. Self-supervised approaches on real data provide weak supervision signals, while prior synthetic approaches (e.g., Anatomix) enforce appearance consistency, limiting generalization to modalities with stable intensity distributions. No existing method demonstrates that MIFMs can be pre-trained competitively using zero real data.

## Method
RaSD comprises two components: (1) a **randomized synthetic data engine** that generates paired image-mask data on-the-fly by sampling Gaussian heatmaps to simulate anatomical structures, applying random deformation fields for geometric variation, and filling pixel intensities from class-conditioned Gaussian noise to produce appearance diversity; (2) a **prototype disentangling learning** objective that applies pull (prototype clustering) and push (prototype separation) losses over dense per-region features to force the backbone to disentangle semantic regions rather than memorize dataset-specific textures. Training is fully streaming (online synthesis), eliminating data storage requirements. Two architectures are instantiated: RaSD-2D (CNN-UNet) and RaSD-3D (Swin Transformer base in Swin UNETR), pre-trained on 9.6M synthetic 2D and 1.2M synthetic 3D image-label pairs respectively.

## Key Contributions
- Demonstrates that MIFMs can be pre-trained entirely on Gaussian-synthesized data with no real medical images.
- Online streaming synthesis pipeline that eliminates storage overhead (zero GB vs. ~10 GB at 1000-image scale) and reduces total training time by ~13% at scale.
- Prototype disentangling learning objective that enforces semantic region separation and cohesion without real-data supervision.
- Comprehensive benchmark across 48 datasets, 56 tasks, and 6 modalities (CT, MRI, X-ray, ultrasound, fundus, pathology).
- Scales to models up to 653M parameters, establishing a privacy-preserving and annotation-free pre-training paradigm.

## Results
- RaSD consistently outperforms training-from-scratch across all 56 evaluated tasks and achieves best performance on 17.
- **3D CT segmentation** (14 datasets vs. Swin UNETR, SuPreM, VoCo, Anatomix): best or tied-best on IRCADb (94%), Covid-19-20 (84%), WHS-CT (98%); outperforms Anatomix on all 12 CT segmentation tasks.
- **3D MRI segmentation** (5 datasets): highest Dice on 3/5 tasks, outperforming all real-data pre-trained FMs on BraTS21, WHS-MR, and ATLAS-MR.
- **CT classification**: 98.8% AUC on CC-CCII (matches VoCo, surpasses SuPreM/Swin-UNETR by up to 0.5%); 98.1% AUC on LUNA16 (within 0.6% of best).
- **Mammography detection**: +4.1% AUC on INbreast and +1.4% on VinDr-Mammo vs. Mammo-CLIP/MAMA.
- **Pathology segmentation**: surpasses PathSegmentor by 5.3% on CoCaHis and 8.1% on Janowczyk; outperforms LVM-Med/MedSAM on 4/9 datasets.
- **Representation quality** (t-SNE NMI on AMOS-MR): RaSD 0.374 vs. Swin UNETR (real-data) 0.379 vs. Anatomix 0.320 vs. Scratch 0.287.
- Online synthesis is 96 s faster than offline at 1000-sample scale with zero storage.

## Limitations
- Rule-based synthesis cannot reproduce rare pathological variations or complex anatomical anomalies not captured by predefined Gaussian rules.
- Performance gap remains against highly specialized modality-specific models (e.g., Mammo-CLIP, MAMA) on narrow domains; gap is within 5% in 80% of comparisons but not eliminated.
- Validation is restricted to benchmark datasets; real-world clinical deployment performance remains unconfirmed.
- Hybrid integration with generative models (to capture organic diversity beyond rule-based patterns) is deferred to future work.

## Relevance to Foundation Models in Medicine
RaSD directly confronts the core data bottleneck constraining MIFM development by decoupling model pre-training from real-data acquisition entirely—a practically significant result for privacy-sensitive clinical settings or under-resourced institutions. The disentanglement objective provides a principled mechanism for learning modality-agnostic structural priors, which explains the observed cross-modal transfer (e.g., synthetic-data-trained models transferring to MRI without CT pre-training data). For the broader MIFM research agenda, this work shifts the question from "how to collect more real data" to "how to design synthesis rules that expose the model to sufficient structural variability," opening a scalable and ethically unconstrained pre-training path. It also establishes that fully supervised pre-training on auto-labeled synthetic data can outperform self-supervised pre-training on real data, challenging the prevailing SSL-on-real-data paradigm.

## Tags
#synthetic-data #pre-training #medical-image-foundation-model #disentanglement #gaussian-synthesis #segmentation #privacy-preserving #multi-modality
