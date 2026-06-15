---
title: "Instruct-Particulate: Scaling Feed-Forward 3D Object Articulation with Kinematic Control"
authors: ["Ruining Li", "Yuxin Yao", "Matt Zhou", "Chuanxia Zheng", "Christian Rupprecht", "Joan Lasenby", "Shangzhe Wu", "Andrea Vedaldi"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14699"
url: "http://arxiv.org/abs/2606.14699v1"
pdf: "paper/vlm/[Arxiv 2026] Instruct-Particulate Scaling Feed-Forward 3D Object Articulation with Kinematic Control.pdf"
---

# Instruct-Particulate: Scaling Feed-Forward 3D Object Articulation with Kinematic Control

## TL;DR
Instruct-Particulate is a feed-forward model that recovers the articulated structure of a 3D mesh by conditioning on an explicit kinematic specification (part descriptions, joint types, point prompts), enabling it to train on a heterogeneous dataset of 150k+ annotated objects. VLMs serve dual roles: as a pseudo-labeling engine to build that dataset and as a test-time oracle to auto-generate kinematic conditions for arbitrary meshes. The model substantially outperforms prior methods on the Lightwheel benchmark across all input modalities.

## Problem
Prior articulation estimation networks are bottlenecked by the scarcity and low diversity of annotated 3D data (dominated by PartNet-Mobility and similar small, category-limited collections), causing poor generalization to novel object categories and AI-generated meshes. Naively aggregating heterogeneous datasets is insufficient because articulation annotations have inconsistent granularity and semantics—a model without explicit structure supervision "averages" over multiple plausible annotations and degrades.

## Method
The approach has two main components:

**Data engine (3 pipelines totaling 150k+ objects):**
1. *VLM pseudo-labeling of static meshes* — multi-view renders of synthetic 3D models are fed to a VLM (Gemini) to extract kinematic structure (parts, connectivity, joint types) and generate per-part color-coded segmentation masks via a fixed color scheme; masks are back-projected to 3D, yielding 27k objects across 432 categories.
2. *Captioning of pre-segmented models* — for datasets with existing part decompositions (117k objects from HY3D-Bench-Part-Level), a VLM generates kinematic part captions using positional language only when canonical orientation is defined, and shared captions with point-prompt disambiguation otherwise.
3. *Coding-agent generation* — 10k fully supervised articulated objects with joint parameters from Articraft across 200 categories.

**Model:** An encoder-decoder transformer takes a surface point cloud (encoded with PartField features + normals) and a kinematic condition (CLIP-encoded text prompts + optional 3D point prompts per part). Shape tokens (L << N via cross-attention compression), part tokens, and query tokens are updated through B attention blocks. Decoder heads predict per-query-point part logits and over-parameterized joint targets (local axis direction, closest point on axis, and limit-pose locations) that are geometrically aggregated to recover shared joint axes and motion bounds. Training uses cross-entropy for segmentation and L1 for joint targets in teacher-forcing style.

## Key Contributions
- Feed-forward articulation model with explicit kinematic conditioning that resolves annotation ambiguity and enables learning from heterogeneous data.
- Category-agnostic VLM-based data annotation pipeline that scales articulated 3D data to 150k+ objects across 432+ categories.
- Demonstration that pairing the model with an off-the-shelf image-to-3D generator enables simulation-ready articulated asset generation from a single real-world image.
- Over-parameterized per-query joint prediction with geometric aggregation, enabling robust axis and range estimation.

## Results
All evaluations on **Lightwheel** (243 high-quality articulated objects, 14 categories, including held-out categories such as stand mixers and range hoods):

**Image Only mode** vs. SINGAPO, PAct, PhysX-Anything, URDF-Anything+:
- Precision 73.4% (next best: URDF-Anything+ 70.7%)
- Recall 57.6% (next best: SINGAPO 25.4%)
- mIoU 0.405 (next best: 0.260)
- Angle error 18.1° (next best: SINGAPO 30.3°)

**Mesh mode** vs. Articulate AnyMesh, PartField, URDF-Anything+, Particulate:
- Precision 94.3% (next best: Particulate 89.9%)
- Recall 74.8% (next best: PartField 62.6%)
- mIoU 0.724 (next best: Particulate 0.576)
- Angle error 13.9° (next best: Particulate 20.9°)

**Mesh + Kinematic mode** vs. P3SAM:
- Precision 97.3% vs. 41.6%; Recall 95.9% vs. 79.7%

**Data ablation (Table 2):** Adding pseudo-labeled part-segmented data (Sec 3.2) and VLM-labeled synthetic data (Sec 3.1) improves part segmentation (mIoU A→B→C: 0.620→0.743→0.813); adding coding-agent data with full joint supervision primarily improves joint axes (AE C→D: 13.1°→11.0°).

**Conditioning ablation (Table 3):** Removing kinematic conditioning entirely drops precision from 87.7% to 64.1% and mIoU from 0.576 to 0.463; point prompts contribute more than text prompts when used at inference.

## Limitations
- Occluded surface regions remain unlabeled during VLM pseudo-labeling, introducing incomplete supervision.
- Part-segmented dataset filtered to ≤10 visible parts, excluding densely articulated objects.
- Joint parameter supervision is confined to the 10k coding-agent subset; pseudo-labeled data provides only part segmentation without ground-truth joint axes.
- Evaluation is restricted to the Lightwheel benchmark (243 objects, 14 categories); broader categorical coverage is claimed but not quantitatively benchmarked.
- Pipeline depends on an external image-to-3D generator for the image-conditioned use case, inheriting its geometry artifacts.
- Kinematic structure must be specified or inferred by a VLM at test time, adding latency and potential errors for uncommon object types.

## Relevance to Vision-Language Models
This paper positions frontier VLMs as the key enabler for scaling 3D articulation understanding: Gemini is used both to pseudo-label large 3D asset libraries with kinematic structures (replacing costly manual annotation) and to auto-generate kinematic conditions at test time, making the pipeline applicable to arbitrary meshes without human intervention. It is a concrete example of using VLMs' 2D object understanding to bridge the annotation gap in a domain (3D articulation) where labeling at scale has been the primary bottleneck. Researchers tracking VLMs should note the specific prompting strategies for disambiguation (fixed color-scheme segmentation, canonical-vs-ambiguous orientation captioning) and the finding that VLM-generated pseudo-labels, despite noise, yield significant generalization gains when coupled with a conditioning mechanism that resolves annotation heterogeneity.

## Tags
#vlm #3d-articulation #data-annotation #pseudo-labeling #part-segmentation #kinematic-control #embodied-ai #feed-forward
