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

Foundation models in medicine have moved past the "can we build one?" phase into a more sober, evaluation-driven era. The digests from late 2025 through mid-2026 show a field simultaneously pushing three frontiers: (1) making large medical FMs *deployable and adaptable* (LoRA/MoE adapters, distillation, quantization, frozen-encoder reuse), (2) *stress-testing* the generalization, robustness, and safety claims that earlier hype implied, and (3) extending FMs beyond static representation learning into *clinical reasoning, dynamics, and multi-agent decision-making*. A recurring theme is disillusionment with naive scaling and domain-specificity: across multiple papers, general-purpose 2D backbones rival bespoke medical FMs, handcrafted radiomics still beats FMs on texture-heavy tasks, and high benchmark scores repeatedly fail to transfer to functional modalities, perturbed inputs, or counterfactual patient facts. The center of gravity is shifting from pretraining tricks toward rigorous benchmarking, parameter-efficient specialization, and outcome-grounded clinical utility.

## Timeline

- **2023–2024**: First-generation medical FMs established as the baselines cited throughout — SAM/MedSAM segmentation, CLIP-style VLMs (BiomedCLIP, CT-CLIP, MONET, DermLIP), and structured-EHR encoders (BEHRT, Med-BERT).
- **2025-12**: Adaptation-over-pretraining turn — AnyMC3D shows frozen 2D FMs + per-task LoRA rival 3D medical FMs at 40–50× fewer params; PRIMED attacks catastrophic forgetting with retrieval-guided continual learning.
- **2026-01**: Critical benchmarking and unification begin — dermatology "granularity gap" exposed; UniX decouples understanding vs. generation; SC-SAM and FMIR repurpose SAM/DINO via co-training and frozen-encoder registration.
- **2026-02**: "Generalization illusion" surfaced (UMD/PET collapse); zero-real-data pretraining (RaSD); training-free transferability estimation; parameter-efficient specialization (MoLRE); zero-shot dermatology VLM with concept discovery (DermFM-Zero).
- **2026-03**: Cross-domain unified benchmarks (UNICORN) and dataset-landscape surveys (Imaging-X); pivot to dynamical/world models (EyeWorld) and semantic-mask SSL (MASS, CVPR 2026).
- **2026-04**: Intrinsic interpretability and spatial grounding (EXACT); modality-specific representation decomposition (M-IDoL); scaling laws for structured claims data; deployment-oriented PTQ (Permutation-COMQ); temporal directionality (TILA).
- **2026-05**: Clinical-reasoning frontier — POMDP/RL inpatient CDS beating frontier LLMs (CLR-voyance); safety≠accuracy scaling (SaFE-Scale); counterfactual evaluation (CSS); heterogeneous multi-agent (HetMedAgent); robustness benchmark (MedFM-Robust); radiomics still SOTA on renal CT.
- **2026-06**: Pretraining-objective science matures into controlled head-to-head MAE vs. JEPA on 3D brain MRI with task-conditioned auxiliary objectives.

## How the field developed

The window opens (late 2025) with a quiet but consequential shift away from training ever-larger domain-specific FMs toward **adapting and maintaining** what already exists. AnyMC3D (2025-12) crystallizes the thesis that properly adapted general-purpose 2D FMs (DINOv2/v3) match dedicated 3D medical FMs, while PRIMED (2025-12) reframes the lifecycle problem: medical VLMs need to *learn continually* across heterogeneous modality topologies without forgetting, using PubMed retrieval to replace inaccessible pretraining corpora. PGMP (2025-12) signals a parallel pattern — frozen medical FMs (MedDINOv3) used not as the system but as a *semantic regularizer* inside a task-specific pipeline.

Early 2026 is dominated by **adaptation mechanics and skepticism**. A cluster of parameter-efficient methods appears: MoLRE (mixture of low-rank experts for multi-label head CT), DRD (cross-architecture distillation bridging task/domain/architecture mismatch), Permutation-COMQ (low-bit PTQ for MedSAM), FMIR (frozen DINO/SAM for 3D registration), and SC-SAM (specialist↔generalist co-training on unlabeled data). Simultaneously, the benchmarking backlash sharpens: the Hierarchical Dermatology benchmark (2026-01) shows binary-screening winners collapse at fine-grained diagnosis; UMD (2026-02) demonstrates catastrophic PET collapse and names the "generalization illusion"; UNICORN (2026-03) and Topology-Driven Transferability (2026-02) build the infrastructure for *fair, leakage-controlled, fine-tuning-free* comparison; and Project Imaging-X (2026-03) diagnoses the root cause — a fragmented, long-tailed dataset landscape.

By spring 2026, two new directions mature. First, **pretraining moves beyond contrastive uniformity**: M-IDoL decomposes the contrastive objective to preserve modality specificity, RaSD shows competitive pretraining on *zero real images*, MASS replaces reconstruction/contrastive pretext tasks with SAM2-driven in-context segmentation, and the MAE-vs-JEPA brain-MRI study (2026-06) elevates the choice of pretraining objective to a first-class, task-conditioned design variable. Second, **FMs become dynamical and reasoning systems**: EXACT adds intrinsic voxel-level anomaly grounding, EyeWorld treats the eye as a partially observed dynamical system with time-conditioned state transitions, and UniX unifies autoregressive understanding with diffusion generation.

