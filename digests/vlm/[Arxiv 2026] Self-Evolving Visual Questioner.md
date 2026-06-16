---
title: "Self-Evolving Visual Questioner"
authors: ["Yijun Liang", "Hengguang Zhou", "Ming Li", "Lichen Li", "Cho-Jui Hsieh", "Tianyi Zhou"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T21:45:46+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13929"
url: "http://arxiv.org/abs/2606.13929v1"
pdf: "paper/vlm/[Arxiv 2026] Self-Evolving Visual Questioner.pdf"
---

# Self-Evolving Visual Questioner

*🕒 **Published (v1):** 2026-06-11 21:45 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13929v1)*

## TL;DR
This paper proposes a self-evolving framework that enables a VLM to continuously improve its visual question generation (VQG) capability without any external supervision, human annotations, or teacher models. The model acts as both proposer and refiner through iterative rounds of question proposal, rewriting, and filtering on unlabeled images. After two self-evolution rounds, the average QG score improves ~82% relative to the base model while QA accuracy is preserved or slightly improved.

## Problem
Existing VQG methods are bottlenecked by static training data distributions — they rely on human annotations, curated datasets, or stronger external models, causing generated questions to cluster around repetitive templates, salient objects, and surface-level recognition. Simple self-training without explicit diversity and grounding controls leads to collapse toward narrow, low-information questions. There is no scalable, autonomous mechanism for a VLM to evolve its own questioning capability beyond the data distribution it was trained on.

## Method
The framework operates as a closed-loop iterative pipeline over an unlabeled image pool:

1. **Question Proposal**: The current model Mt generates K candidate questions per image under multiple visual intents (recognition, comparison, spatial relations, grounded reasoning) to encourage coverage diversity.
2. **Question Rewriting**: The fixed initial checkpoint M0 (not Mt) rewrites proposals along specified directions — visual inspection difficulty, evidence grounding, contextual reasoning, spatial reasoning — producing harder, more visual-centric candidates. Using M0 instead of Mt decouples proposal and rewriting distributions.
3. **Question Filtering**: A model-based filter retains candidates that are (a) visually answerable, (b) grounded in the image, and (c) strictly harder than their original proposals on perception or reasoning. Invalid, ambiguous, or non-improving candidates are discarded.
4. **Dual-Format Training**: Retained QA pairs are used in two supervision formats simultaneously — QG-format (image → question + answer) to strengthen question generation, and QA-format (image + question → answer) to anchor answering behavior. The trained Mt+1 becomes the proposer for the next round.

Evaluation uses an agentic protocol assessing five dimensions: Visual Search Difficulty, Visual Evidence Coverage, Visual Context Reasoning, Visual Spatial Reasoning, and Questioning Diversity (semantic distance among co-image questions via embedding model).

## Key Contributions
- Fully autonomous self-evolving VQG framework requiring no external teacher, reward model, or human annotation
- Proposal-rewriting-filtering mechanism that promotes diversity and prevents degeneration during recursive self-training
- Dual-format (QG+QA) training that improves question generation without sacrificing downstream answering performance
- Structured agentic evaluation protocol measuring fine-grained visual-centric questioning quality across perception, reasoning, and diversity dimensions
- Empirical evidence that higher-quality generated questions provide more informative supervision for downstream QA training

## Results
- **QG improvement**: ~82% relative increase in average QG score from base to second-round model
- **Qwen2.5-VL-3B**: QG avg 0.25 → 0.45 (first round) → 0.50 (second round); QA avg 60.49 → 62.26 → 62.56
- **Qwen2.5-VL-7B**: QG avg 0.26 → 0.47 → 0.51; QA avg 65.90 → 67.02 → 66.90
- **Qwen3VL-4B**: QG avg 0.36 → 0.54 → 0.57; QA avg 71.31 → 71.12 → 71.11
- Spatial reasoning dimension shows the largest absolute gains (e.g., 0.03 → 0.37 → 0.40 for 3B)
- Self-supervision data outperforms directly sampled original SAT annotations under the same 10K budget: QG avg 0.31 vs 0.45, QA avg 57.46 vs 62.26
- Improved-question training raises downstream QA avg from 61.90% to 63.32% (CVBench-3D: 69.25% → 75.58%)
- Ablation: full pipeline (rewrite + filter) outperforms rewrite-only across all dimensions; filtering alone adds +0.08 on Search, +0.03 on Coverage, +0.04 on Context, +0.08 on Spatial

## Limitations
- Filtering criteria cover only answerability and perception/reasoning difficulty; finer-grained criteria for grounding, ambiguity, and instructional value are absent
- Iterative proposal-rewriting-filtering-training loop introduces significant computational overhead versus direct training on existing QA data
- Evaluation is conducted on 100 held-out images from CVBench only, limiting generalization assessment
- The rewriting operator is fixed to M0 throughout all rounds, which may limit the range of question evolution in later iterations

## Relevance to Vision-Language Models
This work directly advances the understanding of VLMs as active visual agents rather than passive answerers, a capability gap that has received little systematic attention despite being central to interactive and agentic VLM deployment. The dual-format training result — that QG-format supervision improves question generation while QA-format preserves answering — is a practically important finding for instruction-tuning VLMs without capability regression. The closed-loop self-improvement paradigm connects to broader work on self-play and self-distillation in LLMs (e.g., self-rewarding models) but grounds it specifically in visual perception and grounding requirements. The introduced evaluation protocol (perception, reasoning, diversity dimensions) also provides a reusable framework for assessing any VLM's questioning capability beyond aggregate accuracy metrics.

## Tags
#vlm #visual-question-generation #self-improvement #instruction-tuning #visual-grounding #self-supervised #agentic-evaluation #multimodal-reasoning
