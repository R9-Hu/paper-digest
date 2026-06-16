---
title: "Trend Analysis: Foundation Models in Medicine"
topic: Foundation Models in Medicine
topic_slug: med-foundation
generated: 2026-06-15
papers_analyzed: 31
---

# Trend Analysis — Foundation Models in Medicine

*Generated 2026-06-15 from 31 digested papers.*

## Overview

Foundation models in medicine have moved past the initial "scale a contrastive backbone and report clean-data AUC" phase into a period of critical consolidation. The digests show three forces operating simultaneously: a maturing toolkit for pretraining and adapting medical FMs (masked/predictive SSL, synthetic-data pretraining, LoRA/MoE adaptation, distillation, quantization), a wave of skeptical benchmarks that expose "generalization illusions," robustness gaps, and granularity gaps where specialists or even radiomics still win, and a fast-moving clinical-LLM/agent track increasingly preoccupied with safety, counterfactual reasoning, and real hospital deployment. A clear methodological pivot is underway from static representation learning toward dynamics-aware and generative models (world models, temporal/interval-change reasoning, unified understanding-and-generation). The net state of play is a field that has enough working models to now ask harder questions: not "can we build a medical FM?" but "where does it actually transfer, is it safe, and is it worth the compute?"

## Timeline

- **2021**: CLIP-style contrastive vision-language pretraining establishes the template later inherited by CT-CLIP, BiomedCLIP, MONET, and DermLIP.
- **2023**: SAM/MedSAM bring promptable segmentation foundation models to medical imaging; structured-EHR encoders (BEHRT, Med-BERT) establish the claims/EHR FM line.
- **2025**: General backbones (DINOv2/v3, MedSigLIP, RAD-DINO, MedGemma) become the de facto frozen feature extractors benchmarked everywhere.
- **2025-12**: Adaptation-and-reuse focus crystallizes — AnyMC3D shows frozen 2D FMs + LoRA rival native 3D FMs; PRIMED tackles catastrophic forgetting via retrieval-guided continual learning.
- **2026-01**: Benchmarks expose gaps (dermatology "granularity gap"); unified understanding+generation (UniX) and FM-adapted registration/segmentation (FMIR, SC-SAM) appear.
- **2026-02**: Evaluation skepticism peaks — UMD's "generalization illusion" (PET collapse), UNICORN cross-domain benchmark; synthetic-only pretraining (RaSD) and zero-shot dermatology VLM (DermFM-Zero) land.
- **2026-03**: Dynamics turn — EyeWorld (ocular world model), MASS (mask-guided 3D SSL, CVPR 2026); Project Imaging-X surveys 1000+ datasets exposing the data bottleneck.
- **2026-04**: Efficiency and scaling-law nuance — Permutation-COMQ quantization, MoLRE, Japanese claims FM scaling saturation; renal-lesion benchmark where radiomics beats all FMs.
- **2026-05**: Clinical-LLM safety/reasoning surge — CLR-voyance (deployed POMDP RL), SaFE-Scale safety scaling laws, counterfactual CSS, HetMedAgent specialists, MedFM-Robust.
- **2026-06**: Controlled SSL-paradigm science — MAE vs JEPA head-to-head on 58k 3D brain MRIs.

## How the field developed

The reconstructable prehistory (referenced throughout the digests rather than dated within them) runs from CLIP-style contrastive pretraining (2021), through SAM/MedSAM promptable segmentation and structured-EHR encoders like BEHRT/Med-BERT (2023), into the 2025 normalization of general backbones (DINOv2/v3, MedGemma, MedSigLIP, RAD-DINO) as standard medical feature extractors. By the time the digest window opens (late 2025), the basic question of *whether* medical FMs work was settled enough that the live questions became adaptation cost, transfer reliability, and clinical trustworthiness.

The **late-2025 phase** is dominated by reuse and efficiency. *Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification* (AnyMC3D) argues frozen 2D FMs plus ~1M-parameter LoRA adapters match 3D medical FMs needing 40–50× more trainable parameters, and explicitly indicts prior evaluation pitfalls (low-data bias, naive pooling, single-modality benchmarks). *PRIMED* attacks catastrophic forgetting in generalist medical VLMs with an 18M-entry PubMed retrieval database, reflecting an emerging assumption that pretraining data is inaccessible and must be substituted.

