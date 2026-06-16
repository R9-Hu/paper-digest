---
title: "GIST-CMTF: Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents"
authors: ["Rahul Suresh Babu", "Rohit Shukla"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T14:57:08+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16813"
url: "http://arxiv.org/abs/2606.16813v1"
pdf: "paper/agentic-ai/[Arxiv 2026] GIST-CMTF Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents.pdf"
---

# GIST-CMTF: Goal-State Inference for Causal Minimal Tool Filtering in LLM Agents

*🕒 **Published (v1):** 2026-06-15 14:57 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16813v1)*

## TL;DR

GIST-CMTF adds a goal-state inference layer on top of Causal Minimal Tool Filtering (CMTF) to handle ambiguous user requests in tool-augmented LLM agents. Instead of assuming a known symbolic goal, it infers candidate goals, detects ambiguity, and exposes clarification as a first-class causal action when the goal is underspecified. Across 120 tasks and 7 model backends, it achieves 97.0% task success vs. 80.1% for the best non-oracle baseline.

## Problem

Causal Minimal Tool Filtering (CMTF) exposes only the next causally necessary tool given a known goal state — but in practice, user requests like "handle my appointment" or "take care of this email" map to multiple plausible symbolic goals. Naive goal inference (picking the top-confidence or most semantically similar goal) causes *wrong-goal execution*: the agent follows a causally valid tool path toward an unintended objective. This is distinct from wrong-tool selection and is not addressed by any prior filtering approach.

## Method

GIST-CMTF inserts a four-stage upstream layer before CMTF:

1. **Candidate goal generation**: Maps natural-language request `q` and current symbolic state `s_t` to a ranked set of candidate symbolic goals `{(g_i, p_i)}` drawn from the same state-variable vocabulary as tool contracts.
2. **Ambiguity detection**: Applies a threshold/margin check — flags ambiguity if top confidence `p*` is below τ, the margin between top-2 candidates is below δ, required goal variables are missing, the request uses vague verbs ("handle," "fix"), or the goal would commit to irreversible actions (send/delete/share).
3. **Clarification as a causal action**: When ambiguous, exposes a clarification action `a_clarify` with its own preconditions (e.g., `{ambiguous_goal}`) and effects (e.g., `{goal_specified}`), integrating it into the precondition-effect framework rather than treating it as an ad hoc fallback.
4. **Goal-aware CMTF**: If the goal passes ambiguity detection, runs standard CMTF with `g*` to produce the minimal one-tool causal frontier.

Tool contracts follow `t_i = (d_i, R_i, E_i, c_i, ρ_i)` (description, required vars, effect vars, cost, risk), compatible with prior CMTF and STRIPS/PDDL formalisms.

## Key Contributions

- Formalizes goal-state inference as the missing upstream layer for causal tool filtering in LLM agents.
- Defines *wrong-goal execution* as a distinct failure mode (causally valid path, wrong objective) separate from wrong-tool selection.
- Introduces clarification as a causal action with preconditions and effects, keeping it inside the state-transition framework.
- Provides a 120-task controlled benchmark covering explicit, ambiguous, missing-variable, and clarification-required request types across calendar, email, files, contacts, and authorization domains.
- Evaluates across 7 model backends (Claude Opus 4.8, Sonnet 4.6, Haiku 4.5, GPT-OSS-120B, Nova Premier, Nova 2 Lite, Nova Pro v1) and 6 filtering methods (5,040 total runs).

## Results

- **Task success**: GIST-CMTF 97.0% vs. top-goal CMTF 80.1%, semantic-goal CMTF 82.9%, state-aware 56.4%, all-tools 53.5%; oracle (gold-goal CMTF) 99.5%.
- **Wrong-goal execution**: GIST-CMTF 2.5% vs. top-goal CMTF 19.4% (87.1% relative reduction) and semantic-goal CMTF 16.7% (85.0% relative reduction).
- **Ambiguous-goal tasks**: GIST-CMTF 97.5% success / 2.1% wrong-goal; top-goal CMTF 52.9% / 46.8%; semantic-goal CMTF 50.0% / 50.0%.
- **Clarification-required tasks**: GIST-CMTF 100.0% success, clarifies in 91.4% of runs.
- **Missing-variable tasks**: GIST-CMTF 98.6% success, clarifies in 81.0% of runs.
- **Explicit-goal tasks (cost)**: GIST-CMTF 94.6% vs. semantic-goal CMTF 98.9%; unnecessary clarification on 16.8% of explicit-goal runs (5.6% overall).
- **Tool exposure**: 1.0 visible tool/step (same as all CMTF variants); all-tools = 32.0, state-aware = 8.1.
- **Token cost**: GIST-CMTF 1,186 vs. all-tools 4,152, state-aware 2,084, semantic-goal CMTF 700, gold-goal CMTF 689.
- **Model robustness**: 100% success on Claude Opus 4.8 and Sonnet 4.6; lowest is 89.2% on Nova 2 Lite; consistently near gold-goal CMTF across all backends.

## Limitations

- Benchmark uses synthetic tasks with mocked, deterministic tool execution — does not reflect noisy real APIs, nondeterministic outputs, or irreversible side effects in production.
- Assumes user requests and tool contracts share a common symbolic state vocabulary; defining and maintaining this vocabulary across dynamic tool ecosystems is an open engineering challenge.
- Goal inference operates over a closed candidate-goal set; open-world goals not present in the predefined set are not addressed.
- Clarification is modeled as a single-turn action; real dialogues may require multi-turn exchanges with incomplete or conflicting user responses.
- Token latency, monetary cost, and user satisfaction under clarification are not measured.
- Over-clarification on clear requests (5.6% unnecessary clarification overall) introduces friction; threshold tuning is domain-dependent and not yet automated.
- No claim of production safety for high-risk irreversible actions; goal validation is positioned as one layer in a broader mediation stack.

## Relevance to Agentic AI / LLM Agents

This work directly addresses a gap in agentic tool-use pipelines: most frameworks treat goal specification as a solved precondition, but realistic user requests are underspecified. By formalizing goal-state inference as a required upstream component and wrong-goal execution as a distinct failure mode, GIST-CMTF establishes a cleaner architectural boundary between intent disambiguation and tool selection — relevant to anyone building multi-step agent orchestration systems. The treatment of clarification as a first-class causal action (with preconditions and effects) rather than an ad hoc interrupt is a principled design pattern applicable to any agent runtime that uses state-transition tool contracts. The cross-model robustness results (7 backends) also provide practical evidence that ambiguity-aware goal validation generalizes beyond any single LLM.

## Tags

#tool-augmented-agents #tool-filtering #goal-inference #intent-disambiguation #clarification #causal-reasoning #multi-step-tool-use #agent-reliability
