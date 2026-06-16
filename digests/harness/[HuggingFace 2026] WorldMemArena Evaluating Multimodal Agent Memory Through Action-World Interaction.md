---
title: "WorldMemArena: Evaluating Multimodal Agent Memory Through Action-World Interaction"
authors: ["Chengzhi Liu", "Yuzhe Yang", "Sophia Xiao Pu", "Yepeng Liu", "Lin Long", "Yichen Guo", "Nuo Chen", "Zhaotian Weng", "Elena Kochkina", "Simerjot Kaur", "Charese Smiley", "Xiaomo Liu", "James Zou", "Sheng Liu", "Yuheng Bu", "Songyou Peng", "Xin Eric Wang"]
source: "HuggingFace"
venue: ""
published: "2026-05-28"
published_time: "2026-05-28T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2605.29341"
url: "https://huggingface.co/papers/2605.29341"
pdf: "paper/harness/[HuggingFace 2026] WorldMemArena Evaluating Multimodal Agent Memory Through Action-World Interaction.pdf"
---

# WorldMemArena: Evaluating Multimodal Agent Memory Through Action-World Interaction

*🕒 **Published (v1):** 2026-05-28 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2605.29341)*

## TL;DR
WorldMemArena is a multimodal multi-session benchmark (461 tasks, 24K QA pairs) that evaluates agent memory as a four-stage lifecycle—write, maintain, retrieve, use—embedded in an Action–World Interaction Loop. It enables the first controlled head-to-head comparison of long-context, manually designed (RAG/external memory), and harness-based memory agents. Key finding: harness-based agents are more flexible than hand-engineered pipelines but remain computationally expensive and less reliable.

## Problem
Existing memory benchmarks measure static recall over dialogue, collapse evaluation to final QA accuracy, and reduce visual observations to captions—making it impossible to localize failures to specific lifecycle stages (write vs. maintain vs. retrieve vs. use). Critically, no benchmark allowed principled comparison between hand-designed memory pipelines and harness-based agents that author and reorganize their own memory during interaction.

## Method
The authors formalize multimodal agent memory as an **Action–World Interaction Loop**: at each step the agent observes a partially visible world state `o_t = Ω(z_t)`, selects action `a_t = π(o_t, m_t)`, and receives environment feedback `(z_{t+1}, f_t) = ε(z_t, a_t)`. Trajectories are segmented into multi-session instances under two regimes:
- **Lifelong Evolution**: synthetic hidden world states evolve across sessions (personal and project scenarios across 6 domains).
- **Agentic Execution**: real agent trajectories (GUI + embodied, 10 subcategories) split at subgoal boundaries.

Each session is annotated with gold memory points, state update markers, distractor interference points, and per-question evidence chains. Evaluation covers Stage 1 (memory recall + LLM-as-Judge for correctness/hallucination/irrelevance), Stage 2 (update handling: revised memory retained, old version removed), Stage 3 (retrieval: recall + NDCG@k), and Stage 4 (QA-Correct/Hallucination/Omission via LLM judge + F1 + BLEU-1).

Three paradigm classes are evaluated: long-context base models (GPT-5.4-mini, Qwen3.5+, Gemini 3 Flash, DeepSeek V4, Claude Haiku 4.5), manually designed memory systems (RAG via UniversalRAG/Qwen3-VL-Embedding; external memory via MemGPT, Mem0, A-Mem, M2A, ViLoMem, MIRIX, AUGUSTUS, SimpleMem), and harness-based agents (OpenClaw + GPT-5.4/DeepSeek-V4, Codex + GPT-5.4-nano).

## Key Contributions
- Formalization of multimodal agent memory as an Action–World Interaction Loop with an observable four-stage lifecycle (write → maintain → retrieve → use).
- WorldMemArena benchmark: 461 multi-session tasks, avg 18.4 sessions/sample, ~9.1K tokens/sample, 15,595 images, 24,258 QA pairs with stage-level annotations (gold memory points, update markers, distractors, evidence chains).
- First unified evaluation enabling direct comparison across long-context, hand-engineered, and harness-based memory paradigms under identical conditions.
- Identification of four failure modes: write≠use, multimodal bottleneck, domain instability, and harness cost/reliability trade-off.

## Results
- **High memory recall ≠ high QA accuracy**: Qwen3-VL-Embedding achieves 86.22% memory recall and 98.15% correctness but only 51.86% QA-Correct; MemGPT achieves 57.81% QA-Correct with 85.20% recall and the highest retrieval coverage (84.99% RC).
- **Update handling is universally weak**: all systems score ~52–59% on update handling, dominated by append-only behavior rather than revise/delete/merge.
- **Harness agents vs. designed systems**: OpenClaw-DeepSeek V4 achieves 50.29% QA-Correct (comparable to top external memory systems) but at ~100K tokens/session vs. ~20–40K for most designed systems (Figure 7).
- **Long-context agents**: DeepSeek V4 leads base models at 69.13% QA-Correct (larger context window benefit); Claude Haiku 4.5 scores 36.71%.
- **Agentic Execution is harder than Lifelong Evolution** for all systems; embodied/visual navigation tasks are the hardest subcategory.
- **Multimodal**: simple visual fact recall is stable; visual update and cross-modal reasoning show high variance and lower performance across all systems.
- **Retrieval saturation**: increasing retrieval k (NDCG@k/Recall@k) does not monotonically improve QA accuracy; redundant/outdated evidence degrades performance.

## Limitations
- Harness-based agent evaluation is limited to end-to-end QA because internal memory state is not exposed for lifecycle decomposition.
- Benchmark is constructed via automated pipeline with human review, but gold memory points for Lifelong Evolution are synthetically derived from hidden world states, which may not capture all natural memory patterns.
- Evaluation of Stage 4 relies on LLM-as-Judge (GPT-5.4-mini), introducing potential evaluator bias.
- Coverage is weighted toward text-rich tasks; purely visual/spatial memory (e.g., navigation maps) remains underrepresented.
- No training or fine-tuning experiments; all results are zero-shot inference, leaving open how systems respond to targeted memory training.

## Relevance to Harnesses / Meta-Harnesses
WorldMemArena directly benchmarks harness-based memory agents (OpenClaw, Codex) against hand-engineered pipelines, providing the first quantitative evidence that harness-managed memory is more adaptive in dynamic agentic settings but incurs 2–5× token cost and lower reliability than structured alternatives. For researchers building or evaluating harnesses, the four-stage lifecycle framework (write/maintain/retrieve/use) offers a principled decomposition that exposes *where* a harness's memory strategy fails—not just whether end-task accuracy is acceptable. The finding that harness memory outperforms designed pipelines on complex agentic tasks but underperforms on simpler long-horizon evolution tasks informs when to invest in harness-native memory versus lightweight RAG. The benchmark's distractor and update annotations are directly applicable to evaluating harness memory-coherence under state change, a critical stress test for any meta-harness that manages its own scratchpad or context.

## Tags
#benchmark #agent-memory #multimodal #harness #rag #long-horizon #evaluation #lifecycle
