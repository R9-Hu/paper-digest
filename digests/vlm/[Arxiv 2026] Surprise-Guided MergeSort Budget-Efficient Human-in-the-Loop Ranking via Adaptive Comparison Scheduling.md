---
title: "Surprise-Guided MergeSort: Budget-Efficient Human-in-the-Loop Ranking via Adaptive Comparison Scheduling"
authors: ["Yujin Park", "Haejun Chung", "Ikbeom Jang"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T06:11:42+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15623"
url: "http://arxiv.org/abs/2606.15623v1"
pdf: "paper/vlm/[Arxiv 2026] Surprise-Guided MergeSort Budget-Efficient Human-in-the-Loop Ranking via Adaptive Comparison Scheduling.pdf"
---

# Surprise-Guided MergeSort: Budget-Efficient Human-in-the-Loop Ranking via Adaptive Comparison Scheduling

*🕒 **Published (v1):** 2026-06-14 06:11 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15623v1)*

## TL;DR
Surprise-Guided MergeSort (SGS) repurposes VLMs as *question prioritizers* rather than annotators in human-in-the-loop pairwise ranking. A composite Surprise Score—combining position-bias-cancelled VLM confidence, Elo rating gap, and vote entropy—routes only genuinely ambiguous comparisons to human annotators, while resolving the rest via MergeSort transitivity. Across six benchmarks, SGS achieves mean Kendall's τ×100 of 71.1, outperforming Active Elo by +7.0 under the same total budget.

## Problem
Exhaustive pairwise comparison for subjective ranking is O(n²). Sorting-based methods reduce this to O(n log n) but still spend human budget on trivially easy comparisons. Existing VLM-as-annotator approaches suffer from 60–70% agreement rates and position bias, while ensemble methods (e.g., Dodgersort) scale poorly. No prior method distinguishes which comparisons truly require human judgment versus which can be safely inferred algorithmically.

## Method
SGS operates in five stages:

1. **Round-0 calibration**: VLM scores all items pointwise (K=5 perturbation samples); human–VLM agreement rate α is computed over n_cal=100 random pairs. If α < 0.70, the system abandons MergeSort and falls back to Active Elo entirely.
2. **Warm-start Elo**: Initial Elo ratings are set via an agreement-conditioned formula blending normalized VLM scores with calibration-phase human comparisons (50/50 blend).
3. **MergeSort scheduler**: Bottom-up MergeSort over the VLM-derived initial ordering π₀ generates O(n log n) candidate cross-run boundary pairs; transitivity propagation removes already-implied pairs.
4. **Surprise scoring**: Each candidate pair receives a composite score S(i,j) = 0.4·S_vlm + 0.3·S_elo + 0.3·S_ent, where S_vlm uses a position-bias-cancelled flip test, S_elo converts Elo gap via Bradley–Terry, and S_ent measures vote entropy across K annotator samples. Pairs are ranked by surprise; top-B go to humans, the rest are eligible for automatic inference.
5. **Safe inference + recalibration**: Low-surprise pairs are inferred from Elo state (requiring |R_i−R_j| ≥ 50), with an inference cap γ_t that tightens as merge passes deepen. A test-time training (TTT) recalibrator refines VLM ambiguity estimates after each round.

## Key Contributions
- **Transitivity-aware MergeSort framework**: Systematically propagates known ordering relations to skip non-informative pairs at zero human cost.
- **Composite Surprise Score**: Integrates three independent uncertainty signals (VLM confidence post-bias cancellation, Elo gap, vote entropy) to route comparisons to humans only when genuinely ambiguous.
- **Adaptive fallback mechanism**: Automatically detects unreliable VLM priors (α < 0.70) and switches to Active Elo, preventing error propagation from a poor MergeSort skeleton.
- **Cross-domain validation**: Demonstrated efficacy on six benchmarks spanning image quality assessment and text similarity.

## Results
- SGS mean τ×100 = **71.1** across six benchmarks vs. Active Elo 64.1 (+7.0), Random Elo 66.8 (+4.3), RAIR-Laplacian 68.1 (+3.0), PairS-MergeSort 37.4 (catastrophic failure).
- Largest gains over Active Elo: **STS-B +12.1** (76.5 vs. 64.4), **LIVE Challenge +12.5** (74.1 vs. 61.6), KonIQ-10k +6.0 (65.8 vs. 59.8).
- SGS infers **38–47% of comparisons via transitivity** at zero human cost on five of six datasets (0% on TID2013 after fallback trigger), effectively achieving a ~1.89× information multiplier on STS-B (600 human comparisons resolve 1,135 total).
- On TID2013 (synthetically distorted images, fallback triggered): SGS τ×100 = 65.5 vs. best baseline 64.8, confirming graceful degradation.
- RAIR-Laplacian outperforms SGS on BIOSSES (83.0 vs. 81.4) and SICKR-STS (66.0 vs. 63.5), where small item count and graph structure favor graph-theoretic selection.
- Warm-start alone (isolated on TID2013 natural ablation) contributes +6.2 over standard Active Elo.

## Limitations
- **Single-seed evaluation**: No variance estimates or bootstrap confidence intervals; marginal gains (e.g., KonIQ +0.3 over Random Elo) are statistically unconfirmed.
- **Simulated human oracle**: Gaussian noise (σ=5) does not capture systematic human biases (fatigue, anchoring); real-annotator validation is absent.
- **Inferred comparison accuracy unmeasured**: The "safe inference" claim is not validated against ground truth; accuracy of transitivity-inferred labels is unreported.
- **Fixed hyperparameters**: Surprise weights (0.4, 0.3, 0.3) and fallback threshold (α=0.70) are domain-agnostic; adaptive tuning could improve text-domain performance.
- **Binary fallback**: The current α < 0.70 threshold cannot detect miscalibration concentrated on easy pairs (evidenced by SICKR-STS underperformance despite α ≥ 0.70).
- **Scalability untested**: Comparisons beyond n≈300 items are not evaluated; the 3B candidate subsampling cap may introduce selection bias at larger scales.

## Relevance to Vision-Language Models
This paper directly concerns how VLMs should be deployed in annotation pipelines: not as drop-in annotators (which fail at 60–70% agreement on fine-grained pairs) but as uncertainty estimators that identify where human effort is most needed. The position-bias cancellation via flip-testing and the multi-signal Surprise Score offer a practical recipe for any task using VLMs for comparative evaluation—including RLHF preference data collection and VLM-based benchmarking. The finding that VLMs are reliably directional for *perceptual* tasks (image quality) but unreliable for *semantic* tasks (text similarity) is a concrete calibration insight for researchers designing VLM-in-the-loop evaluation systems. The adaptive fallback architecture also provides a safety pattern for agentic VLM pipelines where model reliability is task-dependent and unknown a priori.

## Tags
#vlm #human-in-the-loop #active-learning #pairwise-ranking #annotation-efficiency #image-quality-assessment #uncertainty-estimation #mergesort
