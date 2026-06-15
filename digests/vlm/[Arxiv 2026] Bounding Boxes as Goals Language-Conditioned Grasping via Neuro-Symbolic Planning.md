---
title: "Bounding Boxes as Goals: Language-Conditioned Grasping via Neuro-Symbolic Planning"
authors: ["Allison Andreyev", "Landon Eum", "Nestor Tiglao", "Romel Gomez"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.12910"
url: "http://arxiv.org/abs/2606.12910v2"
pdf: "paper/vlm/[Arxiv 2026] Bounding Boxes as Goals Language-Conditioned Grasping via Neuro-Symbolic Planning.pdf"
---

# Bounding Boxes as Goals: Language-Conditioned Grasping via Neuro-Symbolic Planning

## TL;DR
GRASP is a training-free neuro-symbolic framework for language-conditioned tabletop grasping that converts natural-language instructions into symbolic goal states (bounding-box JSON) via an LLM, then grounds them in real-time using GroundingDINO and a proportional RPY controller. It achieves 73.3% overall grasp success across 90 trials without any fine-tuning. The key insight is decoupling high-level semantic parsing from low-level closed-loop control via bounding-box feedback.

## Problem
Existing language-conditioned manipulation methods either require large-scale policy learning/demonstrations or rely on rigid symbolic structures (fixed color lists, hardcoded coordinates) that cannot handle abstract spatial language like "top shelf." No lightweight, training-free pipeline connects open-vocabulary language understanding to closed-loop robot control.

## Method
GRASP has two coupled components:

**Neural (language/perception):** GPT-5.2 parses a natural-language instruction into a JSON goal state — a set of labeled bounding boxes with spatial constraints (e.g., `y ≤ τ₁` for "top shelf"). These object labels are forwarded as candidate queries to GroundingDINO, which produces per-frame bounding-box detections from both a global shelf webcam and an end-effector PiCam.

**Symbolic (control/evaluation):** Each frame is serialized as a JSON scene state. A goal-similarity score `S` is computed by averaging per-object IoU + normalized center-distance scores against goal annotations. A finite-state machine (FSM) drives a proportional RPY controller: image-space offset from the claw's optical center to the highest-logit detection box is deadband-clipped, exponentially smoothed (factor α), and converted to yaw/pitch increments. Grasp is triggered when the target box area fraction exceeds threshold τ_close. Task terminates when S exceeds threshold or objects go undetected for several consecutive frames.

## Key Contributions
- GRASP framework: neuro-symbolic pipeline compiling natural language to explicit JSON goal states (bounding-box coordinate constraints for abstract spatial terms)
- Training-free closed-loop execution via bounding-box goal similarity, requiring no policy learning
- Lightweight grounding pipeline coupling GroundingDINO open-vocabulary detection to proportional RPY control with exponential smoothing and deadband
- User study (n=31) validating goal-state generation quality across four linguistic reasoning categories (mean Likert 4.18/5)

## Results
- **Overall grasp success: 73.33%** across 90 trials (9 object types × 10 trials each, 3 difficulty levels)
  - Easy (single object, minimal occlusion): 86.67% (26/30)
  - Medium (distractors, partial occlusion): 76.67% (23/30)
  - Hard (heavy clutter, specific categories): 56.67% (17/30)
- **Ablation (10 trials each):**
  - Full system (closed-loop + smoothing + deadband + highest-logit): 8/10, 4.04 s total
  - Open-loop variant: 4/10, 12.42 s total
  - No smoothing/deadband: 5/10, 7.07 s total
  - Random logit selection: 3/10, 6.00 s total
  - First-match selection: 4/10, 4.13 s total
- No comparison to prior SOTA baselines on a shared benchmark; all comparisons are ablative

## Limitations
- No end-to-end sorting evaluation (placement verification via goal similarity not tested on hardware); full pipeline left to future work
- Only 3-DOF gantry arm; roll fixed at zero, limiting grasp diversity
- GroundingDINO inference offloaded over WiFi to a MacBook — not a self-contained embedded system; network latency (mean ~3.5 s) dominates trial time
- Hard category success (56.67%) degrades primarily due to missed/incorrect detections, not the control logic, suggesting the perception bottleneck is unresolved
- User study participants rate visualizations, not actual robot performance; spatial ambiguity (left/right shelf halves) causes highest variance
- No comparison against learned baselines (e.g., VoxPoser, CogACT) on standard benchmarks

## Relevance to Vision-Language Models
GRASP demonstrates a concrete lightweight deployment pattern for VLMs in embodied settings: using an LLM strictly for structured semantic parsing (goal state generation) and a specialized open-vocabulary detector (GroundingDINO) strictly for grounding, rather than end-to-end VLA policy models. This modular VLM-as-parser paradigm is directly relevant to VLM researchers studying how to extract structured spatial representations from free-form language without fine-tuning. The work also surfaces a recurring gap in VLM-to-robot pipelines: perception reliability (open-vocabulary detection under clutter) remains the binding constraint even when language understanding is adequate, which has implications for how VLMs are evaluated and deployed in physical grounding tasks.

## Tags
#vlm #embodied-ai #language-conditioned-manipulation #neuro-symbolic #open-vocabulary-detection #grounding #robot-grasping #training-free
