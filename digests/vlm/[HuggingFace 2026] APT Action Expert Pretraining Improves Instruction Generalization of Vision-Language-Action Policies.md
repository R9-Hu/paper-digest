---
title: "APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies"
authors: ["Kechun Xu", "Zhenjie Zhu", "Anzhe Chen", "Rong Xiong", "Yue Wang"]
source: "HuggingFace"
venue: ""
published: "2026-06-10"
published_time: "2026-06-10T17:34:25+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.12366"
url: "https://huggingface.co/papers/2606.12366"
pdf: "paper/vlm/[HuggingFace 2026] APT Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies.pdf"
---

# APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies

*🕒 **Published (v1):** 2026-06-10 17:34 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.12366)*

## TL;DR
APT addresses the poor OOD language instruction generalization of continuous-action VLA models by pretraining the action expert on vision-action pairs before introducing language, using a Bayesian factorization of the policy into a language-agnostic VA prior and a language-conditioned VLA likelihood. A two-stage training procedure and a layer-wise gated fusion mechanism prevent visual shortcuts and VLM corruption. APT consistently outperforms baselines on unseen instructions and compositional tasks in both simulation and real-world settings.

## Problem
Continuous-action VLA models (e.g., π0, GR00T) couple a pretrained VLM with a randomly initialized action expert trained jointly on imbalanced VLA data (many vision-action frames per single language instruction). This imbalance causes the action expert to learn visual shortcuts that bypass language, and its noisy gradients corrupt the VLM's pretrained language representations, leading to near-zero success on OOD instructions and compositional task variations. Knowledge Insulation (stopping gradients) only partially addresses this; it cannot endow the action expert with coherent visuomotor priors.

## Method
APT applies a Bayesian factorization π(a|v,ℓ) ∝ πᵖ(a|v) · L(ℓ|v,a), treating action generation as a two-component problem:

**Stage 1 — VA Prior Pretraining:** The action expert (a diffusion Transformer) is trained on vision-action pairs only, with all language tokens masked and the VLM backbone frozen. Because every visual frame maps to a unique action annotation, the data is balanced and shortcut-free. Only N/2 attention layers are active.

**Stage 2 — VLA Likelihood Alignment:** N/2 new attention layers are interleaved with the Stage 1 layers (initialized from Stage 1 weights). Language tokens are unmasked and injected via a **layer-wise gated fusion** mechanism: intermediate features from uniformly sampled Qwen3-VL layers are added to each action expert attention layer input, gated by a learnable scalar σ(ŵᵢ). The full model (VLM + action expert) is jointly fine-tuned on all pretraining data, aligning the pretrained action prior with language.

**Post-training:** Task-specific fine-tuning on small datasets (30 demos in real-world experiments) follows Stage 2. The method applies to π-style (block-wise cross-attention) and GR00T-style (final-layer cross-attention) architectures.

## Key Contributions
- Bayesian factorization of the VLA policy into a language-agnostic VA prior and a language-conditioned likelihood, enabling principled action expert pretraining within existing VLA datasets.
- Two-stage training recipe that first trains the action expert on balanced vision-action data, then injects language via interleaved attention layers — without requiring additional VL reasoning co-training data.
- Layer-wise gated fusion architecture that integrates intermediate Qwen3-VL features into every action expert attention layer via learnable gates, preserving the VA prior while enabling language conditioning.
- Empirical demonstration that the approach generalizes across π-style and GR00T-style architectures, and that joint VLM fine-tuning (not Knowledge Insulation) is optimal given a well-initialized action prior.

## Results
**LIBERO-PRO (success rate %):**
- APT (Ft VLM) avg 27% vs. π0 0%, π0.5 11%, LangForce 14%, CaP-X ~avg — APT is the only method achieving non-trivial OOD Task generalization across Spatial, Object, Goal suites.
- APT (Ft VLM): Spatial-Pos/Task 62/62, Object-Pos/Task 24/17, Goal-Pos/Task 10/20, Long-Pos/Task 12/12.

**Pick-Place simulation (success rate %):**
- APT (2-Stage, Ft VLM): SO 98, UO 84, UC 92, UOUE 58 vs. π0.5: SO 84, UO 70, UC 86, UOUE 50.
- APT with 2-Stage+KI surpasses π0.5 without any VL reasoning co-training data.

**Architecture ablation (Pick-Place):**
- 2-Stage training improves across π-style (+up to +6%), GR00T-style (+up to +30%), and APT architecture (+up to +50%), with the largest gains in UO/UOUE settings.

**Real-world Pick-Place (successes/trials):**
- APT vs. π0.5: SO 29/30 vs. 27/30, UO 17/20 vs. 11/20, UOUC 16/20 vs. 9/20, UOUCUE 28/40 vs. 16/40.

**Compositional task chaining (real-world):**
- APT ~65% vs. π0.5 ~20% on chained multi-task instructions; π0.5 collapses to over-executing the first task.

## Limitations
- No explicit long-horizon memory modeling; the policy can fail to track multi-step progress in complex sequential tasks.
- Evaluation is limited to tabletop manipulation; generalization to locomotion or mobile manipulation is untested.
- Stage 1 pretraining uses only half the data; large-scale diverse pretraining data is needed to acquire priors for unseen object categories and environments (w/o Pretraining variant degrades significantly on UO/UOUE).
- Goal-Pos performance dips below π0.5, suggesting obstacle avoidance in spatially complex scenarios is not fully resolved.
- APT failure modes include premature task switching in chaining and confusion between visually similar objects.

## Relevance to Vision-Language Models
APT directly addresses a fundamental tension in VLA models: how to couple a pretrained VLM's language understanding with a continuous action module without degrading either capability. The Bayesian prior/likelihood decomposition and gated feature fusion are transferable ideas for any multimodal architecture where a newly initialized head is co-trained with a pretrained language backbone on imbalanced data. The finding that joint VLM fine-tuning outperforms gradient-stopping (Knowledge Insulation) — given proper action expert initialization — challenges a growing consensus in VLA training and has implications for how VLMs are adapted to grounded action tasks more broadly. For VLM researchers, the work highlights that OOD generalization failures in embodied settings are not purely a VLM capacity problem but arise from the interaction dynamics between initialization quality and data imbalance.

## Tags
#vla #instruction-generalization #action-expert #bayesian-factorization #diffusion-policy #robot-manipulation #ood-generalization #vlm-finetuning
