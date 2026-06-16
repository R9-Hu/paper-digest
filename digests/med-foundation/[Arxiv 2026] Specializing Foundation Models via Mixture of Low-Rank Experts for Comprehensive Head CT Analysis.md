---
title: "Specializing Foundation Models via Mixture of Low-Rank Experts for Comprehensive Head CT Analysis"
authors: ["Youngjin Yoo", "Han Liu", "Bogdan Georgescu", "Yanbo Zhang", "Sasa Grbic", "Michael Baumgartner", "Thomas J. Re", "Jyotipriya Das", "Poikavila Ullaskrishnan", "Eva Eibenberger", "Andrei Chekkoury", "Uttam K. Bodanapally", "Savvas Nicolaou", "Pina C. Sanelli", "Thomas J. Schroeppel", "Yvonne W. Lui", "Eli Gibson"]
source: "Arxiv"
venue: ""
published: "2026-02-28"
published_time: "2026-02-28T14:32:38+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2603.00675"
url: "http://arxiv.org/abs/2603.00675v1"
pdf: "paper/med-foundation/[Arxiv 2026] Specializing Foundation Models via Mixture of Low-Rank Experts for Comprehensive Head CT Analysis.pdf"
---

# Specializing Foundation Models via Mixture of Low-Rank Experts for Comprehensive Head CT Analysis

*🕒 **Published (v1):** 2026-02-28 14:32 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2603.00675v1)*

## TL;DR
MoLRE (Mixture of Low-Rank Experts) extends LoRA with K specialized low-rank adapters and unsupervised soft routing, enabling input-conditional feature adaptation for multi-label head CT finding detection with <0.5% additional parameters. Benchmarked across six foundation models (7M–431M params) on 72,756 head CTs with 75 neurological findings, MoLRE consistently improves AUC across all compatible models, with MedGemma+MoLRE achieving 0.917 mean AUC.

## Problem
Standard LoRA applies a uniform low-rank update to all inputs, causing knowledge interference when a single adaptation must simultaneously handle pathologically diverse findings (acute hemorrhage, chronic ischemia, trauma, structural abnormalities). Existing work on foundation model adaptation to complex multi-label clinical head CT tasks—involving dozens of heterogeneous findings—is understudied.

## Method
MoLRE replaces the single LoRA update with K=6 parallel low-rank expert adapters (rank r=8 each), combined via a soft router: a two-layer MLP with softmax output that assigns per-input mixing weights without explicit pathology supervision. The adapted output is `h = W₀x + Σ gᵢ(x)·ΔWᵢx`, where routing is learned end-to-end via multi-label focal loss (γ=2.0, prevalence-based class weights). For 2D models, routing operates at the slice level before attention-weighted pooling aggregates slice features into volume representations; for 3D models (Pillar0-HeadCT), routing operates on the spatially-pooled volume embedding. Labels for 75 findings were extracted from radiology reports using GPT-4-mini, validated at 0.986 finding-level accuracy on 90 neuroradiologist-annotated cases.

## Key Contributions
- MoLRE framework: conditionally routed, parameter-efficient LoRA extension with unsupervised expert routing (<0.5% additional parameters)
- Large-scale benchmark across six foundation models (DINOv3-Base/Large, MedImageInsight, MedGemma, Pillar0-HeadCT, DeepCNTD) spanning 2D/3D, general/medical/CT-specific pretraining, 7M–431M parameters
- Dataset: 72,756 NCCT scans from 9 centers, 75 annotated neurological findings across 6 pathology categories
- State-of-the-art 0.917 mean AUC with MedGemma+MoLRE
- Empirical characterization of when and why conditional adaptation helps (pretraining domain × architecture × scale interactions)

## Results
- MedGemma+MoLRE: **0.917 AUC** (vs. 0.874 baseline, +4.3%)
- DINOv3-Base+MoLRE: 0.902 AUC (vs. 0.856, **+4.6%** — largest absolute gain)
- DINOv3-Large+MoLRE: 0.913 AUC (vs. 0.910, +0.3%)
- MedImageInsight+MoLRE: 0.876 AUC (vs. 0.863, +1.3%)
- Pillar0-HeadCT+MoLRE: 0.893 AUC (vs. 0.891, +0.2% — 3D volumetric model, diminished gains)
- MoLRE shifts findings into high-confidence regime (AUC ≥ 0.90): DINOv3-Base: 33→43 findings; MedGemma: 35→48 findings
- Largest per-finding gains for visually subtle/rare findings: early ischemic signs, venous sinus thrombosis, lipomas, occult bone lesions

## Limitations
- MoLRE inapplicable to DeepCNTD (no attention pooling), limiting benchmark completeness
- 3D volumetric models gain minimally because progressive spatial pooling collapses the feature heterogeneity that enables effective expert routing
- Labels derived from NLP extraction of radiology reports (GPT-4-mini), not primary radiologist annotation—introduces labeling noise
- Dataset limited to non-contrast head CT; generalizability to other modalities or anatomies not demonstrated
- Routing mechanism is fully unsupervised—no analysis of what pathology clusters emerge per expert or interpretability of routing decisions
- All data from Siemens Healthineers infrastructure; cross-vendor generalization beyond GE/Canon in preprocessing is not independently evaluated

## Relevance to Foundation Models in Medicine
MoLRE addresses a fundamental tension in medical foundation model adaptation: PEFT methods that treat all inputs uniformly are ill-suited for multi-label clinical tasks with heterogeneous pathology. The systematic cross-model benchmark reveals that adaptation benefit depends non-trivially on pretraining domain and architecture—generatively pretrained models (MedGemma) gain the most, while task-specialized 3D models gain the least—providing actionable guidance for practitioners selecting and fine-tuning foundation models. The finding that <0.5% additional parameters suffice for conditional specialization is directly relevant to resource-constrained clinical deployment. This work extends the growing literature on mixture-of-experts for medical imaging and provides one of the largest-scale multi-label head CT benchmarks to date.

## Tags
#peft #lora #mixture-of-experts #head-ct #multi-label-detection #radiology #parameter-efficient-finetuning #benchmarking
