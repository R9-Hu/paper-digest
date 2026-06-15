---
title: "A Hierarchical Benchmark of Foundation Models for Dermatology"
authors: ["Furkan Yuceyalcin", "Abdurrahim Yilmaz", "Burak Temelkuran"]
source: "Arxiv"
venue: ""
published: "2026-01-18"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2601.12382"
url: "http://arxiv.org/abs/2601.12382v1"
pdf: "paper/med-foundation/[Arxiv 2026] A Hierarchical Benchmark of Foundation Models for Dermatology.pdf"
---

# A Hierarchical Benchmark of Foundation Models for Dermatology

## TL;DR
This paper benchmarks ten frozen foundation model embeddings (general vision, general medical, dermatology-specific) for hierarchical skin lesion classification across four levels of diagnostic granularity on the DERM12345 dataset. The central finding is a "granularity gap": models excelling at binary malignancy screening (MedImageInsights, 97.52% F1) systematically underperform at fine-grained 40-subclass differential diagnosis, where MedSigLIP (69.79%) and dermatology-specific models lead. Domain specificity alone does not guarantee superiority—scale and pretraining diversity matter.

## Problem
Existing dermatology benchmarks collapse the clinical diagnostic hierarchy into binary or coarse multi-class tasks (e.g., melanoma vs. benign nevi), masking whether foundation models can support fine-grained differential diagnosis needed for real clinical workflows. No prior work systematically compares modern foundation model embeddings across the full diagnostic taxonomy from binary malignancy down to 40 lesion subclasses.

## Method
Frozen embeddings are extracted from ten models spanning three domains: general vision (DINOv2-Base/Giant, DINOv3, CLIP-Base/Large, ResNet-50), general medical (MedSigLIP, BiomedCLIP, MedImageInsights), and dermatology-specific (MONET, PanDerm-Base/Large, Derm Foundation). Lightweight adapters (KNN, LR, SVM, RF, MLP, XGBoost) are trained via 5-fold stratified cross-validation with GridSearchCV on 40-class subclass labels on DERM12345 (12,345 dermoscopic images, 9,860 train / 2,485 test, patient-partitioned). Predictions at coarser levels (15 Main Classes, 4 Superclasses, 2-class Melanocytic/Non-melanocytic, Binary Malignancy) are obtained by probability aggregation up the taxonomy—no separate classifiers per level. Best adapter per model is reported. Primary metric: Weighted F1-Score; secondary: Balanced Accuracy.

## Key Contributions
- Introduces a hierarchical evaluation framework mapping frozen embedding predictions across four clinical granularity levels (40 → 15 → 4 → 2-class → Binary Malignancy) via probability aggregation.
- Identifies and characterizes the "granularity gap": a systematic performance inversion between coarse-level and fine-grained classification across model families.
- Reveals the "Blob Problem" via t-SNE: melanocytic subclasses (Banal Compound, Dysplastic Compound, Dysplastic Junctional nevi) form inseparable dense clusters in embedding space across all evaluated models.
- Shows MLP adapters consistently outperform linear probes and distance-based methods, indicating non-linear decision boundaries between subclasses; critical for high-dimensional embeddings (e.g., Derm Foundation at 6144-dim).
- Flags a likely defective checkpoint: PanDerm (Large) collapses to 36.65% on 40-class task, below ResNet-50 (58.82%).

## Results
- **Binary Malignancy**: MedImageInsights best at 97.52% F1; MedSigLIP second at 96.43%; dermatology-specific models (Derm Foundation 96.04%, MONET 96.02%) closely follow.
- **40-class Subclass**: Performance inversion—MedSigLIP leads at 69.79%, Derm Foundation 69.50%, MONET 69.31%, DINOv2-Giant 68.00%; MedImageInsights drops to 65.50%.
- **15-class Main Class**: MedImageInsights 62.40% (narrow lead), MedSigLIP 62.29%, Derm Foundation 61.34%.
- **4-class Superclass**: MedImageInsights 93.45%, MedSigLIP 91.66%.
- ResNet-50 baseline: 58.82% on 40-class, >10 pp below top models.
- MLP adapter on MedSigLIP (69.8%) vs. SVM (46.9%): large gap underscores adapter sensitivity.
- KNN on Derm Foundation 6144-dim embeddings: 62.1% vs. MLP 69.5% (curse of dimensionality effect).

## Limitations
- DERM12345 sourced exclusively from clinical centers in Türkiye; skin phototype distribution may not generalize globally.
- Evaluation restricted to dermoscopic images; clinical (macroscopic) photography not assessed.
- Adapters trained on 40-class labels only; coarse-level performance is inferred via aggregation, not direct training—may underestimate achievable coarse accuracy.
- "Indeterminate" (actinic keratosis) lesions grouped with benign for binary task, a simplification that aligns with clinical convention but reduces task difficulty.
- Only publicly released checkpoints evaluated; PanDerm (Large) anomaly suggests checkpoint quality is an uncontrolled variable in foundation model benchmarking.

## Relevance to Foundation Models in Medicine
This work directly addresses the evaluation methodology gap for medical foundation models, demonstrating that flat-task benchmarks misrepresent clinical utility by hiding the granularity gap—a phenomenon likely generalizable beyond dermatology to other hierarchically structured diagnostic domains (e.g., pathology subtyping, radiology finding classification). The finding that a large-scale general medical model (MedSigLIP) matches or exceeds domain-specific dermatology models at fine-grained classification challenges the prevailing assumption that specialization is the primary driver of performance, pointing instead to pretraining scale and diversity. The "Blob Problem" and the necessity of non-linear adapters over zero-shot retrieval set a concrete lower bound on what frozen representations can achieve, directly informing how foundation models should be integrated into clinical decision support pipelines. The hierarchical probability-aggregation evaluation protocol is a transferable methodology for future benchmarks in any medical domain with taxonomic label structure.

## Tags
#benchmark #dermatology #hierarchical-classification #foundation-models #embedding-evaluation #granularity-gap #skin-lesion #transfer-learning
