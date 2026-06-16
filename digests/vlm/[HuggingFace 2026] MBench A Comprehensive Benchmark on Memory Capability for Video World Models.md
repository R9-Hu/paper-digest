---
title: "MBench: A Comprehensive Benchmark on Memory Capability for Video World Models"
authors: ["Shengjun Zhang", "Zhang Zhang", "Simin Huang", "Zhenyu Tang", "Hanyang Wang", "Chensheng Dai", "Min Chen", "Yifan Li", "Yuxin Li", "Yingjie Chen", "Hao Liu", "Chen Li", "Jing Lyu", "Yueqi Duan"]
source: "HuggingFace"
venue: ""
published: "2026-06-08"
published_time: "2026-06-08T00:00:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.00793"
url: "https://huggingface.co/papers/2606.00793"
pdf: "paper/vlm/[HuggingFace 2026] MBench A Comprehensive Benchmark on Memory Capability for Video World Models.pdf"
---

# MBench: A Comprehensive Benchmark on Memory Capability for Video World Models

*🕒 **Published (v1):** 2026-06-08 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.00793)*

## TL;DR
MBench is a comprehensive benchmark for evaluating the **memory capability** of video world models — specifically their ability to maintain entity, environment, and causal consistency over long temporal horizons. It introduces 1,040+ evaluation cases across 12 sub-dimensions, a hybrid rule-based + VLM evaluation pipeline, and a Trigger-Conditioned Scoring mechanism that prevents conservative models from inflating scores by avoiding memory challenges entirely.

## Problem
Existing video generation benchmarks (VBench, WorldScore, etc.) focus on visual quality, motion coherence, and text-video alignment, but none jointly cover entity consistency, environment consistency, **and** causal consistency, support both text- and action-conditioned models, and probe long-horizon generation with explicit memory triggers. As a result, models that produce visually plausible short clips cannot be distinguished from models that maintain stable, grounded world states across extended rollouts.

## Method
MBench decomposes world model memory into a **three-level hierarchical taxonomy**:

1. **Entity Consistency** (Object + Human sub-dimensions): measures object geometry via SSIM on SAM2-masked warped frame pairs; texture via DINOv2 cosine similarity to a global track centroid; human identity via ArcFace embeddings; appearance via DINOv2 on full-body SAM2 masks.

2. **Environment Consistency** (Spatial + Rendering): spatial sub-dimensions use DA3-estimated camera poses to compute Epipolar Geometry Error and Reprojection Error on non-adjacent frame pairs; rendering sub-dimensions measure Lighting Consistency (CIELAB illumination + color deviation with exponential decay) and Style Consistency (Gram Matrix Distance via VGG features).

3. **Causal Consistency** (Self-Evolution + Interaction): State Evolution and Evolution Correctness are scored by Qwen3-VL-235B-A22B as a VLM judge, with a soft-gating mechanism (`score = gate × correctness`) that penalizes models that never trigger the required event; Text Interaction uses OpenCLIP cosine similarity between segment prompts and sampled frames; Action Interaction uses cosine similarity between DA3-estimated 6-DoF camera twists and ground-truth action vectors.

**Trigger-Conditioned Scoring**: The final **M-Score** is the harmonic mean of Trigger Coverage (C^trig, fraction of samples where the model executes the memory-triggering event) and Memory Reliability (S^rel, average consistency only on triggered samples). This prevents conservative, static models from gaming scores.

Data is sourced from five real-world video datasets (DL3DV, Tanks and Temples, OpenHumanVID, SpatialVID, Physics-aware-video), filtered by VLM for challenge complexity. Text-conditioned models use multi-granularity captions with camera control instructions; action-conditioned models use an **Exit-and-Reenter** paradigm.