The most recent wave (2026-05) shifts decisively toward **clinical LLMs, agents, and trustworthy evaluation**. CLR-voyance reformulates inpatient care as a POMDP and uses outcome-grounded GRPO to make an 8B model beat GPT-5 — and actually deploys it. CSS introduces counterfactual sensitivity (does the model update when patient facts change?), SaFE-Scale shows safety and accuracy follow *different* scaling laws, HetMedAgent argues specialist models remain irreplaceable inside multi-agent systems, and MedFM-Robust shows fine-tuning strategy, not architecture, governs robustness. The renal-lesion benchmark (2026-05), where radiomics (AUC 0.88) crushes all three FMs (0.70–0.77), is the period's emblematic humility check.

## Current state & major clusters

- **Parameter-efficient & deployment-oriented adaptation.** The dominant practical thread. MoLRE (mixture of low-rank experts), DRD (deep reprogramming distillation across architectures), AnyMC3D (per-task LoRA on frozen 2D FMs), Permutation-COMQ (low-bit quantization of MedSAM), FMIR (frozen-encoder registration), and SC-SAM (semi-supervised SAM co-training) all aim to extract clinical utility from large FMs at low compute/annotation cost.

- **Rigorous, adversarial benchmarking & transferability.** UNICORN (unified radiology/pathology/text), MedFM-Robust (40 perturbation types), UMD (PET generalization illusion), the Hierarchical Dermatology "granularity gap," the renal-lesion radiomics-beats-FMs study, Topology-Driven Transferability Estimation, and Project Imaging-X's dataset survey. The collective message: clean-data leaderboard scores systematically overstate real-world capability.

- **Clinical LLMs, agents, and reasoning.** CLR-voyance (POMDP + outcome-aware GRPO, deployed), HetMedAgent (heterogeneous generalist + specialist + clinician agents), CSS (counterfactual causal-sensitivity evaluation), and SaFE-Scale (safety vs. accuracy scaling). This is the fastest-moving and highest-stakes cluster.

- **Next-generation pretraining objectives & SSL.** M-IDoL (information decomposition for modality specificity), RaSD (synthetic-only pretraining), MASS (mask-guided in-context segmentation SSL), and the MAE-vs-JEPA 3D brain MRI comparison with spectral/VCR auxiliary losses.

- **Generative, dynamical, and intrinsically grounded models.** EXACT (anomaly-aware voxel maps via Y-Mamba dual decoder), EyeWorld (multimodal longitudinal ocular world model), UniX (autoregression+diffusion for CXR understanding and generation), TILA (temporal interval-change directionality).

- **Structured / non-imaging modalities.** The Japanese medical-claims scaling-law study (task-dependent saturation, contradicting "bigger is better") and the imaging-anchored multiomics cardiovascular review point to FMs expanding into EHR/claims and spatial-omics territory. (Quantum-kernel embeddings sit at the experimental fringe.)

## Open problems

- **The generalization illusion.** Curated structural-imaging benchmarks (CT/MRI) do not predict performance on functional modalities (PET), perturbed inputs, or out-of-distribution scanners/protocols (UMD, MedFM-Robust). True zero-shot generalization remains largely unverified.
- **FMs vs. simple baselines on fine-grained/texture tasks.** Handcrafted radiomics beats all tested FMs on renal lesion stratification; the dermatology "granularity gap" persists. When does an FM actually help over a tuned classical baseline?
- **Domain-specificity is not automatically worth it.** General-purpose 2D FMs (DINOv2/v3) repeatedly rival or match dedicated medical FMs, raising the question of when expensive medical pretraining pays off.
- **Evaluation validity.** Coverage/accuracy metrics miss input-responsiveness (CSS), conflate asymmetric clinical risks (SaFE-Scale), and leak answers in longitudinal EHR benchmarks (CLR-voyance). Safety and accuracy are distinct, partly opposed axes.
- **Data fragmentation and scale.** Medical corpora remain orders of magnitude smaller, siloed, and long-tailed (Imaging-X); whether synthetic-only (RaSD) or metadata-fused data can close the gap is unsettled.
- **Spatial/temporal grounding vs. global embeddings.** CLIP-style 1D-pooled embeddings discard voxel structure (EXACT) and temporal directionality (TILA); how to retain dense, dynamical structure without sacrificing scalability is open.
- **Scaling laws are task-dependent.** Disease vs. medication prediction saturate at very different sizes on structured data; no unified compute-optimal recipe exists across medical modalities and tasks.
- **Pretraining-objective choice is unresolved.** MAE-with-spectral beats JEPA for brain-MRI disease detection, but the benefit is conditioned on downstream pathology structure — no universal SSL objective.

## Predicted next steps

