---
title: "Cross-Modal Masked Compositional Concept Modeling for Enhancing Visio-Linguistic Compositionality"
authors: ["Wei Li", "Zhen Huang", "Xinmei Tian"]
source: "Arxiv"
venue: "ACL 2026"
published: "2026-06-11"
published_time: "2026-06-11T12:45:25+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13288"
url: "http://arxiv.org/abs/2606.13288v1"
pdf: "paper/vlm/[Arxiv 2026] Cross-Modal Masked Compositional Concept Modeling for Enhancing Visio-Linguistic Compositionality.pdf"
---

# Cross-Modal Masked Compositional Concept Modeling for Enhancing Visio-Linguistic Compositionality

*🕒 **Published (v1):** 2026-06-11 12:45 UTC  ·  **Source:** Arxiv  ·  **Venue:** ACL 2026  ·  [link](http://arxiv.org/abs/2606.13288v1)*

## TL;DR
MACCO (MAsked Compositional Concept MOdeling) is a fine-tuning framework for CLIP-like models that masks compositional concepts (relations, attributes, word order) in one modality and reconstructs them using full context from the other modality—without requiring hard negative samples. It achieves state-of-the-art compositional understanding across five benchmarks while preserving general representation quality and transferring gains to text-to-image generation and MLLMs.

## Problem
Contrastive VLMs like CLIP exhibit "bag-of-words" behavior: they fail to capture object relations, attribute-object bindings, and word order dependencies. Existing remedies rely on hard negative mining (rule-based, LLM-generated, or diffusion-synthesized), which is costly, noisy, and can induce oversensitivity to paraphrase. The richer compositional signal already latent in paired image-text data is underexploited.

## Method
MACCO operates at fine-tuning time on ~110k MSCOCO pairs. Compositional concepts are extracted from text via a scene graph parser (yielding token masks M_T) and from images via GroundingDINO (yielding patch masks M_I). Masked and unmasked sequences are both passed through shared CLIP encoders. A **global-to-local semantic injection** fuses each masked token's representation with the global CLS feature (averaged 50/50) to compensate for causal text encoding and weak CLIP local supervision.

Two cross-modal predictors operate only at training time:
- **Text predictor** (DT): 2-layer cross-attention from enriched masked text tokens → full image features → vocabulary classification (MLM-style loss L_MLM).
- **Image predictor** (DI): 3-layer cross-attention from enriched masked image patches → full text features → pixel MSE reconstruction (MIM-style loss L_MIM). Image gradient is stop-gradiented in both predictors to focus optimization on the text encoder.

Two auxiliary objectives:
- **MCA (Masked-augmented Cross-Modal Alignment)**: extends InfoNCE contrastive loss by treating masked inputs as soft negatives in both i2t and t2i directions.
- **MIR (Masked-augmented Intra-Modal Regularization)**: intra-modal contrastive loss between masked and full features within each modality to prevent representational collapse.

Total loss: L_total = L_MCA + λ1·L_MIR + λ2·L_MLM + λ3·L_MIM. Predictors are discarded at inference; model architecture is identical to standard CLIP.

## Key Contributions
- Cross-modal masked compositional concept reconstruction framework that avoids explicit hard negative construction.
- Global-to-local semantic injection (parameter-free) to enrich local masked tokens with global contextual semantics.
- MCA loss: integrates masked-input CLS features as soft negatives into contrastive learning.
- MIR loss: prevents masked feature collapse and regularizes masked-to-full feature deviation intra-modally.
- Plug-and-play compatibility with hard negative methods (NegCLIP, CE-CLIP), yielding additive gains.
- Demonstrated transfer to Stable Diffusion (text encoder swap) and LLaVA-1.5-7B (vision encoder swap) without additional fine-tuning of the downstream model.

## Results
Baseline backbone: CLIP ViT-B/32, fine-tuned 5 epochs on MSCOCO, single A100.

**vs. CLIP (zero-shot):**
- ARO-Relation: +14.4% (58.7 → 73.1)
- ARO-Order: +21.9% (54.1 → 76.0)
- SugarCrepe avg: +8.3%

**vs. CLIP-FT (contrastive fine-tune only):**
- ARO-Relation: +8.8% (64.3 → 73.1)
- ARO-Order: +26.9% (49.1 → 76.0)
- SugarCrepe Relation: +6.0%
- VL-Checklist Relation: +9.3%

**vs. CLIP-CAE (prior best):**
- SugarCrepe Relation: +4.1%
- VL-Checklist Relation: +4.8%
- Consistent gains on VALSE and What's-up; ARO-Order not reported for CLIP-CAE.

**Hard positive robustness (Kamath et al., 2024):**
- SWAP subset Aug. Test Acc.: +4.6% over CLIP-FT (53.8 vs. 48.4)

**Combined with hard negatives:**
- +MACCO over NegCLIP: VL-Checklist Relation +3.1%; CE-CLIP: +1.9%

**Zero-shot classification (11 datasets):** -1.5% avg vs. CLIP (59.5 → 58.0); linear probe -0.4%.

**STS (SICK-R Pearson):** +2.5% over CLIP-FT (70.5 vs. 68.0); +1.2% over CLIP-CAE.

**T2I (SD 1.5, T2I-CompBench):** BLIP-VQA color 0.3651 → 0.3815; texture 0.4135 → 0.4236.

**MLLM (LLaVA-1.5-7B, AMBER):** Attribute 75.8 → 76.5; Relation 68.4 → 69.3; MME Perception 1447.1 → 1452.3.

Consistent improvements also reported on ViT-B/16, ViT-L/14, and SigLIP (Appendix I).

## Limitations
- Requires lightweight pre-processing (scene graph parsing + GroundingDINO grounding) per training example, introducing a pipeline dependency not present in end-to-end methods.
- Training overhead is higher than CLIP-CAE due to two additional predictors and prediction heads (removed at inference but increase training cost).
- Designed for contrastive architectures (CLIP-family); applicability to generative VLMs (BLIP, captioning models) has not been explored.
- Lacks interpretability mechanisms (concept probing, attribution tracing) to explain which concepts are captured.
- Attribute binding remains harder to improve than relation understanding, consistent with prior work—root cause not addressed.
- General zero-shot classification performance slightly degraded (-1.5%) relative to base CLIP.

## Relevance to Vision-Language Models
MACCO directly targets the well-documented compositional weakness of CLIP-style contrastive VLMs, offering an alternative training signal that does not require hard negative synthesis. The masked cross-modal reconstruction approach parallels BERT-style self-supervised learning but extends it to paired multimodal grounding, making it relevant to any researcher studying how to inject structural linguistic knowledge into dual-encoder architectures. The finding that compositional improvements transfer to downstream Stable Diffusion and LLaVA systems without retraining those models has practical significance for the broader VLM ecosystem. The compatibility with existing hard-negative pipelines positions MACCO as a composable module rather than a competing paradigm.

## Tags
#vlm #clip #compositionality #masked-modeling #contrastive-learning #attribute-binding #cross-modal #fine-tuning
