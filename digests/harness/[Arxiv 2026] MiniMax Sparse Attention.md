---
title: "MiniMax Sparse Attention"
authors: ["Xunhao Lai", "Weiqi Xu", "Yufeng Yang", "Qiaorui Chen", "Yang Xu", "Lunbin Zeng", "Xiaolong Li", "Haohai Sun", "Haichao Zhu", "Vito Zhang", "Jinkai Hu", "Jiayao Li", "Rui Gao", "Zekun Li", "Songquan Zhu", "Jingkai Zhou", "Pengyu Zhao"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13392"
url: "http://arxiv.org/abs/2606.13392v2"
pdf: "paper/harness/[Arxiv 2026] MiniMax Sparse Attention.pdf"
---

# MiniMax Sparse Attention

## TL;DR
MiniMax Sparse Attention (MSA) replaces full quadratic softmax attention with a two-branch blockwise sparse mechanism: a lightweight Index Branch scores and selects top-k KV blocks per GQA group, and the Main Branch attends only to those blocks. Validated at 109B-parameter MoE scale, MSA matches full-attention quality while delivering 28.4× FLOPs reduction and 14.2×/7.6× prefill/decoding wall-clock speedups at 1M context.

## Problem
Quadratic-cost softmax attention becomes a hard deployment bottleneck for frontier LLMs operating over hundreds of thousands to millions of tokens—the regime required by agentic workflows, repository-scale code reasoning, and persistent memory. Existing sparse-attention approaches either degrade quality, introduce hardware-unfriendly access patterns, or require modifications incompatible with the GQA backbone used by most current models.

## Method
MSA is a GQA-native two-stage sparse attention. The **Index Branch** adds one index query head per GQA group and one shared index key head; it scores all causally visible key tokens via dot product, max-pools scores to block granularity (block size $B_k = 128$), and selects the top-$k = 16$ blocks per group via an exp-free TopK kernel, always forcing inclusion of the local block. The **Main Branch** performs standard scaled dot-product softmax attention restricted to the $kB_k = 2048$ selected tokens. Training stability is achieved through: (1) a KL alignment loss that matches the Index Branch distribution to the group-averaged Main Branch distribution on selected tokens; (2) stop-gradient on the Index Branch inputs to prevent the auxiliary loss from affecting the backbone; (3) a two-stage warmup that runs full attention before switching to sparse. On the GPU side, the kernel uses **KV-outer iteration** (iterating over KV blocks, gathering associated queries) to achieve FLOPs/IO arithmetic intensity of $\frac{2}{3}B_k$ vs. just $G$ under Q-outer, with pre-scheduled tile chunking and a two-phase softmax combine to handle hot KV blocks without atomics.

## Key Contributions
- MSA architecture: per-GQA-group independent block selection with a minimal two-projection Index Branch, supporting both training from scratch and near-lossless conversion from pretrained GQA checkpoints.
- Co-designed GPU kernels: exp-free TopK (5.1× faster than torch.topk at $k=16$), KV-outer sparse attention with query concatenation for full tensor-core utilization, and fused sparse KL loss backward with persistent load balancing.
- Empirical validation at 109B-MoE scale (3T tokens, native multimodal): MSA-PT (from scratch) and MSA-CPT (continued pretraining from dense checkpoint) both match Full-Attention across 30+ text, math, code, image, video, and long-context benchmarks.
- Demonstrated 28.4× theoretical FLOPs reduction and 14.2× prefill / 7.6× decoding wall-clock speedup at 1M context on H800.

## Results
- **FLOPs**: 28.4× per-token attention compute reduction vs. GQA at 1M context (with $k=16$, $B_k=128$, 2048-token budget per query).
- **Prefill speedup**: 14.2× at 1M context on H800.
- **Decoding speedup**: 7.6× at 1M context on H800.
- **Quality parity** (selected benchmarks vs. Full-Attention baseline):
  - MMLU: Full 67.0 / MSA-PT 67.2 / MSA-CPT 66.8
  - RULER-128K overall: Full 72.00 / MSA-CPT 72.12 (Δ +0.12)
  - HELMET-128K overall: Full 46.53 / MSA-CPT 45.93 (Δ −0.60)
  - Agent PPL (τ²-bench): Full 1.155 / MSA-PT 1.148 / MSA-CPT 1.150
  - MSA-PT outperforms Full on several video benchmarks (e.g., VideoMME: 45.48 vs. 41.11) and retrieval (RULER-8K: 84.2 vs. 79.8).
- **TopK kernel**: 5.1× faster than torch.topk and 3.7× faster than TileLang radix-select at $N=128$K, $k=16$.
- Training dynamics: LM-loss curves of MSA-PT and Full-Attention are nearly indistinguishable over 3T tokens; block recall and score recall remain high throughout sparse CPT.

## Limitations
- Runtime speedup (14.2× prefill, 7.6× decode) is substantially below the theoretical FLOPs reduction (28.4×) due to index construction, gather/scatter, and irregular memory access overheads inherent to sparse patterns.
- Fixed attention budget ($kB_k = 2048$ tokens regardless of sequence length) may miss contextually important content; residual long-context retrieval gap acknowledged in the conclusion.
- Index Branch adds two projection matrices and a non-trivial training schedule (warmup phase, KL loss weight tuning); hyperparameter sensitivity is not fully characterized in the main paper.
- Evaluation of MSA under reinforcement learning post-training and agentic deployment (the primary motivation) is left to future work.
- Ablations are conducted at 109B scale for the final design but smaller-scale results are in the appendix, so intermediate-scale behavior is not the focus.

## Relevance to Harnesses / Meta-Harnesses
MSA's primary motivation is enabling ultra-long-context inference for **agentic workflows**—precisely the multi-step orchestration pipelines and meta-harnesses that coordinate tool use, code execution, and persistent memory over thousands of interleaved steps. The paper evaluates explicitly on agent-oriented benchmarks (τ²-bench, TheAgentCompany, SWE-bench) framing attention efficiency as a bottleneck for the harness layer, not just for raw LLM capability. For researchers building or studying meta-harnesses, MSA represents a concrete architectural solution to the context-length scaling wall that currently constrains how many reasoning/action steps a harness can hold in a single context window. The CPT conversion path (dense→sparse in 400B tokens) is also practically significant: existing harness-serving infrastructure can adopt MSA without retraining from scratch.

## Tags
#sparse-attention #long-context #efficient-inference #agentic-workflow #gqa #kernel-optimization #multimodal #pretraining
