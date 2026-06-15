---
title: "Learning Generalizable 3D Medical Image Representations from Mask-Guided Self-Supervision"
authors: ["Yunhe Gao", "Yabin Zhang", "Chong Wang", "Jiaming Liu", "Maya Varma", "Jean-Benoit Delbrouck", "Akshay Chaudhari", "Curtis Langlotz"]
source: "Arxiv"
venue: "CVPR 2026"
published: "2026-03-14"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2603.13660"
url: "http://arxiv.org/abs/2603.13660v1"
pdf: "paper/med-foundation/[Arxiv 2026] Learning Generalizable 3D Medical Image Representations from Mask-Guided Self-Supervision.pdf"
---

# Learning Generalizable 3D Medical Image Representations from Mask-Guided Self-Supervision

## TL;DR
MASS (MAsk-guided Self-Supervised learning) is a self-supervised pretraining framework for 3D medical imaging that uses in-context segmentation as its pretext task, driven entirely by automatically generated class-agnostic masks from SAM2 — no expert annotations required. It learns semantically rich, spatially-precise representations that generalize to few-shot segmentation and frozen-encoder classification on unseen pathologies, outperforming all SSL baselines by wide margins and rivaling supervised pretraining methods in low-data regimes.

## Problem
Existing SSL methods for 3D medical imaging (reconstruction-based like MAE, contrastive like SimCLR) optimize for global or low-level features and fail to capture anatomically grounded semantics. Supervised pretraining is constrained by expensive expert annotations and fixed taxonomies, preventing generalization to novel structures or modalities at scale.

## Method
MASS formulates pretraining as in-context segmentation (ICS): given a reference image-mask pair `(x_s, y_s)`, predict the same masked region in an augmented query view `x_q`. Masks are generated annotation-free by applying SAM2 in automatic mode on 2D slices sampled from unlabeled 3D volumes, then propagating masks volumetrically via SAM2's video prediction — yielding hundreds to thousands of class-agnostic 3D masks per volume. These noisy, unlabeled masks serve as structural anchors. During training, augmented reference/query pairs are created; the encoder `E_θ` extracts features, a task-encoding module `T_φ` computes a task embedding from the reference mask, and a decoder `D_ψ` predicts the query mask. The loss is Dice + BCE. Appearance augmentations (brightness, contrast, noise) and spatial augmentations (rotation, scaling, translation) force the model to learn what remains invariant across views — the semantic identity of structures — without any semantic label supervision. The architecture follows Iris (3D ResUNet backbone). Pretraining scales from 20–200 scans per individual dataset to 5K multi-modal CT/MRI/PET volumes.

## Key Contributions
- Novel SSL pretext task for 3D medical imaging: in-context segmentation driven by auto-generated class-agnostic masks (SAM2), eliminating need for expert annotations.
- Annotation-free mask pipeline that scales across modalities (CT, MRI, PET) and anatomical regions without predefined taxonomies.
- MASS-IC (training-free few-shot inference) and MASS-FT (parameter-efficient finetuning) deployment modes from a single pretrained model.
- Demonstrates that mask quality need not be high: masks with only 7–15% average Dice overlap with ground truth still yield strong learned representations.
- Demonstrates that data diversity (anatomical and modality breadth) matters more than raw data volume.

## Results
- **BCV 1-shot segmentation**: MASS-FT 68.8% Dice vs. best SSL baseline (SimCLR) 44.9% — **+23.9 points**; MASS-IC without any finetuning: 65.5%, surpassing all baselines.
- **BCV 10-shot (large-scale pretraining)**: MASS-FT 70.2% vs. Merlin 50.1%, AnatoMix 53.1% — approaches full supervision (83.6% with 23 labeled scans).
- **AMOS MR 1-shot (large-scale)**: MASS-FT 74.3% vs. best SSL baseline 38.8% — **+35.5 points**.
- **KiTS tumor 30-shot**: MASS-FT 70.0% vs. full supervision 81.7% [159 labels]; best SSL baseline 62.7%.
- **Pelvic 1-shot (OOD, large-scale)**: MASS-FT 92.8% vs. supervised Iris 86.9%, SuPreM 85.4%.
- **Frozen-encoder classification, RSNA ICH 5% data (761 scans)**: MASS 75.4% AUC vs. full training from scratch 72.8%, SuPreM 73.5% — best among all methods.
- **Trauma detection, 30% data**: MASS frozen encoder — liver 86.7% vs. full training 74.4%, kidney 82.9% vs. 75.0%, spleen 85.5% vs. 82.1%.
- Mask quality robustness: BCV masks average only 15.2% Dice overlap with GT; MASS still achieves 65.5% 1-shot ICS.
- Architecture-agnostic: ResUNet vs. I3DResNet152 differ by only 1.31 Dice points on segmentation.

## Limitations
- No expert annotation is used during pretraining by design, but combining auto-masks with expert annotations as a synergistic hybrid is unexplored.
- MASS-IC (training-free) fails on highly variable pathological structures (e.g., KiTS tumors: 2.7% 1-shot); finetuning is required for pathology tasks.
- Pretraining corpus is 5K volumes — large-scale SSL baselines (OpenMind: 114K images) are not matched for scale, making comparisons partially confounded.
- No vision-language alignment; learned representations are not connected to radiology reports or textual semantics.
- SAM2 introduces a domain gap (trained on natural images) that produces coarse, noisy masks; performance ceiling may depend on mask generator quality.

## Relevance to Foundation Models in Medicine
MASS directly addresses one of the core bottlenecks for 3D medical image foundation models: the prohibitive cost of pixel-wise expert annotation. By replacing supervised signals with auto-generated class-agnostic masks and an in-context segmentation pretext task, it offers a scalable path to general-purpose encoders that transfer to both segmentation and classification without task-specific pretraining. The work is positioned in a growing cluster alongside Merlin, SuPreM, and Iris, but is the first to demonstrate that annotation-free SSL can approach — and in OOD settings exceed — supervised pretraining methods on 3D volumetric data. The insight that diversity outweighs data volume is directly relevant to dataset curation strategies for future medical foundation models.

## Tags
#self-supervised-learning #3d-medical-imaging #segmentation #few-shot-learning #foundation-model #annotation-free #in-context-learning #representation-learning
