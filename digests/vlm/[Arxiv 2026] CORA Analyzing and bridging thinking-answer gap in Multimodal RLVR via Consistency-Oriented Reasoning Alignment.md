---
title: "CORA: Analyzing and bridging thinking-answer gap in Multimodal RLVR via Consistency-Oriented Reasoning Alignment"
authors: ["Jiayue Cao", "Zhicong Lu", "Xuehan Sun", "Wei Jia", "Hongling Zheng", "Changyuan Tian", "Zichuan Lin", "Wenqian Lv", "Nayu Liu"]
source: "Arxiv"
venue: "EMNLP 2026"
published: "2026-06-12"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14691"
url: "http://arxiv.org/abs/2606.14691v1"
pdf: "paper/vlm/[Arxiv 2026] CORA Analyzing and bridging thinking-answer gap in Multimodal RLVR via Consistency-Oriented Reasoning Alignment.pdf"
---

# CORA: Analyzing and bridging thinking-answer gap in Multimodal RLVR via Consistency-Oriented Reasoning Alignment

## TL;DR
Multimodal RLVR training with answer-level rewards produces reasoning traces that are semantically inconsistent with final answers — a persistent problem GRPO does not fix on its own. CORA addresses this by adding a lightweight ModernBERT-based Consistency Reward Model (CRM) scoring thinking-answer alignment via NLI, plus Hybrid Reward Advantage Splitting (HRAS) to prevent the consistency signal from interfering with accuracy optimization. The result is simultaneously lower inconsistency rates and higher accuracy across four Qwen-VL backbones.

## Problem
Standard RLVR for LVLMs (e.g., GRPO with answer-correctness rewards) supervises only the final answer, leaving the thinking process under-supervised. This causes **thinking-answer inconsistency**: the reasoning trace either fails to support or actively contradicts the final answer. Empirical analysis of ~719K rollouts shows this inconsistency is widespread, task-dependent (worse on math and puzzle tasks), and does *not* diminish as GRPO training progresses — it often worsens. Concurrent works address it only heuristically or require expensive LLM-judge calls at training time.

## Method
**Consistency Reward Model (CRM):** Offline, training-stage rollouts are labeled for thinking-answer consistency using GPT-5 as judge. This yields ~90K NLI-style premise-hypothesis pairs (premise = question + thinking; hypothesis = "The final answer is {a}"). ModernBERT-large is fine-tuned on this dataset as a lightweight binary discriminator (consistent / inconsistent). The CRM is then frozen and used online during GRPO rollouts to produce a continuous consistency reward: `r_cons = λ_cons · P(consistent | q, t, a)`.

**Hybrid Reward Advantage Splitting (HRAS):** Rather than summing all reward components before group-wise normalization (which lets the continuous CRM signal dominate the sparse accuracy signal), HRAS normalizes task rewards (accuracy + format) and consistency rewards *separately* within each response group, then composes the two advantages with learnable weights α and β: `A = α·A_task + β·A_cons`. Scheduling strategies (warmup, decay) modulate the consistency reward weight across training.

## Key Contributions
- Systematic empirical characterization of thinking-answer inconsistency across GRPO training dynamics (early/middle/late) and post-training evaluation, covering spatial, math, and puzzle reasoning tasks with four Qwen-VL models.
- CRM: a plug-and-play, NLI-framed ModernBERT discriminator trained offline on ~90K annotated rollouts, lightweight enough for online use during RL.
- HRAS: reward-decoupled advantage estimation that prevents the continuous consistency reward from crowding out the discrete accuracy reward under group-wise normalization.
- Demonstration that reduced inconsistency correlates with improved final-answer accuracy, supporting the claim that faithful reasoning causally helps task performance.

## Results
Against standard GRPO baseline on five benchmarks (CVBench, MathVision, MathVista, PuzzleVQA, AlgoPuzzleVQA) with four backbones (Qwen2-VL-2B/7B, Qwen2.5-VL-3B/7B):

- **Qwen2.5-VL-7B:** MathVista accuracy 67.90 → 69.30; MathVision IR 15.80 → 8.28; AlgoPuzzleVQA IR 12.54 → 2.50.
- **Qwen2-VL-7B:** PuzzleVQA accuracy 30.21 → 5.03 IR reduction (from 77.00 to 81.95 accuracy); AlgoPuzzleVQA IR drops from 16.46 to 5.31.
- **Qwen2-VL-2B:** CVBench IR drops from 74.90 to 55.46; PuzzleVQA accuracy 51.10 → 63.35.
- Gains are more pronounced on 7B models and on benchmarks requiring deeper multi-step reasoning (MathVision, AlgoPuzzleVQA).
- Ablation (Qwen2.5-VL-7B): removing CRM degrades accuracy and raises IR; removing HRAS reduces accuracy while sometimes over-suppressing inconsistency, confirming both components are necessary.
- CORA increases Consistent-Correct samples on MathVision (+6.38 pp CC, −29.47 pp IW) and PuzzleVQA (+11.00 pp CC, −10.05 pp IC).

## Limitations
- Evaluated only on models ≤7B parameters; scalability to larger models is untested.
- Restricted to static image-text inputs; video and higher-dimensional multimodal inputs are not considered.
- CRM is trained offline from rollouts of specific task domains; out-of-distribution generalization of the discriminator is not characterized.
- Consistency labeling (and hence CRM training data quality) depends on GPT-5 as judge, introducing cost and potential annotation bias.

## Relevance to Vision-Language Models
CORA directly targets a structural weakness in how RLVR is applied to LVLMs: answer-level rewards do not align the chain-of-thought with the final prediction, undermining trustworthiness of reasoning even when accuracy improves. For researchers tracking VLMs, this is a concrete step toward *process-faithful* reward design — complementary to grounded CoT and visual hallucination work. The NLI-framed CRM is a general-purpose, lightweight plug-in that could be applied to any GRPO-trained LVLM without modifying the base reward structure, making it practically relevant for the broader multimodal reasoning fine-tuning ecosystem.

## Tags
#vlm #rlvr #grpo #chain-of-thought #reward-modeling #multimodal-reasoning #consistency #nli
