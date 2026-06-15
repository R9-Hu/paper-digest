---
title: "Project Imaging-X: A Survey of 1000+ Open-Access Medical Imaging Datasets for Foundation Model Development"
authors: ["Zhongying Deng", "Cheng Tang", "Ziyan Huang", "Jiashi Lin", "Ying Chen", "Junzhi Ning", "Chenglong Ma", "Jiyao Liu", "Wei Li", "Yinghao Zhu", "Shujian Gao", "Yanyan Huang", "Sibo Ju", "Yanzhou Su", "Pengcheng Chen", "Wenhao Tang", "Tianbin Li", "Haoyu Wang", "Yuanfeng Ji", "Hui Sun", "Shaobo Min", "Liang Peng", "Feilong Tang", "Haochen Xue", "Rulin Zhou", "Chaoyang Zhang", "Wenjie Li", "Shaohao Rui", "Weijie Ma", "Xingyue Zhao", "Yibin Wang", "Kun Yuan", "Zhaohui Lu", "Shujun Wang", "Jinjie Wei", "Lihao Liu", "Dingkang Yang", "Lin Wang", "Yulong Li", "Haolin Yang", "Yiqing Shen", "Lequan Yu", "Xiaowei Hu", "Yun Gu", "Yicheng Wu", "Benyou Wang", "Minghui Zhang", "Angelica I. Aviles-Rivero", "Qi Gao", "Hongming Shan", "Xiaoyu Ren", "Fang Yan", "Hongyu Zhou", "Haodong Duan", "Maosong Cao", "Shanshan Wang", "Bin Fu", "Xiaomeng Li", "Zhi Hou", "Chunfeng Song", "Lei Bai", "Yuan Cheng", "Yuandong Pu", "Xiang Li", "Wenhai Wang", "Hao Chen", "Jiaxin Zhuang", "Songyang Zhang", "Huiguang He", "Mengzhang Li", "Bohan Zhuang", "Zhian Bai", "Rongshan Yu", "Liansheng Wang", "Yukun Zhou", "Xiaosong Wang", "Xin Guo", "Guanbin Li", "Xiangru Lin", "Dakai Jin", "Mianxin Liu", "Wenlong Zhang", "Qi Qin", "Conghui He", "Yuqiang Li", "Ye Luo", "Nanqing Dong", "Jie Xu", "Wenqi Shao", "Bo Zhang", "Qiujuan Yan", "Yihao Liu", "Jun Ma", "Zhi Lu", "Yuewen Cao", "Zongwei Zhou", "Jianming Liang", "Shixiang Tang", "Qi Duan", "Dongzhan Zhou", "Chen Jiang", "Yuyin Zhou", "Yanwu Xu", "Jiancheng Yang", "Shaoting Zhang", "Xiaohong Liu", "Siqi Luo", "Yi Xin", "Chaoyu Liu", "Haochen Wen", "Xin Chen", "Alejandro Lozano", "Min Woo Sun", "Yuhui Zhang", "Yue Yao", "Xiaoxiao Sun", "Serena Yeung-Levy", "Xia Li", "Jing Ke", "Chunhui Zhang", "Zongyuan Ge", "Ming Hu", "Jin Ye", "Zhifeng Li", "Yirong Chen", "Yu Qiao", "Junjun He"]
source: "Arxiv"
venue: ""
published: "2026-03-29"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2603.27460"
url: "http://arxiv.org/abs/2603.27460v1"
pdf: "paper/med-foundation/[Arxiv 2026] Project Imaging-X A Survey of 1000+ Open-Access Medical Imaging Datasets for Foundation Model Development.pdf"
---

# Project Imaging-X: A Survey of 1000+ Open-Access Medical Imaging Datasets for Foundation Model Development

## TL;DR
This paper presents the largest survey to date of 1,000+ open-access medical imaging datasets (2000–2025), cataloging them by modality, task, anatomy, and dimensionality. It exposes a fragmented, long-tailed landscape that severely limits medical foundation model development, and proposes a Metadata-Driven Fusion Paradigm (MDFP) alongside an interactive discovery portal to consolidate disparate datasets into larger, coherent training corpora.

