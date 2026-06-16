---
title: "Mirage Probes: How Vision Models Fake Visual Understanding"
authors: ["Daniel Ben-Levi", "Judah Goldfeder", "Weiliang Zhao", "Raz Lapid", "Amit LeVi", "Allen G. Roush", "Ravid Shwartz-Ziv", "Hod Lipson"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T19:51:44+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13870"
url: "http://arxiv.org/abs/2606.13870v1"
pdf: "paper/vlm/[Arxiv 2026] Mirage Probes How Vision Models Fake Visual Understanding.pdf"
---

# Mirage Probes: How Vision Models Fake Visual Understanding

*🕒 **Published (v1):** 2026-06-11 19:51 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13870v1)*

## TL;DR
VLMs can answer image-grounded questions correctly even when no image is provided ("mirage behavior"), inflating benchmarks without genuine visual grounding. This paper introduces Mirage Probes, a contrastive probing framework demonstrating that mirage behavior is linearly decodable from image-present internal activations, and argues that it comprises two mechanistically distinct regimes—spurious images and textual biases—requiring different mitigations.

## Problem
Prior work established that VLMs exhibit "mirage behavior" (confident, often correct answers without images) but treats it as a single failure mode. The internal representational basis of this behavior during normal image-present inference is unknown, and without that understanding it is unclear whether text-distribution cleaning is sufficient or whether representational interventions are also necessary.

## Method
**Dataset construction.** For each base VQA question, GPT-4o-mini generates four paraphrased mutations preserving meaning; the model is run with and without the image on all variants. A response is labeled mirage-like if with-image and without-image answers are similar (bag-of-words cosine ≥ 0.7) and non-mirage if the without-image response explicitly refuses due to missing visual context (regex-detected). Contrastive pairs are drawn from the same base question, keeping image and intent fixed while flipping the mirage label—minimizing surface textual confounds.

**Activation extraction.** Four sites are probed per layer in Ovis2.5-2B and Qwen3-32B-VL-Instruct: residual stream, MLP output, post-attention output, and individual attention heads. Activations are pooled via three schemes (text-token mean, vision-tail, joint vision-text mean). Vision encoder and projection activations showed no detectable mirage signal and were dropped.

**Probe families.** Four classifiers are trained per site: (1) logistic regression (tests linear decodability), (2) two-layer MLP (tests nonlinear advantage), (3) logistic regression on concatenated all-layer activations (tests sparse cross-layer encoding), (4) logistic regression on the difference Δh = h_img − h_∅ (tests representational shift from adding the image).

**Prior Harnessing Index (PHI).** A novel metric defined as log p(a* | Q) − log p(a* | Q∅), measuring how much a question's text alone boosts correct-answer confidence above a null-prompt baseline, capturing VLM-level (not human-level) text-only answer accessibility.

Benchmarks: VQA-RAD (radiology free-form/yes-no), MMMU-Pro (expert multiple-choice), MedXpertQA (medical reasoning), MicroVQA (microscopy; dropped from main results due to insufficient non-mirage samples).

## Key Contributions
- Demonstrates mirage behavior is **linearly decodable** from image-present VLM latent representations across residual stream, MLP, post-attention, and attention-head sites in two open-source VLMs.
- Introduces **Mirage Probes**, a contrastive probing framework using question mutations to suppress surface-level textual confounds; shows probes outperform a Naive Bayes text baseline in all contrastive settings.
- Proposes **two distinct mirage regimes**: *spurious images* (model constructs false visual content in latent space) and *textual biases* (model ignores visual input and answers from language priors), evidenced by cross-benchmark separability patterns and PHI.
- Introduces the **Prior Harnessing Index (PHI)** as a VLM-centric measure of text-only answer accessibility, better explaining per-benchmark mirage rates than human-perceived image reliance.
- Argues **text-distribution cleaning is mechanism-incomplete**: it can target textual-bias mirages but cannot reach spurious-image mirages embedded in visual representations.

## Results
- **Linear probes, residual stream (contrastive):** Ovis up to 75% (VQA-RAD), Qwen up to 72.4% (MMMU-Pro); difference probes reach 97.4% (Ovis, VQA-RAD) and 96.0% (Qwen, VQA-RAD).
- **Attention/post-attention probes (contrastive):** Ovis up to 91.3% (MMMU-Pro difference probe); Qwen up to 95.7% (VQA-RAD difference probe).
- **MLP vs. linear probes:** Two-layer MLP probes do not meaningfully outperform logistic regression in contrastive settings, consistent with linear encoding of mirage information.
- **Naive Bayes text baseline (contrastive):** 45–67% across models and benchmarks, consistently below contrastive probe accuracy, ruling out surface lexical confounds as the source of the probe signal.
- **PHI (Ovis):** VQA-RAD mean PHI = −0.41 (text hurts answer confidence); MMMU-Pro = +1.20; MedXpertQA = +0.30. Mirage correlation with low PHI is −0.36 for VQA-RAD, near zero for the others.
- **Image-reliance annotation (GPT-5-mini):** VQA-RAD mirage examples are overwhelmingly image-reliant (2909/2912); MMMU-Pro and MedXpertQA mirages split ~50/50—supporting the two-mechanism hypothesis.
- Training probes on human-perceived image-reliant vs. image-free subsets of MMMU-Pro/MedXpertQA does not improve separability (60–61%), confirming PHI better captures VLM-level visual dependence.

## Limitations
- Mirage and non-mirage labels are assigned by heuristic (cosine similarity threshold + regex), introducing label noise.
- With-image mirages are unobservable from model outputs alone; probe directions cannot be causally validated (no steering or activation patching experiments).
- The Naive Bayes baseline rules out surface lexical confounds but does not rule out other non-visual confounds; the central claim remains correlational.
- The spurious-images vs. textual-biases decomposition is an empirically motivated hypothesis based on cross-benchmark patterns, not a causally established finding.
- GLM-4.6-flash dropped from main results due to insufficient non-mirage responses; MicroVQA also dropped—the most extreme mirage-rate benchmark is absent from primary analysis.
- Experiments limited to two models (Ovis2.5-2B, Qwen3-32B-VL-Instruct); generalization to other VLM architectures or closed models is untested.

## Relevance to Vision-Language Models
Mirage behavior is a direct threat to the validity of VLM evaluations: benchmarks like MMMU and VQA-RAD may substantially overestimate visual grounding. This paper moves the problem from output-level behavioral observation to representation-level mechanistic analysis, showing that mirage is not an image-absent artifact but a signal encoded in the model's latent space even when an image is present. The two-regime decomposition—spurious images versus textual biases—has immediate practical consequences for VLM alignment and training: RLHF or data cleaning targeting textual shortcuts will leave spurious-image mirages intact, meaning safe deployment in high-stakes domains (medical imaging, document analysis) requires probing or editing the visual representations themselves. The PHI metric also provides a principled benchmark-design tool for distinguishing datasets that genuinely require vision from those solvable by language priors alone.

## Tags
#vlm #hallucination #visual-grounding #probing #mechanistic-interpretability #vqa #mirage #representation-analysis
