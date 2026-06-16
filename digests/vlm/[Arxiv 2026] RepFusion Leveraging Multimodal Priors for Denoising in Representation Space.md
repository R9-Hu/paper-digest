---
title: "RepFusion: Leveraging Multimodal Priors for Denoising in Representation Space"
authors: ["Xichen Pan", "Aashu Singh", "Satya Narayan Shukla", "Xiangjun Fan", "Shlok Kumar Mishra", "Saining Xie"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T17:59:51+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14700"
url: "http://arxiv.org/abs/2606.14700v1"
pdf: "paper/vlm/[Arxiv 2026] RepFusion Leveraging Multimodal Priors for Denoising in Representation Space.pdf"
---

# RepFusion: Leveraging Multimodal Priors for Denoising in Representation Space

*🕒 **Published (v1):** 2026-06-12 17:59 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14700v1)*

## TL;DR
RepFusion repurposes a frozen pretrained multimodal LLM (MLLM) as a noisy visual representation encoder, feeding evolving noisy RAE latents into the MLLM at each denoising step so its outputs condition a small diffusion transformer (DiT). This enables frozen MLLM priors to actively participate in the denoising loop rather than serving only as static text encoders. Under matched inference FLOPs, RepFusion with a 7B frozen MLLM + 1.3B DiT outperforms baselines using 8B of newly trained denoising capacity.

## Problem
In modern text-to-image (T2I) pipelines, LLMs act solely as static text encoders: they produce fixed text embeddings once and play no role in the iterative denoising trajectory. VAE latents are too low-dimensional and reconstruction-optimized for LLMs to meaningfully process, leaving the rich priors of pretrained MLLMs unexploited during generation.

## Method
RepFusion operates in the representation autoencoder (RAE) latent space (CLIP/DINO features), which is semantically structured and already familiar to MLLMs. At each denoising step $t$, the noisy RAE latent $z_t$ is projected via a small MLP into the MLLM's input space, timestep-embedded, and concatenated with text tokens. The frozen MLLM processes this joint sequence causally, and its final $N$ hidden states (corresponding to the noisy visual tokens) are used to condition a DiT via token-wise AdaLN-Single modulation—without cross-attention overhead. Because $z_t$ evolves each step, the MLLM conditioning signal is recomputed at every denoising step, making test-time compute expenditure on repeated MLLM calls productive. Only the MLP projector and the DiT are trained; the 7B MLLM backbone remains frozen.

## Key Contributions
- Demonstrates that frozen pretrained MLLMs can encode noisy RAE latents and provide useful, step-varying denoising priors beyond static text conditioning.
- Shows that allocating capacity to a frozen conditional encoder (7B MLLM + 1.3B DiT) outperforms spending the same parameter budget on newly initialized denoisers (8B DiT or 8B Transfusion joint model) at matched inference FLOPs.
- Identifies noisy representation input—not mere recomputation—as the key mechanism: timestep-dependent learnable queries that rerun at the same MLLM cost yield 0.54 GenEval vs. RepFusion's 0.70.
- Establishes that multimodal perception pretraining is a transferable prior: replacing a language-only LLM with a perception-pretrained MLLM improves both RepFusion and Transfusion-RAE, and fine-tuning a perception-pretrained MLLM for generation degrades performance.
- Provides two independent inference-time scaling axes (MLLM size, DiT size) and shows that, within RepFusion, scaling the DiT is generally more compute-efficient under iso-FLOPs constraints.

## Results
- **GenEval** (primary): RepFusion (7B MLLM + 1.3B DiT, 547 TFLOPs) scores **0.70** vs. TextEmbed-RAE at 0.64 (+30% relative over TextEmbed-VAE at 0.54) and Transfusion-RAE at 0.66.
- RepFusion-SFT (7B MLLM + 3.2B DiT) reaches **0.85–0.87** on GenEval, **0.669–0.707** on GenEval++, **34.9–35.1** on GenEval2 (Soft-TIFA$^{GM}$), and **84.17–85.11** on DPG-Bench—competitive with or exceeding BAGEL (0.82/84.03) and Scale-RAE (0.83/79.70).
- Learnable query baseline (MetaQuery-style, same training FLOPs, inference matched to 552 TFLOPs): **0.54** GenEval; RepFusion at same budget: **0.70**.
- WISE reasoning-generation benchmark (RepFusion-SFT w/ diffusion decoder): overall **0.64**, matching or exceeding MetaQuery-XL (0.55) and BLIP-3o (0.62).
- Iso-FLOPs (~280T): 1B MLLM + 3.2B DiT achieves **0.70/0.289** GenEval/GenEval++; 3B MLLM + 1.3B DiT reaches only **0.67/0.282**—larger DiT preferred.
- Freezing a perception-pretrained MLLM (RepFusion-RAE) yields **0.70** vs. fine-tuning it at **0.65**.

## Limitations
- Requires the latent space to be RAE-based (CLIP/DINO features); gains over TextEmbed are much smaller in VAE latent space (0.54 → 0.64 step requires switching to RAE).
- Repeated MLLM inference at every denoising step substantially increases inference FLOPs (~547T for 7B + 1.3B) compared to single-pass text encoding pipelines.
- Architecture restricted to simple LLaVA-style MLLMs (CLIP-L/14 vision tower + MLP); fine-grained MLLM features (any-resolution, token compression, deep stacks) are not adopted due to complexity.
- Decoder quality affects outputs: the RAE decoder is trained on ImageNet-22k only (576-resolution ViT-XL), and the diffusion decoder is repurposed from SANA, both limiting output resolution and fidelity relative to fully native generation pipelines.
- Scaling DiT is more efficient than scaling MLLM within RepFusion under iso-FLOPs, suggesting the MLLM encoder may become a bottleneck at very large scales.
- Pretrained on ~30M image-caption pairs; BAGEL uses >1B web-scale examples, making direct capability comparisons partially confounded by data scale.

## Relevance to Vision-Language Models
RepFusion directly repurposes the standard MLLM architecture (frozen LLM + MLP projector + vision tower) as a generative component, showing that the same visual-semantic alignment priors that make MLLMs strong at understanding also transfer to denoising noisy visual representations. This challenges the dominant design pattern where MLLMs in T2I serve only as text encoders, and suggests that the MLP projector mechanism—already established for clean-image understanding—generalizes to the noisy, time-varying inputs of a diffusion trajectory. For researchers tracking VLMs, this is notable because it implies that the representation alignment achieved during MLLM pretraining has latent generative utility that can be unlocked without any fine-tuning of the LLM backbone, simply by moving generation into a semantically compatible (RAE) latent space.

## Tags
#vlm #text-to-image #diffusion #mllm #representation-learning #rae #test-time-compute #multimodal-generation
