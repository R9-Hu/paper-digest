---
title: "UniX: Unifying Autoregression and Diffusion for Chest X-Ray Understanding and Generation"
authors: ["Ruiheng Zhang", "Jingfeng Yao", "Huangxuan Zhao", "Hao Yan", "Xiao He", "Lei Chen", "Zhou Wei", "Yong Luo", "Zengmao Wang", "Lefei Zhang", "Dacheng Tao", "Bo Du"]
source: "Arxiv"
venue: ""
published: "2026-01-16"
published_time: "2026-01-16T18:59:58+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2601.11522"
url: "http://arxiv.org/abs/2601.11522v1"
pdf: "paper/med-foundation/[Arxiv 2026] UniX Unifying Autoregression and Diffusion for Chest X-Ray Understanding and Generation.pdf"
---

# UniX: Unifying Autoregression and Diffusion for Chest X-Ray Understanding and Generation

*🕒 **Published (v1):** 2026-01-16 18:59 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2601.11522v1)*

## TL;DR
UniX is a unified chest X-ray foundation model that decouples understanding (autoregressive branch) and generation (diffusion branch) to eliminate the semantic-abstraction vs. pixel-reconstruction conflict that cripples prior parameter-sharing approaches. A cross-modal self-attention mechanism injects understanding features into the diffusion process, enabling synergistic collaboration at 1.5B parameters. On MIMIC-CXR, UniX improves Micro-F1 by 46.1% and FD-RadDino by 24.2% over LLM-CXR using only a quarter of its parameters.

## Problem
Existing unified medical foundation models (e.g., LLM-CXR, HealthGPT) share parameters across understanding and generation, creating feature interference because the two tasks have opposing objectives—semantic abstraction versus pixel-level reconstruction. Additionally, discrete autoregressive generation (codebook-based) loses high-frequency structural detail critical in medical imaging. Superficial stacking of a diffusion model onto a VLM fails to exploit understanding features for guiding generation.

## Method
UniX uses a **dual-branch architecture** initialized from Janus-Pro:

- **Understanding branch**: SigLIP-large visual encoder → 2-layer MLP projector → 24-layer autoregressive LLM backbone. Trained via cross-entropy loss over report tokens conditioned on image+text context.
- **Generation branch**: shares the same LLM backbone (independently parameterized), operates in a 16× downsampled 16-channel VAE latent space using flow-matching (MSE on velocity field). Reports from the understanding branch condition the diffusion process.
- **Cross-modal self-attention**: understanding text tokens and generation noise-conditioned latent embeddings form a unified sequence; modality-specific Q/K/V projection matrices (selected by indicator functions δᵘ, δᵍ) allow joint attention, letting semantic features dynamically modulate the generative trajectory without explicit cross-attention.

**Three-stage training** on MIMIC-CXR (163K understanding / 237K generation pairs, cleaned with DeepSeek):
1. Freeze generation branch; SFT understanding branch at 384×384.
2. Freeze understanding branch; pretrain generation at 256×256 with REPA alignment (hidden-state similarity to RadDino features, loss weight 0.5).
3. Freeze understanding branch; fine-tune generation at 512×512 without REPA.

## Key Contributions
- Dual-branch architecture that structurally decouples understanding (autoregressive) and generation (latent diffusion), preventing task interference while retaining synergy.
- Cross-modal self-attention mechanism enabling dynamic, content-aware semantic conditioning of the diffusion process.
- Three-stage training protocol with a DeepSeek-powered data-cleaning pipeline that removes non-diagnostic noise (underscores, metadata) from MIMIC-CXR reports.
- Demonstrated that freezing the understanding branch during generation training is essential—joint fine-tuning degrades both tasks.

## Results
**Understanding (CheXbert Micro-F1, 14-class, "uncertain" as negative):**
- UniX (1.5B): 53.6 vs. HealthGPT (3.8B): 24.2 — **+121% relative**
- Comparable to LLaVA-Rad (7B, 57.3) despite 4.7× fewer parameters
- Exceeds GPT-4V (35.5), FlamingoCXR (51.9 Micro-F1-5 only)

**Generation (256px vs. LLM-CXR 256px):**
- FD-RadDino: 65.208 vs. 71.243 (↓8.5%); at 512px: 54.022
- KD-RadDino: 0.051 vs. 0.061 at 256px; 0.024 at 512px
- Alignment Score: 0.251→0.635 at 512px vs. LLM-CXR 0.319
- At 512px, UniX matches Sana (0.6B, specialized) on FD-RadDino (54.022 vs. 54.225)

**Pathology-specific generation:** UniX (512px) achieves top FD-RadDino in 13/14 pathology categories vs. LLM-CXR, RadEdit, PixArt-Sigma, and Sana.

**Ablation:** Freezing the understanding branch during generation fine-tuning yields FD 62.1 vs. 76.1 when both branches unfrozen (no understanding data)—confirming the staged training design is critical.

## Limitations
- Evaluated exclusively on chest X-rays (MIMIC-CXR); generalizability to other modalities or anatomical regions is untested.
- Understanding branch is frozen during generation training, creating a strictly sequential dependency that limits joint optimization.
- Discrete data mixing ratios (1:1, 1:2, 1:4) explored for joint fine-tuning all underperform the frozen strategy, suggesting no clean multi-task fine-tuning recipe was found.
- Generation evaluation relies on FD/KD-RadDino and alignment scores; clinical utility of generated images (e.g., downstream diagnostic accuracy) is not assessed.
- Data cleaning relies on a proprietary LLM (DeepSeek), adding an external dependency not fully characterized.

## Relevance to Foundation Models in Medicine
UniX directly addresses a central architectural tension in medical foundation models: how to unify understanding and generation without mutual degradation. By demonstrating that architectural decoupling (rather than parameter sharing with task-specific adapters) is the right inductive bias, it establishes a scalable design principle applicable beyond radiology. The cross-modal self-attention mechanism offers a reusable bridge between autoregressive and diffusion paradigms that could generalize to other medical imaging tasks (pathology, dermatology). The result—matching single-task specialists at a fraction of the parameter count—strengthens the case for unified architectures as competitive alternatives rather than compromises in the medical AI ecosystem.

## Tags
#chest-xray #unified-model #diffusion #autoregressive #report-generation #image-synthesis #latent-diffusion #mimic-cxr
