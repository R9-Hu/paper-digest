---
title: "Safety and accuracy follow different scaling laws in clinical large language models"
authors: ["Sebastian Wind", "Tri-Thien Nguyen", "Jeta Sopa", "Mahshad Lotfinia", "Sebastian Bickelhaup", "Michael Uder", "Harald K\u00f6stler", "Gerhard Wellein", "Sven Nebelung", "Daniel Truhn", "Andreas Maier", "Soroosh Tayebi Arasteh"]
source: "Arxiv"
venue: ""
published: "2026-05-05"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2605.04039"
url: "http://arxiv.org/abs/2605.04039v1"
pdf: "paper/med-foundation/[Arxiv 2026] Safety and accuracy follow different scaling laws in clinical large language models.pdf"
---

# Safety and accuracy follow different scaling laws in clinical large language models

## TL;DR
Clinical LLMs do not become safer simply by scaling model size, adding retrieval, or increasing inference-time compute. This paper introduces SaFE-Scale, a framework pairing a new radiology benchmark (RadSaFE-200) with option-level clinical safety labels, and demonstrates across 34 LLMs that evidence quality—not scale—is the dominant driver of safe clinical behavior. Safety and accuracy respond to different deployment levers and cannot be treated as a single axis.

## Problem
Existing clinical LLM evaluation treats all wrong answers as equivalent and reports mean accuracy as the primary endpoint. This masks clinically asymmetric failure modes—high-risk errors, unsafe answers, evidence contradictions, and dangerous overconfidence—which can matter far more than average accuracy. The implicit assumption that higher accuracy implies safer behavior is untested across the deployment axes actually used in practice (model size, retrieval strategy, context length, inference-time compute).

## Method
The authors construct **RadSaFE-200**, a 200-question multiple-choice radiology benchmark where each question includes: (1) clinician-written *clean evidence*, (2) clinician-written *conflict evidence* (one supporting, one distracting excerpt), and (3) option-level labels for high-risk error, unsafe answer, and evidence contradiction. They define four safety metrics—high-risk error rate, unsafe answer rate, contradiction rate, and dangerous overconfidence rate (requiring incorrectness + high-risk label + entropy-normalized confidence ≥ 0.80)—with accuracy as a secondary endpoint.

They evaluate **34 LLMs** (0.5B–685B parameters; Qwen, Llama, Gemma, MedGemma, DeepSeek, Mistral, OpenAI-OSS) across **six deployment conditions**: closed-book (zero-shot), clean evidence, conflict evidence, standard RAG (Radiopaedia top-k retrieval), agentic RAG (the RaR framework with multi-step query reformulation), and max-context prompting. Secondary experiments add 8-sample self-consistency on 8 models and fixed 3-model majority-vote ensembles (4 compositions). A two-way variance decomposition partitions metric variance into condition, model family, interaction, and residual components across the full 34 × 6 grid.

## Key Contributions
- **SaFE-Scale framework**: operationalizes measurement of clinical LLM safety across five deployment axes simultaneously.
- **RadSaFE-200 benchmark**: 200 radiology MCQs with clinician-defined clean/conflict evidence and per-option clinical safety labels; enables safety-differentiated (not just correctness-differentiated) evaluation.
- **Empirical decoupling of safety and accuracy**: shows the two metrics respond to different deployment levers and do not co-vary monotonically across the six conditions tested.
- **Variance decomposition**: quantifies that deployment condition explains ~43% of accuracy variance and ~45% of high-risk error variance, versus ~9% and ~8% for model family, respectively.
- **Ensemble synchronized failure analysis**: shows that most ensemble high-risk errors are unanimous and ensembles regress toward the member mean rather than the safest member.

## Results
- **Clean evidence vs. closed-book**: accuracy 73.5% → 94.1% (+20.6 pp); high-risk error 12.0% → 2.6%; contradiction 12.7% → 2.3%; dangerous overconfidence 8.0% → 1.6%. All 34/34 models improved on both accuracy and high-risk error.
- **Agentic RAG vs. standard RAG**: accuracy improved (76.0% → 78.1%) but dangerous overconfidence *increased* (5.7% → 8.0%) and high-risk error rose (9.6% → 10.3%); 15/34 models worsened on dangerous overconfidence.
- **Max-context prompting**: accuracy 74.0% (≈ closed-book baseline), latency increased from 18.0 s to 27.0 s; high-risk error 10.6%, dangerous overconfidence 6.0%—no safety gain.
- **Variance decomposition**: condition explains 43%, 45%, 38% of variance in accuracy, high-risk error, dangerous overconfidence; model family explains only 9%, 8%, 17%.
- **Self-consistency (8 samples)**: mean accuracy gain +0.39 pp, high-risk safety gain +0.27 pp, unsafe-answer safety gain +0.02 pp—all within noise; dangerous overconfidence under self-consistency reached 15.5 in some closed-book models.
- **Ensembles**: improved over 34-model panel average (closed-book: 83.0% accuracy, 7.4% high-risk) but mean change vs. best individual member was −0.88 pp accuracy, −0.79 pp high-risk safety; synchronized unanimous failures persisted.
- **Confidence as safety signal**: median confidence gap between correct and high-risk errors was well below 30 pp under all conditions; confidence on high-risk errors tracks confidence on correct answers near y = x.

## Limitations
- RadSaFE-200 is limited to 200 questions from radiology; generalizability to other clinical specialties or longer-form clinical tasks is not established.
- Conflict evidence contains only two excerpts per question; more complex or realistic retrieval noise may not be captured.
- Self-consistency was evaluated on only 8 of 34 models with 8 samples; larger sample counts or broader model coverage could shift results.
- Clean evidence is clinician-curated and idealized; operational RAG systems rarely produce evidence of equivalent quality, so the clean-evidence ceiling may be aspirational rather than achievable.
- Evaluation is text-only MCQ; radiology in practice is multimodal and the benchmark does not include images.
- The dangerous overconfidence metric requires repeated sampling and is undefined under single greedy decoding, limiting direct comparison across regimes.

## Relevance to Foundation Models in Medicine
This paper directly challenges a widely held assumption in medical foundation model deployment—that scaling (larger models, longer context, more compute) is a reliable proxy for safety—by demonstrating with 34 models across six conditions that evidence quality is the dominant determinant of clinical safety metrics. For researchers tracking medical foundation models, the finding that deployment condition accounts for ~5× more variance in high-risk error than model family has immediate practical implications: safety cannot be characterized from benchmark leaderboards alone and must be measured under the specific evidence and retrieval conditions of the target deployment. The introduction of RadSaFE-200 with per-option clinical safety labels also sets a methodological precedent for safety-differentiated benchmarking that complements accuracy-focused evaluations like MedQA or RadBench, and the SaFE-Scale framework is directly extensible to other modalities and specialties.

## Tags
#clinical-llm #safety #scaling-laws #rag #radiology #benchmark #inference-time-compute #evidence-quality
