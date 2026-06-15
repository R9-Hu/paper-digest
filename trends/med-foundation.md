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

Foundation models in medicine have moved past the "scale a contrastive VLM and report benchmark wins" phase into a more skeptical, infrastructure-and-evaluation-driven era. The dominant question is no longer *whether* to build medical foundation models but *how to adapt, evaluate, deploy, and trust* them under the field's defining constraints: small fragmented datasets, heterogeneous modalities (2D/3D, structural/functional, imaging/text/claims/omics), privacy limits, and clinical safety stakes. The digests here (Dec 2025–Jun 2026) reveal a field simultaneously pushing three frontiers: parameter-efficient *specialization* of generalist backbones, rigorous *benchmarking* that repeatedly punctures "general-purpose" claims, and *clinical reasoning/safety* evaluation that decouples looking-right from being-right. A recurring, almost contrarian theme is that bigger and more "foundational" is often *not* better—radiomics, lightweight CNNs, task-saturated small models, and adapted general-vision backbones repeatedly match or beat purpose-built medical FMs.

## How the field developed

**Late 2025 — consolidation and the limits of monolithic FMs.** The earliest digests address what happens *after* you have a generalist VLM. PRIMED (Dec 2025) tackles catastrophic forgetting in continual fine-tuning by replacing inaccessible pretraining data with an 18M-entry PubMed RAG database for distillation. PGMP (Dec 2025) uses a *frozen* medical FM (MedDINOv3) merely as a semantic regularizer inside a physics-grounded artifact-reduction pipeline—FM-as-component, not FM-as-product. Revisiting 2D FMs for 3D classification (AnyMC3D, Dec 2025) sounds the era's keynote: properly adapted *general-purpose* 2D backbones (DINOv2/v3) with ~1M-param LoRA match 3D medical FMs needing 40–50× more parameters.

**Jan–Feb 2026 — adaptation and the "generalization illusion."** A cluster of work converges on parameter-efficient specialization: FMIR (Jan 2026) adapts frozen DINO/SAM for 3D registration via slice-wise features and channel-dropout regularization; SC-SAM (Jan 2026) co-trains U-Net and SAM to exploit unlabeled data; MoLRE (Feb 2026) extends LoRA to a mixture of low-rank experts for multi-label head CT. Simultaneously, benchmarking turns adversarial: the UMD benchmark (Feb 2026) exposes "generalization illusion"—SOTA 3D segmentation FMs collapse on PET because they were trained almost exclusively on CT/MRI. RaSD (Feb 2026) makes the provocative claim that pretraining on *zero real images* (Gaussian-synthesized data) matches real-data FMs across 56 tasks.

**Mar–Apr 2026 — benchmarks, world models, and the "specialist strikes back."** UNICORN (Mar 2026) and Project Imaging-X (Mar 2026) attack the infrastructure layer: unified cross-domain evaluation and a 1,000+ dataset survey diagnosing the fragmented, long-tailed data landscape. EyeWorld (Mar 2026) pushes beyond static representation to a generative *world model* of ocular dynamics. Then the empirical pushback peaks: renal lesion stratification (May 2026) shows handcrafted radiomics (AUC 0.88) crushing three medical FMs (0.70–0.77); the Dermatology hierarchical benchmark (Jan 2026) reveals a "granularity gap"; the Japanese claims model (Apr 2026) finds task-dependent scaling saturation, undercutting "bigger is better."

**Apr–Jun 2026 — safety, reasoning, and deployment.** The newest work shifts to clinical LLMs and trustworthiness: SaFE-Scale (May 2026) shows safety and accuracy follow *different* scaling laws; the Causal Sensitivity Score (May 2026) shows coverage and counterfactual rankings are nearly opposite; CLR-voyance (May 2026) trains an 8B POMDP-reasoning model that beats GPT-5 on inpatient decisions and is *deployed* for 6+ months. MedFM-Robust (May 2026) systematizes robustness across 40 perturbations.

## Current state & major clusters

**1. Parameter-efficient specialization of frozen backbones.** The dominant adaptation paradigm. **AnyMC3D** (2D→3D via LoRA + attention pooling), **MoLRE** (mixture of low-rank experts, <0.5% params, MedGemma+MoLRE 0.917 AUC), **FMIR** (frozen DINO/SAM for registration), **SC-SAM** (specialist↔generalist co-training), and **DRD** (Deep Reprogramming Distillation across task/domain/architecture mismatch) all treat the FM as a frozen asset to be cheaply steered, not retrained.

