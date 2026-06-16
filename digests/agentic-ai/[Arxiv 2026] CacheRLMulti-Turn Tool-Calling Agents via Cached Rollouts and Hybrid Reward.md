---
title: "CacheRL:Multi-Turn Tool-Calling Agents via Cached Rollouts and Hybrid Reward"
authors: ["Md Amirul Islam", "Sumiran Thakur", "Huancheng Chen", "Su Min Park", "Jiayun Wang", "Gyuhak Kim"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T07:01:50+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14179"
url: "http://arxiv.org/abs/2606.14179v1"
pdf: "paper/agentic-ai/[Arxiv 2026] CacheRLMulti-Turn Tool-Calling Agents via Cached Rollouts and Hybrid Reward.pdf"
---

# CacheRL:Multi-Turn Tool-Calling Agents via Cached Rollouts and Hybrid Reward

*🕒 **Published (v1):** 2026-06-12 07:01 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14179v1)*

## TL;DR
CacheRL trains a 4B-parameter agent model (Qwen3-4B-Thinking) for multi-turn tool calling by replacing costly live tool execution with a three-tier fuzzy cache and dynamically adjusting reward weights based on cache fidelity. The system achieves 92% process accuracy on multi-step tool-calling benchmarks, approaching GPT-5's 94%, while requiring 100× less compute than live RL training.

## Problem
Training small models for multi-turn, multi-tool agent tasks faces three compounding barriers: (1) existing agent datasets contain tool call trajectories but lack the causal reasoning traces needed for small models to generalize; (2) RL with live tool execution is prohibitively expensive (seconds of latency and API fees per call, scaled over thousands of GRPO rollouts); (3) replacing live execution with cached results introduces attribution noise—models may receive negative rewards for cache misses, not genuine policy errors.

## Method
**Stage 1 – Hybrid Thinking Trajectory Pipeline.** Each of 44,449 multi-turn trajectories is processed message-by-message. A GPT-5 classifier distinguishes *analytical* content (wrapped in `<think>` tags verbatim) from *user-facing* content (triggers GPT-5 to generate causal reasoning explaining tool selection). Final turns always receive generated reasoning. This saves 15–20% of API calls while augmenting all trajectories with structured `<think>` blocks. Original tool calls, results, and error messages are preserved unchanged. Full SFT on Qwen3-4B-Thinking follows, using sequences up to 132K tokens.

**Stage 2 – CacheAgentLoop.** During GRPO rollouts, the model generates reasoning and tool calls (mask=1). Each `</tool_call>` triggers a three-tier cache lookup: Tier 1 exact hash match (50% hit rate), Tier 2 Jaccard-similarity fuzzy match (17%), Tier 3 tool-name-only fallback (33%). Cached results are injected with mask=0, excluding them from gradient computation. Thinking blocks are pre-closed in injected content to prevent reasoning loops. `min_tokens=150` reduces premature termination from 42% to 13%.

**Cache-Tier-Aware Reward.** The hybrid reward is R = α·R_answer + (1−α)·R_process, where α ∈ {0.60, 0.30, 0.10} for exact/fuzzy/best-effort tiers respectively. R_answer is GPT-5-as-judge on a 0–5 scale (with automatic zero for thinking leakage). R_process is deterministic: valid tool names (40%), thinking blocks (15%), non-empty answers (25%), tool diversity (10%). The worst cache tier across a rollout determines α, ensuring the model is never penalized for cache-induced answer errors.

**GRPO** uses LoRA rank 128, N=16 rollouts per prompt, β=0.15 KL regularization, on 8×H100 GPUs.

## Key Contributions
- First RL system for training 4B-parameter multi-turn tool-calling agents without live execution, reducing per-rollout cost by 100×
- Hybrid thinking trajectory pipeline that augments 44K real trajectories with GPT-5-generated causal reasoning across 1,185 unique tools
- Cache-tier-aware reward design that dynamically shifts between outcome and process signals based on cache fidelity
- Empirical finding that data quality and reward design dominate over RL algorithm complexity for small agent models

## Results
- Validation reward: 0.43 → 0.78 after full SFT+GRPO pipeline
- 92% process accuracy on public agentic tool-calling benchmarks vs. GPT-5's 94%, at 2.4% of GPT-5's parameter count
- Removing knowledge transfer (hybrid thinking pipeline): −41.2% performance drop
- Removing cache-tier-aware reward weighting: −17.2% performance drop
- GRPO training provides stable optimization but minimal reward improvement beyond a strong SFT baseline
- Initial SFT subset (3,689 samples) alone underperformed; combining with 673 rejection-sampled high-quality trajectories improved reward from 0.43 to 0.76
- Cache construction yielded 40,850 exact entries from training data; 50% exact / 17% fuzzy / 33% best-effort hit rate during rollouts

## Limitations
- Cache is derived from training data; best-effort fallbacks (33% of rollouts) inject structurally plausible but factually incorrect results, introducing irreducible noise
- RL contributes training stability but negligible accuracy gains over SFT alone, calling into question whether GRPO adds value beyond data curation
- Validation set is only 120 samples; evaluation breadth on held-out benchmarks is not fully detailed in the provided text
- Training data is 84% from Toucan, limiting domain diversity despite spanning 1,185 tool names
- Evaluation limited to 4B-parameter scale; generalization of the cache-RL approach to other model sizes is unverified
- Cache-tier-aware α values (0.60/0.30/0.10) are hand-tuned; sensitivity analysis is not reported

## Relevance to Agentic AI / LLM Agents
CacheRL directly addresses the deployment gap between frontier-scale and edge-deployable agent models, offering a concrete training recipe for 4B-parameter models approaching GPT-5 on multi-turn tool use. The CacheAgentLoop's token-level masking solution to the credit-assignment problem in cached multi-turn RL is a transferable architectural primitive for any offline or semi-offline agent training setup. The central finding—that SFT data quality and reward attribution design matter more than RL algorithm sophistication—has strong implications for how the field should prioritize research effort in agentic RL. The cache-tier-aware hybrid reward mechanism is directly relevant to broader work on reward shaping in noisy, tool-augmented agent environments.

## Tags
#rl-training #tool-calling #knowledge-distillation #small-models #multi-turn #reward-design #grpo #agent-foundation-model
