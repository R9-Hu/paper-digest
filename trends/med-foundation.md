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
Foundation models in medicine have moved past the initial "scale a pretrained encoder and report a benchmark win" phase into a period of critical consolidation. The digests show three forces operating simultaneously: an expanding methodological toolkit (self-supervised pretraining variants, synthetic-data pretraining, world models, unified understanding-generation architectures), an aggressive efficiency/adaptation push (LoRA-family adapters, distillation, quantization, frozen-2D-to-3D reuse), and—most strikingly—a wave of skeptical benchmarking that repeatedly shows headline generalization claims do not survive controlled scrutiny. The dominant tension is between the field's ambition (general-purpose, multimodal, multi-task medical FMs) and accumulating evidence that modality, task granularity, robustness, and clinical safety each behave as separate axes that scale and domain-pretraining do not automatically conquer. The frontier is shifting from "can we build a medical FM" to "for which task, under what perturbation, with what guarantees, at what deployment cost."

## Timeline
- **2025-12**: Adaptation-and-continual-learning phase — retrieval-guided CL against forgetting (PRIMED) and frozen 2D FMs matching 3D medical FMs at 1/40th the parameters (AnyMC3D).
- **2026-01**: Generative/unified medical FMs emerge (UniX unifying autoregression+diffusion for CXR) alongside FM-as-component frameworks (PGMP, FMIR, SC-SAM) and the first granularity-aware dermatology benchmark.
- **2026-02**: Skeptical-benchmark inflection — UMD exposes PET "generalization illusion," and synthetic-data (RaSD), information-decomposed (M-IDoL), and zero-shot domain VLMs (DermFM-Zero) appear.
- **2026-02 / 03**: Unified cross-domain evaluation standardizes (UNICORN); training-free transferability estimation (topology-driven) and MoE-style specialization (MoLRE) mature adaptation.
- **2026-03**: World models for medicine (EyeWorld) and annotation-free mask-guided SSL (MASS, CVPR 2026); Imaging-X survey quantifies the fragmented-data bottleneck.
- **2026-04**: Efficiency/deployment focus (Permutation-COMQ quantization), interpretable 3D models (EXACT), structured-data scaling laws (Japanese claims FM), and fringe quantum-kernel claims.
- **2026-05**: Reliability axis crystallizes — safety ≠ accuracy scaling (SaFE-Scale), robustness benchmark (MedFM-Robust), counterfactual evaluation (CSS), deployed RL inpatient reasoning (CLR-voyance), and "specialists still matter" multi-agent systems.
- **2026-06**: Controlled SSL paradigm comparison (MAE vs. JEPA for 3D brain MRI) returns to first-principles pretraining-objective questions.

## How the field developed
The earliest digests (December 2025) already assume the existence of large medical FMs and focus on *using them better rather than building them bigger*. PRIMED tackles catastrophic forgetting in generalist medical VLMs via RAG-driven distillation, and AnyMC3D delivers the period's recurring thesis in miniature: a frozen general-purpose 2D model (DINOv2/v3) with ~1M-parameter LoRA adapters matches domain-specific 3D medical FMs that need 40–50× more trainable parameters. This "adapt, don't pretrain from scratch" stance recurs throughout (FMIR adapting frozen DINO/SAM for 3D registration, SC-SAM co-training U-Net with SAM, PGMP using frozen MedDINOv3 as a semantic regularizer).

Through January–February 2026 two parallel tracks develop. One is *generative and unified modeling*: UniX decouples understanding (autoregressive) from generation (diffusion) to resolve the semantic-abstraction-vs-pixel-reconstruction conflict, and later EyeWorld reframes the eye as a partially observed dynamical system—an explicit move from representation-centric to dynamics-centric modeling. The other, more consequential track is *adversarial benchmarking*. UMD (Feb) isolates imaging modality as a variable using paired PET/CT and PET/MRI scans and documents catastrophic collapse on PET, coining the "generalization illusion." The Hierarchical Dermatology benchmark exposes a "granularity gap" (binary-screening winners fail at 40-subclass diagnosis). This skepticism becomes the period's defining intellectual contribution.

By March–April the field professionalizes its infrastructure and questions its own scaling assumptions. UNICORN provides the first unified, leakage-controlled cross-domain (radiology/pathology/text) benchmark; the topology-driven transferability work offers training-free model selection; Imaging-X catalogs 1000+ datasets and names fragmentation as the core bottleneck. Scaling-law studies arrive with counterintuitive results: the Japanese claims FM finds task-dependent saturation (medication prediction saturates at 11M parameters), and RaSD shows pretraining on *zero real images* (pure Gaussian-derived synthetic data) can match real-data pretraining across 56 tasks.

