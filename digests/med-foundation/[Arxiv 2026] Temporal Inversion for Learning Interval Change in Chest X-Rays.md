---
title: "Temporal Inversion for Learning Interval Change in Chest X-Rays"
authors: ["Hanbin Ko", "Kyungmin Jeon", "Doowoong Choi", "Chang Min Park"]
source: "Arxiv"
venue: ""
published: "2026-04-06"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2604.04563"
url: "http://arxiv.org/abs/2604.04563v2"
pdf: "paper/med-foundation/[Arxiv 2026] Temporal Inversion for Learning Interval Change in Chest X-Rays.pdf"
---

# Temporal Inversion for Learning Interval Change in Chest X-Rays

## TL;DR
TILA (Temporal Inversion-aware Learning and Alignment) is a training framework that uses reversed image-pair ordering as a supervisory signal to teach temporal VLP models directional interval-change sensitivity in paired chest X-rays. It introduces inversion-aware losses at pretraining, fine-tuning, and inference without modifying underlying architectures, improving both standard progression classification accuracy and order-consistency metrics across multiple backbones and datasets.

## Problem
Existing medical VLP models analyze CXRs in isolation or, when handling image pairs, still fail to capture the *directionality* of temporal change — they cannot distinguish "improving" from "worsening" reliably. Evaluation is also inadequate: single progression-label metrics cannot reveal whether a model genuinely understands temporal order or merely exploits entity presence and label priors. There is no standardized retrieval benchmark for temporal CXR reasoning.

## Method
TILA augments any paired-image VLP backbone (validated on BioViL-T and ALTA) with three lightweight, architecture-agnostic components:

1. **Pretraining — Change-aware Sigmoid Loss**: Builds on SigLIP contrastive loss. For *unchanged* pairs, both original and temporally-inverted image pairs are aligned with the report. For *changed* pairs, the inverted pair is treated as a negative, preventing cross-temporal alignment. Binary change labels are auto-generated from reports using Gemini 2.0 Flash.

2. **Fine-tuning — BiCE + TCL**: Bidirectional Cross-Entropy (BiCE) enforces that label predictions invert correctly when image order is reversed (improved ↔ worsened, stable → stable). Temporal Consistency Loss (TCL) adds an L2 penalty ensuring the predicted probability distributions themselves mirror under inversion at the probability level.

3. **Inference — Inversion-aware scoring**: Forward prediction is averaged with the inversion-adjusted reversed prediction (`score = ½[p(prev,cur) + S(p(cur,prev))]`), reducing order bias and prediction variance.

A new retrieval benchmark, **MS-CXR-T_retrieval**, is constructed by reformulating radiologist-annotated MS-CXR-T reports into directional variants per finding while neutralizing co-occurring findings.

## Key Contributions
- TILA framework integrating temporal inversion supervision across all three training/inference stages without architectural modification
- Change-aware Sigmoid pretraining loss distinguishing changed vs. unchanged semantics under order reversal
- BiCE + TCL fine-tuning objectives enforcing label- and probability-level inversion symmetry
- Inversion-aware evaluation protocol with four settings (Standard, Reversed, Combined, Consistency) to quantify directional reasoning
- MS-CXR-T_retrieval: reproducible pipeline for progression-aware retrieval evaluation, applicable to any annotated temporal CXR dataset
- Demonstrated transferability to binary interval-change screening (triage task)

## Results
**Retrieval (Table 1, MIMIC / CheXpert):**
- TILA improves TEM score (temporal embedding matching) while maintaining Recall@k; e.g., BioViL-T_TILA TEM: 20.8 vs. 17.1 baseline (MIMIC), 19.2 vs. 17.8 (CheXpert)

**Zero-shot classification (MS-CXR-T, Table 2):**
- BioViL-T_TILA Standard Avg: 47.2% vs. 44.0% (SigLIP baseline) vs. 37.4% (original BioViL-T)
- Consistency Avg: 30.5% (TILA) vs. 24.0% (SigLIP) vs. 11.8% (original BioViL-T)

**Supervised classification (MS-CXR-T, Table 2):**
- BioViL-T_TILA Standard Avg: 64.1% vs. 61.1% (SigLIP) vs. 60.1% (CLIP baseline)
- Consistency Avg: 57.4% (TILA) vs. 39.5% (SigLIP) vs. 42.1% (CLIP)
- ALTA_TILA Standard Avg: 63.6% vs. 61.7% (SigLIP)

**Supervised classification (Private hospital cohort, Table 2):**
- BioViL-T_TILA Standard Avg: 66.1% vs. 55.3% (SigLIP) vs. 38.9% (CNN-TF)
- Consistency Avg: 54.6% (TILA) vs. 31.1% (SigLIP) vs. 17.8% (CNN-TF)

**Binary screening (Table 4):**
- BioViL-T_TILA fine-tune AUC: 0.765 vs. 0.734 baseline (private); 0.702 vs. 0.565 (RexGradient)

**Ablation (Table 3):** Change-aware SigLIP pretraining alone raises Consistency from 39.5% → 45.4%; adding BiCE → 53.1%; adding TCL → 57.4%.

## Limitations
- Inter-reader variability in progression labels creates noisy supervision, particularly for stable/borderline cases; TILA has smaller effect on disagreement cases
- Temporal inversion does not hold clinical symmetry universally — recovery does not always mirror worsening (e.g., post-surgical or fibrotic findings), making BiCE/TCL inversion assumptions imperfect for asymmetric findings
- Lack of standardized consensus definitions for progression across findings undermines ground-truth reliability
- Evaluated only on CXRs; generalizability to other imaging modalities is untested
- LLM-generated binary change labels (Gemini 2.0 Flash) may introduce label noise in pretraining

## Relevance to Foundation Models in Medicine
TILA directly addresses a gap in medical VLP foundation models: the inability to reason about *temporal directionality* across paired studies, which is central to clinical radiology workflows. By treating temporal inversion as a self-supervisory signal rather than requiring new annotation, it offers a scalable technique compatible with any paired-image VLP backbone (BioViL-T, ALTA), positioning it as a modular upgrade layer for existing medical foundation models. The introduction of MS-CXR-T_retrieval as a reproducible evaluation protocol contributes standardization infrastructure that the field currently lacks. For researchers tracking medical foundation models, this work exemplifies how task-specific inductive biases (temporal order symmetry) can be injected into general VLP training pipelines without architectural redesign, improving both accuracy and reliability metrics relevant to clinical deployment.

## Tags
#chest-xray #temporal-reasoning #vision-language-pretraining #contrastive-learning #radiology #interval-change #medical-foundation-model #benchmark
