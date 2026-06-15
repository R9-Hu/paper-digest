---
title: "A Vision-Language Foundation Model for Zero-shot Clinical Collaboration and Automated Concept Discovery in Dermatology"
authors: ["Siyuan Yan", "Xieji Li", "Dan Mo", "Philipp Tschandl", "Yiwen Jiang", "Zhonghua Wang", "Ming Hu", "Lie Ju", "Cristina Vico-Alonso", "Yizhen Zheng", "Jiahe Liu", "Juexiao Zhou", "Camilla Chello", "Jen G. Cheung", "Julien Anriot", "Luc Thomas", "Clare Primiero", "Gin Tan", "Aik Beng Ng", "Simon See", "Xiaoying Tang", "Albert Ip", "Xiaoyang Liao", "Adrian Bowling", "Martin Haskett", "Shuang Zhao", "Monika Janda", "H. Peter Soyer", "Victoria Mar", "Harald Kittler", "Zongyuan Ge"]
source: "Arxiv"
venue: ""
published: "2026-02-11"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2602.10624"
url: "http://arxiv.org/abs/2602.10624v1"
pdf: "paper/med-foundation/[Arxiv 2026] A Vision-Language Foundation Model for Zero-shot Clinical Collaboration and Automated Concept Discovery in Dermatology.pdf"
---

# A Vision-Language Foundation Model for Zero-shot Clinical Collaboration and Automated Concept Discovery in Dermatology

## TL;DR
DermFM-Zero is a dermatology vision-language foundation model trained on 4M+ multimodal data points via masked latent modelling and contrastive learning, enabling zero-shot clinical decision support without task-specific fine-tuning. Across 20 benchmarks and three multinational reader studies involving 1,100+ clinicians, it achieves state-of-the-art zero-shot performance and measurably improves clinical accuracy and management safety. Sparse autoencoders applied to its latent space automatically disentangle interpretable clinical concepts and enable targeted artifact-bias suppression without retraining.

## Problem
Medical foundation models require task-specific fine-tuning for each downstream clinical question, which is unscalable across the long tail of dermatological conditions. Existing domain-specific vision-language models (MONET, DermLIP) are limited in training scale and architecture diversity, and none have been rigorously evaluated in zero-shot human-AI collaborative workflows. Additionally, most models are black boxes, impeding clinical trust and failure-mode identification.

## Method
**Two-stage pretraining:** (1) Masked latent modelling on 3M unlabeled dermatological images to train the vision encoder on fine-grained morphology; (2) bootstrapped image-text contrastive learning on 1M curated image-text pairs (clinical photography, dermoscopy, mobile photos paired with demographics, medical history, diagnostic terminology, and symptom descriptions), aligned with PubMedBERT (extended token window) as the text encoder. Training data spans 400+ conditions across public (Derm1M, Edu) and private (MoleMap, 141 clinics) sources.

**Evaluation framework:** (1) Zero-shot and few-shot benchmarks across 7 public datasets; (2) three multinational reader studies (30 GPs for primary care; 1,090 clinicians for expert benchmarking; 34 specialists for collaborative workflow); (3) Sparse Autoencoder (SAE) "discover-then-name" interpretability applied to latent vision features, with Concept Bottleneck Models (CBMs) trained on auto-discovered neurons and targeted neuron suppression for artifact mitigation.

## Key Contributions
- Zero-shot dermatology VLM (304M parameters) pretrained on 4M+ multimodal data points, outperforming all prior domain-specific and general VLMs on 20 benchmarks without task-specific adaptation.
- First rigorous multinational zero-shot human-AI reader studies in dermatology (primary care n=30, specialist benchmarking n=1,090, specialist collaboration n=34).
- SAE-based automated clinical concept discovery that outperforms predefined expert-vocabulary CBMs (AUROC 0.939 vs. 0.765 for MONET baseline on melanoma prediction).
- Targeted concept-level artifact-neuron suppression achieving 12–38% AUROC improvement on ruler/pen/hair-occluded subsets without retraining.
- Demonstrated "skill-leveling" effect: AI-assisted non-experts surpass unassisted experts in both diagnostic accuracy and management appropriateness under zero-shot conditions.

