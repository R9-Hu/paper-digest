---
title: "Struct-Searcher: Agentic Structural Thinking Advances Multimodal Deep Information Seeking"
authors: ["Fan Zhang", "Vireo Zhang", "Shengju Qian", "Haoxuan Li", "Zheng Lian", "Hao Wu", "Yuan Gao", "Xinyu Geng", "Xin Wang", "Pheng-Ann Heng"]
source: "HuggingFace"
venue: ""
published: "2026-06-05"
published_time: "2026-06-05T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.07689"
url: "https://huggingface.co/papers/2606.07689"
pdf: "paper/harness/[HuggingFace 2026] Struct-Searcher Agentic Structural Thinking Advances Multimodal Deep Information Seeking.pdf"
---

# Struct-Searcher: Agentic Structural Thinking Advances Multimodal Deep Information Seeking

*🕒 **Published (v1):** 2026-06-05 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.07689)*

## TL;DR
Struct-Searcher is a multimodal deep research agent that replaces linear evidence accumulation with belief-revision-driven structural thinking, maintaining an evolving Multimodal Structural Graph (MSG) grounded in AGM theory. It explicitly tracks hypothesis, goal, and evidence nodes with support/refute relations, pruning contradictory branches to synthesize answers from a maximal conflict-free subgraph. It achieves state-of-the-art on MM-BrowseComp, HLE-VL, and BrowseComp-VL while remaining plug-and-play across VLM backbones.

## Problem
Existing deep research agentic workflows follow an Evidence Accumulation Model (EAM): they linearly aggregate evidence until a confidence threshold is met. This is epistemically rigid — once a wrong entity or fact enters the chain, errors propagate monotonically with no mechanism to retract prior beliefs. In multimodal settings, cross-modal conflicts (e.g., text claiming X while a retrieved video shows ¬X) are common, and EAM-based systems cannot handle such contradictions structurally.

## Method
Struct-Searcher maintains a typed directed graph G = (V, E) with node sets V_Q (query), V_G (goals), V_H (hypotheses), V_E (evidence) and edges from C = {decompose, generate, require, support, refute}. The agent state Σ_t = (K_t, c_t, s_t) tracks the current belief set K_t ⊆ V_H, per-hypothesis confidence c_t, and status s_t ∈ {unverified, verified, refuted}.

At each step:
1. **Graph evolution** via four operators — *construct* (decompose query into goals), *populate* (add evidence via multimodal tool calls: web search, image search, web crawl, image analysis), *verify* (match evidence to hypotheses), *prune* (remove refuted branches).
2. **AGM belief revision**: supporting evidence expands K (K⁺φ = Cn(K∪{φ})); refuting evidence contracts it (K_t+1 = K_t − h).
3. **Termination**: fixed point where exactly one hypothesis h★ is verified and all others are outside K★.
4. **Answer synthesis**: conditioned on the maximal conflict-free subgraph G★ induced by h★ and its support edges.

Global context summarization runs every 8 steps to maintain coherence. Implementation uses an OpenAI-compatible Python API with GPT-4o, Gemini-2.5-Pro, or GPT-5 backbones.

## Key Contributions
- Reframes multimodal deep research as a belief revision problem, formally diagnosing EAMs as epistemically rigid under cross-modal conflict.
- Proposes the MSG data structure with typed nodes and semantic-relation edges as an externalized, revisable belief substrate.
- Instantiates AGM belief expansion/contraction/revision operators over the MSG with concrete confidence propagation and status transition rules.
- Demonstrates plug-and-play applicability: average 17.2% relative accuracy improvement across five backbone models on BrowseComp-VL without backbone-specific tuning.

## Results
- **MM-BrowseComp** (GPT-5): 32.7% overall accuracy, 26.0% strict accuracy, 44.6% avg checklist score — best among all baselines including o3 (29.0%) and Flash-Searcher/GPT-5 (28.8%).
- **HLE-VL** (GPT-5): 17.3% overall accuracy vs. Flash-Searcher/GPT-5 at 15.2% (second-best); relative improvement of 1.5% reported in abstract.
- **BrowseComp-VL** (GPT-5): 48.6% overall accuracy vs. Flash-Searcher/GPT-5 at 47.9%; Gemini-2.5-Pro backbone achieves 38.3% vs. Flash-Searcher's 35.2%.
- **Workflow comparison** (GPT-5 backbone, absolute improvements over Flash-Searcher parallel workflow): +21.8% on MM-BrowseComp, +1.2% on HLE-VL, +0.7% on BrowseComp-VL.
- **Backbone sensitivity**: consistent gains across GPT-4.1, GPT-4o, Gemini-2.5-Flash, Gemini-2.5-Pro, GPT-5; average relative improvement 17.2% on BrowseComp-VL.

## Limitations
- Absolute accuracy numbers remain low on harder benchmarks (e.g., 32.7% on MM-BrowseComp even with GPT-5), indicating the task is far from solved.
- Geography sub-task on MM-BrowseComp is the one domain where Struct-Searcher underperforms Flash-Searcher; no explanation is provided.
- The confidence threshold β for hypothesis verification is "implicitly modeled by the agent" — no ablation or formal specification.
- Context summarization every 8 steps is a heuristic with no ablation on interval sensitivity.
- No open-source release of model or code at time of submission; the paper's planned agentic post-training direction is future work.
- Evaluated only with proprietary VLM backbones (GPT-4o, Gemini-2.5-Pro, GPT-5); open-source backbone experiments are limited.

## Relevance to Harnesses / Meta-Harnesses
Struct-Searcher is a concrete example of a **structured agentic harness**: it wraps arbitrary VLM backbones with a deterministic graph-state machine (MSG) that governs tool dispatch, belief tracking, and termination — exactly the kind of scaffold a meta-harness would need to orchestrate. The AGM-grounded belief revision loop is a formal analogue to the retry/verify/prune patterns common in research harnesses, showing how principled state management can replace ad hoc prompt chains. Its plug-and-play, model-agnostic design directly informs how meta-harnesses should separate workflow logic from backbone selection. The explicit conflict-detection and subgraph pruning mechanism offers a template for harnesses that aggregate heterogeneous sources (e.g., arXiv + web + image) and must resolve contradictions before synthesis.

## Tags
#agentic-workflow #belief-revision #multimodal #deep-research #knowledge-graph #information-seeking #harness-design #vlm
