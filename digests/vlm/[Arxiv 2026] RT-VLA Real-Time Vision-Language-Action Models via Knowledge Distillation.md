---
title: "RT-VLA: Real-Time Vision-Language-Action Models via Knowledge Distillation"
authors: ["Xiangyu Huang", "Zhenlin Hua", "Han Zhou", "Shounak Sural", "Ragunathan Rajkumar"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14010"
url: "http://arxiv.org/abs/2606.14010v1"
pdf: "paper/vlm/[Arxiv 2026] RT-VLA Real-Time Vision-Language-Action Models via Knowledge Distillation.pdf"
---

# RT-VLA: Real-Time Vision-Language-Action Models via Knowledge Distillation

## TL;DR
RT-VLA distills a large Vision-Language-Action (VLA) model (SimLingo) into a compact student via multi-level supervised distillation, achieving a 44.8× inference speedup in vision-only mode while maintaining competitive closed-loop driving scores on Bench2Drive. It decouples real-time driving from language reasoning, enabling post-hoc explainability without runtime latency cost.

## Problem
Large VLA models for autonomous driving (e.g., SimLingo with InternVL-2 + Qwen2) incur inference latencies exceeding 1.5 seconds per frame due to heavy vision-language backbones and autoregressive generation, making them unsafe for real-time deployment where sub-100 ms responses are required.

## Method
RT-VLA uses a frozen SimLingo teacher and a lightweight student (EVA-02 vision encoder + compact language modules) trained via **multi-level supervised distillation** across four signal types:
1. **Visual feature distillation** — L2 loss between aligned teacher (InternVL-2) and student (EVA-02) feature maps after learnable projection and adaptive average pooling to reconcile dimension/length mismatches.
2. **Query representation distillation** — L2 loss on trainable query token outputs.
3. **Waypoint prediction distillation** — L2 loss on geometric and temporal speed waypoints pooled to student horizon length.
4. **Language-logit distillation** — token-level KL divergence between teacher and student output distributions over a shared vocabulary, temperature-scaled.

Training is two-stage: stage 1 optimizes the driving branch (Ldriving); stage 2 freezes the driving branch and trains the language branch (Llanguage). An **on-policy language fine-tuning** step then reduces the train/inference distribution shift by generating student rollout tokens autoregressively, evaluating them with the frozen teacher, and minimizing KL divergence over those on-policy positions. At inference, a separate lightweight **language reasoning branch** (with Perceiver Resampler + KV caching) handles post-hoc explanation offline, fully decoupled from real-time control.

## Key Contributions
- Multi-level distillation framework transferring knowledge through visual features, query representations, waypoints, and language logits simultaneously.
- On-policy language fine-tuning to close the teacher-forcing/autoregressive inference gap in the language branch.
- Decoupled architecture: real-time driving branch (34.48 ms/frame) + offline language reasoning branch invoked only when explainability is needed.
- 44.8× speedup vs. SimLingo in vision-only mode; 7.9× speedup in vision+language mode, with only 0.75-point driving score drop and 0.9-point commentary quality drop.

## Results
- **Driving score (DS):** RT-VLA 85.19 vs. SimLingo 85.07 vs. SimLingo-BASE 85.94 on Bench2Drive (220 CARLA routes).
- **Inference time (vision-only):** RT-VLA 34.48 ms vs. SimLingo-BASE 41.11 ms vs. SimLingo 1544.34 ms — 44.8× speedup over SimLingo teacher.
- **Inference time (vision+language):** RT-VLA 196 ms vs. SimLingo 1544.34 ms — 7.9× speedup.
- **Commentary quality (DeepSeek-V4-Flash judge):** RT-VLA 50.9 vs. SimLingo 51.8.
- **Ablation:** Without distillation, student DS collapses to 34.05 (vs. 85.17 with distillation); commentary score improves from 44.6 → 47.0 (distillation) → 50.9 (+ on-policy FT).

## Limitations
- No explicit safety-constrained objective; safety-critical failures (collisions, red-light violations) are not eliminated.
- Camera-only; no LiDAR or geometric sensors, reducing robustness under adverse conditions (rain, fog, low light).
- Inherits teacher and simulation biases; real-world domain shift and long-tail scenarios are unaddressed.
- Evaluated only on CARLA simulation (Bench2Drive); no real-world driving validation.

## Relevance to Vision-Language Models
RT-VLA directly instantiates a VLM compression paradigm for action-conditioned settings, showing that multi-level distillation (features + logits) can preserve language reasoning capability alongside task performance in a student far smaller than the teacher. The language-logit KL distillation technique and on-policy fine-tuning are broadly applicable to any VLM deployment scenario where autoregressive generation latency is prohibitive. The paper also highlights a practical decoupling strategy — separating the VLM's reasoning branch from the task-execution branch — that is relevant to any embodied or real-time VLM application. For VLM researchers, the result that distillation without ground-truth alone recovers 51 DS points (34→85) underscores the essential role of intermediate representation alignment in compressing large multimodal models.

## Tags
#vlm #knowledge-distillation #autonomous-driving #vla #real-time-inference #model-compression #explainability #embodied-ai
