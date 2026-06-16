---
title: "PP-OCRv6: From 1.5M to 34.5M Parameters, Surpassing Billion-Scale VLMs on OCR Tasks"
authors: ["Yubo Zhang", "Xueqing Wang", "Manhui Lin", "Yue Zhang", "Penglongyi Deng", "Ting Sun", "Tingquan Gao", "Zelun Zhang", "Jiaxuan Liu", "Changda Zhou", "Hongen Liu", "Suyin Liang", "Cheng Cui", "Yi Liu", "Dianhai Yu", "Yanjun Ma"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T09:35:16+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13108"
url: "http://arxiv.org/abs/2606.13108v1"
pdf: "paper/vlm/[Arxiv 2026] PP-OCRv6 From 1.5M to 34.5M Parameters, Surpassing Billion-Scale VLMs on OCR Tasks.pdf"
---

# PP-OCRv6: From 1.5M to 34.5M Parameters, Surpassing Billion-Scale VLMs on OCR Tasks

*🕒 **Published (v1):** 2026-06-11 09:35 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13108v1)*

## TL;DR

PP-OCRv6 is a lightweight, three-tier (1.5M–34.5M parameter) OCR system from Baidu that introduces a unified MetaFormer-style backbone (LCNetV4) with structural reparameterization, shared across detection and recognition tasks. It achieves 86.2% detection Hmean and 83.2% recognition accuracy, surpassing both PP-OCRv5_server and billion-parameter VLMs (Qwen3-VL-235B, GPT-5.5, Gemini-3.1-Pro) by wide margins at orders-of-magnitude lower parameter counts.

## Problem

Large VLMs applied to OCR suffer from three fundamental deficiencies: imprecise text localization (bounding boxes), hallucination (generating plausible but nonexistent text), and prohibitive computational cost for production deployment. Prior PP-OCR generations had either reached the structural capacity of their MobileNet-style backbones (LCNetV3, HGNetV2) or relied on a dual-backbone architecture that increased engineering complexity without principled design improvements.

## Method

PP-OCRv6 redesigns the full detection and recognition pipeline around a single unified building block:

**LCNetV4 backbone** follows the MetaFormer paradigm, decomposing each block into an explicit token mixer (3×3 depthwise convolution with RepVGG-style reparameterization: three parallel branches—3×3 DW, 1×1 DW, BN identity—fused to a single 3×3 DW at inference) and a channel mixer (expand-2×→GELU→compress 1×1 pointwise convolutions with residual). A single LCNetV4 codebase serves detection (standard stride-2 downsampling for multi-scale FPN input) and recognition (asymmetric stride (2,1) at Stages 3–4 to preserve width for CTC/NRTR sequential decoding), spanning three tiers (tiny/small/medium) via per-tier depth/width configurations.

**RepLKFPN (detection neck)** replaces RSEFPN's 3×3 per-level refinement blocks with a DilatedReparamBlock (7×7 DW main branch + three dilated parallel branches fused at inference) followed by 1×1 PW + SE, enlarging the local receptive field from 3×3 to 7×7 while reducing neck parameters from 172K to 118K.

**Auxiliary deep supervision (detection)** adds DB prediction heads at FPN levels P2/P3/P4 (weighted 0.4/0.3/0.2) during training only, improving gradient flow to intermediate features without inference cost.

**Focal + Dice loss (detection)** combines global region overlap (Dice) with per-pixel hard-example weighting (Focal, α=0.25, γ=2.5, equal weights).

**EncoderWithLightSVTR (recognition neck)** replaces concatenation-based skip fusion (2C×C projection) with: 1×1 channel reduction to D, DWConv 1×7 for local horizontal context injection, L=2 Transformer blocks (MHSA+FFN), then additive skip fusion via a parallel 1×1 projection of the original input. Cost: C×D parameters vs. 2C² for concatenation.

**Tiny model** omits the neck entirely; backbone output is reshaped and projected via a linear layer, then trained with KL-divergence distillation from a vocabulary-matched medium teacher (λ=1.0 on CTC logit alignment).

## Key Contributions

