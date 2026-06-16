---
title: "LoSoNA: A Benchmark for Local Social Norm Adaptation in Group Conversations"
authors: ["Mateusz Winiarek", "Maksymilian Bilski", "Mateusz Jacniacki"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T16:23:00+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14600"
url: "http://arxiv.org/abs/2606.14600v1"
pdf: "paper/agentic-ai/[Arxiv 2026] LoSoNA A Benchmark for Local Social Norm Adaptation in Group Conversations.pdf"
---

# LoSoNA: A Benchmark for Local Social Norm Adaptation in Group Conversations

*🕒 **Published (v1):** 2026-06-12 16:23 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14600v1)*

## TL;DR
LoSoNA is a benchmark for evaluating whether LLM-based agents can infer and adapt to implicit local social norms in multi-party group chat, without being told those norms explicitly. Eight frontier and open-weight models are evaluated under four prompting conditions; naive prompting leaves most models below 37% accuracy, while explicit norm-aware prompting helps unevenly—Gemini 3.1 Pro reaches 84.2% and Claude Fable 5 reaches 81.6%.

## Problem
LLM agents deployed in group-chat settings face implicit, group-specific conversational norms that are never stated outright. Existing social-interaction benchmarks (Sotopia, SocialIQa, ToM benchmarks) are either dyadic, goal-oriented, or test third-person belief attribution—none isolate the capability of inferring and *acting on* a hidden local norm from conversational precedent in a first-person, multi-party setting.

## Method
Each LoSoNA scenario is generated from a tuple `(event_type, norm)` drawn from a taxonomy of 17 event types × 22 norm types (353 valid cells). A scenario generator produces a multi-turn group-chat transcript in which non-subject participants implicitly demonstrate the target norm; the subject model is then given one elicitor turn and must produce a single response without ever being shown the norm label. Scenarios are screened via a no-demonstration control: candidates are discarded if a Gemini-family naive baseline already responds compliantly without precedent, ensuring the benchmark targets norm inference rather than default assistant behavior.

Four subject-prompt conditions are evaluated: `naive` (no special instruction), `elicitor_only` (reply only to final message), `style_adaptation` (fit local tone/habits), and `norm_informed` (explicitly hints that a repeated local pattern may be present). A fixed Gemini 3.1 Pro Preview judge (temperature 0) scores each response for compliance with the hidden target norm using structured JSON reasoning. Primary metric is majority accuracy over K=3 sampled responses (accuracy-at-3), bootstrapped over 38 curated scenarios. Eight models were evaluated: GPT-5.5, Claude Opus 4.8, Claude Fable 5, Gemini 3.1 Pro, Qwen2.5-72B, Llama 3.3-70B, Mistral Medium 3.1, Gemma 3-27B (3,648 total subject responses).

## Key Contributions
- LoSoNA benchmark: a taxonomy-driven, human-curated, controlled single-turn evaluation for local social norm adaptation in multi-party chat (38 scenarios, 17 event types, 22 norms).
- No-demonstration screening procedure to ensure scenarios require norm inference from precedent rather than reflecting default assistant behavior.
- Systematic evaluation of four prompting conditions across eight frontier and open-weight models, with paired delta analysis (recovered failures vs. introduced regressions).
- Public dataset release on Hugging Face (`Humalike-ai/LoSoNA`).
- Sanity checks: 85% human-judge agreement on 100 audited responses; Claude Opus 4.8 as alternate judge preserves main qualitative patterns.

## Results
- **Naive condition (averaged across models):** 33.2% accuracy-at-3; most models 21–37%, Claude Fable 5 highest at 47.4%.
- **Norm-informed condition (averaged):** 46.1% accuracy-at-3.
- **Soft prompts** (`elicitor_only`: 32.6%, `style_adaptation`: 32.2%) do not consistently improve over naive.
- **Best results under norm-informed:**
  - Gemini 3.1 Pro: 84.2% (+47.4 pp over its naive 36.8%)
  - Claude Fable 5: 81.6% (+34.2 pp over its naive 47.4%)
- **Small or negative norm-informed gains:** GPT-5.5 +2.6 pp, Qwen2.5-72B +0.0 pp, Mistral Medium 3.1 −10.5 pp.
- **Recovered failures / regressions (norm-informed vs. naive):**
  - Gemini 3.1 Pro: recovers 18/24 naive failures, 0 regressions.
  - Claude Fable 5: recovers 14/20 failures, 0 regressions.
  - Mistral Medium 3.1: recovers 2/25, regresses 5/13 (38%).
  - Qwen2.5-72B: recovers 2/26, regresses 7/12 (58%).

## Limitations
- Only 38 curated scenarios; bootstrap intervals are wide and per-norm/per-event breakdowns are not yet inferentially stable.
- Synthetic, English-language only; abstracts away multiple simultaneous norms, threading, timing, long-term memory, and multi-turn repair.
- No-demonstration screening used a Gemini-family baseline, which may inflate headroom for Gemini subject models and bias scenario selection against Gemini default behavior.
- Single fixed LLM judge (Gemini 3.1 Pro Preview) is also an evaluated subject model, creating potential self-preference bias despite sanity checks.
- Curation performed by paper authors only, with no external annotators.
- Benchmark measures one-turn compliance, not multi-turn social repair or sustained community norm adoption.

## Relevance to Agentic AI / LLM Agents
Group-chat agents must navigate implicit social context that is never explicitly specified in their system prompt—exactly the kind of tacit norm inference LoSoNA targets. The finding that `norm_informed` prompting causes large gains for some models but regressions in others is directly actionable for agent designers: adding a meta-instruction to attend to conversational patterns is not a free win and interacts strongly with model identity. The benchmark also operationalizes a first-person, behaviorally grounded form of Theory of Mind—distinct from the third-person question-answering ToM tests common in LLM evaluation—which is more representative of what deployed conversational agents must actually do. Future agentic systems operating in Slack, Discord, or collaborative tools will face exactly this problem at scale, making LoSoNA a useful early diagnostic for social norm adaptation capability.

## Tags
#benchmark #social-norms #multi-party-chat #theory-of-mind #evaluation #prompting #conversational-agents #llm-agents
