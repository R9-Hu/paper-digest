---
title: "Topology-Driven Transferability Estimation of Medical Foundation Models for Segmentation"
authors: ["Jiaqi Tang", "Shaoyang Zhang", "Xiaoqi Wang", "Jiaying Zhou", "Yang Liu", "Qingchao Chen"]
source: "Arxiv"
venue: ""
published: "2026-02-27"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2602.23916"
url: "http://arxiv.org/abs/2602.23916v2"
pdf: "paper/med-foundation/[Arxiv 2026] Topology-Driven Transferability Estimation of Medical Foundation Models for Segmentation.pdf"
---

# Topology-Driven Transferability Estimation of Medical Foundation Models for Segmentation

## TL;DR
Selecting the best SSL-pretrained encoder for a medical segmentation task requires costly exhaustive fine-tuning across a model zoo. This paper proposes a training-free transferability estimation framework that measures topological alignment between feature manifolds and semantic label spaces—using Minimum Spanning Trees—rather than statistical distributional overlap. On the OpenMind benchmark it outperforms prior methods by ~31% in weighted Kendall's τ.

## Problem
Existing transferability estimation (TE) metrics (LEEP, LogME, GBC, CCFV) were designed for classification and rely on global distributional statistics or Gaussianity assumptions. They fail for segmentation because segmentation quality depends on preserving local geometric structure at anatomical boundaries, not coarse class separation. No training-free metric adequately predicts which SSL encoder will fine-tune best on a target segmentation task.

## Method
The framework operates in three stages, all without any fine-tuning:

**Global Representation Topology Divergence (GRTD):** Constructs two MSTs over sampled feature-label pairs—one from the encoder's feature distances (Euclidean), one from a semantically-ideal label-induced graph (intra-class edges forced to zero weight, inter-class capped at λ). GRTD is the negative sum of weight discrepancies between these MSTs aggregated across D decoder stages; a score near zero means feature geometry naturally mirrors semantic hierarchy.

**Local Boundary-Aware Topological Consistency (LBTC):** Extracts local patches centered on boundary anchors (morphological gradient of ground-truth masks). For each patch, a local MST is built and a Topological Leakage Rate ρ_k is computed as the fraction of MST edges bridging distinct semantic classes. LBTC = 1 − mean(ρ_k); scores near 1 indicate the encoder cleanly separates classes at boundaries.

**Task-Adaptive Topological Fusion:** A complexity prior κ = log(|C|) (number of semantic classes) drives a sigmoid gating factor α. Final score S_ϕ = α·N(T_GRTD) + (1−α)·N(T_LBTC). High class count (multi-organ) shifts weight toward GRTD; focal pathology tasks shift weight toward LBTC.

Features are extracted via sliding-window inference through a randomly-initialized nnU-Net decoder attached to the frozen SSL encoder; GRTD uses the final k decoder layers, LBTC uses the last k encoder layers.

## Key Contributions
- First topology-driven, training-free TE framework specifically designed for 3D medical segmentation.
- GRTD: non-parametric MST-based measure of global feature-label manifold isomorphism.
- LBTC: local MST leakage rate targeting anatomical boundary separability, addressing class-imbalance blind spots in global metrics.
- Task-Adaptive Fusion using semantic cardinality as a proxy for structural complexity.
- Validated on OpenMind benchmark (7 SSL models, 114k 3D volumes, 6 downstream tasks including OOD cross-modality).

## Results
- Average weighted Kendall's τ: **0.723** (ours) vs. 0.552 (CCFV), −0.264 (LEEP), −0.280 (LogME), −0.508 (GBC)—~31% relative improvement over best baseline.
- OOD cross-modality task (KiTS19, MR→CT): **0.869** vs. CCFV 0.180—decisive gap where statistical methods collapse.
- Ablation: Global-only GRTD avg 0.436, Local-only LBTC avg 0.475; adaptive fusion avg **0.714** across fragmented and structured targets.
- Computation time for 7 models: **6.99 min** (ours) vs. 8.02–10.07 min (CCFV) vs. **3000+ min** for exhaustive fine-tuning.
- Robust across decoder initializations (Kaiming/Xavier/Gaussian): τ variance < 0.02.

## Limitations
- Gating hyperparameters γ and β are not learned end-to-end; their estimation relies on a pilot set of K=10 cases (sensitivity not fully characterized).
- Evaluated on a single benchmark (OpenMind) with one backbone family (ResEnc-L); generalizability to other architectures (e.g., ViT-based or 2D encoders) is unverified.
- MST construction scales quadratically with sample count; computational complexity at very large feature sets is not analyzed.
- Only SSL encoders are evaluated; supervised pre-training or multi-modal foundation models (e.g., SAM-Med) are not included.
- The semantic-label MST construction requires ground-truth labels from the target task, which may not always be available in abundance in clinical settings.

## Relevance to Foundation Models in Medicine
As the medical foundation model zoo grows (MAE, SimMIM, VoCo, SwinUNETR, etc.), the inability to efficiently select the right encoder without full fine-tuning is a practical deployment bottleneck. This work provides a principled, compute-cheap proxy that is explicitly designed for the SSL-encoder + segmentation-decoder paradigm ubiquitous in medical imaging. The topology-driven approach generalizes across anatomical regions and imaging modalities (including OOD cross-modality transfer), which is directly relevant to the goal of adapting general-purpose foundation models to heterogeneous clinical tasks. It complements work on model zoos and benchmarks (e.g., OpenMind) by providing the missing efficient selection layer.

## Tags
#transferability-estimation #segmentation #self-supervised-learning #topology #model-selection #3d-medical-imaging #foundation-model-adaptation #training-free
