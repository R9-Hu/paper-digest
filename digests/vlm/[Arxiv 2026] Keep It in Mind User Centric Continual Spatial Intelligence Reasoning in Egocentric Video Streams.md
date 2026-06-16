---
title: "Keep It in Mind: User Centric Continual Spatial Intelligence Reasoning in Egocentric Video Streams"
authors: ["Yun Wang", "Junbin Xiao", "Han Lyu", "Yifan Wang", "Jing Zuo", "Zhanjie Zhang", "Hong Huang", "Dapeng Wu", "Angela Yao"]
source: "Arxiv"
venue: "ICML"
published: "2026-06-13"
published_time: "2026-06-13T08:50:49+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15200"
url: "http://arxiv.org/abs/2606.15200v1"
pdf: "paper/vlm/[Arxiv 2026] Keep It in Mind User Centric Continual Spatial Intelligence Reasoning in Egocentric Video Streams.pdf"
---

# Keep It in Mind: User Centric Continual Spatial Intelligence Reasoning in Egocentric Video Streams

*🕒 **Published (v1):** 2026-06-13 08:50 UTC  ·  **Source:** Arxiv  ·  **Venue:** ICML  ·  [link](http://arxiv.org/abs/2606.15200v1)*

## TL;DR
UCS-Bench is a new benchmark of 532 egocentric videos (170+ hours, 8.1K QA pairs) that evaluates whether AI can maintain and update user-centric spatial knowledge — object locations relative to the camera wearer's real-time position — as scenes evolve over long horizons. DirectMe, a training-free framework, incrementally builds a pose-anchored spatial scene graph from streaming observations and uses it to answer queries that require recalling out-of-view objects from the user's current egocentric frame. DirectMe substantially closes the gap over raw MLLM baselines, though a ~37-point gap to human performance (91.7%) remains.

## Problem
Existing spatial benchmarks and MLLMs evaluate static or episodic spatial understanding from third-person views, failing to address user-centric dynamic spatial reasoning: tracking where objects are relative to the camera wearer's real-time heading and location across long streaming egocentric video. When a user turns around, an object's relative direction (e.g., "behind you") changes even if the object has not moved, and no benchmark or method explicitly evaluates this orientation-aware, long-horizon accumulation.

## Method
DirectMe is a training-free, streaming QA framework with four stages:

1. **Multimodal processing (1 fps):** DepthAnything3 estimates metric depth and camera extrinsics (ego-pose trajectory `{T_{w←e}(t)}`); GroundingDINO + SAM2 produce temporally consistent per-object instance tracks with masks and bounding boxes; a lightweight MLLM assigns per-frame semantic scene tags.
2. **Metric-semantic map:** All signals are fused into a global world-coordinate map initialized at t=1 and incrementally updated.
3. **Evolving scene graph G=(V,E):** Nodes are persistent object instances (grounded by 3D world-frame positions) plus semantic place nodes; edges encode object–object and object–place spatial relations in the world frame. At query time t, relations are re-rendered in the current egocentric frame via `T_{e←w}(t) = T_{w←e}(t)^{-1}`.
4. **Online QA:** A structured query intent is parsed from the question; a minimal subgraph and top-K keyframes are retrieved (causally, from observations up to t); world-frame coordinates are transformed to camera-relative directions and distances; the MLLM generates the final answer from the subgraph + keyframes prompt.

## Key Contributions
- **UCS-Bench:** First benchmark targeting user-centric continual spatial intelligence; 8,114 manually annotated QA pairs across four categories (Position & Orientation, Trajectory & Movement, Proximity & Reachability, Category & Quantity), with repeated queries at different timestamps and temporal evidence spans; covers indoor/outdoor, short clips to 44h recordings.
- **DirectMe:** Training-free, causally streaming scene-graph memory framework that integrates depth, camera pose, and semantic tracking to answer ego-centric spatial queries about out-of-view objects.
- Comprehensive evaluation of 18 MLLMs (4B–38B) across proprietary, open-source, spatial-centric, and streaming categories.
- Root-cause analysis identifying tracking failure (40%), ego-pose relation failure (23%), retrieval failure (20%), and reasoning failure (17%) as dominant error sources.

## Results
- **Human accuracy:** 91.7%; **Random baseline:** 25.7%.
- **Best pure MLLM:** InternVL3.5-38B 50.2% and InternVL3-38B 53.7% overall; Doubao-seed-1.6V (proprietary) 49.6%.
- **DirectMe (w/ Qwen3-VL-8B):** 54.1% overall — best reported result, surpassing InternVL3-38B despite using an 8B backbone.
- **DirectMe (w/ InternVL3-8B):** 52.6% overall.
- DirectMe leads on Position & Orientation (47.6% vs. best baseline ~46.5%), Trajectory & Movement (57.2%), and Proximity & Reachability (59.8%).
- Ablation (Table 5): scene-graph retrieval alone drives the gain (baseline Qwen3-VL 44.6% → graph only 54.6%; combining description + graph 54.1%); MLLM-generated textual description alone yields only marginal improvement (44.3%).
- DirectMe's accuracy degrades more slowly than all baselines as the evidence–question temporal gap increases, particularly beyond 3 minutes.
- Models consistently perform better on object-trajectory than ego-trajectory questions; temporal-state tracking failures account for >55% of all errors.

## Limitations
- ~37-point gap to human performance remains unresolved.
- DirectMe relies on DepthAnything3 accuracy; errors in depth or pose estimation propagate directly into the scene graph.
- Tracking failure is the single largest failure mode (40% of errors), suggesting the SAM2+GroundingDINO pipeline is a bottleneck in long-horizon streaming settings.
- All proprietary models are capped at 50 input frames (GPT-5 API limit), potentially underrepresenting their true long-video capability.
- The framework is described as training-free, but integrating learning-based spatial modules could further close the human gap — this direction is not explored.

## Relevance to Vision-Language Models
UCS-Bench directly exposes a failure mode of current MLLMs that is orthogonal to standard VQA: models lack the ability to maintain and update an egocentric spatial reference frame across streaming video, even when they possess strong general visual-language reasoning. The finding that large general-purpose MLLMs (e.g., Qwen3-VL-32B) outperform spatial-centric models on this benchmark challenges the assumption that specialized spatial training transfers to user-centric dynamic settings. DirectMe's training-free scene-graph memory architecture — fusing geometric signals (depth, camera pose) with MLLM reasoning — is a practical blueprint for augmenting VLMs with persistent structured memory, a gap increasingly relevant as VLMs are deployed in wearable and embodied AI contexts.

## Tags
#vlm #egocentric-video #spatial-reasoning #benchmark #scene-graph #streaming-video #memory-augmented #continual-learning
