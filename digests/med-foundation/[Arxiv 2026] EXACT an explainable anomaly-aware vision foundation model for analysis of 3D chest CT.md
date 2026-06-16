---
title: "EXACT: an explainable anomaly-aware vision foundation model for analysis of 3D chest CT"
authors: ["Xuguang Bai", "Mingxuan Liu", "Tongxi Song", "Yifei Chen", "Hongjia Yang", "Kasidit Anmahapong", "Zihan Li", "Ying Zhou", "Qiyuan Tian"]
source: "Arxiv"
venue: ""
published: "2026-04-27"
published_time: "2026-04-27T07:57:47+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2604.24146"
url: "http://arxiv.org/abs/2604.24146v1"
pdf: "paper/med-foundation/[Arxiv 2026] EXACT an explainable anomaly-aware vision foundation model for analysis of 3D chest CT.pdf"
---

# EXACT: an explainable anomaly-aware vision foundation model for analysis of 3D chest CT

*🕒 **Published (v1):** 2026-04-27 07:57 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2604.24146v1)*

## TL;DR
EXACT is a 3D chest CT foundation model that produces intrinsic voxel-level anomaly-aware maps (AAmaps) via anatomy-constrained weakly supervised learning on CT-report pairs, without any manual voxel annotations. Unlike CLIP-based models that compress volumetric features into 1D embeddings, EXACT's Y-Mamba dual-decoder architecture jointly performs organ segmentation and multi-instance anomaly localization, enabling zero-shot diagnosis, lesion localization, and spatially grounded report generation. Evaluated across multinational multi-center cohorts, it consistently outperforms all compared 3D medical foundation models.

## Problem
Existing 3D chest CT foundation models (CT-CLIP, fVLM, MedVista3D, T3D, Merlin) rely on CLIP-style contrastive objectives that compress volumetric features into compact 1D embeddings via global pooling or [CLS] tokens, irreversibly discarding voxel-level spatial structure. This limits their ability to localize spatially sparse or organ-confined pathologies under domain shift, and forces interpretability onto post-hoc gradient methods (Grad-CAM) that produce diffuse, clinically uninformative heatmaps. Task-specific models are annotation-expensive and non-generalizable.

## Method
EXACT uses a Y-Mamba backbone with a shared encoder branching into two decoders: an organ segmentation decoder and a multi-instance anomaly detection (MIL) decoder. Pre-trained end-to-end on 25,692 CT-report pairs from CT-RATE using:
- **Organ masks**: auto-derived from Segment Anything by Text (no manual annotation)
- **Disease pseudo-labels**: extracted from radiology reports via fine-tuned RadBERT for 18 target abnormalities with predefined organ-disease mappings

The MIL decoder treats each organ region as an instance bag, confining disease evidence to anatomically plausible tissue. The output is 18 disease-specific AAmaps (voxel-level anomaly scores) multiplied element-wise by the corresponding organ mask to suppress background noise. For zero-shot diagnosis, organ-guided top-k aggregation of AAmaps produces scan-level predictions. For report generation, EXACT-CHAT integrates the frozen EXACT encoder with a multimodal projector and LLaMA-3.1-8B-Instruct, augmented with structured AAmap-derived diagnostic priors; an optional GPT-4.1 refinement step corrects missed/hallucinated findings.

## Key Contributions
- First 3D chest CT foundation model achieving intrinsic voxel-level anomaly localization from image-level text supervision only, without any manual voxel masks
- Y-Mamba dual-decoder architecture that preserves full voxel-level spatial resolution throughout decoding
- Anatomy-constrained MIL framework that confines disease evidence to organ-specific regions, improving sensitivity to spatially sparse/localized pathologies under domain shift
- EXACT-CHAT: multimodal assistant with AAmap-derived diagnostic priors reducing hallucination and improving clinical fidelity vs. CLIP-encoder-based report generators
- Multinational multi-center benchmark across 5 tasks (zero-shot/fine-tuned diagnosis, zero-shot/fine-tuned localization, report generation) spanning Turkey, US, China, Russia

## Results
**Multi-disease diagnosis (18 abnormalities):**
- Zero-shot AUROC: 0.830 on CT-RATE (internal), vs. fVLM 0.778, CT-CLIP 0.731, and even supervised T3D 0.802
- Zero-shot AUROC: 0.728 on RAD-ChestCT (external), vs. MedVista3D 0.710; all baselines ≤0.720
- Zero-shot AUROC: 0.758 on MianYang (external), vs. fVLM 0.716, CT-CLIP 0.712
- Fine-tuning AUROC: 0.833 / 0.734 / 0.769 on CT-RATE / RAD-ChestCT / MianYang (best across all models)
- Notably, EXACT zero-shot outperforms all baselines including fully supervised ones on CT-RATE

**Zero-shot anomaly localization:**
- COVID-19 (n=20): DSC 0.435 vs. BiomedParse-v2 0.340; Hit Rate@5% 0.950 vs. 0.550
- MosMed (n=50): DSC 0.363 vs. BiomedParse-v2 0.254; Hit Rate@5% 0.960 vs. 0.840
- CT-CLIP near-zero DSCs (0.004–0.023) across all localization datasets

**Supervised segmentation (EXACT-Seg):**
- COVID-19: DSC 0.476 vs. SegMamba 0.332 (+43.4%, P<0.001); AUPR 0.529 vs. 0.358
- MosMed: DSC 0.454 vs. SegMamba 0.352 (P<0.001)
- ReX-Val (internal): DSC 0.215 vs. SegMamba 0.198 (P=0.028)

**Report generation (RadBERT-F1, clinical efficacy primary metric):**
- CT-RATE: EXACT-CHAT (Refined) RadBERT-F1 0.501 vs. CT-CHAT 0.305, CT-GRAPH 0.296, T3D 0.274
- RAD-ChestCT: RadBERT-F1 0.441 vs. Hulu-Med 0.279
- MianYang: RadBERT-F1 0.410 vs. Hulu-Med 0.175; CT-CHAT 0.073, Merlin 0.024

## Limitations
- RadBERT-dependent label extraction for pre-training pseudo-labels; may be superseded by general-purpose LLMs
- Requires manual pre-definition of 18 target abnormalities and organ-disease mappings, limiting scalability to rare or unlisted pathologies
- All evaluations retrospective; no prospective clinical validation of impact on radiologist workflow or patient outcomes
- COVID-19 external localization improvements did not reach statistical significance (n=20, underpowered)
- Pre-training restricted to non-contrast CT from a single source dataset (CT-RATE); contrast-enhanced or other CT protocols not evaluated

## Relevance to Foundation Models in Medicine
EXACT directly challenges the dominant paradigm of transplanting CLIP-based vision-language pre-training from natural images to volumetric medical imaging, demonstrating that anatomy-aware weakly supervised MIL is a superior alternative for tasks requiring spatial precision. The anatomy-constrained AAmap approach—generating intrinsic voxel-level representations without any dense annotation—offers a scalable pre-training paradigm relevant to any 3D medical imaging modality where anatomical priors can be automatically derived. The integration of spatial diagnostic priors into multimodal LLMs (EXACT-CHAT) provides a template for grounding clinical report generation in verifiable spatial evidence, directly addressing the hallucination and clinical fidelity gap that plagues CLIP-encoder-based medical MLLMs under distribution shift.

## Tags
#chest-ct #foundation-model #anomaly-detection #weakly-supervised #voxel-level-localization #report-generation #explainability #multi-instance-learning
