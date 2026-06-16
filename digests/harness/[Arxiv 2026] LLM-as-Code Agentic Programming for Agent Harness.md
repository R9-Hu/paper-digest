---
title: "LLM-as-Code Agentic Programming for Agent Harness"
authors: ["Junjia Qi", "Zichuan Fu", "Jingtong Gao", "Wenlin Zhang", "Hanyu Yan", "Xian Wu", "Xiangyu Zhao"]
source: "Arxiv"
venue: "KDD 2026"
published: "2026-06-14"
published_time: "2026-06-14T15:47:27+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.15874"
url: "http://arxiv.org/abs/2606.15874v1"
pdf: "paper/harness/[Arxiv 2026] LLM-as-Code Agentic Programming for Agent Harness.pdf"
---

# LLM-as-Code Agentic Programming for Agent Harness

*🕒 **Published (v1):** 2026-06-14 15:47 UTC  ·  **Source:** Arxiv  ·  **Venue:** KDD 2026  ·  [link](http://arxiv.org/abs/2606.15874v1)*

## TL;DR
This paper argues that assigning deterministic control flow (looping, branching, sequencing) to a probabilistic LLM is a category error that causes token explosion, control-flow hallucination, and unreliable completion by construction. It proposes **Agentic Programming** ("LLM-as-Code"), where a conventional program owns all control flow and LLMs are invoked only at leaf nodes requiring reasoning or generation. A GUI automation agent built on this design reaches 86.8% on OSWorld in 15 steps, versus 80.4% for the strongest prior system allowed 100 steps.

## Problem
Current dominant frameworks (ReAct, AutoGen, OpenHands, MetaGPT) make the LLM the orchestrator: it decides which tool to call, when to loop, and when to stop. This causes three structural failures on long-horizon tasks: (1) **token explosion** — the context grows O(steps × avg\_output) as the full conversation log must be re-fed each turn; (2) **control-flow hallucination** — the agent reports task completion before required steps run because termination is sampled, not enforced; (3) **unreliable completion** — correct intermediate hypotheses are abandoned because no mechanism guarantees a prescribed sequence executes. The paper claims these are architectural, not tunable: stronger models or better prompts reduce per-step error rate but cannot bound compounding failure over a long run.

## Method
**Agentic Programming** restructures the agent into four components:

1. **Code-driven workflow**: The control graph is ordinary Python; LLMs are invoked only via `@agentic`-decorated functions whose docstrings serve as prompts. The decorator handles prompt templating, model dispatch, and return-type parsing, making an LLM call syntactically identical to a regular function call. The call graph is unfolded at runtime by recursive invocation rather than pre-declared.

2. **DAG-structured context**: Execution history is the call tree, not a flat conversation log. A running call sees only its ancestor chain (O(depth) tokens). When a child returns, its frame is replaced in the parent's context by a one-line summary; completed subtrees do not accumulate. The full DAG is retained at the harness level for replay/debug but no single LLM call ever sees it.

3. **Multi-agent collaboration**: Parallel agents are parallel function invocations; each reasons in its own scoped context and returns a typed value. The join is program logic (dedup, ranking), not a model-mediated merge. A failed sub-agent is a failed call the program can retry or route to a stronger model without perturbing siblings.

4. **Self-programmed evolution**: A meta-`@agentic` function proposes a replacement for a failing function; the replacement is accepted only if it passes a deterministic test suite and is then committed as code. Subsequent invocations run the committed version unconditionally, unlike an orchestrator where an "improvement" is a note the model must re-read and stochastically apply.

## Key Contributions
- Formal diagnosis of LLM-as-Orchestrator as a **category error** (probabilistic system assigned deterministic responsibility), distinguishing it from an engineering shortfall fixable by scaling.
- The **LLM-as-Code** abstraction: LLM calls are first-class functions behind a decorator; the surrounding program owns the sequence.
- **DAG-structured context scoping**: context bounded by call depth rather than step count, achieved via stack-unwinding semantics rather than external compaction.
- **Self-programmed evolution** algorithm: propose (LLM) → test (deterministic) → commit as code; improvement hardens into the deterministic layer.
- Systematic comparison showing why existing patches (bigger context, reflection/retry, structured decoding, CodeAct, plan-and-execute, LangGraph, DSPy) address symptoms without resolving the category error.
- Empirical case study on OSWorld: 86.8% overall in 15 steps vs. 80.4% for best prior system in 100 steps.

## Results
- **OSWorld GUI automation** (overall success %):
  - LLM-as-Code w/ Claude Sonnet 4.6, **15 steps**: **86.8%** overall (Chrome 93.5%, Multi-Apps 80.0%, OS 100.0%)
  - Holo3-35B-A3B, 100 steps: 80.4% (prior best)
  - OpenAPA w/ Gemini-3.1-pro, 100 steps: 78.3%
  - Claude Sonnet 4.6 (general model, no framework), 100 steps: 72.1%
- The proposed method is the best across all three targeted OSWorld domains despite using 6.7× fewer maximum steps.
- A second agent (autonomous overnight research pipeline) is mentioned as built under the same paradigm but no benchmark numbers are reported for it.

## Limitations
- Only one quantitative benchmark reported (OSWorld); no ablations isolating which component (DAG context vs. code control flow vs. step budget) drives the gain.
- The comparison is against public leaderboard numbers accessed on a specific date, not a controlled re-run.
- The paradigm is acknowledged to be inapplicable to fully exploratory, unstructured tasks (open-ended brainstorming, research without a stage model) where LLM-driven orchestration may remain appropriate.
- Self-programmed evolution walkthrough is illustrative (Algorithm 1); no quantitative evaluation of the evolution component is provided.
- The paper is a KDD 2026 workshop paper (6-page format limit), so implementation details (Appendices C–E) are present but the empirical section is thin.

## Relevance to Harnesses / Meta-Harnesses
This paper is a direct architectural statement about how agent harnesses should be structured: it argues the harness — not the LLM — must own the control graph, making "agent harness" a first-class engineering artifact rather than a thin relay layer. The DAG-structured context model is directly applicable to multi-step digest and orchestration harnesses (like paperDigest) where long call chains accumulate context: bounding context to call depth rather than step count solves a concrete scalability problem. The `@agentic` decorator pattern and self-evolution algorithm (test-gated code commit) are concrete implementation primitives a meta-harness can adopt. The contrast with LangGraph (pre-declared graph vs. runtime-unfolded call graph) is particularly relevant for harness designers choosing between static workflow engines and dynamic recursive dispatch.

## Tags
#agent-harness #control-flow #llm-orchestration #dag-context #agentic-programming #multi-agent #computer-use #long-horizon
