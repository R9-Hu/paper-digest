---
title: "OneFocus: Enabling Real-World X-ray Security Screening with a Unified Vision-Language Model"
authors: ["Jiali Wen", "Hongxia Gao", "Litao Li", "Yixin Chen", "Kaijie Zhang", "Qianyun Liu", "Xiaoqin Wen"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T08:02:06+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15663"
url: "http://arxiv.org/abs/2606.15663v1"
pdf: "paper/vlm/[Arxiv 2026] OneFocus Enabling Real-World X-ray Security Screening with a Unified Vision-Language Model.pdf"
---

# OneFocus: Enabling Real-World X-ray Security Screening with a Unified Vision-Language Model

*🕒 **Published (v1):** 2026-06-14 08:02 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15663v1)*

## TL;DR
OneFocus is a unified vision-language model for X-ray contraband detection, built on Qwen2.5-VL-7B and trained on MMXray—a new benchmark of 52,124 image-caption pairs across 28 fine-grained contraband categories. The authors also introduce AnyContraSyn, a physics-informed synthesis method grounded in the Beer-Lambert law, and OnePipe, a semi-automated captioning pipeline. OneFocus achieves state-of-the-art performance across VQA, classification, localization, and image understanding tasks on multiple X-ray security benchmarks.

## Problem
Existing X-ray contraband detection methods rely on closed-set object detectors with poor generalization to novel contraband. VLMs offer open-vocabulary reasoning but are blocked by a severe scarcity of multimodal (image-caption) X-ray data: all major datasets lack captions, and the only prior multimodal dataset (STCray) uses rigid template-based captions covering only 21 categories, which limits textual diversity and scene comprehension. Additionally, naive natural-image augmentation (e.g., Mixup) is physically invalid for X-ray images, distorting material attenuation responses.

## Method
**MMXray construction via OnePipe**: A three-stage semi-automated pipeline—(1) resolution and mask-consistency filtering; (2) manual annotation of 20K captions covering 6 attributes (category, color, quantity, location, container context, bounding box) fed into Qwen2.5-VL-32B for structured caption generation; (3) LoRA fine-tuning of Qwen2.5-VL-7B into a dedicated Captioner, whose outputs are rewritten by GPT-4o for lexical diversity, then used for a second fine-tuning round to annotate remaining images.

**AnyContraSyn**: Physics-informed X-ray image synthesis using Beer-Lambert attenuation additivity. Foreground and background images are mapped to optical-depth (log-attenuation) maps, fused additively in the attenuation domain, and exponentiated back to intensity. This correctly models material superposition—unlike Mixup, which produces a sum of exponentials instead of an exponential of a sum. Mask-constrained placement (via MobileSAMv2 masks) ensures the foreground contraband falls entirely inside the background package region. The CleanDET dataset provides isolated single-contraband images and clean backgrounds as synthesis inputs.

**OneFocus training**: Two-stage fine-tuning on Qwen2.5-VL-7B (ViT + 2-layer MLP projector + Qwen2.5 LM-7B). Stage 1 performs full LLM fine-tuning on captioning data (~1M tokens, batch 64, cosine LR to 2×10⁻⁶, DeepSpeed-Zero2, 1 epoch). Stage 2 applies LoRA (rank 16, alpha 32) to all LLM linear layers on multi-turn Q&A data covering VQA, localization, classification, and image understanding (~1.7M tokens, batch 128, DeepSpeed-Zero3, 2 epochs). An ablation study established that adapting only the LLM (with ViT and projector frozen) is optimal; updating the projector degrades performance.

**Hybrid-format Q&A**: Six evaluation dimensions—Instance Location, Counting, Identity, Feature, Misleading, and Basic Understanding—with both open-ended and multiple-choice formats. Test set contains 2,924 single-choice questions.

