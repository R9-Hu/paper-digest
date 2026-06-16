---
title: "ARM: An AutoRegressive Large Multimodal Model with Unified Discrete Representations"
authors: ["Junke Wang", "Xiao Wang", "Jiacheng Pan", "Xuefeng Hu", "Feng Li", "Jingxiang Sun", "Chaorui Deng", "Zilong Chen", "Yunpeng Chen", "Kaibin Tian", "Matthew Gwilliam", "Hao Chen", "Danhui Guan", "Kun Xu", "Weilin Huang", "Zuxuan Wu", "Haoqi Fan", "Yu-Gang Jiang", "Zhenheng Yang"]
source: "HuggingFace"
venue: ""
published: "2026-06-09"
published_time: "2026-06-09T00:00:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.11188"
url: "https://huggingface.co/papers/2606.11188"
pdf: "paper/vlm/[HuggingFace 2026] ARM An AutoRegressive Large Multimodal Model with Unified Discrete Representations.pdf"
---

# ARM: An AutoRegressive Large Multimodal Model with Unified Discrete Representations

*🕒 **Published (v1):** 2026-06-09 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.11188)*

## TL;DR
ARM is a 7B autoregressive large multimodal model that unifies image understanding, generation, and instruction-guided editing through a single next-token prediction framework over discrete visual tokens. Its key innovation is a unified visual tokenizer trained with four complementary objectives (caption, pixel reconstruction, sigmoid contrastive, feature distillation) that preserves both semantic discriminability and fine-grained appearance detail. Applying GRPO-based reinforcement learning on top reveals an unexpected cross-task synergy: optimizing generation also improves editing, and vice versa.

## Problem
Existing unified multimodal models suffer from a structural mismatch: understanding tasks favor high-level semantic encoders (CLIP/SigLIP), while generation tasks require fine-grained reconstruction-oriented encoders (VQ-VAE). Most systems either maintain two separate visual encoders—incurring redundant context overhead and inference cost—or compromise understanding performance to prioritize synthesis fidelity when using a single generation-oriented tokenizer.

## Method
ARM is built in three stages:

**1. Unified Discrete Visual Tokenizer.** A frozen SigLIP2-SO400M-512 encoder provides semantic features; a learned projection module maps these into a compact latent space quantized via Finite Scalar Quantization (FSQ, 65K codebook). The tokenizer is trained end-to-end with four objectives: caption loss (ℒ_cap, cross-entropy via a frozen 0.5B Qwen2.5 LM), pixel reconstruction loss (ℒ_pix, rectified-flow DiT decoder in pixel space to avoid VAE bottleneck), sigmoid contrastive loss (ℒ_sig, aligns quantized visual tokens with SigLIP2 text embeddings), and feature distillation loss (ℒ_feat, cosine distance to original SigLIP2 visual features). Detokenization at inference uses a full FLUX.1[dev] latent DiT as a high-capacity renderer conditioned on the quantized tokens. Trained on 2.2B image-text pairs.

**2. Autoregressive LMM.** A Qwen2.5-7B backbone with an appended linear head for visual token prediction models all modalities via standard next-token prediction (ℒ_ARM) over interleaved text+visual token sequences. Four training stages: pre-training (2.5T tokens), continual training (2.5T tokens, higher resolution, more interleaved data), SFT (0.2B high-quality instruction-following tokens), then RL.

**3. Preference Alignment via GRPO.** Group Relative Policy Optimization is applied exclusively to visual token prediction. For text-to-image, GPT-o3 scores object appearance, attributes, and spatial relationships; for editing, GPT-4.1 evaluates instruction following, region preservation, and visual quality. Rollout size K=16; rewards are normalized within-group to compute advantages. Joint RL (T2I RL → Edit RL → Joint RL) yields the best overall performance.

## Key Contributions
- A unified FSQ-based visual tokenizer with four complementary supervision signals that simultaneously preserves semantic alignment (for understanding) and fine-grained appearance (for generation/editing) in a shared discrete latent space.
- A fully autoregressive 7B model trained on interleaved multimodal sequences that achieves competitive understanding, generation, and editing without separate visual encoders.
- Demonstration that GRPO-based preference alignment on discrete visual tokens induces cross-task synergy: T2I RL improves editing scores and vice versa, while understanding performance remains stable.
- Empirical finding that a semantically-aligned tokenizer reduces dependence on classifier-free guidance, enabling inference acceleration.
- Ablation showing each tokenizer loss component contributes: ℒ_sig and ℒ_feat are critical for codebook utilization (usage jumps from 69.4% to 75.6% with all losses) and zero-shot recognition (0.2% → 80.2% ImageNet ZS).

## Results
**Understanding (Table 3):**
- POPE: 87.3 (vs. Emu3: not reported, VILA-U: 83.2, Janus-Pro: 85.8 among discrete unified models)
- MMMU: 40.2 (vs. Emu3: 31.6, Chameleon: 22.4)
- MMEPerc: 1463 (vs. Emu3: 1448)
- SeedBench: 73.1

**Text-to-Image Generation (Tables 4 & 5):**
- GenEval Overall: 0.86 (ARM-RL), vs. Janus-Pro 0.80, Bagel 0.82, FLUX.1 0.66; ARM (pre-RL): 0.79
- DPG Overall: 86.00 (ARM-RL), competitive with Bagel (86.48 not shown) and FLUX.1
- WISE Overall: 0.56 (ARM-RL), vs. ARM pre-RL: 0.50; Bagel: 0.52, FLUX.1: 0.50

**Image Editing (Table 6):**
- GEdit-Bench-EN G_O: 6.68 (ARM-RL) vs. 5.75 (ARM-SFT); Bagel: 6.52, Step1X-Edit: 6.70

**RL cross-task synergy (Table 8):**
- T2I RL alone raises GEdit from 5.75 → 5.92 and GenEval from 0.79 → 0.85
- Edit RL alone raises GenEval from 0.79 → 0.80 and GEdit from 5.75 → 6.31
- Sequential T2I→Edit→Joint RL achieves best across all tasks with no understanding degradation

## Limitations
- Detokenization relies on a high-capacity FLUX.1[dev] diffusion decoder as a separate module; this partially externalizes rendering quality and adds inference cost despite conceptual unification.
- Reward models (GPT-o3 for T2I, GPT-4.1 for editing) are proprietary, making the RL stage difficult to reproduce or scale independently.
- Understanding performance, while competitive among discrete unified models, still trails leading understanding-only or continuous-representation models (e.g., Qwen2.5-VL: 58.6 MMMU vs. ARM's 40.2; InternVL2.5: 56.0).
- Codebook perplexity remains low (0.28 even with all losses), suggesting codebook under-utilization may still be a bottleneck at scale.
- No evaluation of video generation or understanding, limiting claims of full multimodal unification.

## Relevance to Vision-Language Models
ARM directly advances the unified VLM paradigm by eliminating the dual-encoder architecture that most prior work (Janus-Pro, Bagel) relies on, instead learning a single discrete representation adequate for both perception and synthesis—a key open challenge in the field. The tokenizer design and four-objective training recipe offer a reusable blueprint for practitioners building unified VLMs on top of frozen semantic encoders like SigLIP2. The GRPO finding—that preference alignment on visual tokens induces cross-task synergy without hurting understanding—has implications for how the community should think about post-training alignment in multimodal settings. The CFG-reduction result also suggests that semantic tokenization may unlock inference efficiency gains currently unavailable to VQ-VAE-based autoregressive generators.

## Tags
#vlm #unified-multimodal #autoregressive #discrete-tokenization #image-generation #image-editing #reinforcement-learning #grpo
