---
title: "Multi-Label Test-Time Adaptation with Bayesian Conditional Priors"
authors: ["Qiru Li", "Ao Zhou", "Zhiwei Jiang", "Zifeng Cheng", "Cong Wang", "Yafeng Yin", "Qing Gu"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T05:29:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.12925"
url: "http://arxiv.org/abs/2606.12925v1"
pdf: "paper/vlm/[Arxiv 2026] Multi-Label Test-Time Adaptation with Bayesian Conditional Priors.pdf"
---

# Multi-Label Test-Time Adaptation with Bayesian Conditional Priors

*🕒 **Published (v1):** 2026-06-11 05:29 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.12925v1)*

## TL;DR
CLIP's zero-shot multi-label inference scores labels independently via softmax, causing dominant labels to suppress co-occurring compatible ones under distribution shift. BCP (Bayesian Conditional Priors) corrects this at test time by selecting a high-confidence anchor label and applying a closed-form logit adjustment equal to the pointwise mutual information (PMI) between each label and the anchor, estimated online from unlabeled test-stream co-occurrence statistics. The method is gradient-free, adds negligible overhead beyond a single forward pass, and consistently outperforms all TTA baselines across CLIP backbones and multi-label benchmarks.

## Problem
Standard zero-shot CLIP applies softmax over class logits, which encodes a mutual-exclusivity bias that ignores label co-occurrence structure — critical for multi-label recognition. Under distribution shift, this produces incoherent label sets where dominant concepts suppress weaker but semantically compatible labels. Existing single-label TTA methods cannot address this; the only dedicated multi-label TTA baseline (BEM) requires iterative backpropagation and external caption retrieval, making it impractical for real-time deployment.

## Method
BCP reframes CLIP's zero-shot softmax posterior as the product of a fixed image–text likelihood and a (mismatched) marginal label prior. Given a test image:
1. **Anchor selection**: the highest-confidence label (above threshold µ) is designated as anchor `ca`.
2. **Bayesian refinement**: each non-anchor logit `sk` is additively corrected by `∆prior = log P(ck=1|ca=1) − log P(ck=1)`, which equals the PMI between `ck` and `ca`. Positive PMI promotes co-occurring labels; negative PMI suppresses incompatible ones.
3. **Online prior estimation**: marginal probabilities `P(ck)` and conditional priors `P(ck|ca)` are estimated causally from running first- and second-order statistics of zero-shot posteriors over the test stream (a K×K co-occurrence matrix `U` and marginal vector `m`), updated only from original CLIP posteriors (not corrected logits) to prevent error feedback.

The entire correction is closed-form in logit space; the backbone is never modified.

## Key Contributions
- Identification of label-independence (from softmax + independent scoring) as the root failure mode of lightweight multi-label TTA for frozen VLMs under shift.
- BCP: an anchor-conditioned Bayesian logit correction with a rigorous PMI interpretation, requiring no backpropagation, no labeled data, and no external knowledge.
- Closed-form online estimator of anchor-conditioned priors from second-order co-occurrence statistics maintained with constant memory.
- Proof that the correction is equivalent to a log Bayes factor and that in expectation it induces a non-negative KL divergence shift toward the conditional prior.

## Results
- **RN50**: CLIP baseline 57.31 mAP → BCP 69.22 mAP (avg. over COCO2014, COCO2017, VOC2007, VOC2012, NUSWIDE); best prior method (DOTA) 64.17.
- **ViT-B/16**: CLIP 62.61 → BCP 71.79; prior SOTA SCA 69.24.
- **Efficiency on COCO2014 (RN50)**: BCP 61.69 mAP at 0.112s/sample vs. BEM 51.58 mAP at 0.24s; BCP is ~2× faster than BEM and faster than TPT while gaining +13.17 mAP over TPT.
- **Anchor-hit subset (ViT-B/16)**: mAP rises from 72.73 (CLIP) to 80.33 (BCP); anchor-hit share exceeds 89% on COCO/VOC.
- **Label-count robustness**: BCP improves over all baselines at all label-count bins ({1,2}, {3,4}, {5,6,7}, {≥8}) on COCO2014.
- **Head/medium/tail splits**: BCP outperforms CLIP and SCA in all frequency bins on all five datasets; tail labels are not suppressed.
- **Ordering robustness**: variance across 5 random test-stream permutations is negligible (e.g., COCO2014 std < 0.05 mAP).

## Limitations
- Relies on a single anchor; semantic correctness of the anchor is critical — on small-labelset datasets (VOC) where a wrong anchor comes from a different semantic scene, Anchor-Miss samples see mAP drops (−3.75 on VOC2007).
- Pairwise co-occurrence statistics cannot capture higher-order label interactions (e.g., triplet co-occurrences).
- Online estimation degrades under severe concept drift or heavily miscalibrated CLIP posteriors.
- Anchor selection via softmax argmax is unsuitable for sigmoid-based multi-label heads; the framework presupposes CLIP's softmax formulation.
- No evaluation on open-vocabulary or dense-prediction (detection/segmentation) settings.

## Relevance to Vision-Language Models
BCP directly addresses a structural weakness of CLIP-style VLMs in multi-label settings: their contrastive pre-training objective induces label independence that is correct for retrieval but harmful for compositional scene recognition. The work contributes a theoretically grounded, deployment-friendly post-hoc correction that preserves the frozen backbone — relevant to the broad trend of adapter-free, inference-time VLM specialization. It connects to the growing literature on TTA for VLMs (TPT, TDA, DOTA) but carves out the underexplored multi-label axis, showing that prior calibration — not prompt or parameter tuning — is the right lever when label co-occurrence structure is the primary source of shift-induced error. For researchers tracking VLMs, BCP illustrates how Bayesian reinterpretation of zero-shot logits can unlock structured prediction without any architectural change.

## Tags
#vlm #clip #test-time-adaptation #multi-label-recognition #bayesian #pointwise-mutual-information #distribution-shift #zero-shot
