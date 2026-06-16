---
title: "IterCAD: An Iterative Multimodal Agent for Visually-Grounded CAD Generation and Editing"
authors: ["Tao Hu", "Jiaxin Ai", "Licheng Wen", "Xueheng Li", "Shu Zou", "Siqi Li", "Nianchen Deng", "Xinyu Cai", "Hongbin Zhou", "Pinlong Cai", "Daocheng Fu", "Yu Yang", "Hairong Zhang", "Botian Shi", "Xuemeng Yang"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T13:53:21+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13368"
url: "http://arxiv.org/abs/2606.13368v1"
pdf: "paper/harness/[Arxiv 2026] IterCAD An Iterative Multimodal Agent for Visually-Grounded CAD Generation and Editing.pdf"
---

# IterCAD: An Iterative Multimodal Agent for Visually-Grounded CAD Generation and Editing

*🕒 **Published (v1):** 2026-06-11 13:53 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13368v1)*

## TL;DR
IterCAD is a closed-loop multimodal agent that recasts CAD generation as multi-turn agent-sandbox interaction, moving beyond one-shot synthesis to iterative "generate–verify–refine" cycles guided by multi-view engineering drawings. A 4B model trained with progressive SFT and geometry-aware RL with Geometry-Viable Prefix Masking (GVPM) outperforms GPT-5 and models an order of magnitude larger on the proposed IterCAD-Bench. A new survivor-bias-free metric (CD-TR / AUC-TR) unifies code executability and geometric fidelity into a single evaluation standard.

## Problem
Existing automated CAD methods use open-loop, one-shot generation that mismatches professional iterative workflows. Prior multi-turn systems use coarse feedback — compiler errors verify only syntactic validity while Chamfer Distance on point clouds captures only global shape error without localizing which sketch parameters or topological entities are faulty, causing iterations to degenerate into blind trial-and-error. Benchmarks are dominated by trivial sketch-and-extrude shapes and suffer from survivor bias: geometric metrics are computed only on successfully executed programs, concealing true robustness.

## Method
**Task formulation.** Three modalities unified under a single protocol: Drawing-to-Code (multi-view engineering drawings → CadQuery), Text-to-Code, and Interactive Editing (source program + natural-language delta → modified program). At each turn `t`, the agent observes full history `O_t = {S, X_ref, (C_1,F_1), ..., (C_{t-1},F_{t-1})}`, emits a `<thinking>` reasoning trace plus a fenced CadQuery block, and receives multimodal feedback `F_t` from an OCCT-kernel sandbox that projects the solid into annotated orthographic views alongside compiler logs.

**Data pipeline.** Drawing-Code pairs are synthesized via the SolidWorks COM interface using an advanced operation space `P_base ∪ P_adv` (fillets, shells, chamfers, etc.). Text-Code pairs are filtered by sandbox execution and CD < 10⁻⁵. Edit-Code pairs apply controlled degradations to create source/target pairs. Qwen3-VL-235B then rolls out multi-turn expert trajectories, filtered for format compliance, logic coherence, and geometric correctness (final CD < 10⁻⁵), yielding 28K SFT trajectories.

**Training (two stages).**
1. *Progressive cold-start SFT*: trains on expert trajectories (DS₁), then augments with on-policy rollouts diagnosed by a teacher model (DS₂) to install iterative debugging behaviors.
2. *Geometry-aware RL via GSPO*: sequence-level policy optimization with length-normalized importance ratios and asymmetric clipping. Composite reward: `R = R_CD + λ_f R_fmt + λ_p R_prog`, where `R_CD` is a piecewise linear function of Chamfer Distance (0 on failure), `R_fmt` enforces structural schema compliance, and `R_prog` gives a sparse bonus for monotonically decreasing CD across ≥2 turns.

**Geometry-Viable Prefix Masking (GVPM).** Identifies a per-trajectory prefix boundary `f = min(f_exec, f_stall)` — either K consecutive runtime errors (execution cascade) or K turns of non-decreasing CD above a quality gate (geometry stall). Tokens beyond `f` are masked from the policy loss, and a one-sided advantage clamp prevents the viable prefix from being penalized by downstream failures, addressing multi-turn credit assignment.

