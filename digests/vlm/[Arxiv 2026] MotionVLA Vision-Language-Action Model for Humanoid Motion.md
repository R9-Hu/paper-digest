---
title: "MotionVLA: Vision-Language-Action Model for Humanoid Motion"
authors: ["Nonghai Zhang", "Siyu Zhai", "Yanjun Li", "Zeyu Zhang", "Zhihan Yin", "Yandong Guo", "Boxin Shi", "Hao Tang"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T06:10:48+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15142"
url: "http://arxiv.org/abs/2606.15142v1"
pdf: "paper/vlm/[Arxiv 2026] MotionVLA Vision-Language-Action Model for Humanoid Motion.pdf"
---

# MotionVLA: Vision-Language-Action Model for Humanoid Motion

*🕒 **Published (v1):** 2026-06-13 06:10 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15142v1)*

## TL;DR
MotionVLA addresses the spectral mismatch in humanoid motion tokenization by introducing DSFT, a dual-stream frequency tokenizer that separately encodes low-frequency pose semantics (Base stream) and high-frequency physical dynamics (Phys stream). Built on Qwen3.5-2B, it generates motion autoregressively conditioned on scene images and text, producing Base tokens first and Phys tokens second via causal attention. On HumanML3D and MBench, it achieves superior diversity and motion-condition consistency while reducing physical artifacts like foot sliding.

## Problem
Existing motion tokenizers — including frequency-domain ones — use a single shared codebook for all motion signals. Joint positions are low-frequency (5 DCT coefficients capture 93% of energy), while joint velocities are broadband (same 5 coefficients cover only 37%), a >50-point gap. Forcing both into a shared BPE vocabulary biases quantization toward pose structure and systematically discards high-frequency physical dynamics, causing temporal drift, foot sliding, and contact distortion that compound over long horizons.

## Method
**DSFT (Dual-Stream Frequency Tokenizer):** Motion dimensions are partitioned by physical semantics into a Base stream (joint positions/rotations, 190D on HumanML3D) and a Phys stream (joint velocities, 73D). Each stream is independently DCT-transformed, then truncated with separate budgets (Kb=5, Kp=25) and encoded by independently trained BPE tokenizers, yielding compact discrete sequences with appropriate frequency coverage per stream.

**MotionVLA:** A Qwen3.5-2B backbone extended with a motion vocabulary (Vbase + Vphys + 3 structural markers). Each training sample is formatted as `[MBOS, b1…bN, MSEP, p1…pM, MEOS]`, with a masked next-token prediction loss restricted to motion tokens. At inference, phase-aware logit masking enforces Base-before-Phys generation order, allowing Phys tokens to attend to complete pose context via causal attention. Scene images and text descriptions serve as multimodal conditioning context.

## Key Contributions
- **DSFT**: dual-stream DCT+BPE tokenizer with stream-specific truncation lengths, eliminating the single-codebook frequency mismatch
- **MotionVLA**: Qwen3.5-based VLA that models Base and Phys token streams in a unified autoregressive sequence with structured semantic-to-physical generation order
- **Empirical validation**: frequency-domain analysis quantifying the bimodal spectral distribution of motion dimensions on HumanML3D and ViMoGen; rFID used to distinguish tokenizer quality from pointwise reconstruction error

## Results
**MBench (scene-conditioned, vs. ViMoGen-228K baselines):**
- Motion-Condition Consistency: 0.55 (best; prior best ViMoGen 0.53, +3.8%)
- Motion Generalizability: 0.66 (best; prior best ViMoGen 0.68, second best)
- Foot Sliding: 0.0049 (best; prior best ViMoGen-light 0.0051)
- Jitter Degree: 0.0110 (second best after ViMoGen 0.0108)

**HumanML3D (text-to-motion):**
- Diversity: 9.548 (closest to real 9.503 among all methods)
- MModality: 2.821 (highest among generated methods)
- FID: 0.071 (competitive but above MoMask 0.045 / GenM3 0.046)
- R-Precision Top-3: 0.798 (competitive with real 0.797)

**DSFT tokenizer (HumanML3D):**
- rFID: 0.1868 vs. single-stream DCT+BPE baseline 0.9461 (5× lower) at 11.24 vs. 15.21 tokens/frame (more compact)

**Human preference (100 prompts × 5 experts vs. ViMoGen):**
- MotionVLA preferred: 64.0%; ViMoGen preferred: 14.0%; tie: 22.0%

## Limitations
- Evaluated only on a 2B backbone; scaling behavior and cross-dataset generalization remain untested at larger scales
- Fixed stream partition and fixed truncation lengths (Kb=5, Kp=25) may not be optimal for all motion types or sequence lengths
- Predefined Base-to-Phys generation order may not generalize to motion types where dynamics precede or co-determine pose
- Target motion length T must be provided externally at inference; the model does not predict duration
- MotionVLA uses additional visual (scene) input on MBench, making direct comparison with text-only baselines not fully controlled

## Relevance to Vision-Language Models
MotionVLA directly instantiates the VLA paradigm for humanoid motion generation, extending a language backbone (Qwen3.5) to condition motion synthesis on scene images and natural language — the same multimodal grounding central to embodied VLMs. Its dual-stream tokenization strategy offers a concrete lesson for VLA design: heterogeneous action signals (analogous to multi-modal perceptual signals in VLMs) may require signal-specific representation spaces rather than unified codebooks. The phase-aware autoregressive ordering (semantic before dynamic) also demonstrates a structured generation curriculum achievable within a standard transformer without architectural modifications, relevant to any VLA work that must balance high-level instruction following with low-level physical fidelity.

## Tags
#vla #motion-generation #tokenization #autoregressive #frequency-domain #humanoid-robotics #multimodal-conditioning #embodied-ai
