---
title: "MASTER: Enhancing Large Language Model via Multi-Agent Simulated Teaching"
authors: ["Liang Yue", "Yihong Tang", "Kehai Chen", "Jie Liu", "Min Zhang"]
source: "NeurIPS"
venue: "NeurIPS 2025"
published: "2025-01-01"
year: 2025
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "openreview:5GaDcRVgBw"
url: "https://openreview.net/forum?id=5GaDcRVgBw"
pdf: "paper/agentic-ai/[NeurIPS 2025] MASTER Enhancing Large Language Model via Multi-Agent Simulated Teaching.pdf"
---

# MASTER: Enhancing Large Language Model via Multi-Agent Simulated Teaching

## TL;DR
MASTER is a data augmentation framework that uses multi-agent teacher-student simulations grounded in three pedagogical scenarios (error correction, collaborative debate, analogical reasoning) to generate high-quality instruction fine-tuning data. Applied to existing datasets, it produces BOOST-QA (19K samples), which consistently outperforms baseline augmentation methods across math, coding, and general reasoning benchmarks. The key insight is that injecting cognitively diverse, structured interactions into training data improves model generalization more than lexical or prompt-based augmentation.

## Problem
High-quality instruction fine-tuning data is scarce and expensive; existing synthetic data methods rely on predefined prompts or simple transformations that lack authentic interaction structure, produce limited cognitive diversity, and fail to match real-world instruction scenarios. Single-agent self-chat methods lack clear interaction mechanisms and generate mismatch between training data and actual reasoning processes.

## Method
MASTER operates via MACLASS, a multi-agent classroom simulator with two agent types (Teacher, Student), each assigned role- and phase-specific prompts to enforce coherent turn-taking and prevent role drift. Three augmentation modules transform original QA data:

1. **Error Correction (ME):** A weak student agent (Qwen2.5-0.5B, temp=0.8) generates a flawed answer; a teacher agent (Qwen2.5-14B, temp=0.2) identifies errors and guides correction; the student revises. This injects structured noise into gradient descent (Eq. 1), helping models escape local minima.

2. **Debate (DB):** Three student agents (7B×2 + 14B summarizer) independently solve a problem, debate over 1-2 rounds, then a 14B summarizer produces a final answer. Multi-perspective disagreement smooths the loss landscape (Eq. 2).

3. **Analogical Expansion (EP):** Using all-MiniLM-L6-v2 embeddings and cosine similarity, a structurally similar question is retrieved from a pool; the student solves both, and the concatenated pair is trained jointly with a mixed log-likelihood loss (Eq. 4), acting as implicit interpolation augmentation.

All three scenario outputs are concatenated in ShareGPT format into BOOST-QA (19K samples, sampled from Orca-Math-200K, ProcQA, OpenHermes2.5). Only 4.1% of augmented samples contained procedural errors per a Qwen2.5-32B verifier.

## Key Contributions
- MASTER: a pedagogically grounded multi-agent data augmentation framework combining three scenario types, each with distinct gradient-level justification.
- BOOST-QA: a 19K instruction fine-tuning dataset augmented from three existing datasets.
- Empirical demonstration that all three scenarios are necessary — single or dual scenario ablations underperform even the original unaugmented data on average.
- Analysis showing MASTER models produce longer reasoning chains, suggesting internalization of structured reasoning rather than shortcut learning.

## Results
- LLaMA3-8B fine-tuned on BOOST-QA vs. Ori-Data (same 19K samples): average score 51.26 vs. 45.98 across 7 benchmarks (MATH, MMLU-PRO-MATH, MBPP, HumanEval, MMLU, ARC, SCI-Q).
- MMLU-PRO-MATH: LLaMA3-8B improves from 13.55 → 27.39; HumanEval: 39.02 → 50.61.
- Compared to TAGCOS (best non-MASTER baseline), BOOST-QA achieves 51.26 avg vs. 47.93.
- BOOST-QA outperforms RandomAug (38.77), SpellingAug (29.21), and CoT-fine (41.11) across all benchmarks on LLaMA3-8B.
- On 8 complex multiple-choice benchmarks (Figure 2): average improvement over Ori-Data is 15.50%, with peak gain of 31.46% on MATH5K-MC.
- Qwen2.5-7B BOOST-QA average: 60.64 vs. 37.27 Ori-Data; Mistral-7B: 35.32 vs. 32.46.

## Limitations
- All agent roles use Qwen2.5-Instruct models; performance and cost of augmentation scale with model size, and results may not generalize to other teacher/student model families.
- BOOST-QA is restricted to 19K samples; it is unclear how MASTER scales with larger augmentation budgets or whether quality degrades.
- Ablations show single-scenario augmentation hurts performance relative to baseline — practitioners must always use all three, which triples augmentation complexity.
- Experiments conducted only on 7B–8B base models; scalability to larger models is untested.
- The 4.1% procedural error rate in augmented data is acknowledged but not ablated for impact.
- No human evaluation of augmented data quality; subjective answer correctness is judged by Qwen2.5-14B-Instruct (potential bias toward Qwen-generated reasoning styles).

## Relevance to Agentic AI / LLM Agents
MASTER directly applies multi-agent interaction — with role specialization, structured turn-taking, and cognitive-level diversity — as a *data generation* tool rather than a task-solving tool, demonstrating that agent collaboration can improve the base capabilities of LLMs themselves. This connects to a growing line of work using agent societies for synthetic data curation, complementing approaches like self-play RLHF and constitutional AI. The pedagogically grounded scenario design (error correction, debate, analogy) is a concrete model for how agent roles can be structured to produce epistemically diverse outputs — a pattern applicable to agentic evaluation, red-teaming, and collaborative reasoning pipelines. The finding that all three scenario types are jointly necessary highlights the importance of cognitive diversity in multi-agent system design.

## Tags
#multi-agent #instruction-tuning #data-augmentation #synthetic-data #reasoning #llm-training #knowledge-distillation #agent-collaboration