**2. Adversarial benchmarking and "illusion-busting."** A large, fast-growing cluster. **UMD** (PET collapse / generalization illusion), **UNICORN** (unified radiology+pathology+text protocol with sequestered data), **MedFM-Robust** (40 perturbations; fine-tuning strategy, not architecture, drives robustness), **Hierarchical Dermatology Benchmark** (granularity gap), **Renal Lesion Stratification** (radiomics > FMs), and **Topology-Driven Transferability Estimation** (training-free MST-based encoder selection for segmentation).

**3. Self-supervised pretraining design.** Active methodological frontier. **MASS** (mask-guided in-context segmentation via SAM2, CVPR 2026), **Masked vs. Predictive (MAE vs. JEPA) for 3D brain MRI** (MAE+spectral loss wins), **M-IDoL** (information-decomposition to fight modality collapse), and **RaSD** (fully synthetic pretraining)—all attacking the data-scarcity bottleneck through better objectives or synthetic data.

**4. Unified understanding+generation and world models.** **UniX** (decoupled autoregressive+diffusion branches for CXR), **EyeWorld** (longitudinal ocular world model), and **TILA** (directional interval-change in CXR pairs) move from static encoders toward generative, temporal, multimodal reasoning.

**5. Clinical LLMs: reasoning, safety, deployment.** **CLR-voyance** (POMDP + outcome-aware GRPO rubrics, deployed), **CSS** (counterfactual evaluation), **SaFE-Scale** (safety ≠ accuracy scaling), and **HetMedAgent** (heterogeneous generalist+specialist+human multi-agent, ICML 2026)—the "specialist models still matter" thesis made architectural.

**6. Deployment/efficiency & frontier curiosities.** **Permutation-COMQ** (low-bit PTQ for MedSAM), the **Japanese claims scaling-law** study, plus structured/omics extensions (**imaging-anchored cardiovascular multiomics**) and the outlier **Quantum Kernel Advantage** on frozen FM embeddings.

## Open problems

