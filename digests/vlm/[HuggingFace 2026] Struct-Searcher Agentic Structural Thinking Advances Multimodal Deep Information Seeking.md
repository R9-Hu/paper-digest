---
title: "Struct-Searcher: Agentic Structural Thinking Advances Multimodal Deep Information Seeking"
authors: ["Fan Zhang", "Vireo Zhang", "Shengju Qian", "Haoxuan Li", "Zheng Lian", "Hao Wu", "Yuan Gao", "Xinyu Geng", "Xin Wang", "Pheng-Ann Heng"]
source: "HuggingFace"
venue: ""
published: "2026-06-05"
published_time: "2026-06-05T00:00:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.07689"
url: "https://huggingface.co/papers/2606.07689"
pdf: "paper/vlm/[HuggingFace 2026] Struct-Searcher Agentic Structural Thinking Advances Multimodal Deep Information Seeking.pdf"
---

# Struct-Searcher: Agentic Structural Thinking Advances Multimodal Deep Information Seeking

*🕒 **Published (v1):** 2026-06-05 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.07689)*

## TL;DR
Struct-Searcher is a multimodal deep research agent that replaces linear evidence accumulation with AGM belief revision theory, maintaining an evolving Multimodal Structural Graph (MSG) whose nodes encode queries, goals, hypotheses, and evidence with explicit support/refute edges. It achieves state-of-the-art performance on MM-BrowseComp, HLE-VL, and BrowseComp-VL, with an average 17.2% relative accuracy gain across five backbone VLMs over the unstructured baseline.

## Problem
Existing deep research agents follow Evidence Accumulation Models (EAM): a hierarchical coordinator dispatches sub-agents that linearly aggregate evidence until a confidence threshold is met. EAMs are epistemically rigid — they treat evidence gathering as monotonic and lack any mechanism to retract or revise prior beliefs when high-fidelity contradictory evidence from a different modality (e.g., a review video contradicting a textual claim) is encountered later. This causes cascading failures in multimodal settings where cross-modal conflicts are common.

## Method
Struct-Searcher formalizes reasoning as AGM belief revision over a typed graph:

- **Multimodal Structural Graph (MSG)**: `G = (V, E)` with node types `{V_Q, V_G, V_H, V_E}` (query, goal, hypothesis, evidence) and directed edge types `{decompose, generate, require, support, refute}`.
- **Initialization**: The query node is decomposed into multiple goal nodes; hypothesis nodes and evidence nodes are generated dynamically during retrieval.
- **Belief state** `K_t ⊆ V_H` tracks accepted hypotheses. Four graph operations — *construct, populate, verify, prune* — evolve the MSG each step.
- **AGM operators**: when evidence `e` supports hypothesis `h`, belief expands (`K_{t+1} = K_t + h`); when `e` refutes `h`, belief revises (`K_{t+1} = K_t * ¬h = K_t − h`). Confidence `c_t(h)` counts net supporting minus refuting evidence nodes as an auxiliary signal.
- **Termination**: Convergence is declared when exactly one hypothesis `h*` is verified (in `K*` with `c ≥ β`) and all others are retracted.
- **Answer synthesis**: The final answer is generated from the maximal conflict-free subgraph `G* = ({h*} ∪ {e | (e, h*) ∈ E_sup}, E_sup ∩ …)` via a graph-to-context projection fed to the backbone VLM.
- **Tools**: web search, image search, web crawl, image/text analysis — orchestrated per-goal.

## Key Contributions
- Reframes multimodal deep research as belief revision rather than evidence accumulation, identifying EAM's epistemic rigidity as a fundamental structural failure mode.
- Proposes the MSG formalism with AGM-grounded operators (expansion, contraction, revision) for dynamic, conflict-aware multimodal reasoning.
- Demonstrates plug-and-play, model-agnostic applicability: average 17.2% relative accuracy improvement on BrowseComp-VL across GPT-4.1, GPT-4o, Gemini-2.5-Flash, Gemini-2.5-Pro, and GPT-5.
- Achieves SOTA on all three evaluated multimodal deep information-seeking benchmarks.

## Results
- **MM-BrowseComp** (GPT-5 backbone): 32.7% overall accuracy (OA), 26.0% strict accuracy (SA), 44.6% avg checklist score — vs. Flash-Searcher (GPT-5): 28.8% OA, 22.5% SA, 40.3% avg (best prior agent).
- **HLE-VL** (GPT-5): 17.3% avg — vs. Flash-Searcher (GPT-5): 15.2%.
- **BrowseComp-VL** (GPT-5): 48.6% avg — vs. Flash-Searcher (GPT-5): 47.9%.
- **Abstract-reported relative improvements** over second-best: +3.7% on MM-BrowseComp, +1.5% on HLE-VL, +0.7% on BrowseComp-VL.
- **Workflow comparison** (vs. ReAct linear baseline, GPT-5): +21.8% absolute on MM-BrowseComp, +1.2% on HLE-VL, +0.7% on BrowseComp-VL.
- Underperforms Flash-Searcher on the Geography sub-task of MM-BrowseComp (only noted exception).

## Limitations
- The convergence threshold `β` for hypothesis verification is "implicitly modeled" by the agent rather than explicitly defined, making reproducibility and failure analysis harder.
- The termination condition (exactly one verified hypothesis) may be brittle for genuinely ambiguous queries where multiple hypotheses remain plausible.
- Computational overhead of MSG construction and evolution is not reported; no latency or token-cost analysis is provided.
- Evaluated on only three benchmarks; all share a web-browsing-centric format, leaving generalization to other multimodal task types unverified.
- No open-source model or code release yet; authors acknowledge agentic post-training (RL) as future work.
- Marginally underperforms Flash-Searcher on the Geography sub-domain, suggesting structured backtracking may not universally help.

## Relevance to Vision-Language Models
Struct-Searcher is directly built on VLM backbones (GPT-4o, Gemini-2.5-Pro, GPT-5) and addresses a core failure mode in multimodal VLM-based agents: inability to resolve contradictions between visual and textual evidence. The model-agnostic scaffold generalizes across current VLM families and improves them all, making it relevant to researchers working on VLM reasoning, agent design, or tool-augmented inference. It also introduces three practical multimodal benchmarks (MM-BrowseComp, HLE-VL, BrowseComp-VL) as evaluation targets for future VLM agent work. The belief revision framing provides a principled theoretical lens for analyzing where VLM agents fail on complex, multi-hop, cross-modal queries.

## Tags
#vlm #multimodal-agents #deep-research #belief-revision #agentic-workflow #information-seeking #knowledge-graph #benchmark