## Problem
Medical imaging datasets are orders of magnitude smaller and more fragmented than natural image corpora (billions of images; trillions of NLP tokens), yet current foundation models require scale and diversity. Public medical datasets are siloed across narrowly scoped tasks, skewed toward a few modalities (CT, MRI) and anatomies (brain, lung), and lack a unifying framework for integration—causing existing dataset fusion efforts to reinforce existing biases rather than enabling balanced, general-purpose pre-training.

## Method
The authors systematically collect 1,000+ open-access datasets from repositories (TCIA, Grand Challenge, etc.) spanning 2000–2025, applying deduplication, manual license verification, and metadata normalization. A four-tier taxonomy (dimensionality → modality → task → anatomy) organizes the corpus. Gap analysis quantifies under-representation across these axes. The MDFP pipeline then operates in four phases: (1) **Metadata Harmonization** — standardizing heterogeneous schema fields; (2) **Semantic Alignment** — mapping native labels to shared medical vocabularies; (3) **Fusion Blueprints** — generating goal-conditioned merge plans (e.g., by shared modality or target anatomy/disease); (4) **Dataset Indexing & Community Sharing** — publishing through an interactive portal that supports fine-grained search, statistical analysis, and automated integration.

## Key Contributions
- Comprehensive catalog of 1,000+ open-access medical imaging datasets with standardized metadata covering modality, task, anatomy, label type, and image count.
- Metadata-Driven Fusion Paradigm (MDFP): a four-phase systematic workflow to aggregate fragmented public datasets into larger, task-coherent training resources.
- Interactive discovery portal enabling end-to-end automated dataset search, filtering, and fusion blueprint generation.
- Quantitative gap analysis identifying underrepresented modalities (PET, mammography, endoscopy), anatomies (foot, bowel, shoulder, heart), and tasks (registration, tracking, reconstruction, VQA).
- Released Python toolkit, structured dataset table with reference links, and a merged large-scale dataset for public use.

## Results
- 502 labeled 2D datasets (≈1.4 M CT slices alone); 3D volumetric and video datasets are substantially fewer and grow more slowly.
- Pathology and X-ray numerically dominate 2D image counts; CT, pathology, and MRI account for the majority pre-2023; post-2023 growth concentrated in pathology, X-ray, fundus, and microscopy.
- Classification and segmentation collectively constitute the largest task shares; registration, detection, tracking, and VQA are severely underrepresented.
- Brain, lung, liver, and breast are the most represented anatomies; foot, blood, heart, bowel, shoulder, humerus, and forearm remain critically underrepresented.
- Largest individual datasets: AbdomenAtlas (1.5 M 2D CT images, 5,195 3D CT volumes); CT-RATE (25,692 3D chest CT volumes from 21,304 patients).
- Medical foundation models are trained on millions of images; general-domain counterparts use billions of natural images—a gap that naïve concatenation of existing public datasets cannot close.

## Limitations
- Restricted to open-access datasets; large proprietary clinical datasets (e.g., hospital EHR-linked imaging) are excluded, potentially underrepresenting clinical diversity.
- Scale gap vs. natural image/NLP corpora persists even after MDFP fusion; no empirical benchmark demonstrates downstream FM improvement from MDFP-fused data.
- Annotation heterogeneity across datasets (varying label granularity, protocols, and quality) is described but not quantitatively assessed.
- Multimodal (cross-modality paired) datasets remain scarce, limiting multi-modal FM pre-training even with MDFP.
- Taxonomy granularity is deliberately coarsened for comparability; finer anatomical sub-structures are unevenly annotated across sources.

## Relevance to Foundation Models in Medicine
This survey directly addresses the data-scarcity bottleneck that most constrains medical FM development, providing the community's first comprehensive map of where public training data exists, where it is absent, and how to systematically close gaps through principled fusion rather than ad-hoc aggregation. The MDFP framework operationalizes dataset integration in a way that is modality- and task-aware, making it immediately applicable to building more balanced pre-training corpora for multi-modal, multi-task medical FMs. The gap analysis serves as a roadmap for targeted dataset curation and reveals which clinical domains (rare modalities, under-imaged anatomies, temporal/tracking tasks) remain bottlenecks for generalist medical AI.

## Tags
#survey #medical-imaging #dataset #data-curation #foundation-model #dataset-fusion #benchmark #open-access