- **The "general-purpose" claim is largely unearned.** UMD, the renal and dermatology benchmarks, and MedFM-Robust repeatedly show FMs failing on out-of-distribution modalities (PET, functional imaging), fine-grained tasks, and perturbations—yet they are marketed as general. There is no agreed protocol for substantiating generality.
- **When do FMs actually beat conventional baselines?** Radiomics beats FMs on texture-dependent renal stratification; lightweight CNNs beat distilled ViTs; task performance saturates at small model sizes. The conditions under which FM pretraining pays off remain poorly characterized.
- **Evaluation validity.** Coverage metrics rank models opposite to counterfactual sensitivity (CSS); benchmarks leak (longitudinal EHR), test sets overlap pretraining distributions, and accuracy masks asymmetric clinical risk (SaFE-Scale). Robustness is dominated by fine-tuning choices that benchmarks don't standardize.
- **Modality fragmentation and information collapse.** Single contrastive objectives collapse modalities (M-IDoL); 3D functional imaging is nearly absent from training corpora; the data landscape is long-tailed and siloed (Project Imaging-X).
- **3D vs. 2D and spatial grounding.** CLIP-style 1D embedding compression discards voxel-level structure (EXACT's critique); slice-wise 2D adaptation works but may not be a principled 3D solution.
- **Synthetic-data validity.** RaSD claims real-data parity from Gaussian synthesis—if robust, it reframes the entire data-scarcity narrative; if benchmark-specific, it's a mirage. Unresolved.
- **Safety, trust, and interpretability** lack standardization; intrinsic explainability (EXACT, DermFM-Zero's sparse autoencoders) is promising but not yet the norm.
- **Generalist vs. specialist orchestration.** HetMedAgent and the multi-agent trend imply no single model suffices, but composition, confidence calibration, and human-in-the-loop integration are unsolved.

## Predicted next steps

- **Benchmark proliferation will continue and consolidate into "stress-test suites."** Expect UMD/UNICORN/MedFM-Robust-style benchmarks to add functional imaging (PET, fMRI), counterfactual sensitivity (CSS-style), and robustness as *mandatory* axes—single clean-accuracy leaderboards will be increasingly rejected by reviewers. Falsifiable: top-venue medical FM papers in late 2026 will routinely report OOD-modality and perturbation results, not just clean AUC.
- **Mixture-of-experts adapters become the default specialization recipe.** MoLRE-style input-conditional low-rank routing will spread from head CT to multi-organ and multimodal tasks, displacing vanilla LoRA. Falsifiable: ≥3 follow-ups extending MoE-LoRA to new anatomies/modalities within ~12 months.
- **"General 2D backbone + cheap 3D adapter" will keep beating bespoke 3D medical FMs**, pressuring labs to stop pretraining 3D FMs from scratch and instead invest in adaptation. Falsifiable: new 3D classification SOTA papers will increasingly build on frozen DINOv3/SigLIP rather than train new 3D encoders.
- **Synthetic and hybrid pretraining data will be tested head-to-head at larger scale.** RaSD will trigger replication attempts; expect papers either validating Gaussian/synthetic pretraining on harder tasks or showing it fails on fine-grained/texture tasks (mirroring the radiomics result). Falsifiable: a 2026 paper directly contests RaSD's real-data-parity claim.
- **Clinical LLM work pivots from MCQ accuracy to deployed, outcome-grounded, safety-aware reasoning.** CLR-voyance's POMDP+rubric+deployment template and SaFE-Scale's safety-axis framing will be widely emulated; counterfactual/causal metrics become standard. Falsifiable: multiple new inpatient/clinical-decision papers report real deployment and counterfactual sensitivity rather than benchmark saturation.
- **World/temporal models expand beyond ophthalmology.** EyeWorld + TILA + EXACT signal a shift to longitudinal, dynamics-aware, spatially-grounded FMs; expect chest CT/CXR and oncology world models forecasting disease progression. Falsifiable: a "world model" framing appears for ≥2 new organ systems in 2026.
- **Heterogeneous generalist+specialist+human orchestration becomes the deployment architecture of choice** for high-stakes multimodal decisions, over monolithic medical LLMs. Falsifiable: more multi-agent clinical systems integrating non-LLM specialist models (imaging, signals) appear, citing HetMedAgent's thesis.
- **Efficiency (quantization, distillation, transferability estimation) becomes a first-class research track** as deployment to clinical edge devices matters more—Permutation-COMQ, DRD, and topology-based encoder selection are early instances.

## Key papers

- **Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification (AnyMC3D)** (2025-12-15, Arxiv) — shows frozen general 2D backbones + ~1M-param LoRA match 3D medical FMs with 40–50× more params; defines the adaptation-over-pretraining thesis.
- **Uncovering Modality Discrepancy and Generalization Illusion for General-Purpose 3D Medical Segmentation (UMD)** (2026-02-07, Arxiv) — isolates modality via paired PET/CT, exposing catastrophic PET collapse and naming the "generalization illusion."
- **Designing UNICORN** (2026-03-03, Arxiv) — first unified, sequestered, cross-domain (radiology+pathology+text) benchmark with a decoupled frozen-encoder + few-shot protocol.
- **MedFM-Robust** (2026-05-18, Arxiv) — first systematic robustness benchmark (40 perturbations, 8 modalities); finds fine-tuning strategy, not architecture, dominates robustness.
- **Benchmarking Foundation Models for Renal Lesion Stratification in CT** (2026-05-08, Arxiv) — clean demonstration that handcrafted radiomics (0.88 AUC) beats medical FMs (0.70–0.77) on texture-dependent tasks.
- **CLR-voyance** (2026-05-10, Arxiv) — POMDP reformulation + outcome-aware GRPO rubrics; an 8B model beats GPT-5 on inpatient decisions and is hospital-deployed 6+ months.
- **Safety and accuracy follow different scaling laws in clinical LLMs (SaFE-Scale)** (2026-05-05, Arxiv) — proves clinical safety is driven by evidence quality, not scale/retrieval/compute; decouples safety from accuracy.
- **Counterfactual Evaluation Reveals Hidden Capability Profiles (CSS)** (2026-05-28, Arxiv) — counterfactual sensitivity ranks models nearly opposite to coverage metrics, exposing the look-right vs. be-right gap.
- **MoLRE: Mixture of Low-Rank Experts** (2026-02-28, Arxiv) — input-conditional MoE-LoRA specialization (<0.5% params) for multi-label head CT; template for adapter-based steering.
- **Free Lunch via Randomized Synthesis and Disentanglement (RaSD)** (2026-02-12, Arxiv) — pretrains competitive MIFMs on *zero real images*, challenging the data-scarcity narrative across 56 tasks.
- **MASS: Mask-Guided Self-Supervision** (2026-03-14, CVPR 2026) — annotation-free in-context-segmentation pretext via SAM2 masks, rivaling supervised pretraining in low-data 3D regimes.
- **EyeWorld: A Generative World Model of Ocular State and Dynamics** (2026-03-14, Arxiv) — moves from static representation to a longitudinal, multimodal world model forecasting disease progression.
- **EXACT** (2026-04-27, Arxiv) — intrinsically explainable, anomaly-aware 3D chest CT FM that rejects CLIP-style 1D compression for voxel-level grounding.
- **Why Specialist Models Still Matter (HetMedAgent)** (2026-05-28, ICML 2026) — argues and demonstrates that generalist+specialist+human orchestration beats any single-paradigm clinical system.
- **Project Imaging-X** (2026-03-29, Arxiv) — surveys 1,000+ datasets, diagnosing the fragmented long-tailed data landscape that bottlenecks the whole field.
