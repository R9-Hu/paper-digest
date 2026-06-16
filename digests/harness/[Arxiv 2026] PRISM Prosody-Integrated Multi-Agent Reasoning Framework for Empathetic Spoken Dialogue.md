---
title: "PRISM: Prosody-Integrated Multi-Agent Reasoning Framework for Empathetic Spoken Dialogue"
authors: ["Wen Zhang", "Xiaocui Yang", "Zhuoyue Gao", "Shi Feng", "Daling Wang", "Yifei Zhang"]
source: "Arxiv"
venue: "INTERSPEECH 2026"
published: "2026-06-11"
published_time: "2026-06-11T04:59:33+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12902"
url: "http://arxiv.org/abs/2606.12902v1"
pdf: "paper/harness/[Arxiv 2026] PRISM Prosody-Integrated Multi-Agent Reasoning Framework for Empathetic Spoken Dialogue.pdf"
---

# PRISM: Prosody-Integrated Multi-Agent Reasoning Framework for Empathetic Spoken Dialogue

*🕒 **Published (v1):** 2026-06-11 04:59 UTC  ·  **Source:** Arxiv  ·  **Venue:** INTERSPEECH 2026  ·  [link](http://arxiv.org/abs/2606.12902v1)*

## TL;DR
PRISM is a four-agent framework for empathetic spoken dialogue that preserves prosodic information lost in cascade ASR→TTS pipelines by translating acoustic cues into natural-language descriptions before LLM reasoning. It decouples perception, coordination, response generation, and speech synthesis into specialized agents (Perceiver, Manager, Responder, Vocalizer) with on-demand external knowledge retrieval. It consistently outperforms both cascade and end-to-end speech baselines on the AvaMERG benchmark.

## Problem
Cascade spoken dialogue systems (ASR→LLM→TTS) irreversibly discard prosodic/emotional cues during transcription, limiting genuine empathy to the textual domain. End-to-end speech models preserve acoustics implicitly but lack interpretable intermediate representations and are inflexible for knowledge integration. No prior work jointly addresses prosodic perception, emotional reasoning, external knowledge augmentation, and expressive speech synthesis in a unified, interpretable architecture.

## Method
PRISM comprises four coordinated agents:

1. **Perceiver**: Extracts a structured paralinguistic state from raw speech using Whisper (ASR), emotion2vec (emotion label + confidence), WebRTC VAD (pause ratio, speaking rate), RMS energy statistics, and a heuristic certainty score combining rate/pause/filler features.
2. **Manager**: Applies a two-stage prosody-to-language translation — rule-based threshold mapping of numeric attributes to text labels, then LLM few-shot prompting to produce a coherent natural-language prosody description `D`. Also runs response-level verification, checking emotion/intensity/strategy alignment and issuing minimal revision suggestions when inconsistencies are detected.
3. **Responder**: Fine-tuned LLM (Qwen2.5-7B or LLaMA-3.1-8B on TOOL-ED) that jointly decides whether to invoke COMET-BART commonsense retrieval and generates response text `R` plus target emotion category `e` and intensity `λ`, conditioned on transcript `T`, prosody description `D`, and dialogue history `H`.
4. **Vocalizer**: StyleTTS2-based TTS with a two-stage prosody parameter computation — base parameters `(α, β, d, κ)` set from predicted `(e, λ)`, then adaptively refined using user paralinguistic attributes `a`. Also applies text-side prosody shaping (pause insertion, punctuation adjustment) before synthesis.

## Key Contributions
- Multi-agent decoupled architecture with feedback-driven coordination across speech perception, reasoning, and synthesis.
- Prosody-to-language translation mechanism converting low-level acoustic features into interpretable natural-language descriptions compatible with LLM reasoning.
- On-demand knowledge invocation (rather than always-on or always-off) via COMET-BART, enabling plug-and-play knowledge source updates without retraining.
- Response-level verification module in Manager that checks empathy-prosody consistency and triggers targeted revision.
- Two-stage adaptive prosody parameter computation in Vocalizer, propagating emotional intent from Responder while mirroring user's prosodic characteristics.

## Results
On AvaMERG test set (vs. best single baseline Qwen2.5-Omni-7B):

- **ROUGE-1/2/L**: PRISM(Qwen) 0.2254/0.0745/0.1872 vs. 0.1880/0.0542/0.1555 (+19.8%/+37.5%/+20.4%)
- **BERTScore**: PRISM(Qwen) 0.8792, PRISM(Llama) 0.8801 vs. best baseline 0.8746
- **BLEU-4**: PRISM(Qwen) 0.0571 vs. best baseline 0.0352 (Qwen2.5-Omni)
- **Dist-2**: PRISM(Llama) 0.2574 vs. best baseline 0.2380 (Qwen2.5-Omni)
- Human evaluation (5-point Likert, 100 samples, ICC=0.81): PRISM shows comparable or superior scores on all six dimensions (Empathy, Informativity, Fluency, Consistency, Prosodic Appropriateness, Audio-Text Alignment) vs. LLaMA-Omni2 and OpenS2S
- GPT-4o A/B evaluation: PRISM achieves higher win rate vs. OpenS2S and LLaMA-Omni2 on empathy, fluency, and consistency
- Ablation: removing prosody description, removing knowledge, or forcing always-on knowledge all degrade performance across all metrics

## Limitations
- Only the Responder is fine-tuned; Manager relies on GPT-3.5-Turbo API, introducing external dependency, latency, and cost.
- Evaluation confined to a single dataset (AvaMERG); generalization to other languages, domains, or acoustic conditions is unverified.
- Prosody-to-language translation uses fixed rule-based thresholds for numeric binning, which may not generalize across speakers or recording conditions.
- The heuristic certainty score (Eq. 6) is hand-tuned with fixed weights; no validation that these weights are optimal.
- No latency or computational cost analysis is reported, making real-time deployment suitability unclear.
- StyleTTS2 reference-based voice cloning requires a reference audio; behavior with mismatched references is not discussed.

## Relevance to Harnesses / Meta-Harnesses
PRISM is a domain-specific multi-agent harness where four specialized agents are orchestrated in a directed pipeline with feedback loops — a canonical harness pattern applied to spoken dialogue. The Manager agent exemplifies a meta-harness role: it coordinates inter-agent information flow, translates between representational modalities (acoustic→language), and enforces consistency via post-hoc verification before passing outputs downstream. The on-demand tool-invocation design in Responder (decide→retrieve→generate) mirrors the tool-calling orchestration patterns studied in meta-harness research, and the ablation study isolating each component's contribution is the kind of modular analysis useful for understanding harness design tradeoffs.

## Tags
#multi-agent #spoken-dialogue #empathy #prosody #tool-calling #pipeline-orchestration #speech-llm #multimodal
