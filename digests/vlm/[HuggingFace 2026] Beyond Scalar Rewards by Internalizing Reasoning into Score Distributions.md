---
title: "Beyond Scalar Rewards by Internalizing Reasoning into Score Distributions"
authors: ["Xin Jin", "Huanqia Cai", "Zhen Li", "Zechao Zhan", "Dengyang Jiang", "Aiming Hao", "Yuming Jiang", "Chunle Guo", "Peng Gao", "Ming-Ming Cheng", "Steven C. H. Hoi"]
source: "HuggingFace"
venue: ""
published: "2026-06-08"
published_time: "2026-06-08T00:00:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.09076"
url: "https://huggingface.co/papers/2606.09076"
pdf: "paper/vlm/[HuggingFace 2026] Beyond Scalar Rewards by Internalizing Reasoning into Score Distributions.pdf"
---

# Beyond Scalar Rewards by Internalizing Reasoning into Score Distributions

*🕒 **Published (v1):** 2026-06-08 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.09076)*

## TL;DR
Z-Reward is a teacher-student reward modeling framework for text-to-image post-training that replaces scalar reward outputs with full score distributions. A large VLM teacher is trained via Group-wise Direct Score Optimization (GDSO) to produce reasoning-conditioned rubric-aligned score distributions, and a compact student is trained via Reasoning-Internalized Score Distillation (RISD) to internalize those distributions without generating reasoning chains at inference time. The 9B student reaches 88.6% human preference accuracy—nearly matching the 27B teacher—while outputting scores in a single token.

## Problem
Existing reward models for visual generation face a core tension: scalar/pairwise models are deployment-efficient but over-compress annotator uncertainty and fine-grained score differences, while reasoning-based generative reward models produce higher-quality judgments but are slow, non-differentiable, and unsuitable for large-scale gradient-based optimization. Explicit distributional approaches require repeated per-sample annotations, which are costly to scale. No existing paradigm simultaneously achieves reasoning-quality judgment, score uncertainty representation, gradient backpropagability, and inference efficiency.

## Method
**Teacher training (GDSO):** Starting from Qwen3.5-27B, the teacher generates a reasoning trace and predicts a distribution over rubric-aligned score bins using a Q-Align-style score decoder. Training augments GRPO's policy-gradient objective with two direct supervised terms: (1) a pointwise cross-entropy loss anchoring each sampled score distribution to the annotated bin, and (2) a pairwise score-gap loss matching the predicted expected-score difference between same-prompt candidate pairs to the annotated gap—replacing the Bradley-Terry binary objective, which permits unbounded margin growth. Rewards are computed from the expectation of the decoded score distribution rather than parsed text tokens, preserving fine-grained sub-integer signals.

**Student distillation (RISD):** The 27B teacher generates reasoning traces and produces calibrated score distributions for each (prompt, image, dimension) triple. The 9B student (Qwen3.5-9B) is trained via forward-KL minimization to match these reasoning-conditioned distributions directly, without producing reasoning tokens—transferring the distributional outcome of reasoning rather than its sequential process. At inference the student outputs a score in a single token.

**Deployment:** The student reward is used as a differentiable signal for text-to-image RL optimization via ReFL-style direct reward backpropagation through the diffusion denoising process, aggregating four dimensions: text-image alignment, realism, aesthetics, and physical plausibility.

## Key Contributions
- Z-Reward teacher-student framework decoupling reasoning-heavy judgment from efficient deployment via score-distribution transfer.
- GDSO: augments GRPO with pointwise cross-entropy and pairwise score-gap supervised losses on decoded score distributions, enabling calibrated absolute scoring alongside relative preference.
- RISD: distills reasoning-conditioned score distributions into a compact student via KL loss, internalizing reasoning effects without requiring inference-time reasoning chains (single-token output).
- Internally annotated multi-dimensional evaluation set (Text-Image Alignment, Realism, Aesthetics, Physical Plausibility) with 9-level half-point rubric scoring.
- Demonstrated use of the student as a differentiable reward for text-to-image RL optimization.

## Results
- **27B GDSO teacher:** 89.6% HPA, 98.85% margin HPA; PLCC 0.7620, SRCC 0.7132—outperforming SFT (81.35%), RewardDance (84.25%), and GRPO (86.04%) at the same scale.
- **9B RISD student:** 88.64% HPA, 98.01% margin HPA; PLCC 0.7391, SRCC 0.6882—outperforming 9B OPD (83.11% HPA), 9B GDSO (83.95% HPA), and matching the 27B teacher within 1%.
- **Output efficiency:** RISD student outputs 1 token vs. ~750 tokens for OPD and GDSO students.
- **Score distribution decoding ablation:** Computing rewards from distribution expectation consistently outperforms parsed-text rewards for both GRPO and GDSO.
- **Text-to-image RL optimization:** 41.3% net GSB human-preference improvement over the SFT baseline across 400 held-out prompts.

## Limitations
- Evaluation is on an internally annotated test set only; no public benchmark comparison is reported.
- GDSO's combined policy-gradient + direct supervised losses can weaken the coupling between the generated reasoning trace and the final score, making score calibration partially independent of reasoning quality.
- Annotation pipeline requires calibrated human annotators with quality-control auditing, limiting scalability to new domains.
- The teacher's reasoning-conditioned distribution depends on the quality of Qwen3.5-27B reasoning; weaker base models would produce less reliable teacher signals.
- Extension to video, audio, or text-only generation remains unexplored.

## Relevance to Vision-Language Models
Z-Reward directly advances VLM-as-judge methodology by showing that a VLM can be trained—not just prompted—to produce calibrated rubric-aligned score distributions through RL, and that this distributional judgment can be efficiently compressed into a smaller VLM without reasoning chains. The GDSO training strategy is a concrete recipe for reward-modeling VLMs beyond binary preference signals, addressing the reward-hacking risk inherent in scalar RLHF for multimodal generation. For researchers tracking VLMs, the teacher-student distillation paradigm (RISD) is broadly applicable to any setting where a large VLM evaluator must be compressed into a fast, differentiable scoring module—including caption evaluation, video quality assessment, or multi-modal RLHF pipelines.

## Tags
#vlm #reward-model #rlhf #knowledge-distillation #text-to-image #score-distribution #reinforcement-learning #post-training
