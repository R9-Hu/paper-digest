---
title: "ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages"
authors: ["Tanmoy Kanti Halder", "Akash Ghosh", "Subhadip Baidya", "Arijit Roy", "Sriparna Saha"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T16:59:42+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13572"
url: "http://arxiv.org/abs/2606.13572v1"
pdf: "paper/harness/[Arxiv 2026] ArogyaSutra A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages.pdf"
---

# ArogyaSutra: A Multi-Agent Framework for Multimodal Medical Reasoning in Indic Languages

*🕒 **Published (v1):** 2026-06-11 16:59 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13572v1)*

## TL;DR
ArogyaSutra is an actor-critic multi-agent framework for multimodal medical reasoning in seven low-resource Indic languages, paired with ArogyaBodha, a 40,857-sample multilingual multimodal medical QA benchmark. The framework combines tool-grounded visual perception, dual-memory error tracking, and adaptive code-switching, then distills the critic's corrective signals into the actor for inference-time efficiency.

## Problem
Existing medical MLLMs are English/Chinese-centric and use direct-prediction paradigms that fail at interleaved image-text reasoning in low-resource languages. Multilingual settings introduce two compounding failure modes: degraded logical fidelity and unstable language behavior (e.g., degenerate token repetition). No benchmark existed for systematic evaluation of step-by-step multimodal medical reasoning across Indic languages.

## Method
**ArogyaBodha (dataset):** 5,107 English QA pairs curated from eight heterogeneous sources (MedXpertQA, MedTrinity-25M, MedPix-2.0, MAMA-MIA, BRATS24, PMC-VQA, GMAI-MMBench, NEET-PG/FMGE), filtered by Gemini-2.5-Flash for clinical coherence, then translated into seven Indic languages via Gemini-2.5-Pro. Translation verified by reverse-translation cosine similarity (~0.93 CosineBack) and BLEU4, plus human review (avg 4.27/5).

**ArogyaSutra (framework):** Both Actor and Critic are instantiated from Qwen2.5-VL-7B. At each step *t*, the Actor invokes four grounding tools (open-vocabulary detection, zoom/crop, edge detection, depth analysis) then proposes a semantic action. The Critic scores confidence ŝ_t ∈ [0,1]; on failure it diagnoses whether the error is linguistic or logical — linguistic errors trigger English code-switching feedback, logical errors trigger feedback in the query's Indic language. Dual memory persists: short-term = last error E_{t-1}; long-term = summarize({E_0,...,E_{t-1}}). Halting: converge within 3 iterations or restart using long-term memory summary; two failed restarts discard the sample. Distillation: actor-critic rollouts produce a refined dataset D†; the Actor is fine-tuned via SFT on critic-approved trajectories (LoRA r=16, 4-bit, 3 epochs, ~12–15h on A100 80GB), removing the Critic at inference.

## Key Contributions
- **ArogyaBodha**: 40,857-sample multilingual multimodal medical benchmark covering 8 sources, 31 body systems, 21 clinical domains, 6 imaging modalities, 7 Indic languages + English; expert-verified QA pairs.
- **ArogyaSutra**: Actor-critic multi-agent framework with tool-grounded visual perception, dual-memory (short/long-term) error tracking, and language-aware code-switching for Indic medical reasoning.
- **Critic-to-actor distillation**: Encodes critic's structured corrective behavior into the actor via SFT on rollout trajectories, eliminating critic overhead at inference.
- **OOD evaluation**: Cross-lingual generalization tested on Spanish MIR residency exam questions translated to all seven Indic languages.

## Results
- ArogyaSutra (Qwen2.5-VL-7B) achieves **43.40% average accuracy** across 7 Indic languages, vs. GPT-4.0 (39.30), Mistral-Small-3.2-24B (42.27), Qwen3-VL-8B (40.71), MedGemma-4B (36.11), base Qwen2.5-VL-7B (34.21).
- **+9.2 pp** over base Qwen2.5-VL-7B; **+4.1 pp** over GPT-4.0.
- ArogyaSutra (Qwen2.5-VL-3B): **35.65%** avg vs. base 29.56% (+6.1 pp).
- OOD (MIR exam, 60 samples/language): ArogyaSutra **50.4%** vs. base Qwen2.5-VL-7B 35.0%, Qwen3-VL-8B 49.6%, MedGemma-4B 45.2%.
- Ablation: removing both critic and image grounding drops to 33.43%; removing image grounding alone drops to 26.86% avg (largest single-component drop of 16.54 pp); removing memory drops 12.83 pp.

## Limitations
- Covers only 7 of India's ~780 languages; dialects and code-mixed clinical language not represented.
- Actor-critic relies on the reliability of the underlying visual grounding tools; perception failures propagate through the reasoning chain despite corrective feedback.
- Still produces reasoning errors in rare or atypical clinical cases; not validated for real-world clinical deployment.
- Accuracy numbers (~43%) remain low in absolute terms, indicating significant headroom before clinical utility.

## Relevance to Harnesses / Meta-Harnesses
ArogyaSutra is a concrete domain-specific instantiation of the actor-critic multi-agent harness pattern: a structured control loop where one agent proposes actions and another evaluates and feeds back corrections, with explicit memory across iterations and a halting/restart policy. The distillation step — compiling the critic's corrective trajectories into the actor via SFT — is a form of harness-level knowledge transfer that collapses a multi-agent runtime into a single-agent inference artifact, directly relevant to cost/latency tradeoffs in meta-harness design. The dual-memory mechanism (short-term per-step error vs. long-term summarized trajectory) is a reusable architectural primitive for any harness requiring iterative self-correction. The explicit error-type diagnosis (linguistic vs. logical) as a routing signal for different feedback channels is an example of conditional dispatch logic within a harness loop.

## Tags
#multi-agent #actor-critic #medical-reasoning #multilingual #tool-grounding #memory #distillation #low-resource