**Early 2026** brings a sharp turn toward skeptical evaluation. *A Hierarchical Benchmark of Foundation Models for Dermatology* surfaces a "granularity gap" — models that ace binary malignancy screening collapse at 40-subclass differential diagnosis. *UMD* (Uncovering Modality Discrepancy) coins the "generalization illusion," showing general-purpose 3D segmentation FMs catastrophically fail on PET because training corpora are overwhelmingly CT/MRI. *UNICORN* builds the first unified, leakage-controlled benchmark across radiology, pathology, and text. This phase reframes the field's self-image: high benchmark scores on curated structural data were masking brittle transfer.

Simultaneously, the **pretraining-methods line** diversifies away from plain contrastive learning. *M-IDoL* decomposes the contrastive objective to fix "information ambiguity" across modalities; *RaSD* demonstrates competitive pretraining on *zero real images* using randomized Gaussian synthesis; *MASS* replaces reconstruction/contrastive pretexts with annotation-free in-context segmentation driven by SAM2 masks. By mid-2026 this culminates in controlled science — *Masked and Predictive Self-Supervised Foundation Models for 3D Brain MRI* runs the first clean MAE-vs-JEPA comparison on ~58k volumes, finding MAE with spectral supervision wins for disease detection and that auxiliary-objective benefit is task-conditioned.

A parallel **adaptation/efficiency cluster** matures through spring 2026: *DRD* distills large ViT FMs into CNNs across task/domain/architecture mismatches; *MoLRE* generalizes LoRA into a mixture of low-rank experts for multi-label head CT; *Permutation-COMQ* pushes MedSAM to 2-bit deployment; *FMIR* adapts frozen DINO/SAM for 3D registration; and a *training-free topological transferability estimator* lets practitioners pick encoders without exhaustive fine-tuning. The *Japanese Medical Claims FM* injects scaling-law realism: downstream performance saturates at task-dependent (often small) model sizes, denting "bigger is better."

The **clinical-LLM/agent track** intensifies in May 2026 and is increasingly governed by safety and causal reasoning rather than accuracy. *CLR-voyance* reformulates inpatient reasoning as a POMDP trained with outcome-grounded rubrics and reports 6+ months of real hospital deployment. *SaFE-Scale* shows safety and accuracy follow *different* scaling laws — scale and retrieval don't buy safety, evidence quality does. The *Causal Sensitivity Score* exposes that coverage-based rankings are nearly inverted from whether models actually respond to changed patient facts. *HetMedAgent* argues specialists remain irreplaceable, echoing the renal-lesion finding that handcrafted radiomics (AUC 0.88) still crushes FMs (0.70–0.77).

Threaded across the whole window is a quieter but important **shift from static representation to dynamics and generation**: *EyeWorld* models the eye as a partially observed dynamical system with time-conditioned state transitions; *TILA* teaches directional interval-change sensitivity in chest X-rays; *UniX* decouples autoregressive understanding from diffusion generation; *EXACT* produces intrinsic voxel-level anomaly maps instead of compressed CLIP embeddings.

## Current state & major clusters

- **Skeptical/unified benchmarking and "illusion-busting."** The dominant near-term mood. *MedFM-Robust* (40 perturbation types, 8 modalities) finds fine-tuning strategy — not architecture — drives robustness. *UMD* exposes structural-vs-functional (PET) collapse. *UNICORN* unifies radiology/pathology/text under one leakage-controlled protocol. *A Hierarchical Benchmark for Dermatology* and *Benchmarking Foundation Models for Renal Lesion Stratification* both show FMs losing to specialists/radiomics on fine-grained tasks. *Project Imaging-X* maps the fragmented 1000+ dataset landscape underpinning all of this.

- **Efficient adaptation and deployment.** *AnyMC3D* (LoRA on frozen 2D FMs), *MoLRE* (mixture of low-rank experts), *DRD* (cross-architecture distillation), *Permutation-COMQ* (low-bit PTQ for MedSAM), *FMIR* (frozen DINO/SAM for registration), and the *topology-driven transferability estimator* form a coherent toolkit for cheaply specializing large FMs.

