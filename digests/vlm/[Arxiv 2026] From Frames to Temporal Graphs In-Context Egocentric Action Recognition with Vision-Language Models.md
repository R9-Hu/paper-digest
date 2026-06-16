---
title: "From Frames to Temporal Graphs: In-Context Egocentric Action Recognition with Vision-Language Models"
authors: ["Bessie Dominguez-Dager", "Francisco Gomez-Donoso", "Miguel Cazorla", "Marc Pollefeys", "Daniel Barath", "Zuria Bauer"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T18:00:42+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15417"
url: "http://arxiv.org/abs/2606.15417v1"
pdf: "paper/vlm/[Arxiv 2026] From Frames to Temporal Graphs In-Context Egocentric Action Recognition with Vision-Language Models.pdf"
---

# From Frames to Temporal Graphs: In-Context Egocentric Action Recognition with Vision-Language Models

*🕒 **Published (v1):** 2026-06-13 18:00 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15417v1)*

## TL;DR
TAG converts egocentric video into text-serialized Temporal Action Graphs via multi-stage VLM prompting, decoupling visual perception from symbolic reasoning. This unlocks efficient in-context learning (ICL) since graph demonstrations cost tens of tokens versus thousands for raw video frames. Evaluated across 11 open-weight VLMs (2B–235B), graph-based reasoning consistently outperforms direct frame-based inference.

## Problem
General-purpose VLMs struggle with fine-grained egocentric action recognition because: (1) their training is dominated by static image-text pairs, not video; (2) raw visual token streams obscure the temporal transitions between hand-object states that define actions like "take" vs. "put"; and (3) few-shot visual ICL is impractical since each video demonstration consumes thousands of image tokens, rapidly exhausting context windows.

## Method
TAG (Temporal Action Graph) is a training-free, three-stage prompting pipeline:

1. **Temporal decomposition**: 16 uniformly sampled frames are partitioned into overlapping sliding windows of size n=4 (stride 1), each anchored to its final frame to extract one interaction snapshot per frame.
2. **Neuro-symbolic mapping (two-stage per window)**: Stage I — the VLM generates a free-form natural-language narrative `N_t` describing the dominant hand-object interaction visible at the anchor frame. Stage II — the narrative alone (no frames) is parsed into a structured JSON local graph `G_t` consisting of attributed triplets `(source, relation, object)`, where source ∈ {hand_left, hand_right, hand_both, camera_wearer}, relation is open-vocabulary, and object is an (attribute, label) pair.
3. **Temporal graph construction**: Window-level graphs are merged into a directed attributed graph `G^τ` with temporal indices, then serialized as a chronologically ordered text string of triplets.

For action prediction, the serialized graph replaces raw frames as VLM input. For ICL (Graphs + ICL), N labeled graph exemplars from the training split are prepended to the query graph prompt.

## Key Contributions
- TAG framework converting egocentric video to open-vocabulary temporal interaction graphs via multi-stage prompting, with no training or fine-tuning required.
- Demonstration that symbolic graph reasoning consistently outperforms raw frame-based inference across 11 VLMs (2B–235B), even when pretraining data contamination should favor pixel-based memorization.
- Text-serialized graphs enable practical few-shot ICL: each demonstration costs ~tens of tokens vs. thousands for visual demonstrations, allowing class-balanced ICL pools.
- Extensive zero/few-shot evaluation on EGTEA (106 classes) and Epic-Kitchens-100 (3,806 composed action classes) with ablations over graph construction components, ICL shot count, and frame budget.

## Results
- **EGTEA (Top-1, best model Qwen3-VL-235B)**: Frames-only 49.7 → Graphs-only 52.3 → Graphs+ICL 56.2.
- **EGTEA MCA, GLM-4.6V (>100B)**: Frames-only 35.8 → Graphs-only 42.4 → Graphs+ICL 47.7 (+11.9 MCA absolute).
- **EGTEA, Llama-4-Scout (weak visual baseline)**: MCA 17.4 (frames) → 29.7 (Graphs+ICL), showing graphs partially compensate for poor temporal pretraining alignment.
- **Epic-Kitchens-100, GLM-4.6V\* (Action Top-1)**: 10.60 (frames) → 14.02 (Graphs+ICL); Action Top-5: 17.68 → 26.69.
- **EK-100 macro-average**: Graphs+ICL beats frames-only on every metric; largest single gain is verb Top-1 (23.14 → 30.25).
- **Ablation (Qwen3.5-35B on EGTEA)**: Sliding windows +4.51 MCA, multi-stage prompting +3.63 MCA, node attributes +2.04 MCA — all three components contribute independently.
- **Frame budget check**: Frames-only at 4 frames underperforms 16 frames, ruling out that graph gains come simply from reduced frame count.
- **ICL scaling**: k=1 example per class already surpasses both baselines for most models; gains are not monotonic with k and are model-dependent (Gemma-3 degrades with ICL).

## Limitations
- Multi-stage pipeline incurs ~27 VLM forward passes per clip (26 for graph construction + 1 for prediction) vs. 1 for frames-only; full latency analysis is deferred.
- Accuracy remains below specialized egocentric models fine-tuned on in-domain data (e.g., EgoVLP, LaViLa).
- Graph quality is bounded by Stage I narrative quality — perception errors (e.g., misreading hand-object interactions) cannot be recovered downstream.
- Optimal ICL shot count k is model-dependent; some architectures (Gemma-3) degrade with added demonstrations.
- Epic-Kitchens-100 ICL evaluation restricts the candidate set to the top 50–100 most frequent classes out of 3,806, limiting coverage of the long tail.

## Relevance to Vision-Language Models
This paper directly quantifies a core VLM architectural limitation: despite strong language-domain reasoning, current VLMs are poor temporal visual observers, and this gap is measurable and consistent across model families from 2B to 235B parameters. The TAG framework offers a practical neuro-symbolic bridge — projecting video into text — that better exploits VLMs' pre-trained strengths without any fine-tuning. For researchers tracking VLMs, the key insight is that structured intermediate representations (graphs serialized as text) enable efficient many-shot ICL that is simply infeasible with raw visual tokens, pointing toward a broader design principle for video-language tasks. The findings also raise questions about what video pretraining would need to look like to close the gap between symbolic and pixel-based reasoning.

## Tags
#vlm #egocentric-video #action-recognition #scene-graphs #in-context-learning #neuro-symbolic #temporal-reasoning #training-free