**Evaluation.** CD-TR Curve sweeps a tolerance threshold `τ`; recall `R(τ)` counts samples that both execute and satisfy CD ≤ τ. Failed samples are zero across all `τ`, eliminating survivor bias. AUC-TR is the normalized area under this curve.

## Key Contributions
- **IterCAD agent framework**: unified closed-loop pipeline covering Drawing-to-Code, Text-to-Code, and Interactive Editing with OCCT-based visual feedback.
- **Two-stage training recipe**: progressive SFT (expert + on-policy refinement data) followed by GSPO RL with geometry-aware rewards.
- **Geometry-Viable Prefix Masking (GVPM)**: per-trajectory token masking that solves credit-assignment in multi-turn trajectories with irrecoverable failure points.
- **IterCAD-Bench**: 1K drawing-generation + 200 instruction-editing tasks with advanced manufacturing features.
- **CD-TR / AUC-TR metric**: survivor-bias-free standard jointly quantifying executability and geometric precision.

## Results
**IterCAD-Draw (Agentic Workflow):**
- IterCAD: IR 0.30%, AUC-TR 0.61, Mean CD 5.09 × 10⁻³, 2.48 avg turns
- vs. GPT-5 (best proprietary): IR 4.70%, AUC-TR 0.50, Mean CD 12.18, 2.44 avg turns
- vs. Qwen3.5-4B backbone: IR −62pp, AUC-TR +0.40, Mean CD −7.95 × 10⁻³
- Qwen3.5-35B-A3B (9× parameters): IR 37.5%, AUC-TR 0.36

**IterCAD-Edit:**
- IterCAD: IR 1.00%, AUC-TR 0.54, 2.34 avg turns (vs. Qwen3.5-4B: IR 63%, AUC-TR 0.18)
- GPT-5 leads on AUC-TR (0.79) due to frontier-scale text-to-code reasoning

**External benchmarks:**
- Text2CAD bench: IR 0.64%, Med. CD 0.10 (vs. CAD-Coder: IR 1.45%, Med. CD 0.17; GPT-4o: IR 93%)
- CADPrompt bench: IR 2.00%, Med. CD 2.42 (vs. CAD-Judge Med. CD ~42.69)

**Ablation (IterCAD-Draw, Agentic Workflow):**
- Backbone only: IR 62.3%, AUC-TR 0.21
- +DS₁ SFT: IR 7.5%, AUC-TR 0.52
- +DS₂ (on-policy): IR 0.80%, AUC-TR 0.52, Mean CD 12.44
- +GSPO: IR 1.30%, AUC-TR 0.58, Mean CD 8.00
- +GVPM (full): IR 0.30%, AUC-TR 0.61, Mean CD 5.09

## Limitations
- Scope limited to single-part parametric modeling in CadQuery; assembly-level and proprietary drawing standards not addressed.
- Geometric metrics (Chamfer Distance) cannot capture mechanical semantics: keyways, bearing fits, thread specifications, and other functional manufacturing intents.
- Agent prioritizes geometric convergence over program maintainability, producing hard-coded implementations that lack hierarchical parametric design trees necessary for human collaboration.

## Relevance to Harnesses / Meta-Harnesses
IterCAD is itself a domain-specific agent harness: it formalizes an explicit action/observation loop over an executable CAD sandbox with structured turn-level feedback, closely matching the "harness" pattern of wrapping a model in a tool-execution loop with verifiable exit conditions. The GVPM technique directly addresses a core harness design problem — credit assignment when a loop enters an irrecoverable state — and is transferable to any multi-turn harness where trajectory prefixes can be independently evaluated. The two-stage training recipe (imitation-from-expert-rollouts → RL-over-closed-loop-feedback) is a reusable pattern for bootstrapping agents inside any harness that exposes a reward signal. The CD-TR/AUC-TR metric also illustrates a principled approach to evaluating harness robustness, accounting for both loop termination validity and output quality across the full test distribution.

## Tags
#agent-harness #multi-turn #cad-generation #reinforcement-learning #closed-loop #credit-assignment #geometric-reward #evaluation-metric
