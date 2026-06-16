---
title: "ReportQA: QA-Based Radiology Report Evaluation"
authors: ["Yiming Shi", "Shaoshuai Yang", "Xi Chen", "Haolin Li", "Hengyu Zhang", "Che Jiang", "Kaiwen Wang", "Xun Zhu", "Dong Xie", "Fei Wang", "Dejing Dou", "Miao Li", "Ji Wu"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T00:43:03+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15037"
url: "http://arxiv.org/abs/2606.15037v1"
pdf: "paper/vlm/[Arxiv 2026] ReportQA QA-Based Radiology Report Evaluation.pdf"
---

# ReportQA: QA-Based Radiology Report Evaluation

*🕒 **Published (v1):** 2026-06-13 00:43 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15037v1)*

## TL;DR
ReportQA is a QA-based radiology report evaluation framework that constructs ~660K clinically grounded QA pairs from structured knowledge trees across four multi-modal datasets. It introduces QAScore, an aggregated metric that outperforms all existing automatic metrics (BLEU, CheXbert, GREEN, RaTEScore) in correlation with radiologist error annotations. Benchmarking of SOTA VLMs reveals that report-based SFT paradigms fail to learn fine-grained clinical attributes and exhibit strong negative prior bias, while question-driven inference is a more promising alternative.

## Problem
Existing radiology report evaluation metrics either rely on surface-level lexical overlap (BLEU, ROUGE) or coarse-grained entity presence detection (CheXbert, RadGraph). Neither captures fine-grained clinical attributes (location, shape, margin, chronicity) nor scales easily to new entities without expensive manual annotation. This limits meaningful feedback for radiology report generation (RRG) systems.

## Method
**Pipeline overview:**
1. **Dataset collection**: Free-form radiology reports from four datasets spanning 2D (MIMIC-CXR chest X-ray) and 3D CT (CTRG-Brain, CT-RATE, AMOS-MM).
2. **Structured extraction**: Radiologists define per-dataset knowledge trees covering clinical entities (findings/diagnoses) and 15 attribute dimensions (presence, location, shape, margin, etc.). DeepSeek-V3.2 extracts structured JSON from free-form reports via two-stage LLM prompting with knowledge-tree remapping.
3. **QA generation**: Template-based construction of three QA types: *base* (leaf-level entity-attribute pairs), *hierarchical* (ancestor-level, ontology-aware), and *negative* (absent entities, with "Insufficient information" option). Two-stage LLM filtering: self-filter (removes context-independent answerable QAs) then report-based filter (removes low-accuracy QAs against ground-truth).
4. **Evaluation**: A local judge model (Qwen3.5-27B via vLLM) answers filtered QAs using the generated report as context. **QAScore** = harmonic mean of Scorepos (accuracy on base+hierarchical questions, with cascading penalty if presence is wrong) and Scoreneg (exponential penalty on false positive rate for absent-entity questions).

## Key Contributions
- ReportQA framework producing ~660K QA pairs (~100/report) across 4 radiology datasets and multiple modalities.
- QAScore metric achieving strongest correlation with radiologist judgments (Pearson 0.4507, Spearman 0.4612, Kendall 0.3910) vs. all prior metrics including GREEN.
- Empirical finding that report-based SFT improves coarse-grained (hierarchical) but not fine-grained (leaf-level) entity understanding in VLMs.
- Empirical finding that report-based inference induces strong negative prior bias, while question-driven inference exhibits milder and more correctable positive bias.
- Public release of knowledge trees, structured reports, QA pairs, and pipeline code.

## Results
- **Metric alignment (RadEvalX, 100 chest X-ray report pairs):** QAScore Pearson |0.4507| > GREEN |0.4194| > CheXbert |0.3870| > RaTEScore |0.3539| > BERTScore |0.2575|; same ordering for Spearman and Kendall.
- **VLM benchmarking (Table 3):** GPT-5.4 tops overall (e.g., CTRG-Brain 0.4536, MIMIC-CXR 0.6126); proprietary VLMs consistently outperform open-source across datasets.
- **Modality gap:** MIMIC-CXR (2D) yields highest scores across all models; AMOS-MM (3D abdomen) yields lowest, reflecting training data scarcity for 3D CT.
- **Attribute difficulty:** Presence easiest (highest median accuracy); margin, chronicity, enhancement near zero for most models.
- **Report-based SFT vs. question-driven (Qwen3.5-2B on CTRG-Brain):** Question-driven zero-shot matches SFT on leaf-level questions; SFT only outperforms on hierarchical (coarser) questions.
- **Judge model scaling:** Qwen3.5 27B achieves near-perfect QAScore (~0.98) on ground-truth reports; 4B/9B exceed 0.95 with feasible GPU cost; 0.8B reaches only ~0.70.

## Limitations
- QAScore quality depends on the judge model's capacity; smaller models (<4B) degrade notably, creating a compute dependency for evaluation.
- Knowledge trees are dataset-specific and require radiologist involvement to construct; extension to new datasets is not zero-cost.
- QA generation uses LLMs (DeepSeek-V3.2) which may introduce extraction noise; structured reports and QAs are not perfectly error-free.
- Evaluation is restricted to the textual report as context; image-grounded evaluation (checking whether the report faithfully reflects the image) is not directly measured.
- 3D volume preprocessing (downsampled to 16 slices) may disadvantage models with native 3D support.

## Relevance to Vision-Language Models
ReportQA directly benchmarks SOTA VLMs (GPT-5.4, Gemini, Claude Opus, InternVL, Qwen, MedGemma, RadFM) on fine-grained clinical understanding, revealing that current VLMs—even proprietary ones—struggle with 3D medical imaging and fine-grained attribute prediction (margin, chronicity, enhancement). The finding that report-based SFT does not improve leaf-level entity perception, while question-driven VQA-style inference does, has direct implications for how VLMs should be trained and prompted for medical tasks. The "mirage reasoning" phenomenon—where removing the image sometimes improves scores due to textual prior dominance—is an important failure mode for the VLM community to address in multimodal grounding research.

## Tags
#vlm #medical-imaging #radiology #evaluation-metric #vqa #report-generation #benchmark #fine-grained-understanding
