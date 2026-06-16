---
title: "Uncovering Modality Discrepancy and Generalization Illusion for General-Purpose 3D Medical Segmentation"
authors: ["Yichi Zhang", "Feiyang Xiao", "Le Xue", "Wenbo Zhang", "Gang Feng", "Chenguang Zheng", "Yuan Qi", "Yuan Cheng", "Zixin Hu"]
source: "Arxiv"
venue: ""
published: "2026-02-07"
published_time: "2026-02-07T17:54:10+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2602.07643"
url: "http://arxiv.org/abs/2602.07643v1"
pdf: "paper/med-foundation/[Arxiv 2026] Uncovering Modality Discrepancy and Generalization Illusion for General-Purpose 3D Medical Segmentation.pdf"
---

# Uncovering Modality Discrepancy and Generalization Illusion for General-Purpose 3D Medical Segmentation

*🕒 **Published (v1):** 2026-02-07 17:54 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2602.07643v1)*

## TL;DR
Current 3D medical segmentation foundation models claim general-purpose capability but are overwhelmingly trained and validated on structural imaging (CT/MRI), leaving functional imaging (PET) almost entirely unaddressed. This paper constructs the UMD benchmark—paired PET/CT and PET/MRI whole-body scans from the same subjects—to isolate imaging modality as the primary variable, revealing catastrophic performance collapse when state-of-the-art models are applied to PET. The findings expose a "generalization illusion" in which high benchmark scores on curated structural data do not transfer to functional or out-of-distribution clinical scenarios.

## Problem
Existing evaluations of 3D medical segmentation foundation models entangle modality with anatomical task complexity: CT is used for abdominal organs, MRI for cardiac/neurological structures, making it impossible to isolate modality as a variable. PET, which captures metabolic activity rather than anatomical density, is essentially absent from training and evaluation corpora. Furthermore, test sets often overlap with or resemble pre-training distributions, inflating reported performance and masking true zero-shot generalization ability.

## Method
The authors curate the **UMD dataset**: 490 whole-body PET/CT and 464 whole-body PET/MRI scans, each acquired from the same subject in a single diagnostic session (Siemens Biograph 64 for PET/CT; 3.0T Siemens Biograph mMR for PET/MRI). Voxel-wise annotations cover 13 organs (liver, kidneys, brain, heart, spleen, aorta, lung, colon, bladder, pancreas, esophagus, stomach). Intra-subject pairing guarantees identical anatomy, orientation, and scale across structural and functional volumes, so modality is the sole independent variable. Five representative foundation models—SAM-Med3D-turbo, SegVol, SAT-Pro, VISTA3D, and nnInteractive—are evaluated zero-shot using their official weights and canonical prompt protocols (class-ID/text for semantic models; simulated point prompts for interaction-based models). A 10-case-per-modality nnU-Net is trained as a task-specific reference baseline.

## Key Contributions
- Novel intra-subject paired benchmark (UMD) with ~675k 2D images and ~12k 3D organ annotations spanning PET/CT and PET/MRI, designed specifically to decouple modality from task complexity.
- Controlled evaluation framework that isolates imaging modality as the primary independent variable, eliminating confounds present in all prior general-purpose benchmarks.
- Systematic empirical demonstration that all five tested 3D foundation models exhibit severe structural bias, with catastrophic Dice collapse on PET relative to CT/MRI.
- Distinction between two failure classes: (1) semantic-guided models (VISTA3D, SAT) undergo near-total collapse (DSC ≈ 0) on nearly all structures across all modalities on unseen data; (2) point-prompt models (SAM-Med3D-turbo, nnInteractive) retain partial performance but still degrade sharply on PET, especially for low-contrast structures.
- Evidence that even within structural CT, SegVol suffers out-of-domain collapse before any PET transition, pointing to overfitting to acquisition-specific priors beyond just modality.

## Results
- **SAM-Med3D-turbo**: CT avg DSC 0.404, PET avg DSC 0.410 (PET/CT); MRI avg 0.433, PET avg 0.397 (PET/MRI) — moderate but far below reported benchmark of 0.790 (CT) / 0.754 (MRI).
- **SegVol**: CT avg 0.107, PET avg 0.075; MRI avg 0.134, PET avg 0.148 — vs. reported 0.793 on CT.
- **nnInteractive**: CT avg 0.481, PET avg 0.342; MRI avg 0.511, PET avg 0.217 — vs. reported ~0.55 average.
- **VISTA3D**: CT avg 0.071, PET avg 0.005; MRI avg 0.003, PET avg 0.006 — near-total collapse despite reporting 0.711 on CT.
- **SAT-Pro**: CT avg 0.018, PET avg 0.003; MRI avg 0.006, PET avg 0.000 — near-total collapse despite reporting 75.6 (CT) / 83.8 (MRI) / 63.4 (PET) in literature.
- **nnU-Net (10-shot reference)**: CT 0.686, PET 0.605, MRI 0.652, PET (MRI split) 0.560 — substantially outperforms all foundation models.
- PET performance recovers partially only for high-radiotracer-uptake organs (bladder), confirming signal-contrast dependency rather than genuine anatomical understanding.

## Limitations
- Evaluation restricted to whole-body organs; pathological targets (tumors, lesions) are not included.
- Only Dice similarity coefficient is reported; no surface distance, HD95, or other metrics.
- Prompt types are limited (single-point and text/class-ID); multi-point, bounding-box, or interactive refinement strategies are not explored.
- Dataset is from a single institution (Shanghai), potentially limiting diversity of acquisition protocols, patient demographics, and scanner heterogeneity.
- The 10-case nnU-Net baseline is not a fair comparison for generalization (supervised on the same distribution) but serves only as a performance reference.

## Relevance to Foundation Models in Medicine
This work delivers a rigorous, methodologically sound indictment of the "general-purpose" claims made by current 3D medical segmentation foundation models, directly relevant to anyone tracking what these models can and cannot do clinically. The identification of a structural bias—where models are essentially modality-locked to CT/MRI priors—sets a concrete agenda for future pretraining data curation and evaluation standards. The UMD benchmark provides the field's first controlled, intra-subject paired testbed for cross-modality robustness, filling a gap that all existing benchmarks leave open. For foundation model developers, the failure of semantic-guided (text/class-ID) prompting and the partial resilience of point-prompt approaches offer actionable signal about which architectural and training strategies need rethinking to achieve genuine clinical generalization.

## Tags
#medical-segmentation #foundation-models #pet-imaging #benchmark #modality-generalization #3d-segmentation #structural-bias #zero-shot
