---
title: "A Nationwide Japanese Medical Claims Foundation Model: Balancing Model Scaling and Task-Specific Computational Efficiency"
authors: ["Nanae Aratake", "Taisei Tosaki", "Yuji Okamoto", "Eiichiro Uchino", "Masaki Nakamura", "Nobutomo Matsui", "Akiko Hatakama", "Yasushi Okuno"]
source: "Arxiv"
venue: ""
published: "2026-04-24"
published_time: "2026-04-24T08:32:47+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2604.22348"
url: "http://arxiv.org/abs/2604.22348v1"
pdf: "paper/med-foundation/[Arxiv 2026] A Nationwide Japanese Medical Claims Foundation Model Balancing Model Scaling and Task-Specific Computational Efficiency.pdf"
---

# A Nationwide Japanese Medical Claims Foundation Model: Balancing Model Scaling and Task-Specific Computational Efficiency

*🕒 **Published (v1):** 2026-04-24 08:32 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2604.22348v1)*

## TL;DR
This paper systematically investigates scaling laws for encoder-only Transformer foundation models pretrained on structured Japanese medical claims data (2.3M patients, 519-hospital nationwide database). It finds that downstream task performance saturates at task-dependent model sizes—disease prediction benefits from larger models (32M–101M parameters) while medication prediction saturates at 11M—challenging the "bigger is always better" paradigm in structured healthcare AI.

## Problem
Existing structured medical foundation models (BEHRT, Med-BERT, etc.) evaluate only a single, typically large, model scale, leaving the performance–compute tradeoff unexplored. It is also unclear whether NLP-style scaling laws apply to structured EHR data with limited vocabulary (~1,930 codes) and sparse, heterogeneous observations, or whether downstream task characteristics dictate optimal model capacity.

## Method
Five encoder-only BERT-style Transformers (2.2M, 4.7M, 11M, 32M, 101M parameters; hidden dimensions 128–2048, 4 layers, 16 attention heads) were pretrained via masked language modeling (MLM) on patient token sequences from the MDV Japanese DPC/claims database. Each token pairs an ICD-10 or YJ medication code with age-in-days; age is encoded using Piecewise Linear Encoding (PLE) mapped into the same embedding space as categorical codes. MLM loss is a sum of cross-entropy (diagnosis codes, medication codes) and MSE (age-in-days). Models were then independently fine-tuned for four one-year binary prediction tasks—two disease (primary hypertension I10, chronic kidney disease N189) and two medication (amlodipine, pregabalin)—under limited-label conditions (100/500/1,000 labeled patients, 1:1 class balance). A LightGBM model trained on count-based code-history features served as the structured-data baseline.

## Key Contributions
- First systematic multi-scale evaluation (5 sizes, 2.2M–101M) of encoder-only Transformers on structured medical claims data for downstream discriminative tasks.
- Demonstrates task-dependent saturation: disease prediction requires 32M–101M parameters; medication prediction saturates at 11M, reducing pretraining time by 76% (53.9 h vs. 232.2 h) with no AUPRC loss.
- Shows pretraining loss decreases monotonically with scale (consistent with NLP scaling laws) while downstream performance does not—confirming the two phenomena are decoupled for structured medical data.
- Task-optimal pretrained Transformers consistently outperform LGBM in AUPRC across all four tasks and all label-count conditions.
- Provides practical guidance: rule-governed tasks (medication initiation, driven by clinical guidelines) saturate early; biologically complex tasks (disease incidence) benefit from larger capacity.

## Results
- **Pretraining time**: 14.4 h (2.2M) → 53.9 h (11M) → 232.2 h (101M) on 16 NVIDIA GH200 nodes; test loss decreases monotonically from ~8.22 (2.2M) to ~5.74 (101M).
- **Disease prediction (hypertension, CKD)**: 32M or 101M models are optimal; pretrained models outperform LGBM in AUPRC across all label counts.
- **Medication prediction (amlodipine, pregabalin)**: 11M model is optimal; scaling to 101M (+178 h pretraining) yields no additional AUPRC gain.
- **Pretrained vs. from-scratch**: pretrained models generally outperform randomly initialized counterparts of identical architecture, with gains more pronounced in AUPRC than AUROC (reflecting clinical class imbalance of 2.63%–14.9% positive rates).
- **LGBM**: consistently beaten in AUPRC by the task-optimal pretrained Transformer at all fine-tuning set sizes.

## Limitations
- Claims/DPC data only; no laboratory values, vital signs, or clinical notes, which could enrich representations.
- 32 of 519 hospitals sampled; no guaranteed cross-facility longitudinal linkage, limiting generalizability to the full national database.
- Evaluation restricted to disease onset and medication initiation; other clinically relevant tasks (readmission, mortality) may show different scaling behavior.
- Single-dataset evaluation with no external validation or prospective study.
- Vocabulary is small (~936 ICD-10, ~994 YJ codes after filtering), which may itself impose an upper bound on capacity needs not seen in text-based models.

## Relevance to Foundation Models in Medicine
This work directly addresses a critical design question for structured EHR foundation models: how much to scale. By demonstrating that downstream utility saturates at task-dependent thresholds well below the largest tested size, it counters the tendency to adopt the largest available model by default and offers a principled framework for resource-efficient deployment. It also highlights a fundamental distinction between structured healthcare data (sparse, limited vocabulary, guideline-regularized) and free clinical text, suggesting that scaling intuitions from LLMs like GatorTron or Med-PaLM do not transfer directly. For researchers tracking medical foundation models, this paper provides actionable evidence that architecture type (discriminative vs. generative) and task regularity together determine the optimal compute budget—a design principle relevant to deploying foundation models under real clinical resource constraints.

## Tags
#structured-ehr #scaling-laws #claims-data #self-supervised-learning #clinical-risk-prediction #transformer #japan #computational-efficiency
