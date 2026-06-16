---
title: "Reroute, Don't Remove: Recoverable Visual Token Routing for Vision-Language Models"
authors: ["Cheng-Yu Yang", "Shao-Yuan Lo", "Yu-Lun Liu"]
source: "HuggingFace"
venue: ""
published: "2026-06-10"
published_time: "2026-06-10T00:00:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.12412"
url: "https://huggingface.co/papers/2606.12412"
pdf: "paper/vlm/[HuggingFace 2026] Reroute, Don't Remove Recoverable Visual Token Routing for Vision-Language Models.pdf"
---

# Reroute, Don't Remove: Recoverable Visual Token Routing for Vision-Language Models

*🕒 **Published (v1):** 2026-06-10 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.12412)*

## TL;DR
Existing visual-token reduction methods for VLMs irreversibly discard low-ranked tokens after a single scoring decision, but token importance shifts substantially across decoder depth, causing grounding to collapse under aggressive reduction. Reroute replaces permanent removal with recoverable deferral: low-ranked tokens bypass the current decoder stage via a residual path and re-enter the candidate pool at the next routing decision. This training-free plug-in augments FastV, PDrop, and Nüwa with no additional parameters, matched theoretical FLOPs/KV-cache cost, and consistent grounding improvements.

## Problem
Decoder-side visual-token pruning (FastV, PDrop, Nüwa) commits irreversibly at early/middle layers using text-to-vision attention scores. Because visual-token importance is unstable across decoder depth—tokens ranked near-zero at layer 3 can climb to the 97th percentile by layer 25—permanently discarding low-ranked tokens causes grounding accuracy to collapse under aggressive reduction (IoU < 0.4 at 88.9% token reduction). The flaw is not the scorer but the post-selection action of permanent deletion.

## Method
Reroute recasts stage-wise pruning as recoverable routing. The decoder is partitioned into S stages, each at routing layer ℓᵢ with keep ratio rᵢ. At each stage, text-to-vision attention scores rank the full candidate pool V; the top-K tokens are routed through the full Attn+FFN block, while deferred tokens bypass it via a residual path (hidden states unchanged) and re-enter the full candidate set V at the next stage. Crucially, the candidate set resets to all V at every stage (`C_{i+1}^{reroute} = V`), whereas pruning contracts it to only the previously selected tokens (`C_{i+1}^{prune} = V_i^{sel}`). Conventional pruning is the degenerate case where deferred tokens have zero re-entry probability. No router is trained; the mechanism reuses existing attention scores and stage schedules. This is framed as a training-free, attention-driven instantiation of Mixture-of-Depth for VLM visual tokens.

## Key Contributions
- **Recoverable routing formulation**: Reframes decoder-side token reduction as stage-wise routing with deferred-token bypass, making irreversible pruning a degenerate special case.
- **Training-free plug-in with matched budget**: No extra parameters; reuses existing scorers and schedules; preserves the same theoretical TFLOPs and KV-cache class as the augmented pruning method.
- **Consistent cross-method and cross-backbone gains**: Applied to FastV, PDrop, and Nüwa on LLaVA-1.5-7B, Qwen2.5-VL-7B, and Qwen3.5-9B-Hybrid, with the largest improvements under aggressive reduction and grounding-heavy evaluation.

## Results
**LLaVA-1.5-7B (RefCOCO-series, HuggingFace format):**
- At 192 avg tokens (↓66.7%): FastV+Reroute raises average ratio 45.5%→59.2%; PDrop+Reroute raises 71.3%→82.3%
- At 128 avg tokens (↓77.8%): FastV+Reroute +12.0 points; PDrop+Reroute +7.8 points
- At 64 avg tokens (↓88.9%): PDrop+Reroute raises average ratio 22.2%→34.0%

**Qwen2.5-VL-7B (RefCOCO-series):**
- At 77.8% reduction: PDrop+Reroute 29.3%→37.4%
- At 88.9% reduction: PDrop+Reroute 11.1%→18.6%

**Qwen3.5-9B-Hybrid (largest gains):**
- At 66.7% reduction: FastV+Reroute 31.1%→77.5%; PDrop+Reroute 40.0%→77.7%
- At 77.8% reduction: PDrop+Reroute 25.8%→59.7%

**General VQA (LLaVA-1.5, 8 benchmarks):** Reroute matches or improves matched baselines at all budgets; grounding gains are not obtained at the expense of VQA performance.

**Efficiency (LLaVA-1.5, 64-token budget):** FastV+Reroute reduces TFLOPs/KV-cache by 80%/86%; PDrop+Reroute by 77%/83% — within ~2–5% of the corresponding pruning baseline.

## Limitations
- Inherits the attention-score router's weaknesses: poor ranking or overly aggressive budgets can leave useful tokens inactive across multiple stages.
- Efficiency gains are theoretical; practical wall-clock latency depends on optimized gather/scatter kernels and KV-cache management not yet delivered.
- Evaluated only for decoder-side reduction; combinations with encoder-side compression, token merging, and KV-cache eviction are not exhaustively studied.
- In hybrid architectures (Qwen3.5), routing is restricted to softmax-attention blocks; interaction with linear-attention (Gated DeltaNet) state dynamics is unanalyzed.

## Relevance to Vision-Language Models
This paper directly addresses a core bottleneck in VLM inference: the quadratic cost of attention over hundreds of visual tokens. By demonstrating that token importance is non-stationary across decoder depth—a phenomenon documented but not previously exploited for routing—Reroute provides a principled, training-free retrofit for the widely-used FastV/PDrop family of pruning methods. The framing of pruning as degenerate Mixture-of-Depth is a conceptual unification relevant to researchers designing efficient decoder architectures and dynamic computation strategies for MLLMs. The strong Qwen3.5-Hybrid results also open a direction for applying depth-wise routing to emerging hybrid Mamba-Transformer VLMs.

## Tags
#vlm #visual-token-reduction #efficient-inference #mixture-of-depth #token-routing #visual-grounding #training-free #decoder-side-pruning