- **Unified three-tier model family** (1.5M / 7.7M / 34.5M end-to-end parameters) sharing a single LCNetV4 backbone codebase for both detection and recognition tasks.
- **LCNetV4**: MetaFormer-style lightweight backbone with asymmetric structural reparameterization on the DW token mixer only, with BN zero-initialization on the compress layer for training stability.
- **RepLKFPN**: Reparameterizable large-kernel FPN neck using dilated depthwise convolutions, achieving 7×7 effective RF at lower parameter count than the 3×3 baseline.
- **EncoderWithLightSVTR**: Local-then-global recognition neck with additive skip connection, replacing the parameter-heavy concatenation fusion.
- **50-language support** (medium/small) via expanded diacritical character dictionaries; tiny supports 49 (omits Japanese Kanji/Kana to limit output layer size).
- **Hallucination benchmark**: First systematic hallucination evaluation comparing specialized OCR vs. VLMs on OCR outputs.

## Results

**Text Detection (in-house benchmark, 16 categories, Hmean):**
- PP-OCRv6_medium: 86.2% avg Hmean (+4.6% over PP-OCRv5_server 81.6%; +39.4% over best VLM Gemini-3.1-Pro 46.8%)
- PP-OCRv6_small: 84.1% (surpasses PP-OCRv5_server)
- PP-OCRv6_tiny: 80.6% (+33.8% over Gemini-3.1-Pro)
- Qwen3-VL-235B: 38.3%; Kimi-K2.6: 12.8%; MiniMax-M3: 12.0%

**Resolution robustness (CV across 0.35×–2.83× scales):**
- PP-OCRv6_medium: CV 5.19% (lowest); PP-OCRv5_server: 8.02%
- At 2.83× scale: PP-OCRv6_medium 87.94% vs. PP-OCRv5_server 67.28%

**Text Recognition (in-house benchmark, 15 categories, weighted avg accuracy):**
- PP-OCRv6_medium: 83.2% (+5.1% over PP-OCRv5_server 78.1%)
- PP-OCRv6_small (5.2M): 81.3% (+3.2% over PP-OCRv5_server 21M params)
- PP-OCRv6_tiny (1.1M): 73.5% (beats 4 of 5 VLMs; trails Qwen3-VL-235B by 1.4%)
- Best VLM Qwen3-VL-235B: 74.9% (~6800× more parameters than PP-OCRv6_medium)
- Notable per-category gains (medium vs. v5_server): Japanese +16.8%, Ancient text +12.0%, Screen displays +14.4%

**Hallucination benchmark:**
- PP-OCRv6_medium: 93.2% vs. Kimi-K2.6: 85.0%, Qwen3-VL-235B: 80.6%, MiniMax-M3: 72.6%

**Crop margin robustness (consistency across crop margins):**
- PP-OCRv6_medium: 75.32% (+20.5% over PP-OCRv5_server 54.82%)

**Inference speed (end-to-end, s/image):**
- PP-OCRv6_tiny vs. PP-OCRv5_mobile: 3.9× faster on Intel Xeon OpenVINO (0.20s vs. 0.78s), 6.1× on Apple M4 PaddlePaddle
- PP-OCRv6_medium vs. PP-OCRv5_server: 5.2× faster on Intel Xeon OpenVINO (1.40s vs. 7.30s)

## Limitations

- Benchmarks are entirely in-house; no evaluation on standard public OCR datasets (e.g., ICDAR, Total-Text, CTW1500), limiting independent reproducibility.
- Tiny model drops Japanese entirely to control output layer size, reducing practical multilingual coverage at the edge tier.
- No PP-OCRv6_large model yet; authors note it as future work.
- VLM comparisons are restricted to text detection and recognition accuracy/hallucination; no evaluation of VLM-native end-to-end document understanding tasks (e.g., layout parsing, table structure, visual question answering) where VLMs may hold advantages.
- Hallucination benchmark methodology and composition are not publicly described in detail, making reproducibility of those comparisons unclear.

## Relevance to Vision-Language Models

This paper provides a direct, empirical challenge to the assumption that scaling VLMs resolves OCR: even Qwen3-VL-235B (235B parameters) is outperformed on both detection and recognition by a 34.5M-parameter specialized model, and surpassed in hallucination control by all three PP-OCRv6 tiers. For VLM researchers, the hallucination gap (93.2% vs. 80.6%) and localization gap (86.2% vs. 46.8% Hmean) quantify where autoregressive generation fails structurally compared to CTC-grounded decoding. The MetaFormer backbone design (LCNetV4) and structural reparameterization techniques are architectural insights transferable to efficient vision encoders within VLM pipelines. The work also exemplifies the data-centric + architecture co-design paradigm as a competitive alternative to scaling, relevant to researchers designing lightweight vision encoders for VLM backbone components.

## Tags

#ocr #lightweight-model #metaformer #structural-reparameterization #vlm-comparison #text-detection #text-recognition #hallucination
