---
title: "Forging a Dynamic Memory: Retrieval-Guided Continual Learning for Generalist Medical Foundation Models"
authors: ["Zizhi Chen", "Yizhen Gao", "Minghao Han", "Yizhou Liu", "Zhaoyu Chen", "Dingkang Yang", "Lihua Zhang"]
source: "Arxiv"
venue: ""
published: "2025-12-15"
published_time: "2025-12-15T08:09:40+00:00"
year: 2025
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2512.13072"
url: "http://arxiv.org/abs/2512.13072v1"
pdf: "paper/med-foundation/[Arxiv 2025] Forging a Dynamic Memory Retrieval-Guided Continual Learning for Generalist Medical Foundation Models.pdf"
---

# Forging a Dynamic Memory: Retrieval-Guided Continual Learning for Generalist Medical Foundation Models

*🕒 **Published (v1):** 2025-12-15 08:09 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2512.13072v1)*

## TL;DR
PRIMED is a continual learning (CL) framework for generalist medical Vision-Language Models that integrates Retrieval-Augmented Generation (RAG) with dynamic knowledge distillation to combat catastrophic forgetting across diverse medical imaging domains. It builds an 18M-entry multimodal PubMed retrieval database and a 3,000-entry question pool to construct dynamic reference datasets at training time, replacing the inaccessible pretraining data typically required by distillation-based CL. The method achieves SOTA across all metrics on the authors' new MGTIL benchmark covering both intra- and inter-domain medical CL scenarios.

## Problem
Continual fine-tuning of medical VLMs (e.g., BiomedCLIP, PMC-CLIP) causes catastrophic forgetting in two distinct regimes: fine-grained intra-domain feature degradation (medical images are minimally variable within a domain) and coarse cross-domain forgetting (imaging modalities follow heterogeneous physical principles, creating a clustered, discontinuous embedding topology). Existing CL strategies for VLMs rely on replay from the original pretraining corpus (inaccessible in practice) or ImageNet-label-based synthesis (invalid for caption-supervised medical VLMs). No prior benchmark simultaneously evaluates intra-domain feature retention and cross-domain transfer for medical generalist models.

## Method
**Data infrastructure.** An 18M image-caption retrieval database is constructed from PubMed via Qwen3-Embedding-8B embeddings; a 3,000-entry question pool covers medical domains, anatomical sites, and disease types.

**Dynamic multi-stage retrieval (Dynamic Siphon).** Before each task, queries are partitioned into three pools—task-specific (`M_task`), domain-related (`M_domain`), and general (`M_gen`)—with proportional sampling. Retrieval proceeds in three stages: (1) dense embedding similarity search, (2) VLM-based cross-modal reranking, (3) BM25 lexical gating. This produces per-task reference datasets tailored to the current domain mix without accessing original training data.

**Distillation and alignment losses.**
- *Contrastive Knowledge Transfer (CKT)*: KL-divergence between the current student and the previous-task teacher on B×B cross-modal similarity matrices, applied bidirectionally (image→text and text→image).
- *Cross-Modality Consistency (CMC)*: contrastive alignment of the student's similarity matrix against the identity, preserving zero-shot image-text correspondence.
- Total loss: `L_Train = L_CE + α·L_CKT + β·L_CMC`.

**Dynamic Fisher Weight Guard (DFG).** Fisher Information Matrix diagonals are recomputed at each optimization step from the distillation+alignment gradient (excluding `L_CE`), then used as per-parameter L2 regularization weights. This dynamically protects parameters critical to the distillation objective rather than using static (EWC) or uniform (L2) penalties.

**Backbone.** BiomedCLIP (ViT-B/16), fine-tuned with the above losses; 1,000 iterations per task, batch size 64, lr 1e-5, 4× A6000 GPUs.

## Key Contributions
- **18M multimodal medical retrieval database** built from PubMed via Qwen3-Embedding-8B with multi-image decomposition and pseudo-labeling.
- **3,000-entry hierarchical question pool** enabling fine-grained, domain-partitioned RAG queries.
- **MGTIL benchmark** with two sub-benchmarks: *HieraMedTransfer* (9 datasets, 3 domains, 2 task orders testing intra/cross-domain CL) and *MedXtreme* (6 domains, up to 33 classes, low-data high-difficulty tasks).
- **PRIMED framework** unifying dynamic RAG-based reference construction, CKT+CMC distillation, and DFG weight regularization into a single pipeline.
- SOTA on all MGTIL metrics without requiring access to original pretraining data or rehearsal buffers.

## Results
**HieraMedTransfer (vs. `l2` baseline):**
- PRIMED_dyn: Transfer +4.7 pp, Avg +4.6 pp, Last +8.0 pp on Order I
- PRIMED_dyn: Transfer +2.7 pp, Avg +4.1 pp, Last +14.4 pp on Order II
- Best competing method (ZSCL/DIKI): Last ~+3.3–3.5 pp on Order I; PRIMED_dyn exceeds all on both orders

**MedXtreme (vs. `l2` baseline):**
- PRIMED_dyn: ACC +7.5 pp, AUC +4.5 pp, BWT improvement +7.3 on Order I
- PRIMED_dyn: ACC +10.8 pp, AUC +5.1 pp, BWT improvement +11.1 on Order II
- Best prior method (GIFT, CVPR 2025): ACC +4.9/+8.4 pp on Order I/II — PRIMED_dyn surpasses by ~2.6/+2.4 pp

**Ablation highlights (HieraMedTransfer Order I):**
- Removing CKT: Last drops from 82.1 → 78.9; the largest single-component degradation
- DFG vs. EWC: Last 82.1 vs. 80.6; DFG vs. plain L2: 82.1 vs. 81.8
- Hierarchical retrieval vs. BM25 alone: Last 82.1 vs. 81.8; Transfer 58.3 vs. 55.1

## Limitations
- Retrieval database and question pool were constructed from PubMed only; domains absent from PubMed literature (e.g., rare or proprietary imaging modalities) are not covered.
- The 18M database uses pseudo-labels and embedding-based segmentation; label noise is not quantified.
- Experiments use a single backbone (BiomedCLIP ViT-B/16); scalability to larger VLMs (e.g., generative multimodal models) is not directly demonstrated (though appendix claims cross-backbone robustness).
- MGTIL is task-incremental with known task identity at inference, which is a relaxed assumption compared to class-incremental settings.
- Retrieval and re-embedding at each task boundary incurs non-trivial computational overhead not fully characterized.
- Teacher model is always the immediately preceding task checkpoint, which itself suffers forgetting — a recognized but partially mitigated limitation.

## Relevance to Foundation Models in Medicine
PRIMED directly addresses a critical practical barrier to deploying generalist medical foundation models in clinical settings: how to continuously update a VLM across new tasks and imaging modalities without retraining from scratch or retaining patient data. By substituting the inaccessible pretraining corpus with a dynamically queried public literature database, it offers a data-privacy-compatible CL paradigm relevant to federated or regulated healthcare environments. The MGTIL benchmark fills an important gap — prior medical CL benchmarks were single-domain, making it difficult to assess models that must serve as generalists across radiology, pathology, dermatology, and ophthalmology simultaneously. This work is a direct methodological extension of the BiomedCLIP/PMC-CLIP line and engages with the fundamental tension in foundation model deployment between plasticity (learning new tasks) and stability (retaining prior knowledge).

## Tags
#continual-learning #vlm #retrieval-augmented-generation #knowledge-distillation #medical-imaging #catastrophic-forgetting #benchmark #multimodal
