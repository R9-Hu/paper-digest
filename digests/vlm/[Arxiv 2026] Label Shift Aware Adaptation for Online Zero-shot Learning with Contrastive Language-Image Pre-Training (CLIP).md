---
title: "Label Shift Aware Adaptation for Online Zero-shot Learning with Contrastive Language-Image Pre-Training (CLIP)"
authors: ["Pengxiao Han", "Changkun Ye", "Yanshuo Wang", "Jinguang Tong", "Miaohua Zhang", "Xuesong Li", "Jie Hong", "Lars Petersson"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T07:36:24+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15169"
url: "http://arxiv.org/abs/2606.15169v1"
pdf: "paper/vlm/[Arxiv 2026] Label Shift Aware Adaptation for Online Zero-shot Learning with Contrastive Language-Image Pre-Training (CLIP).pdf"
---

# Label Shift Aware Adaptation for Online Zero-shot Learning with Contrastive Language-Image Pre-Training (CLIP)

*🕒 **Published (v1):** 2026-06-13 07:36 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15169v1)*

## TL;DR
Existing online zero-shot CLIP methods adapt representations at test time but ignore the mismatch between CLIP's training label distribution and the streaming test distribution. This paper proposes Label Shift Aware (LSA), a training-free posterior adjustment that dynamically estimates the test-time label prior via an EM algorithm and reweights CLIP's class probabilities accordingly. LSA is non-parametric, memory-efficient, and plug-and-play over any CLIP-based classifier.

## Problem
In online zero-shot learning (ZSL) with CLIP, test images arrive sequentially in a single pass with no storage—combining the difficulty of unseen-class recognition with streaming constraints. Prior methods (TPT, OnZeta) focus on prompt or modality alignment but ignore label shift: the class prior of CLIP's pretraining source domain (approximately uniform over massive web data) diverges from the target stream's class distribution. This mismatch biases posterior predictions and degrades accuracy, especially on imbalanced or domain-shifted test streams.

## Method
LSA reframes online ZSL with CLIP as a domain adaptation problem under the label shift assumption (p(x|y) invariant, p(y) shifts). It operates entirely on CLIP's frozen output probabilities through three components:

1. **LSA Weight Generation**: An EM algorithm (Algorithm 1) iterates E-steps and M-steps over the accumulated prediction buffer to estimate the target label distribution π. The M-step combines a data term (soft responsibilities g_{t,j}) with a Dirichlet prior Dir(K, α) via a balancing weight λ, assuming a uniform source prior c = 1/K.

2. **Active Prior Adaptation**: λ is annealed linearly as λ_t = (t/N)·λ₀, so the estimator relies more on the Dirichlet prior early in the stream (few samples, high variance) and increasingly trusts the empirical distribution as t → N.

3. **LSA Classifier Correction**: At each timestep t the corrected prediction is f̃(x_t)_j = [f(x_t)_j / π_j] / Σ_l [f(x_t)_l / π_l], reweighting CLIP's softmax scores by the inverse of estimated class priors—directly compensating for prior mismatch.

No backbone weights are modified; the only memory overhead is a buffer of CLIP softmax vectors.

## Key Contributions
- Formal identification of label shift as the dominant failure mode in online ZSL with CLIP, motivating a domain-adaptation perspective.
- Non-parametric EM-based label distribution estimator that operates on unlabeled streaming data without storing raw images.
- Active prior adaptation schedule (linear λ annealing) that prevents high estimation error early in the stream.
- Posterior reweighting correction that is model-agnostic and composable with any CLIP-based online ZSL baseline.

## Results
- **ImageNet (5 backbones)**: LSA consistently outperforms both CLIP baseline and OnZeta. Gains over CLIP baseline range from +2.12% (ViT-L/14@336) to +2.56% (ResNet-50); gains over OnZeta are +0.49%–+0.57%.
- **13 additional datasets (ResNet-50 backbone)**: LSA surpasses OnZeta by **+2.91%** on average; LSA+OnZeta achieves +3.16% avg over CLIP baseline.
- **13 additional datasets (ViT-B/16 backbone)**: LSA surpasses OnZeta by **+2.02%** on average; LSA+OnZeta achieves +1.94% avg over CLIP baseline.
- Largest single-dataset gains for LSA (ResNet-50): EuroSAT +8.70%, Cifar10 +5.96%, Cifar100 +4.62%, CUB +3.72%—all high-shift domains.
- LSA+OnZeta further improves over standalone LSA on most datasets, confirming composability.
- Evaluated across 14 datasets covering fine-grained recognition, texture, satellite imagery, scene understanding, and action recognition.

## Limitations
- Assumes label shift (p(x|y) invariant across domains); covariate shift is explicitly out of scope, so performance may degrade when both shift types are present.
- Requires accumulating a prediction buffer over the stream; very short streams give a noisy π estimate despite the annealing heuristic.
- Source prior c is fixed to uniform (1/K), which may not hold for CLIP trained on long-tailed web data.
- No theoretical convergence guarantee for the online EM under the active (streaming) regime.
- Ablation studies are deferred to supplementary material, limiting reproducibility from the main paper alone.

## Relevance to Vision-Language Models
LSA exposes a fundamental calibration problem in deploying CLIP-style VLMs in non-i.i.d. inference settings: the model's implicit source prior is baked into its softmax outputs but rarely matches real deployment distributions. The posterior-reweighting correction is a principled, lightweight layer that requires no changes to the VLM itself, making it immediately applicable to any frozen CLIP variant. For researchers tracking VLMs, this paper establishes label shift correction as a complementary axis to prompt engineering and feature alignment for improving zero-shot reliability. It also connects the VLM adaptation literature to classical domain adaptation theory (MAPLS, Dirichlet priors), opening a line of work on statistically grounded inference-time calibration for large vision-language models.

## Tags
#vlm #clip #zero-shot-learning #test-time-adaptation #label-shift #domain-adaptation #online-learning #calibration
