---
title: "EChO-Agent: Evidence Chain Orchestration Agent for Audio Reasoning"
authors: ["Siyuan Zhang", "Jian Zong", "Junyu Wang", "Peiyuan Jiang", "Jiahao Yan", "Jingyu Zhang", "Tianrui Wang", "Xiaobao Wang", "Longbiao Wang", "Jianwu Dang"]
source: "Arxiv"
venue: "INTERSPEECH 2026"
published: "2026-06-13"
published_time: "2026-06-13T06:05:59+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.15141"
url: "http://arxiv.org/abs/2606.15141v1"
pdf: "paper/harness/[Arxiv 2026] EChO-Agent Evidence Chain Orchestration Agent for Audio Reasoning.pdf"
---

# EChO-Agent: Evidence Chain Orchestration Agent for Audio Reasoning

*🕒 **Published (v1):** 2026-06-13 06:05 UTC  ·  **Source:** Arxiv  ·  **Venue:** INTERSPEECH 2026  ·  [link](http://arxiv.org/abs/2606.15141v1)*

## TL;DR
EChO-Agent is a modular, tool-augmented agent framework that decomposes complex audio question answering into a four-stage pipeline: Tool → Evidence → Reason → Verify. The key insight is that raw tool outputs must be actively distilled into a structured evidence chain before being fed to the reasoning model, not passed through directly. On the MMAR benchmark it achieves 71.0% accuracy and 63.0 rubric score, ranking 5th in the Interspeech 2026 Audio Reasoning Challenge Agent Track.

## Problem
Large Audio Language Models (LALMs) lack question-conditioned perception, produce weakly grounded reasoning chains, cannot revisit audio to recover missed cues, and have no mechanism to verify evidence–answer consistency. Prior tool-augmented approaches (AuTAgent, AudioRouter, CoFi-Agent, AudioRAG) improve acoustic perception but pass raw tool outputs directly to the reasoner, introducing distracting context that can degrade inference rather than improve it.

## Method
EChO-Agent uses a fixed four-stage pipeline with two distinct LLM roles:

1. **Tool stage** — a question-type-conditioned static dispatcher selects a predefined tool combination from four classes: Audio Event Detection (YAMNet), ASR (Whisper), Speech Emotion Recognition (SpeechBrain/wav2vec2), and Music Analysis (Essentia). Failed calls are retried up to 2× then marked `[UNAVAILABLE]` to suppress hallucination.

2. **Evidence stage** — DeepSeek-V3 distills raw observations O into a compact evidence set E via three structured operations: relevance filtering, cross-observation synthesis (conflict resolution by confidence/specificity), and evidence structuring into a decision-ordered chain.

3. **Reason stage** — Qwen-3-Omni-Instruct receives raw audio + question + E, generates two candidate answers ŷ⁽¹⁾ and ŷ⁽²⁾ under different temperature/evidence-ordering configurations, with diagnostic feedback from the prior verification pass injected when retrying.

4. **Verify stage** — the orchestrator LLM performs format compliance repair, reasoning–answer consistency checking, and dual-pass arbitration: if candidates agree, the shared answer is selected; if they disagree, the verifier picks the candidate with stronger evidence alignment, avoiding expensive majority voting.

## Key Contributions
- Four-stage Tool → Evidence → Reason → Verify pipeline that cleanly separates perception, evidence construction, grounded reasoning, and output validation.
- LLM-based evidence integration module (DeepSeek-V3) that filters, synthesizes, and structures heterogeneous multi-tool outputs into a question-tied evidence chain rather than concatenating raw outputs.
- Dual-pass arbitration with targeted feedback: two reasoning candidates with varied configurations, arbitrated by evidence alignment rather than answer frequency.
- Ablation demonstrating that unfiltered tool output *harms* performance (removing evidence integration drops below the tool-free end-to-end baseline).

## Results
- **Full pipeline**: 71.0% accuracy, 63.0 rubric score on MMAR (5th place, Agent Track).
- **vs. Qwen-3-Omni-Instruct baseline**: +2.3 accuracy points (68.7→71.0), +4.3 rubric points (58.7→63.0).
- **Ablation on MMAR**:
  - w/o Evidence Integration: 65.4% / 56.9 rubric — largest drop, falls below the tool-free baseline (68.7 / 58.7).
  - w/o Observation (tools disabled): 69.2% / 60.2 rubric — −1.8% accuracy, −2.8 rubric.
  - w/o Verification: 69.1% / 61.5 rubric — −1.9% accuracy, −1.5 rubric.
- Best average accuracy (71.0%) among all compared models in Table 1, including Gemini 2.0 Flash (65.6%) and Qwen-3-Omni-thinking (69.0%).

## Limitations
- Sound-modality granularity is bounded by YAMNet's coarse frame-level event labels, which limit fine-grained sound understanding and remain a bottleneck on sound-centric questions.
- No dynamic tool selection — static dispatch may miss edge cases where question type is ambiguous.
- Tool uncertainty and cross-tool conflict resolution are acknowledged as future work, not addressed by the current system.
- Gains over baseline are modest in absolute accuracy (+2.3%), though rubric improvement (+4.3) reflects the process-quality focus of the challenge.

## Relevance to Harnesses / Meta-Harnesses
EChO-Agent is a direct instantiation of the meta-harness pattern: an orchestrator LLM (DeepSeek-V3) manages a heterogeneous tool fleet, integrates their outputs through a structured distillation stage, then hands a cleaned context to a specialist model (Qwen-3-Omni) for domain reasoning, followed by a verification pass. The finding that unfiltered tool output *degrades* performance is directly actionable for harness designers — it argues for mandatory evidence-distillation middleware between tool execution and the reasoning LLM, not raw context injection. The dual-pass arbitration with targeted feedback also illustrates a lightweight alternative to majority-vote self-consistency within a harness loop.

## Tags
#agent-framework #tool-augmented #audio-reasoning #evidence-chain #multi-stage-pipeline #orchestration #chain-of-thought-verification #lalm