## Key Contributions
- **MMXray**: 52,124 image-caption pairs across 28 contraband categories, the largest multimodal X-ray security dataset, combining real scans from airports/subway/parcel facilities with physics-accurate synthetic data.
- **AnyContraSyn**: Beer-Lambert-grounded attenuation-domain fusion for physically plausible X-ray occlusion synthesis, outperforming Mixup in photometric consistency.
- **CleanDET**: A curated dataset of isolated single-contraband foreground images and contraband-free backgrounds from 3 real inspection scenarios, enabling controllable synthesis.
- **OnePipe**: Extensible semi-automated captioning pipeline with multi-round LoRA fine-tuning and GPT-4o-based linguistic diversification.
- **OneFocus**: Unified VLM achieving SOTA on VQA, classification, localization, and image understanding across PIDray, OPIXray, STCray, and MMXray benchmarks.

## Results
- **VQA (avg accuracy)**: OneFocus 72.8% vs. STING-BEE 47.8%, Qwen2.5-VL 56.9%, InternVL3.5 56.7% (evaluated on STCray+MMXray test sets, 40,589 Q&A pairs).
- **Classification F1/mAP** — PIDray: 29.5/30.8 vs. Qwen2.5-VL 22.6/22.8 (+6.9% F1, +8.0% mAP); OPIXray: 29.4/34.7 vs. InternVL3.5 22.4/22.8 (+7.0% F1, +11.9% mAP); MMXray: 66.0/60.9 vs. Qwen2.5-VL 46.1/47.2 (+19.9% F1, +13.7% mAP).
- **Localization mAP50/mAP25** — PIDray: 18.5/31.2 vs. GroundingDINO 17.5/22.6; MMXray: 32.2/51.6 vs. STING-BEE 20.5/29.6 (+11.7% mAP50, +22.0% mAP25).
- **Image understanding** (BLEU-4/ROUGE-L on STCray+MMXray): OneFocus 12.3/36.6 vs. STING-BEE 6.9/27.7 (+5.4% BLEU-4, +8.9% ROUGE-L).
- **Cross-domain generalization** (trained on MMXray only, zero-shot on STCray): VQA 48.0, Loc mAP 43.1—surpassing STING-BEE trained on MMXray (42.4/38.8) and approaching STING-BEE trained in-distribution on STCray (52.8/46.5).
- **Data efficiency**: LLaVA-1.5 fine-tuned on MMXray achieves VQA 55.6% vs. naive Qwen2.5-VL at 56.9%, demonstrating that domain-specific data quality dominates over backbone pre-training scale.
- **Synthetic data ablation**: Using synthetic data in both training stages yields 72.8% vs. 64.7% without any synthetic data.

## Limitations
- Localization errors persist when multiple contraband items share similar visual appearance (e.g., visually similar knives overlapping), as shown qualitatively in failure cases.
- VLMs prioritize semantic alignment over spatial precision; the architecture lacks explicit coordinate awareness, making precise bounding-box prediction inherently weak even after domain fine-tuning.
- Reliance on global context causes confusion of overlapping contraband—a structural problem not resolved by fine-tuning alone.
- MMXray caption quality depends on Qwen2.5-VL-32B for initialization; errors in the seed captions can propagate through the captioner fine-tuning loop despite human review.

## Relevance to Vision-Language Models
This paper provides empirical evidence for a critical finding in VLM domain adaptation: the vision encoder and projector generalize surprisingly well to out-of-distribution X-ray imagery, and the binding constraint is language-side domain knowledge rather than visual representation. The result that LLM-only LoRA adaptation matches or exceeds full fine-tuning (BLEU-1 55.81 vs. 55.43) directly informs efficient adaptation strategies for other specialized imaging modalities. The paper also highlights a persistent VLM architectural weakness—coarse spatial reasoning and lack of coordinate awareness—that is not resolved by instruction fine-tuning, motivating spatially-aware VLM architectures. For researchers tracking VLMs, OneFocus and MMXray establish a strong baseline for studying multimodal understanding under domain shift in safety-critical vision tasks.

## Tags
#vlm #x-ray #security-screening #multimodal-benchmark #domain-adaptation #data-synthesis #contraband-detection #fine-tuning
