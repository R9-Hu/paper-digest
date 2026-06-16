---
title: "Gaze Heads: How VLMs Look at What They Describe"
authors: ["Rohit Gandikota", "David Bau"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T17:59:57+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14703"
url: "http://arxiv.org/abs/2606.14703v1"
pdf: "paper/vlm/[Arxiv 2026] Gaze Heads How VLMs Look at What They Describe.pdf"
---

# Gaze Heads: How VLMs Look at What They Describe

*🕒 **Published (v1):** 2026-06-12 17:59 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14703v1)*

## TL;DR
This paper identifies "gaze heads"—a small subset (~9%) of attention heads in VLM language-model backbones that causally track and control which image region the model is currently describing. A single attention-mask intervention on these heads (no retraining) steers the model's output to any chosen visual region at 83.1% accuracy. The mechanism recurs across model sizes (2B–32B) and multiple architectures, but is absent in frozen-encoder families.

## Problem
It is unknown which internal components of a VLM couple visual grounding to language generation—i.e., *which* attention heads determine what image region gets described at each token, and whether those heads constitute a causally sufficient and manipulable control surface.

## Method
Using comic strips as a controlled testbed (panels laid out left-to-right provide unambiguous spatial ground truth), the authors score every attention head in Qwen3-VL-8B (1,152 heads across 36 layers) by a **gaze score**: the average diagonal mass of a 6×6 attention matrix where rows are queried panels and columns are attended panels, across 500 forward passes. This selects heads that *re-route* attention to whichever panel changes across queries. Causal control is tested by injecting additive attention-mask biases (+∞ on target panel tokens, −∞ elsewhere) on the top-K gaze heads during both prefill and decoding. Layer localization uses a difference-of-means residual-stream probe (normal vs. reverse reading direction). Evaluation uses a held-out set of 500 GPT-Image-1-generated six-panel strips with 3,000 strip-target pairs, judged by an LLM (Claude Sonnet) forced to pick which panel the steered answer matches.

## Key Contributions
- **Gaze head identification**: a training-free, label-free correlation score over a handful of forward passes finds the causal head set.
- **Causal steering**: attention-mask intervention on the top-100 gaze heads redirects VQA answers to a chosen comic panel at 83.1% accuracy (chance 16.7%), versus failure with random heads and generation collapse with all heads.
- **Dynamic mid-generation control**: switching the gaze target every 50 tokens during free narration achieves Spearman ρ=0.87 between the steering schedule and the order actually described.
- **Natural image generalization**: the same heads ground spatially on COCO images; steering to a bounding box doubles non-gaze baseline accuracy (76.5% vs. 25.9% overall).
- **Architecture survey**: the mechanism transfers to Ovis1.5, Qwen2-VL, InternVL3.5, and all Qwen3-VL sizes, but is absent in LLaVA-1.5, LLaVA-NeXT, and Bunny-3B—consistent with a hypothesis that joint encoder+LM fine-tuning is required.
- **Layer localization**: gaze heads cluster in a narrow mid-late band (layers 20–28 of 36), matching where residual-stream probes show reading-order information.

## Results
- **VQA redirection (top-100 gaze heads, Qwen3-VL-8B):** 83.1% accuracy (chance 16.7%; Image Heads baseline and Localization Heads baseline both below this; random non-gaze heads near chance).
- **Static narration redirection:** 79.4% accuracy.
- **Dynamic switching (Spearman ρ):** Gaze heads 0.87; Image Heads 0.42; Localization Heads 0.33; Random −0.15.
- **COCO natural images:** 80.3% (large), 76.2% (medium), 61.7% (small) vs. 36.6%, 19.4%, 18.6% for non-gaze control.
- **Cross-architecture peak accuracy:** Ovis1.5-8B 68.7%, Qwen2-VL-7B 66.2%, InternVL3.5-8B 62.7%, LLaVA-1.5-13B 39.0%, LLaVA-NeXT-7B 35.3%, Bunny-3B 8.3%.
- **Top-K saturation:** accuracy climbs from 36% at K=5 to peak 83.1% at K=100, then degrades past K≈100.
- **Gaze head count:** 100 of 1,152 heads (8.7%), concentrated in layers 20–28.

## Limitations
- Primary experiments conducted on a single model (Qwen3-VL-8B); cross-model results exist but depth of analysis varies.
- The hypothesis that joint encoder training enables gaze head formation is not confirmed with controlled ablations; frozen-encoder vs. fine-tuned encoder confound is acknowledged but unresolved.
- Steering accuracy degrades on small COCO objects (61.7%), limiting utility for fine-grained spatial grounding.
- Discovery pipeline uses comic strips; generalization to arbitrary natural image structure is demonstrated but not exhaustively benchmarked.
- No analysis of whether gaze heads mediate downstream failure modes (e.g., hallucination, spatial reasoning errors) beyond the steering task.
- Intervention is a hard attention mask; interaction with KV-cache or other inference optimizations is not discussed.

## Relevance to Vision-Language Models
This work provides the first mechanistic, causally verified account of how VLMs internally route visual attention to language output, identifying a sparse, layer-localized head set as the operative control channel. For VLM researchers, it offers a zero-shot, training-free inference-time lever for spatial grounding—relevant to hallucination mitigation, visual QA, and region-conditioned generation without fine-tuning. It also sharpens the interpretability picture by distinguishing gaze heads from previously described image-attending heads (Image Heads, Localization Heads) through their temporal re-routing criterion rather than static attention properties. The architecture-dependence finding—that frozen-encoder models lack this mechanism—has direct implications for VLM design choices regarding encoder co-training.

## Tags
#vlm #mechanistic-interpretability #attention-heads #visual-grounding #inference-time-steering #multimodal #spatial-reasoning #hallucination