- **Pretraining-objective science.** *MAE vs JEPA for 3D Brain MRI*, *M-IDoL* (information decomposition), *RaSD* (synthetic-only), and *MASS* (mask-guided in-context segmentation) reflect a move from "more data, one contrastive loss" toward principled, task-conditioned objective design and data-free pretraining.

- **Clinical LLMs, agents, safety, and reasoning.** *CLR-voyance* (POMDP RL, deployed), *SaFE-Scale* (safety scaling laws), *Counterfactual CSS* (input responsiveness), and *HetMedAgent* (heterogeneous specialist+generalist+human agents) define a track where evaluation rigor and safety dominate raw accuracy.

- **Dynamics-aware and generative/unified models.** *EyeWorld* (world model), *TILA* (temporal interval change), *UniX* (autoregression + diffusion), and *EXACT* (intrinsic anomaly localization) push beyond static embeddings toward spatially grounded and temporally aware modeling.

- **Beyond imaging: structured/multiomics/exotic.** The *Japanese Medical Claims FM* (structured EHR scaling laws), the *imaging-anchored multiomics* cardiovascular review, and the *Quantum Kernel Advantage* study show the FM concept spreading into claims data, spatial transcriptomics, and frontier compute substrates.

## Open problems

- **Generalization is overstated and entangled with task confounds.** UMD and the renal/dermatology benchmarks show curated structural-imaging scores don't transfer to functional modalities (PET), rare subtypes, or fine-grained taxonomies; modality and anatomy remain confounded in most evaluations.
- **Specialists and radiomics still win on hard, texture- or signal-specific tasks** — when and why FMs underperform classical methods is not predictable a priori.
- **Safety ≠ accuracy.** SaFE-Scale and CSS show standard accuracy/coverage metrics can be nearly orthogonal (or inverted) relative to safe, input-responsive clinical behavior; there is no consensus safety metric.
- **The data bottleneck is structural.** Project Imaging-X documents a fragmented, long-tailed corpus that biases pretraining; whether synthetic (RaSD) or metadata-fused data truly substitute for balanced real data at scale is unproven.
- **Scaling laws are task-dependent and weak.** The Japanese claims FM shows saturation at small sizes; clinical LLM safety doesn't scale with size/retrieval/compute — so where to spend parameters is unclear.
- **SSL paradigm choice (MAE vs JEPA vs mask-guided) is task-conditioned**, not universal; no theory predicts which objective fits which pathology.
- **Interpretability and dynamics remain bolt-on.** Voxel-grounded explanation (EXACT), temporal directionality (TILA), and concept discovery (DermFM-Zero) are demonstrated piecemeal, not unified.
- **Deployment, quantization, and continual learning interact poorly** — low-bit PTQ, distillation, and continual fine-tuning each trade off accuracy/forgetting in ways not jointly characterized.

## Predicted next steps

- **Counterfactual/causal-sensitivity evaluation will become standard for clinical LLMs**, expanding beyond oncology tumor boards (CSS) to radiology and inpatient care; expect coverage-only leaderboards to be openly distrusted within a year.
- **Safety will be reported as a separate axis from accuracy** in most new clinical-LLM papers, with evidence-quality interventions (curated retrieval, option-level safety labels à la RadSaFE-200) prioritized over scale.
- **Modality-stratified, leakage-controlled benchmarks become the default**, with functional imaging (PET) and fine-grained taxonomies deliberately included to pre-empt "generalization illusion" critiques; UNICORN/UMD-style protocols proliferate per specialty.
- **Frozen general 2D backbones + lightweight adapters (LoRA/MoE) will keep displacing bespoke 3D medical FMs** for classification/registration, because AnyMC3D-style results show parameter parity at 40–50× lower training cost; native 3D FMs will need to justify themselves on dense/temporal tasks.
- **World-model and temporal/longitudinal framing spreads to new organs** beyond ophthalmology (EyeWorld) and chest X-ray (TILA) — expect cardiac and neuro disease-progression world models, since longitudinal cohorts already exist.
- **Synthetic-only and metadata-fusion pretraining gain traction as privacy-and-scarcity workarounds**, with RaSD-style data engines benchmarked head-to-head against real-data pretraining across more modalities.
- **Heterogeneous specialist+generalist agent systems** (HetMedAgent) will be the architecture of choice for multimodal clinical decision support, formalizing the recurring "specialists/radiomics still win" finding into routing frameworks.
- **Hospital-deployed, outcome-grounded RL training** (CLR-voyance) sets a new bar; expect more small-model (4B–8B) systems trained on real EHR trajectories outperforming frontier general models on narrow inpatient tasks.
- **Robustness and quantization will be co-reported**, as MedFM-Robust's "fine-tuning strategy dominates robustness" finding pushes deployment papers (Permutation-COMQ) to validate under perturbation.

