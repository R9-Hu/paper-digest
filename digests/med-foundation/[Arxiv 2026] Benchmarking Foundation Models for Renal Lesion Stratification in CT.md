---
title: "Benchmarking Foundation Models for Renal Lesion Stratification in CT"
authors: ["Hartmut H\u00e4ntze", "Sarah de Boer", "Myrthe Buser", "Alessa Hering", "Bram van Ginneken", "Mathias Prokop", "Jawed Nawabi", "Sebastian Ziegelmayer", "Lisa Adams", "Keno Bressem"]
source: "Arxiv"
venue: ""
published: "2026-05-08"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2605.07749"
url: "http://arxiv.org/abs/2605.07749v1"
pdf: "paper/med-foundation/[Arxiv 2026] Benchmarking Foundation Models for Renal Lesion Stratification in CT.pdf"
---

# Benchmarking Foundation Models for Renal Lesion Stratification in CT

## TL;DR
This paper benchmarks three open-source medical foundation models (FMCIB, CT-FM, MMM) against a radiomics classifier and a from-scratch 3D ResNet-50 for six-class renal lesion stratification in CT, using a frozen feature-probing protocol. On an external TCIA test set (234 lesions), all FMs matched the ResNet baseline (AUC 0.70–0.77 vs. 0.72) but were significantly outperformed by handcrafted radiomics (AUC 0.88). Radiomics remains state-of-the-art for this texture-dependent task.

## Problem
Renal lesion subtype classification in CT is constrained by severe data scarcity for rare histological subtypes (e.g., renal oncocytoma: as few as 17 cases in some studies), making from-scratch deep learning unreliable. Medical foundation models promise robust transfer to data-scarce tasks, but their actual utility for fine-grained renal lesion stratification had not been rigorously benchmarked against established conventional baselines.

## Method
Frozen feature-probing (Strategy B) was the primary protocol: embeddings from three FMs (FMCIB: 4096-d, CT-FM: 512-d, MMM: 1024-d aggregated via max-pooling and lesion-area-weighted average) were extracted from lesion-cropped 3D CT volumes and fed to XGBoost classifiers tuned via 10-fold cross-validation. A 107-feature PyRadiomics pipeline (resampled to 1 mm isotropic, soft-tissue window) and a 3D ResNet-50 trained from scratch served as baselines. FMCIB was additionally fine-tuned end-to-end (Strategy A) for comparison. Training used 2,854 lesions (in-house + KiTS23); external evaluation used 234 lesions from TCIA. Statistical comparison used a max-type percentile bootstrap with family-wise error rate control.

## Key Contributions
- Systematic frozen-probing benchmark of three open-source CT foundation models (FMCIB, CT-FM, MMM) on a clinically relevant six-class renal lesion task with external validation.
- Demonstrates that FM embeddings match from-scratch ResNet performance (AUC 0.70–0.77 vs. 0.72) while requiring only CPU-seconds of classifier training after one-time feature extraction (vs. 16 GPU-hours for ResNet).
- Shows radiomics significantly outperforms all deep learning approaches (AUC 0.88 vs. best FM 0.77; Δ=0.11, 95% CI [0.03, 0.18], p=0.002).
- Feature importance analysis reveals texture features dominate radiomics predictions (65% relative importance), explaining the performance gap with generalist FM embeddings.
- Open-source RenalVision framework released with model weights and inference code.

## Results
- **Radiomics (XGBoost):** AUC 0.88 (95% CI 0.85–0.91), AP 0.64 — best overall on external TCIA set.
- **MMM (best FM):** AUC 0.77 (95% CI 0.73–0.82), AP 0.50.
- **CT-FM:** AUC 0.70 (95% CI 0.65–0.74), AP 0.43.
- **FMCIB (probing):** AUC 0.69 (95% CI 0.64–0.74), AP 0.40.
- **FMCIB (fine-tuned):** AUC 0.70 (95% CI 0.64–0.75), AP 0.42.
- **ResNet-50 (scratch):** AUC 0.72 (95% CI 0.68–0.77), AP 0.45.
- Radiomics vs. all FMs statistically significant (p ≤ 0.002); FMs vs. ResNet non-significant (p = 0.31–0.98).
- Class-wise (radiomics, external): cysts AUC 0.93, ccRCC AUC 0.84, pRCC AUC 0.90 (AP 0.58), chrRCC AUC 0.86 (AP 0.30 — low precision reflects class imbalance).
- Internal validation (6-class): radiomics AUC 0.84, MMM 0.75, ResNet 0.64.

## Limitations
- External TCIA set covers only four of six classes (no RO or "Other"), limiting evaluation of rare subtypes.
- Training data histopathologically confirmed, introducing selection bias toward ambiguous/atypical lesions; real screening performance may differ.
- No consensus on FM implementation details (patch size, resampling, normalization, aggregation), making FM-to-FM comparisons confounded by hyperparameter sensitivity rather than architecture alone.
- Low AP values across all models (including radiomics) indicate high false-positive rates precluding autonomous clinical use.
- Frozen-probing may underestimate FM potential; fine-tuning did not help here but may be architecture/data dependent.
- FMCIB fine-tuning used author-recommended settings; other FMs were not fine-tuned, limiting Strategy A comparisons.

## Relevance to Foundation Models in Medicine
This paper provides direct empirical evidence that current generalist CT foundation models do not yet surpass hand-engineered radiomics for fine-grained, texture-critical lesion classification — a finding that challenges the assumption that FM pretraining generalizes to all clinically relevant tasks. It highlights a key architectural gap: FMs pretrained on large anatomical contexts may not optimize for intra-lesion microstructure, which is the discriminative signal for histological subtype stratification. For researchers tracking medical FMs, the computational efficiency finding is practically significant: FM probing achieves ResNet-level performance at a fraction of the compute, even if the ceiling remains below radiomics. The call for standardized "instructions for use" for medical FM benchmarking is an important methodological contribution to the field.

## Tags
#ct-imaging #foundation-models #radiomics #renal-lesion #benchmarking #feature-probing #cancer-imaging #transfer-learning
