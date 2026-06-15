---
title: "Deep Reprogramming Distillation for Medical Foundation Models"
authors: ["Siyuan Du", "Yuhang Zhou", "Haolin Li", "Jiangchao Yao", "Haishuai Wang", "Hui Lin", "Ya Zhang", "Yanfeng Wang"]
source: "Arxiv"
venue: ""
published: "2026-05-06"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2605.04447"
url: "http://arxiv.org/abs/2605.04447v1"
pdf: "paper/med-foundation/[Arxiv 2026] Deep Reprogramming Distillation for Medical Foundation Models.pdf"
---

# Deep Reprogramming Distillation for Medical Foundation Models

## TL;DR
DRD (Deep Reprogramming Distillation) is a framework for adapting large medical foundation models into lightweight task-specific models by bridging task, domain, and architectural mismatches simultaneously. It introduces learnable reprogramming projectors on the teacher's intermediate features, co-trains them with the student via supervised and logits-level losses, and applies CKA-based feature distillation for robustness. Evaluated on 18 datasets across 8 foundation models, it consistently outperforms prior KD and PEFT baselines.

## Problem
Standard knowledge distillation (KD) assumes teacher and student share the same task, training strategy, and model family — assumptions violated when a large medical FM (e.g., ViT-based MedSAM) is distilled into a CNN (e.g., ResNet18, ShuffleNet). PEFT methods reduce training cost but not inference-time deployment cost. Combining PEFT+KD ignores structural and training-strategy inconsistencies, causing negative transfer: e.g., applying MobSAM or LoRA+KD from a ViT teacher to CNN students drops accuracy by up to 11.8 points on FIVES. Meanwhile, large FMs can underperform vanilla lightweight models on specialized tasks (MedSAM: 16.53 DSC on FIVES vs. ViT-Tiny: 83.06).

## Method
DRD has three core components operating on a coarse N-stage teacher–student block decomposition:

1. **Reprogramming Module**: For each teacher block i, a lightweight 3-layer convolutional projector ϕᵢ remaps the teacher feature map fᵢᵀ (shape C×H×W) to match the student's spatial/channel dimensions: fᵢᵀ→ˢ = ϕᵢ(fᵢᵀ).

2. **Deep Co-training Reprogramming**: The reprogrammed feature fᵢᵀ→ˢ is injected into student block i+1 onward, producing N "hybrid logits" {zᵢᵀ→ˢ}. These are trained with the same task loss as the student's own logits zˢ, plus KL divergence between hybrid and student logits (LKD = Σ KL(zᵢᵀ→ˢ, zˢ)). This co-training forces the projectors to produce student-compatible, task-relevant features without hand-crafted layer matching.

3. **CKA Distillation**: Feature-level alignment uses normalized HSIC (Centered Kernel Alignment) between reprogrammed teacher features and student features: LCKA = −HSIC(K,L)/√(HSIC(K,K)·HSIC(L,L)), computed per-stage. CKA is invariant to orthogonal transformations and insensitive to feature dimensionality, making it robust across architectural mismatches.

Total loss: Ltrain = Lsup + αLhybrid + βLKD + LCKA, with α,β initialized to 1 and linearly decayed.

## Key Contributions
- Unified one-stage framework jointly resolving task/domain discrepancy, teacher–student structural heterogeneity, and lightweight deployment — without backpropagating through the frozen FM backbone.
- Deep Co-training Reprogramming: end-to-end learned alignment that avoids heuristic stage-wise pretraining.
- CKA distillation for robust feature transfer under varied training conditions (random seeds, structure differences).
- Largest evaluation scope for FM downstream adaptation: 8 medical FMs (PMC-CLIP, RadDenseNet, LVM-Med, Merlin, MedSAM, MSA, Swin-UMamba, SAT) × 18 datasets × 2D/3D classification and segmentation.

## Results
- **BUSI (2D classification)**: DRD with ResNet18+PMC-CLIP reaches 88.31% accuracy, matching the teacher and surpassing vanilla (77.92%) and best KD baseline (83.12%).
- **FIVES (2D segmentation)**: ShuffleNet+MedSAM, vanilla=56.25 DSC → DRD=73.06 DSC (~17pp gain); ViT-Tiny+MedSAM vanilla=83.06 → DRD=88.35.
- **CDPRD (2D segmentation)**: ViT-Tiny+MedSAM DRD=95.33 DSC (highest across all methods).
- **BTCV-Gallbladder (3D segmentation)**: Unet3D vanilla=19.15 → DRD=43.80 (+24.6pp), versus best KD baseline (Hint: 27.23).
- **MSD-Spleen (3D)**: Unet3D vanilla=80.87 → DRD=89.83, exceeding teacher SAT (87.21).
- **3D classification (MMD)**: ResNet3D vanilla=55.14 → DRD=62.70 vs. best KD (Hint: 58.92).
- DRD is the only method in comparison that handles all of: efficient deployment, one-stage training, classification, segmentation, task discrepancy, and structural discrepancy simultaneously (per Table III).
- On heterogeneous teacher–student pairs (ViT→CNN), prior KD and LoRA+KD methods degrade performance; DRD consistently improves it.

## Limitations
- Stage count N is set coarsely and architecture-dependently; no ablation on sensitivity to N is reported.
- Hyperparameters α, β require a linear decay schedule; their initialization and schedule are fixed heuristically.
- Evaluation uses only publicly available, relatively small datasets for some modalities (USC: 206 images; BTC: 3264); performance on large-scale clinical cohorts is untested.
- The reprogramming projectors add training-time overhead (3-layer convs per stage) and require a GPU capable of holding the frozen FM in memory alongside student training.
- Text is truncated before MSD-Prostate and MSD-Pancreas 3D results are fully reported.
- No evaluation on multimodal FMs or large language model-integrated medical models (e.g., LLaVA-Med variants).

## Relevance to Foundation Models in Medicine
DRD directly addresses the central deployment bottleneck for medical FMs: the gap between a powerful but resource-heavy general-purpose model and the lightweight, task-specific models required in real clinical settings. By demonstrating that a single adaptation framework can work across CNN, ViT, and Mamba architectures and across 2D/3D classification and segmentation, it establishes a practical pathway for democratizing medical FM use without sacrificing specificity. The finding that large FMs like MedSAM can be substantially outperformed by a DRD-distilled ShuffleNet challenges the assumption that scale alone is sufficient, motivating richer downstream adaptation research. This work also highlights CKA as a principled, architecture-agnostic distillation signal — a reusable technique for the broader medical FM community.

## Tags
#knowledge-distillation #model-adaptation #parameter-efficient-fine-tuning #medical-imaging #segmentation #classification #model-compression #transfer-learning
