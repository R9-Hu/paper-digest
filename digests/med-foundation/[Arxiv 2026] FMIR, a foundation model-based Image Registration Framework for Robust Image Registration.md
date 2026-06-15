---
title: "FMIR, a foundation model-based Image Registration Framework for Robust Image Registration"
authors: ["Fengting Zhang", "Yue He", "Qinghao Liu", "Yaonan Wang", "Xiang Chen", "Hang Zhang"]
source: "Arxiv"
venue: "ISBI 2026"
published: "2026-01-24"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2601.17529"
url: "http://arxiv.org/abs/2601.17529v2"
pdf: "paper/med-foundation/[Arxiv 2026] FMIR, a foundation model-based Image Registration Framework for Robust Image Registration.pdf"
---

# FMIR, a foundation model-based Image Registration Framework for Robust Image Registration

## TL;DR
FMIR is a medical image registration framework that adapts frozen 2D foundation model encoders (DINO, SAM) for 3D volumetric registration via slice-wise feature extraction and a pyramid-based registration head. Trained on a single dataset, it achieves state-of-the-art in-domain performance while generalizing robustly to out-of-domain imaging modalities and anatomies. A channel regularization strategy — random channel dropout during training, PCA during inference — is the key mechanism driving cross-domain generalization.

## Problem
Deep learning registration models assume training and test data are i.i.d., causing catastrophic failure on out-of-domain images (different modality, anatomy, or scanner). Existing registration foundation models (e.g., uniGradICON) address this but require complex architectures and long inference times. There is no lightweight framework for adapting general-purpose vision foundation models to robust medical image registration.

## Method
FMIR has two modules:

1. **Foundation Model-based Encoder**: A frozen 2D foundation model (DINO ViT-B or SAM) processes each 3D volume slice-by-slice (after padding to K×K=512×512). Per-slice features are reduced to 256 channels via channel regularization, then reassembled into 3D volumes and passed through a 3-layer 3D conv block (output: n=32 channels) to restore local volumetric context.

2. **Registration Head**: A five-level coarse-to-fine pyramid structure. At each scale, a 3-layer conv block predicts a residual deformation field; fields are composed progressively from coarse to fine. The head is backbone-agnostic — PCA or random channel selection standardizes features from any encoder.

**Channel Regularization (CR)**: During training, a random subset of the 256 feature channels is selected per forward pass (stochastic "channel dropout"), preventing reliance on fixed channel patterns. During inference, PCA selects the top channels deterministically. This train/test discrepancy suppresses dataset-specific biases and forces learning of structural correspondences.

Loss: NCC + Dice (weakly supervised) + diffusion-based smoothness regularization.

## Key Contributions
- Framework for plugging frozen 2D foundation model encoders (DINO, SAM) into 3D medical image registration via slice-wise processing and 3D context recovery.
- Backbone-agnostic pyramid registration head compatible with any foundation encoder without structural changes.
- Channel regularization strategy that explicitly differentiates training and inference feature selection to suppress domain-specific priors and improve cross-domain generalization.
- Demonstration that a model trained on a single dataset (cardiac MR or abdominal CT) can generalize across anatomies and modalities.

## Results
**In-domain (ACDC cardiac MR, Dice ↑):**
- FMIR (DINO): **79.82%** vs. uniGradICON 78.89%, RDP 78.06%, CorrMLP 77.31%, VoxelMorph 75.26%
- FMIR inference time: 0.62s vs. uniGradICON 4.95s

**Out-of-domain generalization (Table 2, cross-dataset):**
- FMIR trained on abdominal CT, tested on ACDC cardiac: ~73% Dice — comparable to TransMorph trained directly on ACDC (~75%)
- Removing CR ('-CR') causes severe out-of-domain performance degradation, especially with SAM backbone
- Unsupervised training generalizes better out-of-domain than weakly supervised training; hybrid (ACDC+Abdomen) training underperforms single-dataset training for each respective test set

**Backbone interoperability:**
- FMIR trained on DINO features, tested with SAM features (no retraining): comparable Dice to DINO-trained inference

## Limitations
- Slice-wise 2D processing of 3D volumes sacrifices native 3D spatial context; recovered only partially by a shallow 3D conv block.
- Only validated on two datasets (cardiac MR, abdominal CT); anatomies tested are limited.
- Hybrid multi-anatomy training degrades rather than improves performance, suggesting the framework does not yet scale to multi-domain joint training.
- Weakly supervised training (which uses segmentation labels) improves in-domain performance but hurts out-of-domain generalization — trade-off not fully resolved.
- Foundation models used (DINO ViT-B, SAM) were pre-trained on natural images; domain gap to medical imaging is handled implicitly but not explicitly studied.
- No evaluation on multi-modal registration (e.g., MR-CT).

## Relevance to Foundation Models in Medicine
FMIR demonstrates a resource-efficient paradigm for repurposing general-purpose vision foundation models for a medical task (registration) that has been largely overlooked compared to segmentation. The channel regularization mechanism is a lightweight, generalizable technique for suppressing dataset-specific priors that could transfer to other medical foundation model adaptation settings. The plug-and-play backbone compatibility (DINO↔SAM) without retraining is relevant to the broader question of how to build modality-agnostic medical AI. This work also highlights that unsupervised objectives generalize better out-of-domain than label-supervised ones — an important design consideration for medical foundation model fine-tuning.

## Tags
#image-registration #foundation-model-adaptation #domain-generalization #dino #sam #deformable-registration #medical-imaging #cross-domain