The May–June phase pushes hardest on *clinical reliability and deployment*. SaFE-Scale demonstrates safety and accuracy follow different scaling laws—evidence quality, not model size or inference compute, drives safe radiology behavior. MedFM-Robust shows fine-tuning strategy, not architecture, determines robustness across 40 perturbations. CSS uses counterfactual mutations to reveal that coverage-based and causal-sensitivity rankings are nearly opposite. CLR-voyance shows an 8B RL-trained model beating GPT-5 on inpatient decision support with a real 6-month hospital deployment, while HetMedAgent argues specialist models remain irreplaceable. The June MAE-vs-JEPA study closes the loop, returning to controlled first-principles questions about which pretraining objective fits which pathology.

## Current state & major clusters
- **Self-supervised pretraining objectives:** Active reexamination of what to predict. *Masked and Predictive Self-Supervised Foundation Models for 3D Brain MRI* (MAE+spectral loss vs. JEPA+VCR), *MASS* (in-context segmentation via SAM2-generated masks), *M-IDoL* (information-decomposed contrastive objective separating inter/intra-modality terms), and *RaSD* (synthetic-only pretraining) collectively argue the objective and data source matter more than raw scale.
- **Parameter-efficient adaptation & deployment:** *AnyMC3D* (LoRA + slice aggregation on frozen 2D FMs), *MoLRE* (mixture of low-rank experts with soft routing for multi-label head CT), *DRD* (reprogramming distillation bridging task/domain/architecture mismatch), and *Permutation-COMQ* (low-bit PTQ for MedSAM) target the train-once/deploy-cheaply problem.
- **Critical benchmarking & evaluation rigor:** The largest and most distinctive cluster. *UNICORN* (unified cross-domain, leakage-controlled), *MedFM-Robust* (robustness under 40 perturbations), *UMD* (modality-isolated PET collapse), the *Hierarchical Dermatology* and *Renal Lesion* benchmarks (where handcrafted radiomics still beats FMs), and *topology-driven transferability estimation* (training-free model selection).
- **Clinical LLMs, agents, and safety:** *CLR-voyance* (POMDP + GRPO with outcome-grounded rubrics, deployed), *SaFE-Scale* (safety ≠ accuracy scaling), *CSS* (counterfactual causal-sensitivity evaluation), and *HetMedAgent* (heterogeneous generalist+specialist+human agents).
- **Generative, unified, and world models:** *UniX* (AR+diffusion for CXR), *EyeWorld* (longitudinal ocular world model), *EXACT* (intrinsic voxel-level anomaly maps via Y-Mamba), *TILA* (temporal-inversion supervision for interval change), *PGMP* (deterministic manifold projection for CBCT MAR).
- **Domain-specific and non-imaging FMs:** *DermFM-Zero* (4M-sample dermatology VLM with SAE concept discovery), the *Japanese medical claims FM* (structured EHR scaling laws), and the *cardiovascular imaging-anchored multiomics* review.

## Open problems
- **The generalization illusion:** High curated-benchmark scores do not transfer to out-of-distribution modalities (PET in UMD), fine-grained granularity (dermatology), or perturbed inputs (MedFM-Robust). True zero-shot generalization remains largely unverified.
- **FMs vs. classical baselines on specialized tasks:** Handcrafted radiomics beats all three FMs on renal lesion stratification (AUC 0.88 vs. 0.70–0.77); MedSAM underperforms ViT-Tiny on FIVES. When FM transfer actually helps is unresolved.
- **Safety as a distinct, unscaled axis:** Safety, accuracy, robustness, and causal input-responsiveness scale differently (SaFE-Scale, CSS). The "surgery-status blind spot" universal across frontier models shows reasoning failures are invisible to coverage metrics.
- **Data fragmentation and scale:** Medical corpora are orders of magnitude smaller and long-tailed (Imaging-X); whether synthetic data (RaSD) or metadata-driven fusion can substitute at scale is unproven beyond initial demonstrations.
- **Modality and information collapse:** Single contrastive objectives collapse heterogeneous modalities (M-IDoL); CLIP-style 1D embedding compression discards voxel structure (EXACT). The right multimodal pretraining objective is contested.
- **Generalist vs. specialist tension:** HetMedAgent and the imaging benchmarks argue specialists remain irreplaceable, directly contesting the monolithic-generalist-FM vision.
- **Deployment cost vs. capability:** PEFT reduces training but not inference cost (DRD motivation); quantization and distillation are early-stage for clinical edge devices.
- **Temporal/dynamical reasoning:** Most FMs treat images as independent observations; directional interval-change (TILA) and disease-progression dynamics (EyeWorld) are nascent.

