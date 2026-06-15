---
title: "CausalMotion: Structured Physical Reasoning as Keyframe and Trajectory Guidance for Training-Free Video Generation"
authors: ["Sihan Zhuang", "Xinyuan Chen", "Tianfan Xue", "Yaohui Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14317"
url: "http://arxiv.org/abs/2606.14317v1"
pdf: "paper/vlm/[Arxiv 2026] CausalMotion Structured Physical Reasoning as Keyframe and Trajectory Guidance for Training-Free Video Generation.pdf"
---

# CausalMotion: Structured Physical Reasoning as Keyframe and Trajectory Guidance for Training-Free Video Generation

## TL;DR
CausalMotion is a training-free framework that uses a VLM (Qwen-VL-2.5-72B) to decompose text prompts into causally consistent keyframes and explicit object trajectory plans, then injects these as soft latent-space constraints into a pretrained video diffusion model (LTX-Video). Without any additional training, it scores 0.65 on PhyGenBench (67% above the LTX-Video baseline of 0.39) while also improving VBench perceptual quality from 80.57% to 82.52%.

## Problem
Video diffusion models learn physical consistency implicitly from statistical co-occurrences in large-scale data, producing physically impossible outputs: objects skip intermediate states (e.g., ice cream jumping from solid to puddle), exhibit temporal discontinuities, or violate basic physical laws (e.g., liquid surface rising outside a cup). Training-based remedies require large annotated datasets and expensive supervision; this work targets inference-time correction without retraining.

## Method
Three-stage pipeline, all at inference time:

**1. Keyframe Generation via Visual Thought Reasoning.** A VLM first infers a global "consequence" (end state) of the scene, then autoregressively generates N textual descriptions and corresponding images (via gpt-image-1.5) representing causally ordered key states. Each step conditions on the prior image, prior description, and the global consequence anchor.

**2. Physical State and Trajectory Planning.** Grounded SAM2 localizes key objects in the initial keyframe as bounding boxes {b₀,ₖ}. The VLM then predicts sparse physical state vectors sτⱼ = [x, y, w, h, vₓ, vᵧ, c] at ~13 key timesteps via chain-of-thought (identifying applicable physical laws → inferring motion under those constraints → predicting bounding-box evolution). Dense 121-frame trajectories are constructed by physics-aware interpolation: linear for uniform motion, quadratic (bτⱼ + vτⱼΔt + ½aΔt²) for accelerated motion.

**3. Time Alignment + Trajectory-Guided Latent Guidance.** Keyframes are greedily assigned to trajectory timesteps by IoU maximization (tₖ = argmax IoU(k,t) subject to temporal ordering). During diffusion denoising, each object's trajectory is encoded into the latent space via a Gaussian soft mask Mᵢ,τ. A dynamic reference appearance Pʳᵉᶠᵢ,τ blends anchors from the two neighboring keyframes and local propagation from the previous step. The latent is updated per denoising step as: Lτ ← (1 − αs Mᵢ,τ) ⊙ Lτ + αs Mᵢ,τ ⊙ Pʳᵉᶠᵢ,τ, spatially localizing physical constraints while preserving the global generative distribution.

## Key Contributions
- Training-free, inference-only framework that integrates VLM chain-of-thought reasoning into video diffusion without modifying model parameters.
- Structured intermediate representation decoupling reasoning (keyframes + physical state vectors) from synthesis (LTX-Video diffusion backbone).
- Physics-aware interpolation distinguishing uniform vs. accelerated motion regimes for dense trajectory construction.
- Dynamic reference appearance blending enabling smooth cross-keyframe appearance transitions in latent space.
- State-of-the-art PhyGenBench score of 0.65, a 67% absolute improvement over LTX-Video baseline (0.39).

## Results
**PhyGenBench (physical plausibility):**
- CausalMotion: 0.65 avg (Mechanics 0.61, Optics 0.71, Thermal 0.68, Material 0.61)
- VLIPP: 0.60 | PhyGDPO: 0.55 | DiffPhy: 0.54 | PhyT2V: 0.52 | LTX-Video: 0.39
- Largest gains over VLIPP in mechanics (+0.06) and thermal (+0.08)

**VBench (perceptual quality, same 20 prompts as VChain):**
- CausalMotion: 82.52% > LTX-Video 80.57% > VChain 78.49% > Wan2.1 76.21%

**VLM-as-judge (Gemini 2.5 Flash, higher-level properties):**
- Overall: 3.58 vs LTX-Video 2.70; Physical plausibility: 3.10 vs 2.53; Temporal consistency: 3.95 vs 3.89; Semantic alignment: 3.70 vs 1.68

**Ablation (PhyGenBench average):**
- Full model: 0.654 | −keyframe reasoning: 0.471 | −trajectory physical state: 0.642 | −latent trajectory guidance: 0.645
- Removing keyframe reasoning is most damaging; trajectory guidance primarily benefits optics and mechanics

## Limitations
- VLM trajectory planning errors accumulate in highly interactive or complex multi-object scenes; keyframe-trajectory coordinate alignment degrades with scene complexity (per-prompt IoU variance is high).
- Trajectory guidance is ineffective for appearance-only changes (e.g., oxidation, color transitions) where objects remain spatially stationary; full model occasionally underperforms ablations in the material category.
- High inference latency: ~448 sec/sample total, dominated by API-based keyframe generation (271 sec via gpt-image-1.5); not suitable for real-time or large-batch use.
- Framework depends on proprietary API models (gpt-image-1.5, Qwen-VL-2.5-72B), constraining reproducibility and adding cost.
- Temporal resolution of VLM trajectory prediction is inherently sparse (13 keyframes), requiring interpolation that may misrepresent non-smooth physical phenomena.

## Relevance to Vision-Language Models
CausalMotion is a direct demonstration of VLMs functioning as structured world-model planners: rather than fine-tuning generative models on physical data, it offloads causal and physical reasoning entirely to VLM chain-of-thought, then converts that reasoning into geometric constraints a diffusion model can consume. This "reason-then-generate" decomposition is a significant paradigm for VLM-augmented generative systems, showing that VLM priors can substitute for expensive physics simulators at inference time. The use of a VLM (Gemini 2.5 Flash) as an evaluation judge for physical plausibility and semantic alignment also illustrates the dual role VLMs play—as both reasoning engine and evaluator—in the emerging evaluation stack for video generation. For researchers tracking VLMs, this paper marks a concrete integration point between multimodal reasoning and temporal visual synthesis.

## Tags
#vlm #video-generation #physical-reasoning #training-free #diffusion-model #chain-of-thought #trajectory-planning #temporal-consistency
