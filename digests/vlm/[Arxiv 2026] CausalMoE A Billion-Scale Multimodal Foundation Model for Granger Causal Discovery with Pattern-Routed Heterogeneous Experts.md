---
title: "CausalMoE: A Billion-Scale Multimodal Foundation Model for Granger Causal Discovery with Pattern-Routed Heterogeneous Experts"
authors: ["Bo Liu", "Di Dai", "Jingwei Liu", "Jiarui Jin", "Xiaocheng Fang", "Guangkun Nie", "Hongyan Li", "Shenda Hong"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T07:57:23+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13024"
url: "http://arxiv.org/abs/2606.13024v1"
pdf: "paper/vlm/[Arxiv 2026] CausalMoE A Billion-Scale Multimodal Foundation Model for Granger Causal Discovery with Pattern-Routed Heterogeneous Experts.pdf"
---

# CausalMoE: A Billion-Scale Multimodal Foundation Model for Granger Causal Discovery with Pattern-Routed Heterogeneous Experts

*🕒 **Published (v1):** 2026-06-11 07:57 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13024v1)*

## TL;DR
CausalMoE is a billion-scale multimodal foundation model for Granger Causal Discovery (GCD) that replaces the standard "uniform distribution modeling" assumption with a Pattern-Routed Mixture of Heterogeneous Experts (MoHE), dynamically routing time-series patches to specialized experts including frozen LLMs and VLMs. It is the first GCD system to integrate VLMs into the causal inference loop, converting time-series patches into normalized images for a frozen VLM to extract shape-level visual priors. It achieves state-of-the-art on five synthetic and real-world benchmarks with strong few-shot generalization.

## Problem
Existing neural GCD methods assume a homogeneous data-generating process (Uniform Distribution Modeling, UDM), which fails when real-world time series exhibit distribution shifts and regime changes within short temporal windows. Conflating heterogeneous temporal regimes entangles representations and induces spurious causal links. Additionally, all prior GCD methods are strictly unimodal (numerical only), discarding semantic and visual context that could disambiguate causal relationships.

## Method
CausalMoE operates in three stages:

1. **Multimodal Patch Encoding**: Input time series are segmented into patches and converted into three modalities: (a) raw numerical patches, (b) structured textual prompts encoding statistics and task context, (c) normalized images via bilinear interpolation of patch values to [0,255] pixels, aligned to a VLM vision encoder's input distribution.

2. **Patch-Specific Pattern Routing (PSPR)**: A subspace clustering module learns K orthogonal latent subspaces (basis B ∈ R^{K×q×d}). Each patch embedding is assigned to the nearest subspace via affinity scores (Eq. 6–7), with confidence-weighted refinement. An orthogonality regularizer (L_Ortho) enforces geometric distinctiveness across subspaces. The routing objective combines L_Ortho with a KL divergence term on soft assignments.

3. **Mixture of Heterogeneous Experts (MoHE)**: Four functionally distinct experts are available: (i) Semantic Expert — frozen LLM encodes text prompts; (ii) Multimodal Expert — frozen VLM encodes text + rendered image (Eq. 10); (iii) Temporal-Frequency Expert — combines time-domain and Fourier features; (iv) Multiscale Temporal Expert — aggregates downsampled representations across resolutions. A patch gating network selects top-k=2 experts per patch (K=4 total) and fuses outputs by weighted sum.

4. **Causal Graph Recovery**: A Causality-Aware Self-Attention (CASA) mechanism performs attention across variables (not time), with variable-level projection matrices ω_q, ω_k, ω_v ∈ R^{D×D}. Proximal gradient descent with group soft-thresholding enforces sparsity in ω_v, from which the Granger causal graph is read off by non-zero columns.

## Key Contributions
- First multimodal GCD framework integrating frozen LLMs and VLMs as heterogeneous experts within the causal discovery loop.
- Pattern-Routed Mixture of Heterogeneous Experts (MoHE) with subspace-clustering-based routing that explicitly decouples regime-specific from shared temporal dynamics.
- Causality-Aware Self-Attention (CASA) operating across variables (not time) with proximal optimization for sparse, interpretable Granger graph recovery.
- Formal definition of Multimodal Granger Causality (MGC) extending GC to joint text and image modalities.
- Billion-scale foundation model with a practical accuracy–efficiency trade-off via frozen backbone caching.

## Results
- **VAR (N=20, T=1000, τ=5)**: AUROC 0.989 vs. JRNGC 0.972, CUTS 0.944; SHD 4±1 vs. CUTS 5±2.
- **VAR (N=40, T=1000, τ=20)**: AUROC 0.953, F1 0.956, SHD 8±1 vs. JRNGC (AUROC 0.922, SHD 33±6).
- **Lorenz-96 (N=40, T=1000, F=20)**: AUROC 0.939 vs. JRNGC 0.913, CUTS 0.828.
- **DREAM-3**: Best AUROC across all 5 sub-datasets (e.g., Ecoli-1: 0.845 vs. JRNGC 0.713).
- **DREAM-4**: Best AUROC across all 5 Gene sub-datasets (e.g., Gene-1: 0.829 vs. JRNGC 0.739).
- **fMRI**: Competitive AUROC in 22/28 simulations with lower variance than JRNGC.
- **Few-shot**: Achieves AUROC >0.6 on DREAM-4 with only 5% training data, matching baselines trained on 50–100% data.

## Limitations
- Identifies predictive (Granger) dependencies, not interventional causality; assumes no hidden confounders and no instantaneous effects.
- Frozen LLM/VLM embedding extraction adds computational overhead, limiting real-time applicability.
- Pre-training data of LLMs/VLMs is not fully auditable; benchmark leakage from LLM/VLM pretraining cannot be ruled out.
- VLM and LLM biases or hallucinations may propagate into causal estimates in sensitive domains.

## Relevance to Vision-Language Models
CausalMoE demonstrates a novel application of frozen VLMs as visual feature extractors over non-image data: time-series patches are rendered as normalized images and fed to a VLM to extract perceptual priors (peak sharpness, envelope morphology, regime boundaries) that complement numerical and textual representations. This extends the known capability of VLMs to process visually-encoded structured data beyond natural images, directly analogous to prior work repurposing VLMs for scientific charts and plots. The paper also provides empirical evidence that VLM-derived features are non-redundant with LLM text features and raw numerical features (ablation in Fig. 7b), supporting the hypothesis that vision encoders capture structural patterns invisible to scalar statistics. For VLM researchers, the multimodal Granger causality formalization (Definition 3.1) and the frozen-backbone grafting diagnostic (Fig. 8) offer a rigorous testbed for evaluating whether VLM representations carry generalizable semantic structure transferable to entirely new domains.

## Tags
#vlm #granger-causality #mixture-of-experts #time-series #multimodal #causal-discovery #foundation-model #few-shot
