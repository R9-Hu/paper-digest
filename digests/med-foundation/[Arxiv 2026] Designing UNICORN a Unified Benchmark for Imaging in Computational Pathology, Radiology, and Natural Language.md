---
title: "Designing UNICORN: a Unified Benchmark for Imaging in Computational Pathology, Radiology, and Natural Language"
authors: ["Michelle Stegeman", "Lena Philipp", "Fennie van der Graaf", "Marina D'Amato", "Cl\u00e9ment Grisi", "Luc Builtjes", "Joeran S. Bosma", "Judith Lefkes", "Rianne A. Weber", "James A. Meakin", "Thomas Koopman", "Anne Mickan", "Mathias Prokop", "Ewoud J. Smit", "Geert Litjens", "Jeroen van der Laak", "Bram van Ginneken", "Maarten de Rooij", "Henkjan Huisman", "Colin Jacobs", "Francesco Ciompi", "Alessa Hering"]
source: "Arxiv"
venue: ""
published: "2026-03-03"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2603.02790"
url: "http://arxiv.org/abs/2603.02790v1"
pdf: "paper/med-foundation/[Arxiv 2026] Designing UNICORN a Unified Benchmark for Imaging in Computational Pathology, Radiology, and Natural Language.pdf"
---

# Designing UNICORN: a Unified Benchmark for Imaging in Computational Pathology, Radiology, and Natural Language

## TL;DR
UNICORN is the first unified public benchmark for evaluating medical foundation models simultaneously across radiology, digital pathology, and clinical text, spanning 20 tasks under a single standardized protocol. It introduces a two-step evaluation framework that decouples frozen encoder inference from lightweight few-shot adaptation, isolating representation quality. A new aggregate metric—the UNICORN Score—enables direct cross-model, cross-domain comparison.

## Problem
Existing medical AI benchmarks are fragmented by task, organ, or modality, making it impossible to assess cross-domain generalization of foundation models under a consistent protocol. Evaluation data are rarely sequestered, enabling leakage, and heterogeneous metrics across benchmarks preclude fair comparison. No single public framework covers the full breadth of tasks (vision, language, vision-language) that a general medical foundation model must handle.

## Method
UNICORN is hosted on Grand Challenge and enforces a containerized two-step pipeline. **Step 1 (Algorithm container):** the submitter's foundation model extracts generic representations from each case (patch-level for dense tasks, case-level for classification/regression) without internet access. **Step 2 (Evaluation container, organizer-controlled):** lightweight adaptors (k-NN to small learned heads) trained on 48 labeled few-shot examples per task transform representations into task-specific predictions; pretrained weights are disallowed in adaptors. For language tasks, the algorithm outputs predictions directly; for vision-language, the model generates text given the task description. All test labels are sequestered. Performance per task is normalized as `(S − S_ref) / (S_max − S_ref)` anchored at a trivial baseline, then averaged equally across all 20 tasks into the **UNICORN Score**. Domain-specific sub-scores (pathology-vision, radiology-vision, language) are computed analogously.

## Key Contributions
- First unified benchmark evaluating medical foundation models across radiology, pathology, and clinical language under one protocol and leaderboard.
- 20 clinically motivated tasks (8 classification, 4 detection, 3 regression, 3 segmentation, 1 NER, 1 caption generation) covering 8 anatomical regions and 4 imaging modalities.
- Novel UNICORN Score: normalized, task-equally-weighted aggregate metric enabling single-number cross-model comparison despite heterogeneous per-task metrics (Dice, AUROC, c-index, BLEU-4, etc.).
- Strictly sequestered test sets from 2,400+ patients across 17 institutions in 8 countries (3,700+ vision cases, 2,400+ clinical reports), preventing data leakage.
- Open-source adaptor repository and public evaluation code promoting reproducibility; baseline implementation achieves UNICORN Score 0.378.

## Results
- Baseline model (publicly available foundation models + lightweight adaptors) achieves a **UNICORN Score of 0.378** across all 20 tasks.
- No per-task breakdown for submitted models is reported in this paper (benchmark description paper; leaderboard results are hosted externally at unicorn.grand-challenge.org).
- Benchmark engagement: 270+ researchers across 6 continents participated.
- Dataset scale: >2,400 patients, >3,700 vision cases, >2,400 clinical reports from 17 institutions, 8 countries.

## Limitations
- Most test data sourced from a single academic center (Radboud UMC), limiting assessment of cross-scanner and cross-institution generalization.
- Case-level classification/regression tasks require a single vector representation per case, excluding models that depend on dense patch-level prediction heads at inference time.
- Pretrained decoders are disallowed, preventing submission of state-of-the-art task-specific models in their original form.
- Submission caps (6 per task in validation, 1 in test) and per-case execution time limits exclude computationally expensive architectures.
- No direct comparison to task-specific supervised baselines within the framework yet; prior challenge-winning models have not been re-evaluated under UNICORN.
- Only few-shot (48-example) adaptation is assessed; full fine-tuning regimes are out of scope by design.

## Relevance to Foundation Models in Medicine
UNICORN directly addresses the evaluation bottleneck for medical foundation models by providing the first benchmark where a single frozen encoder can be scored across 20 heterogeneous clinical tasks via standardized few-shot adaptation—the paradigm these models are actually intended for. The UNICORN Score gives the community a concrete, comparable signal for generalization quality that existing fragmented benchmarks (UNI, Phikon, CT-FM, CONCH evaluations) cannot provide. For researchers tracking medical foundation models, this benchmark establishes the reference infrastructure needed to distinguish genuinely general representations from task-overfitted ones, and its extensible design means new modalities and tasks can be added as the field matures.

## Tags
#benchmark #evaluation #foundation-model #few-shot #radiology #pathology #vision-language #multi-task