## Key Contributions
- First benchmark to jointly evaluate entity, environment, and causal consistency for video world models, supporting both text- and action-conditioned interaction on long videos.
- Three-level hierarchical memory taxonomy decomposed into 12 quantifiable sub-dimensions with dedicated metrics per sub-dimension.
- Trigger-Conditioned Scoring (M-Score) that decouples trigger coverage from consistency quality, eliminating the conservative-model inflation problem.
- Evaluation of 14 state-of-the-art models (8 text-conditioned + 6 action-conditioned), revealing systemic memory failures across all paradigms.

## Results
From Table 2 (all scores in [0, 100]; higher = better memory):

**Text-conditioned models:**
- **Object Geometry**: Helios best (79.43), Self Forcing worst (34.97)
- **Object Texture**: Helios best (63.70), Self Forcing (33.02)
- **Human Identity**: Causal Forcing (42.53), Cosmos-Predict 2.5 worst (16.95)
- **Epipolar**: Self Forcing best (67.44), Longcat-Video worst (28.28)
- **Reprojection**: Self Forcing best (55.19), Causal Forcing worst (2.88)
- **Style Consistency**: all models score <31; Self Forcing (30.15), worst Skyreels V2 (20.33) — consistent low scores indicate style forgetting is universal
- **Causal State Evolution**: Longcat-Video best (84.17), Self Forcing worst (50.19)

**Action-conditioned models:**
- **Style Consistency**: Matrix-Game 3.0 (95.17), HY-WorldPlay (98.23), Infinite-World (96.87) — dramatically higher than text-conditioned models
- **Action Interaction**: Matrix-Game 3.0 (81.93), HY-WorldPlay (85.69), Infinite-World (86.37)
- **Causal State Evolution**: Yume-1.5 (97.90), Lingbot-World (96.00) vs. text-conditioned best ~84
- **Object Geometry**: Matrix-Game 2.0 collapses (14.62); HY-WorldPlay/Yume-1.5 competitive (~47-61)

Key finding: models strong on visual quality/epipolar geometry (Self Forcing, Helios) remain weak on style and causal consistency. No single model dominates across all 12 dimensions. Spatial metrics — especially reprojection — are the most commonly failed dimension.

## Limitations
- The benchmark currently covers 1,040 cases, which may undersample the diversity of real-world interaction types and physical domains.
- VLM-based causal scoring (Qwen3-VL-235B-A22B) introduces evaluator bias; the paper does not report VLM evaluator calibration against human judgments.
- The Exit-and-Reenter action paradigm is a specific structured test; free-form long-horizon rollouts with less structured prompts are not covered.
- The benchmark does not address audio-visual or multi-modal consistency dimensions.
- Trigger-Conditioned Scoring requires the VLM to correctly verify trigger execution; errors in trigger verification propagate into M-Score computation.
- Style consistency uses adjacent-frame Gram matrix distance (Eq. 13), which may not capture long-range style drift as effectively as departure-return pairing used in other dimensions.

## Relevance to Vision-Language Models
MBench is directly relevant to VLM researchers because it deploys VLMs in two critical roles: (1) as a **data curator** for filtering video clips by challenge complexity across the three consistency dimensions, and (2) as a **judge** for causal consistency evaluation (State Evolution and Evolution Correctness via Qwen3-VL-235B-A22B), making VLM reasoning quality a direct bottleneck in benchmark reliability. The benchmark also uses OpenCLIP for text-interaction scoring, connecting to the CLIP-family evaluation literature. More broadly, MBench highlights that the "memory" problem in video world models is structurally analogous to long-context faithfulness challenges in LLMs — and suggests that VLMs acting as evaluators must themselves handle long-horizon temporal grounding, an open challenge. As video-generation capabilities improve, this benchmark defines the next frontier: from perceptual quality to **world-state fidelity**, a gap VLMs are increasingly called on to measure and possibly bridge.

## Tags
#benchmark #video-world-models #memory-consistency #long-horizon-generation #vlm-evaluation #temporal-consistency #causal-reasoning #entity-consistency
