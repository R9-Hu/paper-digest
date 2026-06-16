---
title: "Post-Launch Capability Expansion of Vision-Language Models via Prompting for On-Orbit Spacecraft Inspection"
authors: ["Nicholas A. Welsh", "Lennon J. Shikhman", "Monty Nehru Attazs", "Seemanthini K. Putane", "Van Minh Nguyen", "Ryan T. White"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T18:29:24+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15427"
url: "http://arxiv.org/abs/2606.15427v1"
pdf: "paper/vlm/[Arxiv 2026] Post-Launch Capability Expansion of Vision-Language Models via Prompting for On-Orbit Spacecraft Inspection.pdf"
---

# Post-Launch Capability Expansion of Vision-Language Models via Prompting for On-Orbit Spacecraft Inspection

*🕒 **Published (v1):** 2026-06-13 18:29 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15427v1)*

## TL;DR
Spacecraft perception models must be deployed before launch with fixed weights, making post-launch semantic expansion via retraining operationally infeasible. This paper evaluates whether frozen, prompt-driven VLMs (specifically SAM3) can extend semantic coverage of new spacecraft components via natural-language prompt uplinks alone. Results show reliable zero-shot segmentation for large structures but substantial failure on fine-scale appendages.

## Problem
Supervised spacecraft perception models have fixed label sets baked in at launch; post-launch weight updates require multi-gigabyte uplinks, software recertification, and are often operationally prohibited. No systematic evaluation existed for whether prompt-conditioned VLMs could serve as a lightweight, byte-scale alternative for semantic expansion after deployment.

## Method
The authors evaluate SAM3 (Segment Anything with Concepts) in a strictly frozen, zero-shot, single-pass inference regime on the Web Satellite Dataset (WSD), augmented with instance-level segmentation masks for four spacecraft component classes: antenna, thruster, solar array, and spacecraft body. A single fixed natural-language prompt per class is applied uniformly across all 129 held-out test images. Prompts are engineered on the development split using compound subtype descriptions, explicit spatial grounding phrases (e.g., "extending from the spacecraft"), and geometric descriptors (e.g., "boxy or cylindrical"). No fine-tuning, adapter layers, post-processing, or interactive refinement is used. Predictions are binarized at a fixed mask threshold of 0.40 with a score threshold of 0.05.

## Key Contributions
- Deployment-faithful evaluation protocol: frozen weights, single-pass inference, no post-processing, uniform thresholds across classes.
- Empirical characterization of scale-dependent asymmetry in zero-shot VLM grounding on orbital imagery.
- Prompt engineering ablation demonstrating that structured prompts (spatial + geometric descriptors) outperform category-name prompts by up to 82% AP@0.5.
- Feasibility assessment of prompt-driven semantic expansion as a post-launch mechanism within embedded GPU compute envelopes (Jetson Orin-class).

## Results
- SAM3 achieves **0.385 mAP@0.5** and **0.267 mAP@0.5:0.95** on the 129-image held-out test set (871 instances), zero-shot.
- Per-class AP@0.5: spacecraft body **0.639**, solar array **0.598**, antenna **0.221**, thruster **0.081**.
- Structured prompt vs. category-name prompt: solar array AP@0.5 improved from 0.367 → 0.580 (+58%); spacecraft body from 0.267 → 0.485 (+82%).
- No supervised baseline is reported; evaluation is absolute (the contribution is characterizing feasibility, not beating a prior model).

## Limitations
- Only one VLM (SAM3) is evaluated; findings are not generalizable to other promptable models.
- Only one dataset (WSD, four component classes) is used; findings may not transfer to other satellite configurations or orbital conditions.
- Runtime and energy measurements on actual flight-relevant hardware (e.g., Jetson Orin) are not reported—compute compatibility is inferred, not measured.
- Prompt sensitivity means prompt selection itself constitutes implicit task calibration, introducing an uncontrolled design variable.
- Thrusters (AP@0.5 = 0.081) remain far below operational reliability; fine-scale component localization is unsolved.
- No comparison to any closed-set supervised baseline, making it hard to quantify the zero-shot capability gap.

## Relevance to Vision-Language Models
This paper directly probes a practical deployment constraint for VLMs: what happens when prompt engineering is the *only* available adaptation mechanism after deployment? The finding that structured prompts incorporating spatial and geometric descriptors can recover up to 82% more AP than naive category-name prompts is directly relevant to open-vocabulary grounding research, underscoring that prompt formulation is a non-trivial hyperparameter even for large, general-purpose models like SAM3. The domain-shift regime (natural-image-pretrained models applied to orbital imagery) connects to ongoing VLM generalization work, and the scale-dependent failure mode (thin, low-pixel-support objects) is a known VLM weakness that this paper concretely quantifies in a new, high-stakes domain. For researchers tracking VLMs, this provides a real-world stress test of zero-shot grounding under strict frozen-weight constraints.

## Tags
#vlm #zero-shot #instance-segmentation #open-vocabulary #prompt-engineering #domain-shift #spacecraft #sam
