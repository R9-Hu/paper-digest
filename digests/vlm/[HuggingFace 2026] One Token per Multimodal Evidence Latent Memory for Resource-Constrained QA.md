---
title: "One Token per Multimodal Evidence: Latent Memory for Resource-Constrained QA"
authors: ["Zhi Zheng", "Ziqiao Meng", "Hao Luan", "Wei Liu", "Wee Sun Lee"]
source: "HuggingFace"
venue: ""
published: "2026-06-09"
published_time: "2026-06-09T08:36:08+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.10572"
url: "https://huggingface.co/papers/2606.10572"
pdf: "paper/vlm/[HuggingFace 2026] One Token per Multimodal Evidence Latent Memory for Resource-Constrained QA.pdf"
---

# One Token per Multimodal Evidence: Latent Memory for Resource-Constrained QA

*🕒 **Published (v1):** 2026-06-09 08:36 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.10572)*

## TL;DR
Latent Memory replaces each raw text or image evidence item in external memory with a single high-dimensional latent token produced by a small compressor LLM/VLM, enabling retrieval and generation to operate entirely in a unified latent space. This yields 3–10× token reduction at the generator compared to standard RAG while maintaining competitive QA accuracy across text-only and multimodal benchmarks.

## Problem
RAG systems for LLM/VLM-based QA must pass raw retrieved text or images—expanding to hundreds of visual tokens per image—directly into the generator, creating prohibitive token costs, latency, and storage pressure that make memory-augmented systems impractical for edge, on-device, or resource-constrained deployments.

## Method
A small compressor LLM/VLM (e.g., LLaMA-3.2-1B or LLaVA-7B) equipped with trainable LoRA adapters encodes each evidence unit (text passage or image) into a single latent token `z_i ∈ R^{d_θ}` via the final hidden state of a special `[MEM]` embedding appended to the input. These latent tokens form the memory store.

At query time, the query is similarly compressed into the same latent space and retrieval is performed via inner-product search over MLP-projected latent vectors. Retrieved tokens are projected by a learned `W^g` into the frozen generator's hidden dimension and concatenated directly with the query embeddings—replacing raw context entirely.

Training jointly optimizes three objectives:
1. **Reconstruction loss** (`L_Recon`): cross-entropy autoregressive recovery of text evidence from `z_i`; CLIP-embedding MSE for image evidence.
2. **Contrastive loss** (`L_Contrast`): multi-positive InfoNCE to align query embeddings with supporting evidence and repel negatives in the retrieval projection space.
3. **Distillation loss** (`L_Distill`): token-level KL divergence between the frozen generator conditioned on raw evidence (teacher) and on latent tokens (student).

The frozen large generator is never fine-tuned; only the compressor LoRAs and projection heads (`W^r`, `W^g`) are updated.

## Key Contributions
- Latent Memory paradigm: each multimodal evidence unit (text or image) compressed to one high-dimensional latent token usable for both retrieval and generation.
- Unified end-to-end training combining reconstruction, contrastive, and distillation objectives to make a single token simultaneously informative for all three roles.
- Extension to multimodal (image+text) memory: image evidence reconstructed via CLIP-embedding prediction + unCLIP diffusion; unified retrieval over mixed text-image candidates.
- Demonstration that the same latent representation space improves Recall@k (stronger retrieval) compared to raw-evidence RAG baselines.

## Results
**Text-only QA (LLaMA-3-8B generator, HotpotQA train → OOD eval):**
- Latent Memory k=5: out-of-domain avg F1 = 28.0, using 71 generator tokens vs. 209 for BM25 (k=5) and 208 for Dense Retrieval (k=5) — ~3× token reduction at competitive F1.
- OOD Recall@5 = 52.2 vs. 49.6 for Qwen3-Emb-0.6B (same retriever size).
- 8-token Latent Memory exceeds strongest RAG baseline (Qwen3-Emb-0.6B-ft) on OOD avg EM/F1 at all k while still using fewer tokens.

**Multimodal QA (WebQA, LLaVA-1.5-13B generator):**
- Latent Memory k=5: image-grounded F1 = 69.4 with 82 tokens vs. Nemo-Emb-1B k=5 F1 = 53.0 at 1,885 tokens — ~23× token reduction with +16.4 F1.
- Best image-grounded F1 among all reported baselines.
- Text-grounded F1 = 30.7 (competitive; Nemo-Emb-1B at 48.6 with 22× more tokens).

**Ablation:**
- Removing `L_Recon` drops OOD avg F1 by ~1.2 at k=5; removing reconstruction on negatives drops Recall@5 by ~1.5.

## Limitations
- Assumes evidence decomposes into atomic, independent text or image units; structural dependencies (table row-column relations, video temporal ordering, document layout with figures and captions) are lost when each unit is compressed in isolation.
- Text-grounded performance in multimodal settings lags behind specialized retrievers (e.g., Nemo-Emb-1B text-grounded F1 = 48.6 vs. 30.7 for Latent Memory k=5 with LLaVA-13B generator).
- High-dimensional latent tokens in text-only settings are larger in raw bytes than the original short text evidence, so storage savings apply primarily in multimodal (image) settings.
- Training requires a labeled pool of positive (supporting) evidence per query; no supervision from labeled answers is needed, but positive-evidence annotations are necessary.
- Evaluated on a frozen generator paradigm; compatibility with instruction-tuned or RLHF-fine-tuned generators that have shifted hidden-space distributions is not validated.

## Relevance to Vision-Language Models
Latent Memory directly addresses the token-budget bottleneck in VLM-augmented RAG: image evidence typically expands to 256–576 visual tokens per image in LLaVA/Gemma VLMs, making multi-image retrieval in long-context or multi-turn settings practically infeasible. By compressing each image into a single latent vector fed as a soft prompt to a frozen VLM generator, this work establishes a principled pathway for memory-efficient multimodal grounding without modifying the base VLM. The unified text-image latent retrieval space—where the same 1-token representation supports both retrieval and generation—is a meaningful architectural alternative to the dominant paradigm of separate embedding models plus raw-image VLM prompting, with direct implications for on-device VLM assistants, agentic memory systems, and multi-turn dialogue grounding.

## Tags
#vlm #retrieval-augmented-generation #efficient-inference #multimodal-qa #latent-representation #knowledge-grounding #evidence-compression #on-device
