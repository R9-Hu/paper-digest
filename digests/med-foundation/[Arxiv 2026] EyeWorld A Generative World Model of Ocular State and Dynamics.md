---
title: "EyeWorld: A Generative World Model of Ocular State and Dynamics"
authors: ["Ziyu Gao", "Xinyuan Wu", "Xiaolan Chen", "Zhuoran Liu", "Ruoyu Chen", "Bowen Liu", "Bingjie Yan", "Zhenhan Wang", "Kai Jin", "Jiancheng Yang", "Yih Chung Tham", "Mingguang He", "Danli Shi"]
source: "Arxiv"
venue: ""
published: "2026-03-14"
published_time: "2026-03-14T17:19:57+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2603.14039"
url: "http://arxiv.org/abs/2603.14039v1"
pdf: "paper/med-foundation/[Arxiv 2026] EyeWorld A Generative World Model of Ocular State and Dynamics.pdf"
---

# EyeWorld: A Generative World Model of Ocular State and Dynamics

*🕒 **Published (v1):** 2026-03-14 17:19 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2603.14039v1)*

## TL;DR
EyeWorld is a generative world model that represents the eye as a partially observed dynamical system, learning a single observation-stable latent ocular state shared across seven ophthalmic imaging modalities. It unifies segmentation, cross-modality translation, quality enhancement, and longitudinal disease-progression forecasting within one framework. By adding time-conditioned state transitions via longitudinal supervision, it moves beyond static representation learning to explicit disease dynamics modeling.

## Problem
Existing ophthalmic AI systems are narrow and static: each is trained for a single task, modality, or dataset and cannot reason across modalities or time. Medical foundation models improve generalization but remain representation-centric—they treat images as independent observations, are sensitive to modality/acquisition shifts, and cannot model disease progression as an evolving dynamical process. No prior unified, multimodal, longitudinal model exists for ophthalmic disease.

## Method
EyeWorld is initialized from the OmniGen2 backbone and restructured into a domain-specific world model with two explicit objectives: (i) an observation-stable latent ocular state learned from simultaneous supervision across modalities (CFP, FFA, ICGA, OCT, MRI, AF, UWF), and (ii) time-conditioned latent state transitions learned from 16,645 longitudinal examinations. A dual-path language-vision encoder tokenizes multimodal images and free-form text prompts into a shared latent space; an "Ophthalmic World Simulator" operates on this latent state; a unified generative projection head decodes it into segmentation masks, translated images, enhanced images, or future-state predictions depending on the prompt. Coarse-to-fine training jointly preserves global vascular topology and fine lesion boundaries. For longitudinal tasks, patient metadata (age, sex) and follow-up interval are included as conditioning. An exemplar-based conditioning mode additionally allows task inference from a reference input–output pair without task-specific reconfiguration.

## Key Contributions
- Generative world-model formulation for ophthalmology: shared latent ocular state across seven modalities with explicit time-conditioned state transitions.
- Single framework supporting fine-grained segmentation (60 tasks, 29 anatomical structures, 25 lesion types), bounding-box detection (14 tasks), cross-modality translation (18 directions), quality enhancement (4 types), and longitudinal progression forecasting—no task-specific architectural branches.
- Large-scale multimodal dataset: 108,672 images; 85,638 image-mask pairs; 31,179 paired cross-modality samples; 16,645 longitudinal examinations.
- Counterfactual progression synthesis that selectively perturbs pathological factors while preserving uninvolved anatomy, probing whether the model captures disease mechanisms rather than appearance.
- Exemplar-conditioned inference: task specification via a visual before–after demonstration pair, enabling zero-shot adaptation to infrequent targets without retraining.

## Results
**Segmentation (60 tasks, multimodal):**
- EyeWorld mean Dice 0.77 vs. Step1X-Edit 0.52, ChronoEdit 0.61, OmniGen2 0.64, Qwen-Image 0.69.
- Anatomical structures Dice 0.84, lesions Dice 0.66; strongest baseline 0.76 / 0.58.
- CFP anatomical Dice 0.858 (+8.72% over OmniGen2); CFP lesion Dice 0.71 (+5% over Qwen-Image; all p < 0.05).
- Ambiguous boundary setting (optic disc/cup): Dice 0.865, mIoU 0.764 vs. OmniGen2 0.778 / —.

**Detection (14 tasks):**
- EyeWorld: 4 tasks with mean IoU > 0.7 vs. 3 (OmniGen2), 1 (ChronoEdit), 1 (Qwen-Image), 0 (Step1X-Edit).
- EyeWorld reduced tasks with IoU < 0.5 to 6 vs. 7–10 for baselines.

**Cross-modality translation (18 directions):**
- Lowest LPIPS, highest PSNR/SSIM distributions across all baselines.
- IS improvement: +4.05% (CFP→FFA), +8.12% (ICGA→CFP) over strongest baseline; consistently lower PID.

**Quality enhancement:**
- LPIPS: 0.142 (combined degradation), 0.170 (super-resolution), 0.215 (inpainting), 0.301 (outpainting)—lowest across all four categories.
- Combined degradation margin over best baseline: 0.208–0.265 LPIPS reduction.

**Robustness under degraded input:**
- Segmentation Dice on degraded images: EyeWorld 0.722 vs. OmniGen2 0.623 (best baseline).
- Enhance-then-analyse raised EyeWorld slightly (0.722→0.731) while decreasing all baselines.

**Longitudinal progression forecasting (AMD + macular hole OCT):**
- LPIPS 0.371, SSIM 0.651, PSNR 21.462; exceeds best baseline by 2.3% LPIPS, 6.1% SSIM, 2.278 dB PSNR.

**Exemplar-conditioned inference:**
- Segmentation Dice: CFP 0.79, ICGA 0.76, OCT 0.60, FFA 0.56, MRI 0.53.
- Detection IoU 0.73; SSIM for translation 0.60, quality enhancement 0.77, longitudinal prediction 0.55.

## Limitations
- Class imbalance noted (text truncated before full elaboration).
- Evaluation against general-purpose instruction-following models rather than task-specialized ophthalmic baselines, which may underrepresent the ceiling of prior specialized systems.
- Longitudinal prediction evaluated only on OCT (AMD and macular hole), not across all seven modalities.
- Counterfactual progression synthesis is qualitative; no downstream clinical validity (e.g., Kaplan–Meier concordance or physician grading study) reported.
- Generalizability beyond the curated internal dataset to heterogeneous real-world scanner populations is not directly tested.

## Relevance to Foundation Models in Medicine
EyeWorld directly addresses a recognized limitation of medical foundation models—their reliance on static, representation-only paradigms—by introducing a world-model architecture that explicitly models latent state transitions under longitudinal supervision. For researchers tracking this topic, it demonstrates that a generative world-model objective (rather than a discriminative or masked reconstruction objective) can unify perception, synthesis, and prognosis tasks within a single domain-specific model. The counterfactual progression capability is particularly significant: it moves medical foundation models from pattern recognition toward causal/mechanistic reasoning, a key aspiration in the field. The exemplar-conditioned interface also offers a practical blueprint for flexible clinical deployment without task-specific fine-tuning.

## Tags
#ophthalmology #generative-world-model #multimodal-imaging #longitudinal-prediction #cross-modality-synthesis #segmentation #disease-progression #medical-foundation-model
