---
title: "On the Adversarial Robustness of Multimodal LLM Judges"
authors: ["Zihan Wang", "Guansong Pang", "Zelin Liu", "Wenjun Miao", "Jin Zheng", "Xiao Bai"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T05:30:20+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15608"
url: "http://arxiv.org/abs/2606.15608v1"
pdf: "paper/vlm/[Arxiv 2026] On the Adversarial Robustness of Multimodal LLM Judges.pdf"
---

# On the Adversarial Robustness of Multimodal LLM Judges

*🕒 **Published (v1):** 2026-06-14 05:30 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15608v1)*

## TL;DR
MLLM judges—widely deployed for image quality and safety evaluation—are highly vulnerable to adversarial perturbations that inflate their scores. This paper introduces RobustMLLMJudge, the first systematic framework for auditing this vulnerability, and proposes MGSIA, a transferable attack that combines token-level affirmative semantic induction with representation-level manifold alignment to fool heterogeneous judge protocols simultaneously.

## Problem
MLLMs are increasingly used as automated evaluators (for text-to-image quality, text-image alignment, and safety compliance), yet their adversarial robustness has not been studied. An attacker who can add imperceptible perturbations to a candidate image could inflate leaderboard rankings, bypass content-safety filters, or inject biased reward signals into RLAIF pipelines. Existing adversarial attacks target MLLMs as general-purpose models and fail to generalize across the heterogeneous evaluation protocols (token-probability scoring, fine-grained decomposition, direct judge prompting) used in practice.

## Method
**RobustMLLMJudge Framework**: Categorizes MLLM judges into three protocol families—Token Probability Scoring (e.g., VQAScore, Ensemble), Fine-grained Decomposition (e.g., TIFA, DSG, CLUE), and MLLM-as-a-Judge Prompting (e.g., VIEScore, T2I-CompBench++)—and evaluates them under image degradation, handcrafted, and learnable perturbation attacks.

**MGSIA (Manifold-Guided Semantic Induction Attack)**: A two-objective optimization method constrained to L∞-norm perturbations (ε = 8/255), solved with 100-step PGD:

1. **Affirmative Semantic Induction (ASI)**: Decomposes the target semantic cue `t_tar` into fine-grained binary queries via an LLM generator, then minimizes negative log-probability of generating "Yes" for each query: `L_ASI(δ) = −E_{q∼G(t_tar)}[log P_F("Yes" | v+δ, q)]`. The single-token "Yes" anchor avoids gradient attenuation from long-sequence targets.

2. **High-Score Manifold Alignment (HMA)**: Offline, identifies top-K scoring proxy samples under multiple proxy protocols and extracts hidden-state centroids `µ_p` at the last-prompt-token position. During attack optimization, minimizes MSE between the adversarial image's hidden states and these centroids: `L_HMA(δ) = E_{p∼P}[||h_F(v+δ, p) − µ_p||²_2]`. This pulls adversarial representations toward the latent region genuine high-scoring images occupy, improving transferability across unseen protocols.

Combined objective: `δ* = argmin_{||δ||_∞ ≤ ε} [L_ASI(δ) + λL_HMA(δ)]`.

## Key Contributions
- **RobustMLLMJudge**: First comprehensive evaluation framework covering three judge protocol families across quality and safety tasks, with nine adapted baseline attacks under white-box, black-box, and gray-box settings.
- **Empirical finding**: All three judge protocol families are vulnerable to score-inflating attacks; however, naive adaptations of existing attacks are partially constrained by the tight threat model (attacker cannot modify prompts/protocols) and protocol heterogeneity.
- **MGSIA**: Novel attack that bypasses protocol specificity by targeting shared binary semantic verification underlying all three judge types, achieving superior cross-protocol and cross-model transferability.

## Results
- **LLaVA-1.5-7B, quality (VQAScore)**: MGSIA achieves 98.59 (+35.59 over benign 63.00); nearest baseline (Target Text Embedding) achieves 79.82 (+16.82).
- **LLaVA-1.5-7B, quality (DSG)**: MGSIA 98.06 (+10.66); second-best 91.997 (+4.59) from Target Text Embedding.
- **LLaVA-1.5-7B, quality (TIFA)**: MGSIA 94.00 (+9.17).
- **Qwen2.5-VL-7B, quality (VQAScore)**: MGSIA 89.04 (+13.64); Target Text Embedding 86.69 (+11.29).
- **Qwen2.5-VL-7B, quality (VIEScore)**: MGSIA 96.58 (+14.26).
- **Safety (Fig. 1, qualitative)**: LLaVAGuard score inflated from 11.20 → 54.89; Ensemble safety score inflated from 32.14 → 60.21 under adversarial perturbation.
- MGSIA consistently ranks first or second across all judge protocols and both MLLM backbones tested.

## Limitations
- Evaluation is restricted to score-inflating attacks; score-deflating attacks (e.g., suppressing a legitimate high-quality image) are not studied.
- The framework requires knowledge of the proxy protocols used to compute high-score manifold centers, which may not always match the target judge's internal structure.
- The paper text is truncated before full safety-task quantitative tables; complete safety transfer results are not available in the provided excerpt.
- MGSIA's transferability to black-box settings with no surrogate model access is not fully characterized in the provided text.
- Defenses against MGSIA are not proposed, leaving the field without a clear mitigation direction.

## Relevance to Vision-Language Models
This paper directly addresses a critical but underexplored failure mode of VLMs deployed as automated judges—a role that is becoming central to RLHF/RLAIF pipelines for text-to-image models and content moderation systems. It reveals that standard MLLM architectures (LLaVA, Qwen-VL) share a structural vulnerability: their intermediate representations can be steered toward high-score manifolds via imperceptible pixel perturbations, undermining the trustworthiness of any evaluation system built on them. For VLM researchers, this raises fundamental questions about the reliability of MLLM-based benchmarks and reward signals, and motivates adversarially robust training or protocol-hardening as a new research axis.

## Tags
#vlm #adversarial-robustness #mllm-as-a-judge #image-quality-evaluation #safety-evaluation #adversarial-attack #text-to-image #automated-evaluation
