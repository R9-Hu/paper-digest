---
title: "PhysVLA: Towards Physically-Grounded VLA for Embodied Robotic Manipulation"
authors: ["Namai Chandra", "Shriram Damodaran", "Lin Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13886"
url: "http://arxiv.org/abs/2606.13886v1"
pdf: "paper/vlm/[Arxiv 2026] PhysVLA Towards Physically-Grounded VLA for Embodied Robotic Manipulation.pdf"
---

# PhysVLA: Towards Physically-Grounded VLA for Embodied Robotic Manipulation

## TL;DR
PhysVLA is a training-free, plug-and-play inference-time wrapper that adds physics awareness to any frozen Vision-Language-Action (VLA) model without touching its weights. It intercepts predicted actions and applies a two-branch correction — a phase-aware finite-state machine and a selective Euler-Lagrange gate — adding under 1 ms overhead per control step. On LIBERO-Spatial, it yields up to +17 pp success and +19 pp stability across four distinct VLA backbones with zero per-task regressions.

## Problem
VLA models are trained purely on demonstration data and encode no explicit physical constraints (rigid-body dynamics, contact feasibility, energy balance), producing a "physics gap": they emit kinodynamically inconsistent actions, such as premature grasps or full-velocity placements onto sub-centimetre targets. Off-the-shelf fixes like uniform temporal smoothing (EMA) improve trajectory smoothness but degrade task success by flattening responsive bursts needed during contact; memory-augmented chunking recovers local coherence but lacks global phase-level physical context and increases inference cost.

## Method
PhysVLA wraps a frozen VLA backbone at inference time via two parallel branches applied to each intercepted action vector:

**Branch A — Phase-Aware FSM Injector:** A rule-based finite-state machine detects one of four manipulation phases (approach, grasp, transport, place) using geometric predicates on horizontal end-effector-to-object distances. Each phase applies a qualitatively distinct correction: approach uses a premature-grasp veto (gripper command zeroed when distance ≥ 6 cm); grasp applies a guidance bias (β=0.5) toward a computed waypoint with no smoothing; transport applies a vertical lift bias (+2 cm) and position EMA (α=0.92) to suppress jitter; placement scales action magnitude by proximity to enforce a deceleration ramp.

**Branch B — Selective Euler-Lagrange Gate:** Computes the Euler-Lagrange residual r_EL = M(q)q̈ + C(q,q̇)q̇ + G(q) − τ using MuJoCo's internal dynamics oracle. The gate fires only when ‖r_EL‖ > ε (ε=0.05 N·m), blending an inertia-weighted correction into the action only when kinodynamic inconsistency is detected; otherwise it is a no-op.

The two branches are combined into a physics candidate a_phys, then blended with the original VLA output via a global capped blender: a_t = 0.95·a_VLA + 0.05·a_phys, with a hard gripper override for deliberate grasp commands. No backbone weights are modified; no per-task or per-backbone hyperparameter tuning is performed.

## Key Contributions
- Empirical characterisation of the "physics gap" in both single-step and chunked VLA models on LIBERO-Spatial, showing uniform temporal smoothing consistently degrades success.
- PhysVLA: a backbone-agnostic, training-free inference-time corrector combining a phase-aware FSM and a selective Euler-Lagrange gate, adding <1 ms latency per step.
- Systematic evaluation across four VLA paradigms (single-step autoregressive, chunked, force-residual, flow-matching) under a unified PyTorch stack with zero per-task regressions.
- Cross-simulator validation on Robosuite Lift showing ~10× jerk robustness improvement over baseline under Gaussian XY noise.
- Real-world transfer to an Agilex Piper 6-DoF arm with no retraining, achieving 95% vs. 45% baseline placement success.

## Results
- **LIBERO-Spatial (aggregate over T0–T9, n=5 trials, seed 7):**
  - OpenVLA: success 36% → 53% (+17 pp), stability 20.1% → 36.8% (+16.7 pp)
  - OpenVLA-OFT (chunked): success 92% → 95% (+3 pp), stability 86.1% → 88.9% (+2.8 pp)
  - Force-VLA: success 40% → 53% (+13 pp), stability 20.0% → 38.2% (+18.2 pp)
  - Generalist-VLA: success 36% → 50% (+14 pp), stability 29.9% → 49.2% (+19.3 pp)
- **Temporal smoothing degrades every single-step backbone:** OpenVLA 36% → 28%, Force-VLA 40% → 36%, Generalist-VLA 36% → 26%.
- **Robosuite Lift cross-simulator sweep (σ=0.40 XY noise):** PhysVLA mean jerk 0.075 vs. Baseline 0.176 (58% reduction, ~10× lower degradation rate); reward 11.06 vs. 10.89.
- **Real-world Agilex Piper (n=20 trials):** success 45% → 95%; mean trajectory jerk ≈0.05 → ≈0.005 (~10× smoother).
- **Inference overhead:** ≈0.6 ms per step (Branch A ≈0.2 ms, Branch B ≈0.4 ms) vs. VLA forward pass of 30–90 ms.
- **Hard failure ceiling:** Tasks T4 and T9 remain at 0% across all single-step backbones, identified as the structural limit of post-hoc injection for occluded contact-rich targets.

## Limitations
- Requires accurate URDF/XML kinematic and inertial parameters; miscalibrated robot models force fallback to data-driven dynamics approximations, losing the closed-form Euler-Lagrange guarantee.
- The 5% blend cap is insufficient to resolve tasks requiring sub-centimetre precision (e.g., T5) where physical structure must be integrated at training time.
- Phase predicates use fixed geometric thresholds (6 cm) derived from the LIBERO-Spatial bowl/plate task; generalisation to deformable objects or non-pick-place morphologies requires learned visual cues (acknowledged as future work).
- Branch B (EL gate) is evaluated on OpenVLA only; chunked OFT's step-level coherence renders it redundant there, but its standalone contribution is not isolated for force-conditioned or flow-matching heads.
- Simulation dependency: dynamics oracle is sourced from MuJoCo; on-board sensor-based dynamics is left to future work.

## Relevance to Vision-Language Models
PhysVLA addresses a structural deficit of VLA models — the conflation of semantic reasoning with physical plausibility — by treating physics enforcement as a composable inference-time module rather than a training objective, which directly enables reuse of large frozen VLM backbones (e.g., OpenVLA-7B) without retraining. This is highly relevant to researchers tracking VLMs because it demonstrates that post-hoc physical grounding can close a non-trivial performance gap (up to 17 pp on established benchmarks) without modifying the multimodal reasoning layer, suggesting a path toward modular specialisation of general-purpose VLMs for safety-critical embodied tasks. The work also empirically distinguishes failure modes attributable to the VLM backbone's physics blindness from those resolvable by temporal ensembling, contributing a diagnostic framework useful for benchmarking future VLA architectures.

## Tags
#vla #embodied-ai #physics-informed #robotic-manipulation #inference-time-adaptation #frozen-backbone #finite-state-machine #euler-lagrange
