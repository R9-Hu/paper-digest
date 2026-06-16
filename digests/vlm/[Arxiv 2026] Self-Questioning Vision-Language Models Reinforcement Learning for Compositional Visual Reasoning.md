---
title: "Self-Questioning Vision-Language Models: Reinforcement Learning for Compositional Visual Reasoning"
authors: ["Saraswathy Amjith"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T07:42:34+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.15651"
url: "http://arxiv.org/abs/2606.15651v1"
pdf: "paper/vlm/[Arxiv 2026] Self-Questioning Vision-Language Models Reinforcement Learning for Compositional Visual Reasoning.pdf"
---

# Self-Questioning Vision-Language Models: Reinforcement Learning for Compositional Visual Reasoning

*🕒 **Published (v1):** 2026-06-14 07:42 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15651v1)*

## TL;DR
This paper proposes a self-questioning framework that trains a VLM (Qwen2.5-VL-3B) via GRPO reinforcement learning to decompose compositional visual questions into sub-question–answer chains, without any human-annotated reasoning demonstrations. The reward function jointly incentivizes structured format compliance and final answer correctness. Results on A-OKVQA show both RL training and the self-questioning format improve over the base model, though RL alone accounts for the majority of gains.

## Problem
State-of-the-art VLMs fail at compositional visual reasoning (multi-step questions requiring object identification, counting, spatial comparison, etc.) because they produce answers in a single forward pass with no intermediate reasoning. Existing remedies—chain-of-thought prompting, supervised fine-tuning on rationales, and visual programming—all depend on expensive human-authored reasoning traces or hand-designed tool libraries, limiting scalability.

## Method
The framework fine-tunes Qwen2.5-VL-3B-Instruct using GRPO. At inference, a system prompt instructs the model to emit alternating `Sub-question / Answer` pairs before a final answer; no example decompositions are provided. The binary reward function scores +1.0 only when the output contains at least one sub-question–answer pair **and** the normalized ground-truth answer appears as a substring of the final answer, −1.0 otherwise. GRPO samples G=8 completions per prompt, normalizes advantages within the group (eliminating a separate value network), and applies a KL-divergence penalty against the reference policy to prevent catastrophic forgetting. LoRA (rank 16, α=32, targeting q_proj/v_proj) keeps GPU memory within 48 GB. Training runs ~7,000 steps on 10,000-example subsets of CLEVR and A-OKVQA separately.

## Key Contributions
- First application of GRPO to a VLM for compositional visual reasoning, eliciting sub-question decomposition with no human reasoning demonstrations.
- A reward function that makes structural decomposition (not just answer correctness) a training objective.
- Empirical isolation of the self-questioning effect from the general RL effect via a matched Direct+GRPO baseline.
- Cross-domain transfer analysis showing that sub-question decomposition learned on synthetic CLEVR scenes transfers to real-world A-OKVQA images (+2.6%), whereas standard RL does not (+0.2%).
- Identification and characterization of the "format tax"—accuracy degradation on simple questions caused by unnecessary decomposition overhead.

## Results
- **A-OKVQA accuracy (500-example validation set):**
  - Base model: 46.8%
  - Direct+GRPO (A-OKVQA-trained): 51.6% (+4.8%)
  - SQ+GRPO (A-OKVQA-trained): 52.2% (+5.4%)
  - Self-questioning margin over direct RL: +0.6 pp
- **Cross-domain transfer to A-OKVQA from CLEVR-trained models:**
  - SQ+GRPO (CLEVR→A-OKVQA): 49.4% (+2.6% over base)
  - Direct+GRPO (CLEVR→A-OKVQA): 47.0% (+0.2% over base)
- **CLEVR accuracy:** Near ceiling for all models (97.4–98.6% direct prompt); A-OKVQA-trained SQ model drops to 81.0% on CLEVR with SQ prompt (format tax), recovers to 97.6% with direct prompt.
- **Per-category gains (A-OKVQA):** counting +50% over base, material identification +33%; losses on color recognition −37.5%, spatial relations −13.3%, activity identification −16.7%.

## Limitations
- Small model scale (3B with LoRA); larger models or full fine-tuning may yield qualitatively different trade-offs.
- Evaluated on only two VQA benchmarks (CLEVR, A-OKVQA); tasks requiring deeper multi-step reasoning may show larger self-questioning benefits.
- Self-questioning margin over direct RL is marginal (+0.6 pp), and ablations show RL output-distribution calibration dominates the gains.
- Model generates superficial sub-questions (paraphrases of the original) rather than genuinely decomposing on ~8% of A-OKVQA cases.
- Format tax: forcing decomposition on simple questions actively hurts accuracy; no adaptive mechanism to suppress sub-questions when unnecessary.
- Prompt-dependency: SQ-trained model reverts to near-baseline (47.8%) when evaluated with a direct prompt, indicating the learned behavior is tightly coupled to the SQ prompt structure.

## Relevance to Vision-Language Models
This work directly addresses a core weakness of compact VLMs—single-pass compositional reasoning—using a training signal (GRPO) that requires no human annotations, making it highly relevant to scalable VLM improvement research. The cross-domain transfer finding (decomposition strategy generalizing from synthetic to real-world images) is notable because it suggests RL can instill domain-general meta-reasoning skills rather than mere answer-level calibration. The format-tax analysis provides a concrete empirical counterpoint to blanket application of chain-of-thought-style reasoning, pointing toward adaptive decomposition as a necessary next step for VLM reasoning systems. The work also extends the DeepSeek-R1/GRPO paradigm from text-only LLMs into the multimodal setting at a practically trainable scale.

## Tags
#vlm #compositional-reasoning #reinforcement-learning #grpo #chain-of-thought #visual-question-answering #self-questioning #multimodal
