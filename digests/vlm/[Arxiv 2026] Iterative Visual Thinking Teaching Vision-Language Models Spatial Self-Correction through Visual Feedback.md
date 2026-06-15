---
title: "Iterative Visual Thinking: Teaching Vision-Language Models Spatial Self-Correction through Visual Feedback"
authors: ["Animesh Tripathy", "Aswanth Krishnan"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13156"
url: "http://arxiv.org/abs/2606.13156v1"
pdf: "paper/vlm/[Arxiv 2026] Iterative Visual Thinking Teaching Vision-Language Models Spatial Self-Correction through Visual Feedback.pdf"
---

# Iterative Visual Thinking: Teaching Vision-Language Models Spatial Self-Correction through Visual Feedback

## TL;DR
VLMs achieve strong single-shot spatial grounding but catastrophically fail (−31pp Acc@0.5) when naively asked to iterate over rendered visualizations of their own predictions. Iterative Visual Thinking (IVT) closes this self-correction gap with a two-phase SFT+GRPO recipe, recovering and surpassing the base model on referring expression comprehension using only 2,400 training samples on a single GPU.

## Problem
VLMs that excel at single-shot referring expression comprehension (REC) have no mechanism to observe and correct their own spatial predictions. Naively injecting rendered bounding-box overlays as visual feedback produces catastrophic degradation (79.6% → 48.7% Acc@0.5), revealing that spatial grounding capability does not imply spatial self-correction capability. Test-time compute scaling, proven for textual reasoning (o1, DeepSeek-R1), had no principled extension to the visual-spatial domain.

## Method
IVT implements a closed-loop predict-render-refine loop. At step 0, the model predicts a bounding box from the image and expression. At each subsequent step, the previous prediction is rendered as a semi-transparent red overlay on the original image, injected as a new visual input, and the model generates a corrective reasoning trace followed by a refined box — all within a single autoregressive continuation via prefix-continuation.

**Training is two-phase:**

1. **SFT warm-up:** The base Qwen3-VL-4B generates step-0 predictions for 2,400 samples; those with IoU ∈ [0, 0.85] are retained (934 trajectories). A teacher VLM generates step-conditioned corrective reasoning traces along linear-interpolation trajectories from student prediction to ground truth. The student is fine-tuned on these via cross-entropy loss (LoRA rank 64, 4-bit NF4 quantization). Crucially, student predictions rather than randomly perturbed GT boxes are used as step-0 errors to avoid "step-0 sandbagging" during GRPO.

2. **GRPO fine-tuning:** Starting from the SFT checkpoint, N=6 trajectories are sampled per prompt and scored with a simple reward: final-step IoU plus a 0.1-scaled format bonus. Group-relative advantages normalize within the batch; KL regularization (β=0.04) anchors to the SFT reference policy.

## Key Contributions
- Empirical demonstration of the spatial self-correction gap: naive iterative visual prompting collapses Acc@0.5 by 31pp, extending the LLM self-correction failure finding to the spatial-visual domain.
- IVT closed-loop framework: predict → render overlay → inject as visual input → refine, operating within a single autoregressive sequence.
- Self-referential data synthesis: using the student model's own predictions as step-0 errors eliminates human annotation and avoids the sandbagging artifact of GT-perturbation.
- Asymmetric two-phase training: SFT bootstraps all accuracy gains; GRPO reduces per-step IoU degradation 5× (0.140 → 0.029), stabilizing multi-step refinement.
- Data efficiency: full pipeline trains on 934 effective trajectories (2,400 raw samples) on a single GPU.

## Results
All results on a balanced 505-sample test set (RefCOCOg + Ref-Adv-S + Ref-L4):

- Base (single-shot): Acc@0.5 = 79.6%, Acc@0.7 = 70.9%, Acc@0.9 = 45.5%, mean IoU = 0.719
- Base + IVT (no training): Acc@0.5 = **48.7%** (−31pp), Acc@0.7 = 44.2%, Acc@0.9 = 28.3%, mean IoU = 0.442
- SFT + IVT: Acc@0.5 = **82.0%** (+2.4pp), Acc@0.7 = **74.1%** (+3.2pp), Acc@0.9 = **48.3%** (+2.8pp), mean IoU = 0.743 — best overall accuracy
- SFT + GRPO + IVT: Acc@0.5 = 80.6%, Acc@0.7 = 72.5%, mean IoU = 0.729; per-step IoU degradation reduced from 0.140 (SFT alone) to **0.029** (5× improvement); samples degrading across steps: 63.4% → 24.8%
- Single-step GRPO (no IVT): Acc@0.5 = 80.0% — matches base, confirming GRPO benefit is specific to multi-step refinement
- Hard cases (step-0 IoU < 0.5) benefit most from IVT: mean IoU 0.108 → 0.149

## Limitations
- Training scale is small (2,400 samples across three datasets); generalization to production-scale REC systems is untested.
- Iterative inference costs T+1× single-step latency (3× for T=2).
- Reward and evaluation target single-object grounding; multi-object and segmentation tasks require new reward designs.
- Evaluated on one model family (Qwen3-VL-4B); dynamics may differ for larger models or other architectures.
- Easy samples occasionally degrade during refinement, motivating adaptive step allocation.
- GRPO stabilizes trajectories but genuine step-over-step IoU improvement across all samples remains unsolved; 64% of GRPO+IVT samples stagnate at step-0 quality.

## Relevance to Vision-Language Models
This paper directly addresses a structural limitation of all current VLMs: their single-shot grounding paradigm prevents closed-loop spatial reasoning, a capability critical for embodied agents. The finding that self-correction is absent from base model rollouts means RL alone cannot discover it — SFT on synthetic correction traces is a prerequisite, which has implications for how test-time compute scaling approaches should be designed for vision-language tasks. The predict-render-refine loop is representation-agnostic and connects to broader work on visual reasoning chains (CogCoM, ViGoRL) while being distinguished by re-injecting the model's own prediction rather than zooming to gather new information. For VLM researchers, the 5× stability improvement from GRPO over SFT alone in multi-step settings provides a concrete recipe for extending R1-style RL training to iterative spatial tasks.

## Tags
#vlm #spatial-grounding #self-correction #referring-expression-comprehension #grpo #test-time-compute #rlvr #visual-feedback
