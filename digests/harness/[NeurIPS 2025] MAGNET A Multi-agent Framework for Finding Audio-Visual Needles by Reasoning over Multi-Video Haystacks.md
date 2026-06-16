---
title: "MAGNET: A Multi-agent Framework for Finding Audio-Visual Needles by Reasoning over Multi-Video Haystacks"
authors: ["Sanjoy Chowdhury", "Mohamed Elmoghany", "Yohan Abeysinghe", "Junjie Fei", "Sayan Nag", "Salman Khan", "Mohamed Elhoseiny", "Dinesh Manocha"]
source: "NeurIPS"
venue: "NeurIPS 2025"
published: "2025-01-01"
year: 2025
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "openreview:CwXyUdqFqW"
url: "https://openreview.net/forum?id=CwXyUdqFqW"
pdf: "paper/harness/[NeurIPS 2025] MAGNET A Multi-agent Framework for Finding Audio-Visual Needles by Reasoning over Multi-Video Haystacks.pdf"
---

# MAGNET: A Multi-agent Framework for Finding Audio-Visual Needles by Reasoning over Multi-Video Haystacks

## TL;DR
MAGNET is a retrieval-augmented multi-agent framework that answers queries by spawning one audio-visual LLM agent per retrieved video clip, then passing all partial responses to a meta-agent (GPT-4o) for synthesis. It is paired with AVHaystacks, a new 3,100-QA benchmark requiring evidence from up to 500 videos per query. MAGNET achieves up to 89% and 65% relative improvement in BLEU@4 and GPT evaluation over baselines.

## Problem
Existing video QA benchmarks pair each question with a single clip, failing to capture real-world scenarios (personal archives, how-to libraries) that demand retrieval and reasoning across hundreds of videos jointly using both audio and visual signals. No benchmark or model had systematically evaluated cross-video multi-modal retrieval with temporal grounding.

## Method
**Pipeline overview:** Given a query and a pool of N videos (up to 500):
1. **AV-RAG retrieval** computes cosine similarity between the query and per-video fused audio-visual embeddings (ImageBind, Hadamard fusion) plus caption embeddings (Gemini 1.5 Pro → ImageBind), averaging both scores to rank and select top-K videos.
2. **Salient Frame Selector (SFS)** selects k diverse frames from each retrieved video by minimizing pairwise audio-visual embedding similarity subject to a temporal-separation penalty (parameter γ), solved via dynamic programming.
3. **Parallel AVLLM agents:** One Qwen 2.5 Omni instance is dynamically spawned per retrieved video; each agent independently identifies relevant temporal segments and generates a partial response.
4. **Meta-agent aggregation:** GPT-4o ingests all per-agent outputs and synthesizes a coherent, temporally grounded, step-by-step final answer.

Fine-tuned (FT) variants use supervised training on the AVHaystacks train split (2,000 QA pairs); zero-shot (ZS) variants do not.

## Key Contributions
- **AVHaystacksQA task**: multi-video linkage and reasoning task where 82% of QA pairs require evidence from ≥2 distinct videos.
- **AVHaystacks benchmark**: 3,100 QA pairs (2k train / 1k test) drawn from 500 YouTube videos across 27 categories; average video duration 738 s; each answer includes ⟨videoID, start, end⟩ grounding references.
- **MAGNET framework**: model-agnostic, dynamically spawning per-video agents with a meta-agent aggregator; compatible with multiple AVLLM backbones.
- **STEM metric**: step-wise error metric using Hungarian matching to count missing steps, hallucinated steps, wrong order, and video-ID false positives/negatives + temporal IoU.
- **MTGS metric**: Matched Temporal Grounding Score — average temporal IoU computed only over video IDs present in both prediction and ground truth.

## Results
**Response alignment (AVHaystacks-Full, best open-source model: MAGNET+Qwen2.5Omni-FT):**
- BLEU@4: 55.82 vs. best baseline (VideoRAG) 41.59 — ~34% absolute gain
- CIDEr: 153.98 vs. 115.97
- GPT Eval: 7.84 vs. 6.32
- Human Eval: 4.15 vs. 3.42

**MAGNET+Gemini-1.5-Pro (closed-source upper bound):**
- BLEU@4: 57.67, GPT Eval: 8.03, MTGS: 0.81

**Retrieval (AVHaystacks-Full):**
- R@3: 73.15 vs. VideoRAG 70.43 (+2.7 pts)
- R@5: 79.20 vs. VideoRAG 74.96 (+4.2 pts)

**Ablations:**
- SFS vs. uniform sampling: +17 BLEU@4 points (36.58 → 53.61) for Qwen-FT
- Audio+Visual vs. visual-only: +14.65 BLEU@4 for Qwen-FT; audio-only underperforms visual-only

## Limitations
- Off-the-shelf components (ImageBind encoder, GPT-4o meta-agent) are not end-to-end trainable; retrieval and generation stages are decoupled.
- Evaluation currently limited to instructional/how-to video genres with synchronized audio; generalization to other domains is untested.
- Full AVHaystacks-Full results are only reported for ZS variants; FT results on the full split appear incomplete in the tables (only ZS rows show AVHaystacks-Full columns).
- Performance dip at γ=25 suggests sensitivity to the SFS penalty hyperparameter, with no principled selection criterion provided.
- No collaborative inter-agent mechanisms (e.g., voting, planning) — agents are fully independent before the meta-agent step.

## Relevance to Harnesses / Meta-Harnesses
MAGNET is a direct instantiation of the scatter-gather meta-harness pattern: a retrieval stage fans out work to dynamically spawned specialist agents (one per video), and a meta-agent (GPT-4o) reduces their outputs into a grounded final answer — exactly the orchestrator-worker topology central to meta-harness design. The paper concretizes how to handle variable fan-out (top-K retrieval controls agent count), inter-agent independence (no cross-agent communication), and synthesis (meta-agent ingests all partial responses as context). The SFS module illustrates a recurring harness sub-problem: intelligent input preprocessing to manage context budgets before dispatching to worker agents. STEM and MTGS also offer reusable evaluation primitives for multi-step, multi-source agent pipelines that need to measure grounding fidelity beyond text similarity.

## Tags
#multi-agent #meta-agent #rag #audio-visual #benchmark #temporal-grounding #video-qa #harness
