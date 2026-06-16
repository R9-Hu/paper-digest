---
title: "Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification"
authors: ["Han Liu", "Bogdan Georgescu", "Yanbo Zhang", "Youngjin Yoo", "Michael Baumgartner", "Riqiang Gao", "Jianing Wang", "Gengyan Zhao", "Eli Gibson", "Dorin Comaniciu", "Sasa Grbic"]
source: "Arxiv"
venue: ""
published: "2025-12-15"
published_time: "2025-12-15T00:01:19+00:00"
year: 2025
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2512.12887"
url: "http://arxiv.org/abs/2512.12887v3"
pdf: "paper/med-foundation/[Arxiv 2025] Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification.pdf"
---

# Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification

*🕒 **Published (v1):** 2025-12-15 00:01 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2512.12887v3)*

## TL;DR
AnyMC3D adapts frozen 2D foundation models (FMs) to 3D medical image classification via lightweight task-specific LoRA adapters (~1M parameters per task) and a query-based attention pooling slice aggregator. It achieves 0.894 average AUROC across a 12-task benchmark, matching or surpassing 3D medical FMs that require 40–50× more trainable parameters. A key finding is that properly adapted general-purpose 2D FMs (e.g., DINOv2/v3) can match domain-specific medical FMs.

## Problem
Three critical pitfalls plague prior work on medical FMs for 3D classification: (1) **data-regime bias** — evaluation in low-data few-shot settings that are clinically unrepresentative; (2) **suboptimal adaptation** — naive frozen-backbone + average/median pooling strategies that severely underestimate FM capacity; (3) **insufficient task coverage** — benchmarks limited to a single modality or anatomy, preventing assessment of true generalization.

## Method
AnyMC3D freezes a 2D ViT backbone (DINOv2/v3 ViT-L 300M, MedImageInsight DaViT 365M, or MedGemma SigLIP 432M) and adds task-specific lightweight plugins:

- **LoRA adaptation** (rank 8, α=16) applied to patch embedding and all self-attention projection layers (~1.2–2M trainable params per task), enabling task-specific in-plane feature refinement without altering the shared backbone.
- **Permutation-invariant slice aggregation**: per-slice CLS token embeddings are pooled via a learnable task query using scaled dot-product attention, producing a single volume embedding robust to anisotropic spacing and variable slice counts.
- **Optional auxiliary pixel-level supervision**: patch tokens from the last ViT block are reshaped into a pseudo-3D token volume and decoded with a lightweight 3D decoder to produce voxel-wise logits; the combined loss couples classification and segmentation objectives (Eq. 8).
- **Multi-view/modal fusion**: view-specific LoRA adapters and queries encode each MRI view separately; view embeddings are fused by a second attention pooling step.
- **Interpretable 3D heatmaps**: per-slice class-to-patch attention maps (averaged over heads) are weighted by slice importance scores from the task query to yield a volumetric saliency map.

## Key Contributions
- Identification and characterization of three pitfalls (data-regime bias, suboptimal adaptation, insufficient task coverage) that have led the field to systematically underestimate 2D FM potential.
- AnyMC3D: a single frozen-backbone framework scalable to arbitrary new 3D classification tasks with ~1M additional parameters per task.
- A 12-task benchmark spanning CT and MRI, abdomen/chest/shoulder/head anatomies, multi-label and binary settings, with realistic class-imbalanced dataset sizes (1,140–50,188 volumes per task).
- First-place finish in the VLM3D challenge (118 participants) using only ~0.5M trainable parameters, without task-specific engineering or large-scale CT pretraining.
- Empirical demonstration that general-purpose 2D FMs, when properly adapted, match domain-specific medical FMs.

## Results
- **Average AUROC (10-task benchmark)**: AnyMC3D (MII) = 0.894 (rank 1.7), AnyMC3D (DINOv3) = 0.894 (rank 2.0); best prior baseline MST = 0.869 (rank 4.0); 3D medical FMs VoCo = 0.793, MedicalNet = 0.783.
- **Parameter efficiency**: AnyMC3D uses 1.2–2.0M trainable params vs. MST 23.05M, VoCo 50.49M (10–50× reduction).
- **Adaptation gap (MII)**: naive linear probing AUC 0.785 → AnyMC3D 0.894 (ΔAUC = +0.109); adaptation raises rank from 8.7 to 1.7.
- **Adaptation gap (DINOv3 on CT-RATE T5)**: frozen backbone + average pooling underperforms; LoRA adaptation yields ΔAUC = +0.11 vs. same backbone with naive fusion.
- **PDAC detection (T5 vs. PANORAMA winner PanDx)**: AnyMC3D (DINOv3) AUC 0.962 vs. PanDx 0.949 (classification labels only); +pixel supervision pushes to 0.973.
- **Chest CT (CT-RATE T11, 18 classes)**: AnyMC3D (DINOv2) mean AUC 0.884 vs. CT-CLIP 0.748 vs. CT-Net 0.631.
- **Head CT (75 findings)**: AnyMC3D (DINOv2) avg AUC 0.820 vs. DeepCNTD 0.768.
- **Data efficiency (T3, 20% data)**: AnyMC3D (DINOv3) AUC 0.924 vs. DenseNet 0.741; outperforms DenseNet trained on 60% of data (3× data efficiency).

## Limitations
- Findings are limited to the evaluated FM backbones; other FMs may exhibit different adaptation characteristics.
- All tasks use in-domain CT/MRI; generalization to out-of-domain modalities (e.g., PET) is untested.
- Auxiliary pixel-level supervision requires expensive segmentation annotations; weaker supervision (bounding boxes, radiology report grounding) is unexplored.
- Permutation-invariant slice fusion discards through-plane ordering, which may disadvantage tasks requiring explicit inter-slice spatial reasoning.
- 2D slice-by-slice processing may underperform for tasks requiring fine-grained 3D spatial context (e.g., segmentation), which still favors 3D architectures.
- DINOv3's enhanced spatial features did not improve over DINOv2 for classification; benefit for dense 3D prediction tasks is unexplored.

## Relevance to Foundation Models in Medicine
This paper directly challenges two dominant assumptions in medical FM research: that 3D architectures are necessary for 3D tasks, and that medical-domain pretraining is essential for competitive performance. The finding that a properly adapted general-purpose 2D FM (DINOv2) matches medical-specific FMs (MII, MedGemma) shifts the locus of effort from pretraining to adaptation strategy, with significant implications for how the community should allocate investment. The AnyMC3D framework offers a practical scalability paradigm — one frozen backbone, lightweight per-task plugins — that addresses the core bottleneck of deploying FMs across the long tail of clinical 3D imaging tasks. The rigorous multi-task benchmark with realistic data sizes fills a methodological gap and provides a more honest evaluation standard than the low-data regimes that have dominated prior FM papers.

## Tags
#3d-classification #foundation-models #lora-adaptation #transfer-learning #benchmark #ct #mri #parameter-efficient
