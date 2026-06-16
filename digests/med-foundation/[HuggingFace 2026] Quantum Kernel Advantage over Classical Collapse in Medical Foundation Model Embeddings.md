---
title: "Quantum Kernel Advantage over Classical Collapse in Medical Foundation Model Embeddings"
authors: ["Sebastian Cajas Ord\u00f3\u00f1ez", "Felipe Ocampo Osorio", "Dax Enshan Koh", "Rafi Al Attrach", "Aldo Marzullo", "Ariel Guerra-Adames", "J. Alejandro Andrade", "Siong Thye Goh", "Chi-Yu Chen", "Rahul Gorijavolu", "Xue Yang", "Noah Dane Hebdon", "Leo Anthony Celi"]
source: "HuggingFace"
venue: ""
published: "2026-04-27"
published_time: "2026-04-27T15:21:53+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2604.24597"
url: "https://huggingface.co/papers/2604.24597"
pdf: "paper/med-foundation/[HuggingFace 2026] Quantum Kernel Advantage over Classical Collapse in Medical Foundation Model Embeddings.pdf"
---

# Quantum Kernel Advantage over Classical Collapse in Medical Foundation Model Embeddings

*🕒 **Published (v1):** 2026-04-27 15:21 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2604.24597)*

## TL;DR
This paper demonstrates quantum kernel advantage over classical SVM in noiseless simulation on a binary insurance classification task using frozen embeddings from three medical foundation models (MedSigLIP-448, RAD-DINO, ViT-patch32) applied to MIMIC-CXR chest radiographs. A two-tier fair comparison framework shows QSVM wins minority-class F1 in all 18 tested model×qubit configurations over untuned and hyperparameter-tuned classical baselines. The classical collapse is mechanistically explained by the structural low-rank degeneracy of linear kernel matrices after PCA-q compression.

## Problem
Empirical demonstrations of quantum advantage on real-world medical imaging tasks are rare, and prior QML benchmarks typically use synthetic data or toy datasets with 100–500 samples. Rigorous fair comparisons require identical hyperparameters and dimensionality on both classical and quantum sides — a constraint rarely enforced. Additionally, classical linear SVMs collapse to majority-class prediction under aggressive PCA dimensionality reduction (low-q), creating a structurally degenerate setting where no regularization tuning can rescue them; the question is whether quantum kernels can exploit the same compressed feature space.

## Method
Frozen CLS-token embeddings are extracted from three medical foundation models — MedSigLIP-448 (448-dim), RAD-DINO (768-dim, DINO-pretrained on radiology), and ViT-patch32 (768-dim, general-purpose) — on 2,371 MIMIC-CXR samples (DT9 preprocessing stratum). Embeddings are compressed via a three-stage pipeline: StandardScaler → PCA-q → MinMaxScaler[−1,1], where q ∈ {4,6,8,9,10,11,12,16} matches qubit count. The quantum circuit uses Block-Sparse Parameterization (BSP) with 1-DOF angle encoding (single Ry per qubit) and ring CNOT entanglement; the quantum kernel is computed via the compute-uncompute strategy with trace normalization. A two-tier fair comparison is applied: **Tier 1** pairs untuned QSVM (C=1) against untuned linear SVM (C=1) at identical PCA-q dimensionality; **Tier 2** pairs untuned QSVM against C-tuned RBF SVM. Statistical validation uses 10 independent embedding seeds with paired bootstrap (10,000 resamples). Eigenspectrum analysis (Shannon effective rank) provides the mechanistic explanation for classical collapse.

## Key Contributions
- **18/18 Tier-1 wins**: QSVM beats untuned linear SVM on minority-class F1 across all model×qubit configurations (10 seeds; 17 at p<0.001, 1 at p<0.01, paired bootstrap); classical linear SVM collapses to F1=0 on 90–100% of seeds at every qubit count.
- **7/7 Tier-2 wins**: Untuned QSVM beats C-tuned RBF SVM at equal PCA-q dimensionality (mean gain +0.068, max +0.112).
- **Structural collapse explanation**: After PCA-q, the linear kernel KL has effective rank exactly q (3.77–5.85 out of N=1,896), making collapse C-invariant. The quantum kernel KQ reaches effective rank 69.80 at q=11 (multi-seed mean), a ~6.3× increase at the performance peak.
- **Three circuit design rules**: (1) Trace normalization is necessary — Frobenius normalization collapses F1 to zero on all models; (2) 1-DOF encoding (one Ry per qubit) consistently outperforms 3-DOF (Rz-Ry-Rz); (3) increasing re-uploading depth (reps=2) degrades performance at q=8, indicating the bottleneck is sample count, not circuit expressivity.
- **Architecture-dependent concentration**: MedSigLIP-448 collapses at q=16 (seed-dependent), while RAD-DINO and ViT-patch32 improve monotonically; projected quantum kernel recovers F1 at q=16 (+0.223), isolating swap-test fidelity concentration (not the circuit) as the bottleneck.