## Results
- **Zero-shot classification:** HAM-10000 balanced accuracy 0.744, PAD-UFES balanced accuracy 0.743, exceeding next-best (DermLIP) by 23.7% and 23.2% respectively (P<0.001). SNU-134: 0.452; SD-128: 0.498, exceeding DermLIP by 22.3% and 20.9% (P<0.001). DAFFODIL-5 rare disease: 0.893, +15.6% over next-best (P<0.001). Average zero-shot classification 73.3% vs. DermLIP 56.1%.
- **Cross-modal retrieval:** Derm1M R@50 I2T: 0.601, T2I: 0.598, +32.3% over BiomedCLIP (P<0.001); SkinCap I2T: 0.623, T2I: 0.586, +23.8%/22.6% over MONET (P<0.001). Average R@50: 60.2% vs. MONET 31.9%.
- **Reader study 1 (primary care, n=30 GPs, 98 conditions):** Top-3 diagnostic accuracy 0.266→0.482 (+81%, P=0.004); mean diagnostic score 2.24→3.05 (P=0.006); appropriate management 0.504→0.592 (P=0.018); harmful decisions 0.400→0.341 (P=0.048).
- **Reader study 2A (n=1,090 clinicians):** DermFM-Zero diagnostic accuracy 0.717 vs. clinician average 0.663 (+5.4%, P<0.001); outperformed board-certified dermatologists (0.694) by 2.3% and GPs (0.596) by 12.1%; a fine-tuned ResNet50 baseline underperformed the clinician average by 9.6%.
- **Reader study 2B (n=34 specialists):** Overall accuracy 0.50→0.61 (P<0.001); management appropriateness 0.70→0.73 (P=0.010); non-expert accuracy 0.45→0.59 (P<0.001), surpassing unassisted expert performance (0.55).
- **SAE-CBM (melanoma):** AUROC 0.939 vs. predefined-vocabulary MONET CBM 0.765; vs. black-box DermFM-Zero linear probe 0.947.
- **Artifact suppression:** AUROC increases of 12–38% across ruler, purple pen, and hair-occlusion subsets by suppressing top-5 artifact-activating neurons.

## Limitations
- Reader studies are retrospective simulations; real-world workflow interruptions, time pressure, and EHR integration are not captured.
- Pretraining covers 400+ of 2,000+ dermatological entities; long-tail rare conditions underrepresented.
- Skin-tone fairness within the human-AI collaboration dynamic was not specifically analyzed despite geographically diverse pretraining data.
- Interpretable concept discovery and artifact intervention have not been tested within the reader study collaborative workflow; their direct effect on clinician trust and decision-making is unquantified.
- Human-AI collaboration matched but did not consistently exceed standalone AI performance, consistent with prior findings.

## Relevance to Foundation Models in Medicine
DermFM-Zero directly addresses the central challenge in medical FM deployment: eliminating task-specific fine-tuning while preserving—and here demonstrating—clinical utility in real collaborative settings. The multinational reader studies at scale (1,100+ clinicians) provide unusually rigorous evidence that zero-shot FM capability translates to measurable clinical benefit, establishing a methodological template for clinical validation of medical FMs beyond benchmark leaderboards. The SAE-based interpretability framework advances the field's ability to audit and correct FM behavior without retraining, addressing a key barrier to clinical trust. The finding that domain-specific pretraining (304M parameters) outperforms a 7B general-domain model underscores the representational efficiency of curated medical pretraining over parameter scaling.

## Tags
#dermatology #vision-language-model #zero-shot #contrastive-learning #interpretability #sparse-autoencoder #human-ai-collaboration #clinical-validation
