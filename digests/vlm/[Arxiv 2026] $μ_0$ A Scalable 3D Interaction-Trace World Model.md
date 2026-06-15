---
title: "$\u03bc_0$: A Scalable 3D Interaction-Trace World Model"
authors: ["Seungjae Lee", "Yoonkyo Jung", "Jusuk Lee", "Jonghun Shin", "Amir Hossein Shahidzadeh", "Yao-Chih Lee", "H. Jin Kim", "Jia-Bin Huang", "Furong Huang"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13769"
url: "http://arxiv.org/abs/2606.13769v1"
pdf: "paper/vlm/[Arxiv 2026] $\u03bc_0$ A Scalable 3D Interaction-Trace World Model.pdf"
---

# $μ_0$: A Scalable 3D Interaction-Trace World Model

## TL;DR
µ0 is a query-conditioned world model that predicts smooth 3D trajectories for semantically selected interaction keypoints (objects, tools, hands, contact regions) rather than pixels or robot-specific actions. A scalable data engine (TraceExtract) converts heterogeneous human and robot videos into event-captioned 3D trace supervision without any action labels. The frozen pretrained µ0 can be paired with lightweight action experts for downstream robot control, matching or exceeding action-labeled VLAs like π0.

## Problem
Pixel-space video world models waste capacity on dense appearance reconstruction and miss metric geometry critical for manipulation; direct action-prediction (VLA) models require scarce, embodiment-specific labeled robot data that does not scale. Existing 3D motion-centric methods under-sample task-critical regions (tool tips, contact patches), conflate camera motion with object motion by operating in local/2D coordinates, and use episode-level rather than event-level language — limiting their utility as transferable motion priors.

## Method
**TraceExtract (data engine):** (1) Extracts semantic keypoints by clustering DINOv2 patch features into entity groups and allocating a fixed budget per entity; a movement filter removes static/background tracks. (2) Lifts keypoints into globally aligned 3D using sparse anchor frames and chunk-wise local reconstruction, then reprojects into a per-chunk reference camera to remove camera motion. (3) Segments demonstrations into motion-centric events via trace-acceleration peaks (Savitzky–Golay smoothed), then captions each event with a VLM at three frames (start, midpoint, end), merging adjacent captions hierarchically.

**µ0 model:** Built on a frozen SmolVLM2-2.2B VLM backbone whose KV cache is cross-attended to by a permutation-equivariant Trace Expert. Each query keypoint is tokenized with Fourier location embeddings, DINO local features, and segment embeddings for history vs. future. Future traces are represented as cubic B-spline control points (compact, smooth, lower-dimensional). Training uses a semantic flow-matching objective (L = L_flow + λ_done L_done + λ_rig L_rig): L_flow matches control-point velocity fields, L_done predicts trajectory validity under occlusion, L_rig enforces local geometry preservation within DINO clusters. Inference denoises noisy control points via the flow model.

**Action expert:** The pretrained µ0 is frozen; a separate action expert reads features from a single partial-denoising step of µ0 via gated cross-attention, combined with gripper-camera, proprioception, and language, to predict continuous action chunks.

## Key Contributions
- **TraceExtract**: scalable pipeline producing {observation, 3D trace, event caption} tuples from heterogeneous videos; scales trace curation ~8× over prior 3D trace datasets
- **µ0**: query-conditioned trace world model combining a VLM backbone with a permutation-equivariant Trace Expert, B-spline targets, and semantic flow matching
- **Trace-conditioned action adaptation**: frozen µ0 reused across embodiments by training only a thin action expert on its trace-denoising features, enabling action-free video pretraining to transfer to robot policies

## Results
- **2D trace prediction** (vs. Gemini-3.1-Pro, GPT-5.5, Track2Act, Hamster): µ0 achieves best Top-5 ADE, FDE, and DTW across all horizons T∈{8,16,32}; Top-1 ADE at T=32 is 0.315 (competitive with but not always best vs. VLM APIs)
- **3D trace prediction** (vs. 3DFlowAction, Dream2Flow, TraceGen): µ0 is best on every reported ADE, FDE, and DTW metric (e.g., Top-1 ADE T=8: 0.209 vs. TraceGen 0.327, 3DFlowAction 0.615)
- **Inference latency**: 0.29s, 2.9× faster than Track2Act (0.85s), orders of magnitude faster than API-based VLM baselines (38–78s)
- **RoboCasa365 simulation** (8 tasks): µ0 + action expert achieves 30.25% avg success rate vs. π0 25.25%, Diffusion Policy 22.75%, TraceGen 23%; π0.5 outperforms at 42% (but uses action-labeled pretraining)
- **Real-world UR3** (3 tasks, 20 rollouts each): µ0 achieves 91.7% avg success rate vs. π0 73.3%, π0.5 80.0%, TraceGen 81.7%, VLM+action expert (no trace) 73.3%
- **Ablation**: removing trace features widens performance gap as action head size decreases, confirming the motion structure provided by trace-space pretraining is essential

## Limitations
- Supervision quality depends on the perception stack; errors in semantic clustering, 3D reconstruction, point tracking, or VLM captioning propagate as noisy training signal
- Traces encode geometry and motion but not forces, tactile feedback, or contact modes — may be insufficient for precision assembly or deformable object manipulation
- Robot experiments limited to tabletop manipulation on UR3 and RoboCasa365; generalization to mobile manipulators, dexterous hands, and long-horizon tasks is unvalidated
- In simulation, π0.5 (action-labeled) still outperforms µ0 by 11.75 percentage points; the gap likely reflects the information advantage of large-scale action supervision

## Relevance to Vision-Language Models
µ0 demonstrates a principled pattern for leveraging pretrained VLMs as frozen semantic backbones within a specialized modular architecture: the VLM's KV cache provides language-grounded scene context while a dedicated Trace Expert handles metric 3D motion prediction — separating semantic memory from motion computation. The work shows that frontier VLMs (Gemini-3.1-Pro, GPT-5.5) are surprisingly weak at precise trajectory forecasting despite strong visual understanding, pointing to a systematic gap in spatial-metric reasoning. TraceExtract's use of VLMs for hierarchical event captioning also illustrates scalable semi-supervised annotation pipelines that reduce reliance on human labeling. For VLM researchers, µ0 establishes a compelling benchmark for evaluating whether VLMs can ground language instructions in physically accurate 3D motion.

## Tags
#world-model #3d-traces #robot-manipulation #vlm-backbone #flow-matching #cross-embodiment #keypoint-tracking #action-free-pretraining