## Results
- **Tier 1 (strongest config)**: MedSigLIP-448, q=11 — QSVM mean F1=0.343±0.170 vs. classical F1=0.050±0.159 (ΔF1=+0.293, 95% CI [+0.190,+0.385], p<0.001; classical collapses to F1=0 on 9/10 seeds).
- **Tier 1 across all models** (Table II, 10 seeds):
  - RAD-DINO q=16: QSVM F1=0.450±0.083 vs. classical F1=0.079±0.127 (F1 WIN)
  - ViT-patch32 q=16: QSVM F1=0.399±0.098 vs. classical F1=0.000±0.000 (F1 WIN)
- **Tier 2** (Table IV): QSVM wins all 7 tested configurations; largest gain MedSigLIP q=8 (+0.112, +53% relative); ViT-patch32 q=4 smallest gain (+0.004).
- **Rank-matched RBF experiment**: At q=4 with γ∗ tuned to match QSVM effective rank, RBF achieves mean F1=0.110 (30% collapse rate) vs. QSVM F1=0.212 (20% collapse rate), indicating spectral structure beyond rank drives QSVM advantage.
- **Projected kernel at q=16**: Recovers MedSigLIP-448 F1 from 0.173 (fidelity) to 0.396 (+0.223), confirming measurement bottleneck rather than circuit limitation.
- **Feature selection sensitivity**: QSVM F1 at q=4,6 exceeds best classical SVM with MI-ranking or kPCA feature selection across all three models (e.g., MedSigLIP MI/kPCA best: 0.404 vs. QSVM q=4: 0.488).

## Limitations
- All experiments run in **noiseless simulation** (Qiskit Statevector); no noise models or real quantum hardware results are reported, making hardware-realistic advantage unconfirmed.
- **Single preprocessing stratum (DT9)** selected post-hoc based on strongest quantum results in preliminary experiments; non-collapse Tier-1 advantage (q≥10) not validated on other strata.
- **Training set limited to ~1,896 samples** by quantum hardware constraints; advantage regime is conditioned on this small-sample, low-dimensional (q≤16) setting.
- **Insurance status is a non-clinical proxy**: the task explicitly avoids causal clinical claims; generalization to pathology-relevant classification tasks is unproven.
- **Classical F1 collapse at low q is structural** (rank=q), so the comparison may not reflect a general quantum advantage beyond this degenerate regime; the C-only Tier-2 does not tune RBF bandwidth γ.
- **q=16 multi-seed behavior** of MedSigLIP-448 is seed-dependent (not structural), and the projected kernel finding at q=16 is mechanistic/diagnostic only — not part of the primary comparison framework.
- Dataset size (~2,371) is larger than most prior QML medical imaging work but still far below what is needed for clinical deployment or generalization conclusions.

## Relevance to Foundation Models in Medicine
This work is directly relevant to the intersection of medical foundation models and downstream classifier design: it uses frozen embeddings from MedSigLIP-448 and RAD-DINO as representation providers and treats the linear probing regime as the experimental scaffold for quantum kernel evaluation. The finding that PCA compression of high-dimensional medical foundation model embeddings creates a structurally degenerate low-rank classical kernel is a novel, practically important failure mode insight for practitioners who probe foundation model representations with linear classifiers on small datasets. The architecture-dependent concentration behavior (MedSigLIP-448 vs. RAD-DINO) implies that the geometry of a foundation model's embedding space interacts non-trivially with quantum feature maps, suggesting that quantum methods may be differentially suited depending on the pretraining objective and modality of the foundation model. For those tracking QML applications to clinical AI, this is one of the first studies to rigorously apply quantum kernels to medical foundation model embeddings on a real clinical imaging dataset at this scale, with mechanistic grounding rather than just empirical claims.

## Tags
#quantum-ml #foundation-models #medical-imaging #kernel-methods #chest-xray #mimic-cxr #radiology #health-equity
