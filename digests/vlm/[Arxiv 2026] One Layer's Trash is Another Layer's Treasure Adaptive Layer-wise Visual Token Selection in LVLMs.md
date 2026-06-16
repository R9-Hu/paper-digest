---
title: "One Layer's Trash is Another Layer's Treasure: Adaptive Layer-wise Visual Token Selection in LVLMs"
authors: ["Yongru Chen", "Kai Zhang", "Zeliang Zong", "Yuchen Lu", "Wenming Tan", "Ye Ren", "Jilin Hu"]
source: "Arxiv"
venue: "CVPR 2026"
published: "2026-06-12"
published_time: "2026-06-12T08:58:58+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14277"
url: "http://arxiv.org/abs/2606.14277v1"
pdf: "paper/vlm/[Arxiv 2026] One Layer's Trash is Another Layer's Treasure Adaptive Layer-wise Visual Token Selection in LVLMs.pdf"
---

# One Layer's Trash is Another Layer's Treasure: Adaptive Layer-wise Visual Token Selection in LVLMs

*🕒 **Published (v1):** 2026-06-12 08:58 UTC  ·  **Source:** Arxiv  ·  **Venue:** CVPR 2026  ·  [link](http://arxiv.org/abs/2606.14277v1)*

## TL;DR
ALVTS (Adaptive Layer-wise Visual Token Selection) addresses the permanent token loss problem in existing LVLM pruning methods by allowing each decoder layer to independently select which visual tokens to process, while skipped tokens remain accessible to later layers. A lightweight token selector based on importance-consistency-constrained low-rank approximation emulates full attention without retraining. At 89% token compression, ALVTS retains 96.7% of LLaVA-1.5-7B's performance with 1.6× prefill speedup.

## Problem
Existing visual token pruning methods (e.g., FastV, PyramidDrop, DART) prune tokens at a single fixed layer and permanently discard them from all subsequent layers. This causes irrecoverable information loss because different decoder layers attend to different visual regions — a token irrelevant at layer 2 may be critical at layer 20. No prior method allows later layers to "reclaim" tokens that earlier layers deemed unimportant.

## Method
ALVTS inserts a lightweight **token selector** before each LLM decoder layer. The selector computes per-token importance scores using low-rank approximations of the layer's query and key projection matrices (rank R ≪ D, initialized via SVD of the original W_Q and W_K). Importance scores combine visual-to-visual attention (average attention a token receives from other visual tokens) and text-to-visual attention (average attention from text tokens) multiplicatively: S(i) = S_V2V(i) · S_T2V(i). Top-k tokens (k = ⌊r·N⌋) are selected to participate in the layer's full computation; the remaining tokens skip the layer entirely. After each layer, selected and skipped tokens are recombined in original order before the next layer — preserving positional information and token accessibility. The low-rank selectors are optimized independently per layer by minimizing L2 distance between approximate importance scores and oracle scores (from full-rank attention) on 256 calibration samples from LLaVA-655k, taking ~15 minutes for LLaVA-1.5-7B. Only selector parameters are updated; the base LVLM is frozen. Parameter overhead is <2% per decoder layer.

## Key Contributions
- Empirical demonstration of cross-layer heterogeneity in visual token attention patterns, motivating layer-specific token selection rather than global pruning.
- ALVTS framework: per-layer dynamic token selection with seamless token reintegration, enabling "soft" pruning where tokens skipped at one layer remain available to later layers.
- Importance-consistency-constrained low-rank approximation for token importance estimation, faithfully emulating full attention without retraining or full attention computation overhead.
- Training-free, plug-and-play deployment: optimization requires only 256 calibration samples and ~15 minutes.

## Results
- **LLaVA-1.5-7B, 89% compression (576→64 tokens):** 96.73% avg. performance across 8 benchmarks; outperforms DART (+3.46%), PyramidDrop (+8.21%), FastV (+11.60%). POPE: 83.87 vs. FastV's 59.55.
- **LLaVA-1.5-7B, 78% compression:** 98.77% avg. performance, +1.51% over second-best DART.
- **LLaVA-1.5-7B, 67% compression:** 99.60% avg., +1.41% over PyramidDrop.
- **LLaVA-1.5-13B, 89% compression:** 96.63% avg., outperforming second-best by 2.65%.
- **LLaVA-NeXT-7B, 89% compression (2880→320 tokens):** 96.25% avg. performance; POPE score of 87.09 slightly exceeds the uncompressed baseline (86.41).
- **Qwen2.5-VL-3B, 89% compression:** 86.39% avg., vs. FastV 80.23% and PyramidDrop 78.43%.
- **Efficiency (LLaVA-1.5-7B, single 4090 GPU):** prefill latency reduced from 165ms to 103ms (1.6× speedup); end-to-end latency 211ms→156ms (1.35×). At equal inference speed, ALVTS at 89% compression outperforms FastV at 60% compression by 4.5 percentage points.

## Limitations
- Adds a small but non-zero parameter and compute overhead per decoder layer (~2% parameter overhead; selector inference cost not fully quantified).
- Requires a calibration set (256 samples) and ~15 minutes of optimization per model; not completely zero-cost to deploy on a new model.
- Evaluated on standard VQA/captioning benchmarks; performance on fine-grained spatial reasoning or dense prediction tasks not reported.
- Token selection ratio r is fixed per layer rather than learned end-to-end, which may be suboptimal across heterogeneous architectures.
- No evaluation on video LVLMs or models larger than 13B parameters.

## Relevance to Vision-Language Models
ALVTS directly addresses a fundamental efficiency bottleneck in deploying LVLMs at scale: the quadratic cost of attending over hundreds to thousands of visual tokens in each transformer layer. By demonstrating that layer-wise attention patterns are heterogeneous and that a single-layer pruning decision creates irreversible information loss, the paper challenges the dominant paradigm used by FastV, PyramidDrop, and similar methods. The approach is plug-and-play and training-free, making it practically relevant for inference optimization across the LLaVA and Qwen2.5-VL families. For researchers tracking VLMs, this work highlights that token compression methods must account for inter-layer diversity in visual focus — a design principle likely to inform future efficiency work across multimodal architectures.

## Tags
#vlm #visual-token-pruning #inference-efficiency #lvlm #token-compression #attention #low-rank-approximation #multimodal
