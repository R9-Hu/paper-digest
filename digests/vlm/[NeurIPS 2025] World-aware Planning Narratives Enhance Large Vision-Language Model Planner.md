---
title: "World-aware Planning Narratives Enhance Large Vision-Language Model Planner"
authors: ["Junhao Shi", "Zhaoye Fei", "Siyin Wang", "Qipeng Guo", "Jingjing Gong", "Xipeng Qiu"]
source: "NeurIPS"
venue: "NeurIPS 2025"
published: "2025-01-01"
year: 2025
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "openreview:fggSyPPk0K"
url: "https://openreview.net/forum?id=fggSyPPk0K"
pdf: "paper/vlm/[NeurIPS 2025] World-aware Planning Narratives Enhance Large Vision-Language Model Planner.pdf"
---

# World-aware Planning Narratives Enhance Large Vision-Language Model Planner

## TL;DR

WAP (World-Aware Planning Narrative Enhancement) is a data augmentation and curriculum training framework that systematically develops four cognitive capabilities in LVLMs for embodied planning. By generating multi-dimensional instruction variants and stepwise reasoning chains from existing ALFRED trajectories, then training via a three-stage curriculum, WAP elevates a 7B open-source model from 4.7% to 62.7% task success on EB-ALFRED—surpassing GPT-4o and approaching Claude-3.5-Sonnet—using only raw egocentric visual observations without privileged environmental feedback.

## Problem

Existing embodied planning systems use environment-agnostic imitation learning that treats task instructions and environmental context as disconnected elements. Models trained on simplified, environment-independent instructions (e.g., "put the apple on the table") fail to generalize to context-sensitive instructions, unfamiliar environments, and long-horizon multi-step tasks. They also depend on supplementary runtime cues (action success signals, task progress indicators) that are unavailable in genuine deployment.

## Method

WAP operates in three steps:

1. **Multi-dimensional instruction augmentation**: A teacher model (Qwen2.5-VL-72B) rewrites each original ALFRED instruction into four variants targeting distinct cognitive dimensions—Visual (object appearance attributes), Spatial (landmark-relative positions), Functional (affordances and causal relationships), and Syntactic (indirect references, linguistic ambiguity). Semantic consistency verification ensures augmented instructions preserve the original intent; failing instructions are regenerated. This expands 16,145 ALFRED trajectories to 80,875 instruction-trajectory pairs.

2. **Stepwise reasoning generation**: For each action step $a_t$, the teacher generates an explicit reasoning chain $r_t$ conditioned on the augmented instruction, current observation, and prior action-reasoning history. These serve as intermediate supervision targets.

3. **Three-stage curriculum learning**: Training proceeds from (D1) base instruction-trajectory pairs → (D2) visual and spatial augmentations → (D3) functional and syntactic augmentations, progressively increasing cognitive complexity. The model operates in closed-loop on egocentric RGB observations only.

## Key Contributions

- Multi-dimensional cognitive enhancement data pipeline that converts environment-agnostic imitation data into world-aware training signal across four complementary reasoning dimensions.
- Demonstration that closed-loop embodied agents using only raw visual observations can match or surpass proprietary models with privileged feedback.
- New state-of-the-art on EB-ALFRED: +60.7 absolute success rate over baseline, outperforming GPT-4o (56.3) and approaching Gemini-1.5-Pro (62.3) without action feedback.

## Results

**EB-ALFRED (Qwen2.5-VL-7B):**
- Baseline: 4.7% → WAP + Curriculum: 62.7% (+58.0 absolute; ~13.5× improvement)
- Commonsense reasoning: 22 → 62 (+40)
- Long-horizon planning: 2 → 70 (+68)
- Complex: 6 → 70 (+64)
- STD (robustness): 14.0 (basic reasoning) → 6.3 (full WAP), lower than Claude-3.5-Sonnet (8.6)

**EB-ALFRED (InternVL3-8B):**
- Baseline: 10.7% → WAP + Curriculum: 61.0% (+50.3 absolute)

**Closed-loop setting vs. proprietary:**
- GPT-4o closed-loop: 26.0; Claude-3.5-Sonnet closed-loop: 57.3; WAP: 62.7

**VOTA-Bench unseen split (vs. GPT-4o):**
- Overall SR: GPT-4o 20.36% → WAP 64.56%; PL: 16.83 → 59.86
- WAP outperforms GPT-4o across all five task families

**Ablation (Qwen2.5-VL-7B):**
- Removing curriculum: 62.7 → 58.0 (−4.7); removing stepwise reasoning: 58.0 → 54.0; removing first-step reasoning: 54.0 → 46.7; removing WAP instruction: 47.0

**Teacher model scaling:**
- Qwen2.5-7B teacher: 54.67 avg; 32B: 57.33; 72B: 62.67

## Limitations

- Operates at symbolic action level only; lacks continuous control parameter modeling, requiring future integration with low-level motor controllers.
- Evaluated only on household environments (ALFRED-derived); generalizability to industrial or outdoor settings with dynamic obstacles is unverified.
- Training-time enhancement of instructions and reasoning does not support mid-execution error correction; the fine-tuned model has limited capacity for dynamic recovery during deployment.

## Relevance to Vision-Language Models

WAP directly addresses the embodied grounding frontier for LVLMs, showing that targeted data augmentation—rather than model scaling or privileged runtime signals—can unlock dramatic gains in visuospatial reasoning and long-horizon planning. The framework's four cognitive dimensions (visual, spatial, functional, syntactic) map onto known weaknesses in current VLMs when applied to interactive environments, making it a concrete recipe for improving LVLM grounding without architectural changes. The result that a 7B open-source model surpasses GPT-4o on a closed-loop embodied planning benchmark is a strong signal that training data quality and curriculum structure matter more than raw model capacity for this task class. This work connects to the broader line of VLM-for-robotics research by establishing that world-aware narrative generation from existing trajectory data is a scalable path to embodied intelligence.

## Tags

#vlm #embodied-planning #curriculum-learning #data-augmentation #spatial-reasoning #long-horizon-planning #alfred #embodied-ai