- **Counterfactual/causal-sensitivity and safety-stratified evaluation will become standard reporting**, displacing single-number accuracy. Expect CSS-style and SaFE-Scale-style metrics to be demanded by reviewers and to appear in unified benchmarks like UNICORN within the next cycle.
- **Heterogeneous and tool-augmented agents will outpace monolithic medical LLMs** on multimodal decision tasks, with explicit specialist models (imaging, ECG/ECHO, radiomics) retained as confidence-weighted components (HetMedAgent), precisely because pure FMs underperform on texture/functional tasks.
- **Outcome-grounded RL on real trajectories (POMDP + GRPO) will spread from inpatient CDS to other longitudinal settings** (oncology tumor boards, ICU), with more small (4B–8B) deployed models beating frontier general LLMs on narrow clinical endpoints — following CLR-voyance's deploy-and-measure template.
- **Frozen general-purpose backbones + lightweight task adapters will become the default deployment pattern**, with bespoke medical pretraining increasingly justified only where it beats DINOv3-class baselines on sequestered, fine-grained tasks. Expect more head-to-head "do we even need a medical FM?" studies.
- **PET, functional imaging, and other under-represented modalities will get dedicated FMs/benchmarks** as the generalization illusion drives funding toward the long tail (UMD-style paired-modality datasets).
- **Pretraining will move toward task-conditioned objective selection and synthetic/mask-guided supervision** — expect RaSD-style synthetic scaling and MASS-style semantic-mask SSL to be combined, and MAE/JEPA objectives chosen per downstream pathology rather than by default.
- **Dynamical/world-model framing will expand beyond ophthalmology** (EyeWorld) to oncology and cardiology progression forecasting, fusing imaging with spatial/single-cell omics (imaging-anchored multiomics) as single-cell foundation models mature.
- **Deployment-side compression (PTQ, distillation, MoE adapters) will consolidate into integrated toolchains** as hospital deployment (already real in CLR-voyance) forces edge/terminal-device constraints into the mainstream research agenda.

## Key papers

- **CLR-voyance: Reinforcing Open-Ended Reasoning for Inpatient Clinical Decision Support with Outcome-Aware Rubrics** (2026-05, preprint) — POMDP + GRPO with EHR-trajectory rubrics lets an 8B model beat GPT-5 and run in a real hospital for 6+ months; the strongest evidence that clinical utility comes from outcome grounding, not scale.
- **Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents** (2026-05, preprint) — introduces the Causal Sensitivity Score, showing coverage-based and counterfactual rankings are nearly opposite; reframes "look-right vs. be-right" as a first-class evaluation axis.
- **Safety and accuracy follow different scaling laws in clinical large language models** (2026-05, preprint) — RadSaFE-200 + SaFE-Scale demonstrate across 34 LLMs that evidence quality, not size/retrieval/compute, drives safe behavior; decouples safety from accuracy.
- **Uncovering Modality Discrepancy and Generalization Illusion for General-Purpose 3D Medical Segmentation** (2026-02, preprint) — paired PET/CT–PET/MRI UMD benchmark exposes catastrophic PET collapse, naming the field's central evaluation failure mode.
- **Designing UNICORN: a Unified Benchmark for Imaging in Computational Pathology, Radiology, and Natural Language** (2026-03, preprint) — first leakage-controlled, frozen-encoder + few-shot protocol spanning 20 cross-domain tasks; the reference framework for fair FM comparison.
- **Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification** (2025-12, preprint) — AnyMC3D shows frozen DINOv2/v3 + ~1M-param LoRA match 3D medical FMs, challenging the value of bespoke 3D medical pretraining.
- **Why Specialist Models Still Matter: A Heterogeneous Multi-Agent Paradigm for Medical Artificial Intelligence** (2026-05, ICML 2026) — argues and shows that specialist + generalist + clinician collaboration beats any single-paradigm system on multimodal cardiovascular tasks.
- **Benchmarking Foundation Models for Renal Lesion Stratification in CT** (2026-05, preprint) — radiomics (AUC 0.88) decisively beats three medical FMs (0.70–0.77); the period's clearest "FMs aren't always the answer" result.
- **Free Lunch in Medical Image Foundation Model Pre-training via Randomized Synthesis and Disentanglement** (2026-02, preprint) — RaSD pretrains competitively on zero real images across 56 tasks, opening a privacy-preserving synthetic-scaling path.
- **EXACT: an explainable anomaly-aware vision foundation model for analysis of 3D chest CT** (2026-04, preprint) — Y-Mamba dual decoder yields intrinsic voxel-level anomaly maps without manual annotation, exemplifying the shift from 1D-pooled embeddings to spatially grounded FMs.
- **MedFM-Robust: Benchmarking Robustness of Medical Foundation Models** (2026-05, preprint) — first systematic robustness benchmark (40 perturbations, 8 modalities), finding fine-tuning strategy, not architecture, governs reliability.
- **Masked and Predictive Self-Supervised Foundation Models for 3D Brain MRI** (2026-06, preprint) — first controlled MAE-vs-JEPA comparison for 3D MRI; establishes pretraining-objective choice as task-conditioned rather than universal.
