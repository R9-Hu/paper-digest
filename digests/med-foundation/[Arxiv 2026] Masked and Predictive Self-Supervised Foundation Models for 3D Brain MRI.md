---
title: "Masked and Predictive Self-Supervised Foundation Models for 3D Brain MRI"
authors: ["Esra Erg\u00fcn", "Hersh Chandarana", "Dan Sodickson", "G\u00f6zde \u00dcnal"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T13:09:59+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2606.13315"
url: "http://arxiv.org/abs/2606.13315v1"
pdf: "paper/med-foundation/[Arxiv 2026] Masked and Predictive Self-Supervised Foundation Models for 3D Brain MRI.pdf"
---

# Masked and Predictive Self-Supervised Foundation Models for 3D Brain MRI

*🕒 **Published (v1):** 2026-06-11 13:09 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13315v1)*

## TL;DR
This paper systematically compares two self-supervised pretraining paradigms—Masked Autoencoders (MAE) and Joint Embedding Predictive Architectures (JEPA)—for 3D structural brain MRI disease detection, pretrained on ~58k heterogeneous MRI volumes. Two auxiliary objectives are introduced: a spectral-domain reconstruction loss for MAE and variance–covariance regularization (VCR) for JEPA. MAE with spectral supervision consistently outperforms JEPA for MRI-based disease detection, and the benefit of each objective is shown to be conditioned on the pathological structure of the downstream task.

## Problem
Existing MRI foundation model work has concentrated on segmentation and dense prediction; systematic investigation of self-supervised pretraining specifically for disease detection (Alzheimer's, MCI, autism, tumor grading) is absent. Additionally, no controlled side-by-side comparison of MAE and JEPA has been performed for structural 3D MRI, and the role of auxiliary pretraining objectives in shaping downstream transfer behavior across tasks with heterogeneous pathological signals is poorly understood.

## Method
**Pretraining data:** 58,781 3D MRI volumes (T1, T2, FLAIR, T2*) from 7 neuroimaging datasets (ADNI, NACC/SCAN, PPMI, OASIS-3, IXI, MOOD, BraTS-2024), processed as single-contrast inputs without spatial normalization, intensity harmonization, or modality concatenation. Volumes are processed with randomized native in-plane orientation sampling and fixed-size cropping (160×160) + depth interpolation (64 slices).

**MAE baseline:** Standard ViT-based masked autoencoder with 3D volumetric patch masking adapted from V-JEPA's spatiotemporal block masking strategy (75% masking). Loss is pixel-wise MSE (L_MAE).

**SL-MAE (spectral loss augmentation):** Adds a 3D FFT-based spectral loss (L_spec) computed on the log-magnitude high-pass filtered spectra of reconstructed vs. original volumes, encouraging sensitivity to high-frequency anatomical detail. L_spec is amortized—computed every n iterations and cached—to limit compute overhead. Final loss: L_Total = L_MAE + λ_FFT · L_spec.

**JEPA baseline:** Student–teacher architecture where the student encoder predicts EMA-teacher latent representations of masked 3D MRI target regions, optimized with L1 loss and stop-gradient on the teacher (following V-JEPA).

**JEPA+VCR:** Adds variance–covariance regularization to the JEPA latent space: a variance term enforces per-dimension spread across samples; a covariance term penalizes off-diagonal covariance to discourage feature redundancy. Applied jointly to concatenated context and target encoder representations.

**Downstream evaluation:** Pretrained encoder (frozen or fine-tuned) + lightweight Attentive Classifier, evaluated on five binary/multiclass disease classification tasks across ADNI, NACC/SCAN, UCSF-PDGM, and ABIDE using AUROC, accuracy, and F1. Subject-level splits are enforced to prevent leakage.

## Key Contributions
- First controlled comparison of MAE vs. JEPA as primary self-supervised pretraining paradigms for 3D structural MRI disease detection.
- Novel spectral-domain auxiliary loss (3D FFT + log-magnitude + high-pass filter + amortized computation) for MAE to explicitly supervise high-frequency anatomical structure.
- Integration of variance–covariance regularization (VCR) into a 3D MRI JEPA framework to promote decorrelated, distributed latent representations.
- Contrast-agnostic, normalization-free pretraining framework using single-channel MRI and randomized native orientation sampling; accommodates incomplete contrast series.
- Empirical demonstration that the downstream benefit of each SSL objective is conditioned on the pathological structure of the task (frequency content, feature dimensionality of discriminative signal).
- Public release of all subject-level pretraining and downstream train/validation/test splits for reproducibility.

## Results
*(The results section of the provided text is truncated; only qualitative findings from the abstract are available.)*

- MAE with spectral-domain supervision (SL-MAE) **consistently achieves superior downstream performance** over JEPA across MRI-based disease detection tasks.
- Spectral regularization yields the **largest improvements when downstream discriminative signal is characterized by strong high-frequency anatomical structures**.
- Variance–covariance regularization in JEPA is **most beneficial when discriminative information spans multiple decorrelated feature dimensions**.
- The relative benefit of each auxiliary objective is **not uniform across tasks**—performance patterns depend on task-specific pathological structure.
- No specific AUROC/accuracy/F1 numbers are present in the provided excerpt.

## Limitations
- Results section is not fully available in the provided text; specific benchmark numbers cannot be assessed.
- Pretraining is restricted to 3D structural MRI (brain); generalizability to other organs or modalities (CT, fMRI) is not examined.
- Contrast-agnostic single-channel design, while flexible, does not exploit complementary information across simultaneously acquired contrasts.
- Comparison is limited to MAE and JEPA; contrastive methods (SimCLR, DINO) and hybrid approaches are not benchmarked as primary alternatives.
- Downstream task set covers four neurological/oncological conditions; broader clinical coverage would strengthen generalizability claims.
- The amortized spectral loss introduces a design hyperparameter (period n) whose sensitivity is not analyzed in the provided text.

## Relevance to Foundation Models in Medicine
This work directly advances medical foundation model research by addressing the underexplored problem of SSL pretraining for disease detection (as opposed to segmentation), the dominant benchmark in MRI SSL literature. The finding that MAE with frequency-domain supervision outperforms JEPA—despite JEPA's strong track record in natural image modeling—illustrates that SSL objective design must account for the statistical and spectral properties of medical images rather than importing strategies from natural vision. The principle that the utility of a pretraining objective is conditioned on downstream task structure is a generalized design insight applicable to foundation model development across medical imaging modalities. The contrast-agnostic, normalization-free framework also advances clinical deployability of MRI foundation models by reducing preprocessing assumptions.

## Tags
#foundation-models #self-supervised-learning #brain-mri #masked-autoencoders #jepa #disease-detection #neuroimaging #3d-medical-imaging
