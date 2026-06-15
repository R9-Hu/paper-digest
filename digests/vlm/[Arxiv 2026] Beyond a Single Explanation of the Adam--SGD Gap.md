---
title: "Beyond a Single Explanation of the Adam--SGD Gap"
authors: ["Chenxiang Zhang", "Rustem Islamov", "Enea Monzio Compagnoni", "Jun Pang", "Aurelien Lucchi", "Antonio Orvieto"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14259"
url: "http://arxiv.org/abs/2606.14259v1"
pdf: "paper/vlm/[Arxiv 2026] Beyond a Single Explanation of the Adam--SGD Gap.pdf"
---

# Beyond a Single Explanation of the Adam--SGD Gap

## TL;DR
This paper challenges the prevailing single-factor explanations for why Adam outperforms SGD, showing through controlled experiments across language, vision, genomics, and graph tasks that the gap arises from nontrivial interactions between data properties and architecture design. The unifying empirical finding is a crossover batch size—below which SGD can match or beat Adam, above which Adam dominates—that shifts depending on architecture and data. A geometry-based theoretical model using SignSGD as an Adam proxy predicts this batch-size-dependent crossover via the smoothness ratio r = L∞/L₂.

## Problem
Prior explanations for the Adam–SGD performance gap—heavy-tailed vocabulary distribution, softmax-attention heterogeneity, component-level Hessian heterogeneity, large batch size—are each studied in isolation and mostly within Transformer-based LLM settings, leaving their relative importance and interactions uncharacterized. No unified account predicts when each hypothesis holds, when it fails, or how they interact.

## Method
Controlled empirical study across four modalities (language, vision, genomics, graphs) using both Transformer (GPT, ViT, GRIT) and non-Transformer (GCNN, ResNet, GAT, GDN) architectures. Key design choices: joint hyperparameter sweeps over learning rate η and momentum β for both Adam and SGD; tied Adam parameterization β₁=β₂ to match SGD's tuning budget; global gradient-norm clipping; bfloat16; cosine schedule with 10% warmup. Gap is defined as Δ* = L*\_Adam − L*\_SGD over final training loss. Batch size is treated as a central variable, swept from B=4 to B=65536 under fixed training tokens. Architecture interpolation experiments (ResNet50 → ConvNeXt on ImageNet21K) isolate the contribution of individual design choices (BatchNorm→LayerNorm, ReLU→GeLU, Dense→Depthwise). Theory uses NSGD vs. SignSGD with momentum bounds from Kovalev [2025], characterizing gap regimes via the ratio r = L∞/L₂ of ℓ∞ to ℓ₂ smoothness constants.

## Key Contributions
- Demonstrates empirically that no single factor (vocabulary imbalance, softmax-attention, component heterogeneity) is necessary or sufficient to explain the Adam–SGD gap across diverse settings.
- Identifies a crossover batch size as the unifying pattern: SGD advantage at small B, Adam advantage at large B, with the crossover point determined jointly by data and architecture.
- Shows that architectural design choices (GeLU over ReLU, LayerNorm over BatchNorm) progressively shift optimizer preference from SGD toward Adam, with a 3-modification interpolation from SGD>Adam (+13%) to Adam>SGD (−15.5%) on ImageNet21K.
- Demonstrates that gradient norm clipping plus modern architecture choices reduce the ViT class-imbalance gap by ≈93%, challenging Kunstner et al. [2024]'s class-imbalance explanation.
- Provides a theoretical gap model (SignSGD vs. NSGD under Kovalev bounds) with two regimes: Regime I (r < d^{1/3}) admits a batch-size crossover; Regime II (r > d^{1/3}) favors SGD for all B.
- Connects training regime (over- vs. underparametrized) to gap behavior: the gap shrinks under multi-epoch overparametrized training but persists in the modern one-epoch underparametrized LLM regime.

## Results
- GPT vs. GCNN on FineWeb at B=1024: gap persists after removing softmax-attention (Δ* = −0.454 for GCNN vs. −0.316 for GPT), SGD ≈10% slower for GCNN.
- GPT on HG38 genomics with char tokenizer (v=5, near-uniform distribution): Adam>SGD with Δ* = −0.127 (≈11% SGD slowdown), refuting the vocabulary-imbalance hypothesis.
- GRIT on ZINC250K (regression, no class structure): Δ* = −0.026 MAE gap, ≈20% worse for SGD.
- ViT on heavy-tailed ImageNet1K with modern recipe + gradient clipping: gap reduced to Δ* = −0.012 (≈3% SGD slowdown) vs. Δ* = −0.183 in the original SimpleViT setup—a 93% reduction.
- ViT on ImageNet21K at B=256: SGD>Adam with Δ* = +0.851 (≈12% Adam slowdown), showing component heterogeneity does not guarantee Adam advantage.
- Architecture interpolation (ImageNet21K, one epoch): ResNet50 baseline SGD>Adam +13.00%; +LayerNorm: +7.29%; +GeLU: −0.49%; +Depthwise: −11.86%; full ConvNeXt: −15.53%.
- Hybrid optimizer (GPT, FineWeb): using Adam only on the output head reduces the all-Adam vs. all-SGD gap by 69%; adding embedding reduces it by 33% incremental; full combination reduces to 0.98% remaining gap.
- Batch size crossover generalizes across all 8+ dataset–architecture combinations tested; I21K configurations have the largest crossover batch sizes, consistent with SGD's historical strength on vision.

## Limitations
- Experiments fix training tokens rather than wall-clock time, conflating step count with batch size; the step-count confounder is acknowledged but only partially addressed in an appendix.
- Tied momentum parameterization β₁=β₂ for Adam deviates from standard (β₁, β₂)=(0.9, 0.999); independent tuning of β₂ can further close the gap at small batch sizes (reported only in ablation).
- Theory uses SignSGD and NSGD as proxies for Adam and SGD, respectively; the connection between Adam and SignSGD is approximate (especially without gradient clipping or with ε≠0).
- Theoretical model assumes a quadratic stochastic loss and fixed gradient noise variance σ²/B; this may not capture the heterogeneous noise structure of deep networks.
- Generalization performance (test metrics) is deferred to appendices and not the primary analysis target.
- The crossover batch size and slope are characterized descriptively; no predictive formula is given to compute them from first principles for a new architecture–dataset pair.

## Relevance to Vision-Language Models
VLMs inherit both the Transformer architecture and the large-scale one-epoch (underparametrized) training regime, making the Adam-vs-SGD question directly operational for practitioners choosing or developing optimizers. The paper's finding that architectural design choices—especially normalization (LayerNorm) and activation (GeLU), both standard in VLMs—progressively shift optimizer preference toward Adam helps justify why Adam-family methods dominate VLM training. Conversely, the result that SGD can outperform Adam for ViT on ImageNet21K at small batch sizes signals that multimodal pretraining at low batch sizes (constrained by memory) may warrant reconsideration of SGD with tuned momentum. The crossover batch size framework provides a principled lens for understanding optimizer behavior in VLM scaling experiments where batch size varies across compute budgets.

## Tags
#optimization #adam #sgd #transformer #vision-language #training-dynamics #batch-size #architecture
