---
title: "Dense Supervision, Sparse Updates: On the Sparsity and Geometry of On-Policy Distillation"
authors: ["Guo Yu", "Wenlin Liu", "Yulan Hu", "Hao-Xuan Ma", "Jun-Peng Jiang", "Han-Jia Ye"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13657"
url: "http://arxiv.org/abs/2606.13657v2"
pdf: "paper/vlm/[Arxiv 2026] Dense Supervision, Sparse Updates On the Sparsity and Geometry of On-Policy Distillation.pdf"
---

# Dense Supervision, Sparse Updates: On the Sparsity and Geometry of On-Policy Distillation

## TL;DR
On-policy distillation (OPD) — training a student on its own rollouts with dense teacher token-level feedback — produces parameter updates that are small, coordinate-sparse, spectrally concentrated, and biased away from the source model's principal singular directions. Despite the dense supervision signal, OPD behaves geometrically closer to sparse on-policy post-training (RLVR) than to offline distillation. Training only the discovered sparse subnetwork nearly recovers full-model performance, but AdamW remains necessary because the dense teacher preserves gradient heterogeneity.

## Problem
Post-training pipelines occupy a spectrum: SFT/offline distillation provides dense supervision on fixed data, RLVR provides sparse reward on on-policy data. OPD sits in between (dense supervision, on-policy data), but whether its weight-space dynamics resemble supervised fine-tuning, RLVR, or constitute a distinct regime was unknown.

## Method
The authors compute checkpoint deltas (∆W = W_trained − W_src in bfloat16, float32 arithmetic for statistics) across ten model pairs: six OPD-style checkpoints (covering LLM and VLM settings including Qwen2.5-VL-3B with NoisyRollout teacher), three RLVR references, and one offline distillation contrast. They measure:
- **Scale/sparsity**: relative Frobenius norm ‖∆W‖_F/‖W_src‖_F and coordinate sparsity at threshold 10⁻⁵.
- **Spectral structure**: top-k singular-value energy ratio and stable rank of each 2D weight-matrix delta.
- **Source-geometry alignment**: projection of ∆W onto the leading k singular subspaces of W_src; complementary coverage by low-magnitude source coordinates.
Two interventions test operational significance: (1) masked retraining restricted to the OPD-discovered nonzero coordinate support; (2) AdamW vs. SGD optimizer ablation under an OPD objective.

## Key Contributions
- Establishes that OPD updates are **small** (relative norm 0.036–0.142%) and **coordinate-sparse** (66.7–89.5% of coordinates unchanged at 10⁻⁵), contrasted with offline distillation (11.9% norm, 3.1% sparsity).
- Shows OPD updates are **numerically full-rank but spectrally concentrated** (top-16 SVD energy 19.7–40.9%; stable rank 7.25–20.31), unlike offline distillation (stable rank 82.74).
- Demonstrates **off-principal geometry**: OPD update energy falls disproportionately on low-magnitude source coordinates (24.99–48.57% coverage at 10% mask) and avoids principal source directions (<5.5% at 10% mask vs. 10% random baseline).
- Shows **OPD-RLVR mask overlap** is ~3× the random-density baseline, and different-teacher OPD masks overlap at 80.17% in one direction.
- Proves the sparse subnetwork is **operationally sufficient**: masked retraining on ~17.5% of coordinates recovers full-OPD peak (35.10% vs. 35.52% mean@16 on AIME24/25).
- Demonstrates **AdamW necessity**: SGD lags AdamW by ~4 pp peak accuracy (39.06% vs. 43.02%), attributable to persistent gradient heterogeneity from dense token supervision (second-moment CV averaging 4.85).
- FFN modules typically show the largest relative movement; normalization layers are nearly unchanged across all OPD checkpoints.

## Results
- **OPD sparsity**: 66.72–89.50% coordinate sparsity vs. 3.06% for offline distillation; relative norm 0.036–0.142% vs. 11.936%.
- **Spectral concentration**: median top-16 SVD energy 19.69–40.94% for OPD; 8.57% for offline distillation.
- **Subnetwork sufficiency**: OPD-mask run peaks at 35.10% mean@16 (AIME24+25); full OPD at 35.52%; RLVR-mask at 34.69%; random mask at 32.92%.
- **Optimizer gap**: AdamW 43.02% peak / 42.40% final vs. SGD 39.06% peak / 37.92% final (JustRL-teacher OPD setting).
- **Mask overlap**: OPD covers 53.21% of DeepScaleR RLVR coordinates (vs. 17.50% random baseline); 73.53% of Qwen2.5-VL GRPO coordinates covered by OPD (vs. 33.28% baseline).
- Low-magnitude source coordinates contribute 24.99–48.57% of visible OPD updates at 10% mask; principal coordinates contribute only 4.39–5.46%.

## Limitations
- Analysis is restricted to small-scale checkpoints (1.5B–4B parameters); scaling behavior at frontier model sizes is unknown.
- Interventional experiments (masked training, optimizer ablation) are limited to DS-Qwen (math reasoning) and Qwen2.5-VL; generalization to other domains (agentic, embodied) untested.
- Only final-checkpoint deltas are analyzed; training trajectory dynamics are not traced, so how the sparse task vector accumulates during training remains open.
- OPD-RLVR mask overlap analysis uses one-sided coverage due to density mismatches, limiting symmetry of conclusions.
- SGD ablation uses a single learning rate per optimizer; a more exhaustive hyperparameter search could narrow the gap.

## Relevance to Vision-Language Models
The paper directly includes a VLM checkpoint (Qwen2.5-VL-3B-Instruct distilled via NoisyRollout) and confirms that OPD sparsity/geometry findings hold in the multimodal setting, including off-principal update bias and high OPD-RLVR mask overlap (73.53% vs. 33.28% baseline). For practitioners fine-tuning VLMs post-training via OPD, the finding that the vision tower accumulates a non-negligible relative delta (0.158%) alongside language components has direct implications for adapter placement and parameter-efficient fine-tuning budget. The spectral concentration result (but numerical full-rank) clarifies that LoRA applied to OPD will capture meaningful update energy but not the full delta, which is especially relevant for VLMs where parameter budgets are tighter due to dual encoder+LLM stacks. More broadly, the off-principal geometry result challenges assumptions about whether dense distillation signals preserve the principal feature directions learned during VLM pre-training.

## Tags
#distillation #on-policy-training #parameter-efficiency #rlvr #vlm #sparse-finetuning #post-training #weight-geometry