## Key papers

- **Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification (AnyMC3D)** (2025-12-15, Arxiv) — frozen 2D FMs + ~1M-param LoRA match 3D medical FMs at 40–50× less cost, reframing the build-vs-adapt question.
- **Forging a Dynamic Memory: Retrieval-Guided Continual Learning (PRIMED)** (2025-12-15, Arxiv) — uses an 18M-entry PubMed retrieval DB to fight catastrophic forgetting without inaccessible pretraining data.
- **UniX: Unifying Autoregression and Diffusion for Chest X-Ray Understanding and Generation** (2026-01-16, Arxiv) — decouples understanding and generation to resolve the abstraction-vs-reconstruction conflict in unified medical FMs.
- **A Hierarchical Benchmark of Foundation Models for Dermatology** (2026-01-18, Arxiv) — names the "granularity gap": binary-screening champions fail at fine-grained differential diagnosis.
- **Uncovering Modality Discrepancy and Generalization Illusion for General-Purpose 3D Medical Segmentation (UMD)** (2026-02-07, Arxiv) — paired PET/CT-MRI benchmark exposes catastrophic collapse on functional imaging.
- **A Vision-Language Foundation Model for Zero-shot Clinical Collaboration in Dermatology (DermFM-Zero)** (2026-02-11, Arxiv) — 4M+ data points, SOTA zero-shot, SAE-based interpretable concept discovery and bias suppression.
- **Free Lunch via Randomized Synthesis and Disentanglement (RaSD)** (2026-02-12, Arxiv) — competitive medical FM pretraining on zero real images, establishing synthetic data as a privacy-preserving substitute.
- **Designing UNICORN** (2026-03-03, Arxiv) — first unified, leakage-controlled benchmark spanning radiology, pathology, and clinical text with a decoupled frozen-encoder/few-shot protocol.
- **Learning Generalizable 3D Medical Image Representations from Mask-Guided Self-Supervision (MASS)** (2026-03-14, CVPR 2026) — annotation-free in-context segmentation pretext (SAM2 masks) rivaling supervised pretraining in low-data regimes.
- **EyeWorld: A Generative World Model of Ocular State and Dynamics** (2026-03-14, Arxiv) — shifts medical FMs from static representation to explicit, time-conditioned disease-dynamics modeling.
- **Project Imaging-X** (2026-03-29, Arxiv) — surveys 1000+ open datasets, quantifying the fragmented, long-tailed data bottleneck constraining medical FM development.
- **EXACT** (2026-04-27, Arxiv) — anatomy-constrained weakly supervised 3D chest CT FM producing intrinsic voxel-level anomaly maps instead of compressed CLIP embeddings.
- **Safety and accuracy follow different scaling laws in clinical LLMs (SaFE-Scale)** (2026-05-05, Arxiv) — across 34 LLMs, evidence quality — not scale/retrieval/compute — drives safe clinical behavior.
- **CLR-voyance** (2026-05-10, Arxiv) — POMDP + GRPO with outcome-grounded rubrics; a deployed 8B model beats GPT-5 on inpatient decision support, proving small outcome-trained models can win.
- **MedFM-Robust** (2026-05-18, Arxiv) — first systematic robustness benchmark (40 perturbations, 8 modalities), finding fine-tuning strategy dominates architecture.
- **Counterfactual Evaluation Reveals Hidden Capability Profiles (CSS)** (2026-05-28, Arxiv) — pre-registered causal-sensitivity metric whose rankings nearly invert coverage-based ones, exposing input-insensitivity.
- **Masked and Predictive Self-Supervised Foundation Models for 3D Brain MRI** (2026-06-11, Arxiv) — first controlled MAE-vs-JEPA comparison at scale, showing objective choice is task-conditioned.