## Predicted next steps
- **Counterfactual/causal evaluation becomes standard.** Following CSS and SaFE-Scale, expect new benchmarks to report input-responsiveness and option-level safety alongside accuracy; coverage-only leaderboards will be increasingly treated as insufficient for clinical claims.
- **Modality-isolated and perturbation-stratified reporting will be demanded by reviewers.** UMD and MedFM-Robust set a template; near-term papers claiming "general-purpose" 3D/medical FMs will be expected to report PET/functional-imaging and corruption results, or be discounted.
- **Synthetic and metadata-fused pretraining corpora will scale up.** RaSD's zero-real-image result plus Imaging-X's MDFP proposal point to hybrid synthetic+fused training as the practical answer to data fragmentation and privacy; expect larger synthetic-pretrained 3D FMs within the year.
- **Small, RL-tuned, outcome-grounded clinical models will proliferate over frontier-scale LLMs for deployment.** CLR-voyance's deployed 8B model beating GPT-5 will motivate more POMDP/GRPO-with-outcome-rubric pipelines, especially where EHR trajectories supply reward.
- **Routing/MoE adaptation will displace single-LoRA fine-tuning for multi-label clinical tasks.** MoLRE's per-input expert routing addresses LoRA knowledge interference; expect mixture-of-adapters to become the default for heterogeneous-finding detection.
- **World/dynamical models extend beyond ophthalmology.** EyeWorld's latent-state-plus-time-transition formulation is portable; near-term work should apply it to longitudinal CT/MRI progression forecasting (oncology, neurodegeneration).
- **Frozen general-purpose 2D/3D backbones keep eroding the case for bespoke medical pretraining.** AnyMC3D and FMIR suggest more results showing DINOv2/v3-class models, properly adapted, match domain FMs—pushing investment toward adaptation methods and away from from-scratch medical pretraining.
- **Training-free transferability and robustness-aware fine-tuning selection will be productized** into model-zoo tooling, given the topology-driven estimator's ~31% gain and MedFM-Robust's finding that fine-tuning strategy dominates architecture.
- **Quantum-kernel claims will remain a fringe curiosity** absent noisy-hardware validation; the noiseless-simulation insurance-classification result is unlikely to generalize to mainstream medical imaging soon.

## Key papers
- **Uncovering Modality Discrepancy and Generalization Illusion for General-Purpose 3D Medical Segmentation** (2026-02-07) — coins the "generalization illusion" and shows catastrophic PET collapse, reframing how the field must evaluate generality.
- **Safety and accuracy follow different scaling laws in clinical large language models** (2026-05-05) — demonstrates evidence quality, not scale/retrieval/compute, drives clinical safety, decoupling safety from accuracy.
- **Counterfactual Evaluation Reveals Hidden Capability Profiles in Clinical LLMs and Agents** (2026-05-28) — CSS shows coverage and causal-sensitivity rankings are nearly opposite, exposing a universal reasoning blind spot.
- **CLR-voyance: Reinforcing Open-Ended Reasoning for Inpatient Clinical Decision Support with Outcome-Aware Rubrics** (2026-05-10) — a deployed 8B RL model beating GPT-5 via POMDP formulation and outcome-grounded rewards; a proof point for small specialized clinical models.
- **Designing UNICORN** (2026-03-03) — first unified, leakage-controlled cross-domain (radiology/pathology/text) benchmark with a representation-isolating two-step protocol.
- **MedFM-Robust** (2026-05-18) — first systematic robustness benchmark (40 perturbations, 8 modalities); finds fine-tuning strategy, not architecture, governs robustness.
- **Revisiting 2D Foundation Models for Scalable 3D Medical Image Classification** (2025-12-15) — AnyMC3D shows adapted general-purpose 2D FMs match 3D medical FMs at 1/40th the trainable parameters.
- **Free Lunch in Medical Image Foundation Model Pre-training via Randomized Synthesis and Disentanglement** (2026-02-12) — RaSD establishes zero-real-image synthetic pretraining as competitive across 56 tasks, a privacy-preserving data path.
- **EyeWorld: A Generative World Model of Ocular State and Dynamics** (2026-03-14) — moves medical FMs from static representation to explicit time-conditioned disease-progression dynamics.
- **UniX: Unifying Autoregression and Diffusion for Chest X-Ray Understanding and Generation** (2026-01-16) — resolves the understanding/generation objective conflict via a decoupled dual-branch design.
- **Specializing Foundation Models via Mixture of Low-Rank Experts for Comprehensive Head CT Analysis** (2026-02-28) — MoLRE introduces input-conditional mixture-of-adapters, addressing LoRA knowledge interference for multi-label clinical tasks.
- **Project Imaging-X** (2026-03-29) — quantifies the fragmented, long-tailed dataset landscape and proposes metadata-driven fusion as the path to scale.
- **A Hierarchical Benchmark of Foundation Models for Dermatology** (2026-01-18) — documents the "granularity gap" where coarse-screening leaders fail at fine-grained diagnosis.
- **Why Specialist Models Still Matter: A Heterogeneous Multi-Agent Paradigm** (2026-05-28, ICML 2026) — argues collaborative generalist+specialist+human intelligence beats any monolithic medical FM.
