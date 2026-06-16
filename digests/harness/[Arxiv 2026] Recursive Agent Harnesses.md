---
title: "Recursive Agent Harnesses"
authors: ["Elias Lumer", "Sahil Sen", "Kevin Paul", "Vamse Kumar Subbiah"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T17:47:30+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13643"
url: "http://arxiv.org/abs/2606.13643v1"
pdf: "paper/harness/[Arxiv 2026] Recursive Agent Harnesses.pdf"
---

# Recursive Agent Harnesses

*🕒 **Published (v1):** 2026-06-11 17:47 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13643v1)*

## TL;DR
Recursive Agent Harnesses (RAH) names and evaluates the pattern of using a full agent harness—with filesystem tools, code execution, and planning—as the recursive unit instead of a bare model call. A parent agent generates and executes a script that spawns parallel subagent harnesses per document entry, bypassing per-turn tool-call caps. On Oolong-Synthetic (199 samples, up to 4M tokens), RAH improves the Codex coding-agent baseline from 71.75% to 81.36% with the backbone held fixed at GPT-5.

## Problem
Long-context tasks requiring per-entry LLM reasoning across thousands of independent entries expose a gap between two prior approaches: coding agents reduce per-entry reasoning to regex heuristics (no recursive LLM calls per entry), while recursive language models (RLMs) compose bare model calls recursively but lack filesystem access, code execution, and external tools. Neither approach handles fine-grained, tool-augmented reasoning at scale over multi-million-token documents.

## Method
RAH designates the full agent harness (tools + planning + spawning capability) as the recursive unit. A parent agent inspects the document, decides on decomposition, and selects between two spawning paths:

- **Code-execution path (primary):** The parent writes an executable Python/asyncio script instantiating `Task()` objects—one per entry or entry group—and runs them in parallel via its shell tool. This path bypasses the API's per-turn parallel tool-call limit, enabling thousands of concurrent subagent harnesses.
- **JSON tool-call path (1–5 entries):** The parent emits a structured function call directly, without generating an intermediate script.

Each subagent is itself a full harness with `read_file`, `write_file`, `ls`, `glob`, `grep`, `execute`, and web search, plus a planning step. Subagents are context-isolated (no shared memory or peer communication); results are aggregated by the parent reading a shared output file. Recursion depth is configurable (default 3). Implementation uses LangChain + asyncio; answer extraction uses a fixed GPT-5 follow-up call with regex fallback.

## Key Contributions
- Formally names the **Recursive Agent Harness (RAH)** pattern and defines **harness recursion** as the code-first extension of model recursion (RLMs).
- Provides a controlled evaluation on Oolong-Synthetic with backbone held fixed (GPT-5), isolating the harness architecture as the sole variable.
- Reports results across 13 context-length buckets (1K–4M tokens) and 5 answer types (USER, COMPARISON, LABEL, DATE, NUMERIC).
- Situates RAH in the lineage of RLMs and relates it to Anthropic's dynamic workflows as a production instantiation of the same pattern.

## Results
- **RAH (GPT-5):** 81.36% Oolong Score (95% CI [76.0, 86.5]) vs. Codex baseline 71.75% — +9.61 points (CI [4.2, 14.8], excludes zero).
- **RAH (Claude Sonnet 4.5):** 89.77%.
- **RLM baseline:** 64.38%; **Full-context baseline:** 59.22%.
- Semantic answer types (USER 87.27%, COMPARISON 89.29%, LABEL 86.54%) all exceed 86% under GPT-5.
- NUMERIC degrades to 69.33% due to compounding penalty from the 0.75^|y−ŷ| scoring function.
- Sonnet 4.5 remains above 86% through 524K tokens and above 76% through 4M tokens with no monotone degradation.
- All 199 instances used the code-execution spawning path (entry counts uniformly exceeded the 5-entry JSON threshold).

## Limitations
- Evaluation limited to Oolong-Synthetic; generalization to Oolong-Real and more ambiguous domains untested.
- Parent occasionally answers directly without spawning (collapses to single coding agent), concentrated at longer context lengths.
- NUMERIC scoring penalty (0.75^|y−ŷ|) understates reasoning quality on continuous-quantity tasks.
- No ablations of recursion depth, entries-per-subagent, or code-execution vs. tool-call path.
- Exact token cost and wall-clock latency for the GPT-5 configuration not instrumented.
- Answer-extraction step shares the GPT-5 model family with the system under test; no separate human validation of extraction.
- DATE results (n=5) have high variance and are not statistically reliable.

## Relevance to Harnesses / Meta-Harnesses
RAH is a direct theoretical contribution to the harnesses/meta-harnesses topic: it names the pattern where a harness spawns child harnesses recursively via generated executable code, establishing **harness recursion** as a distinct axis from model recursion (RLMs) and schema-driven delegation (AGENTHIVE). The paper's controlled design—backbone fixed, harness varied—provides the first clean evidence that harness architecture itself, not model capability, drives the performance delta. It also explicitly connects to Anthropic's dynamic workflows as a production deployment of the same code-driven spawning primitive, situating meta-harness design as an emerging production norm rather than a research artifact.

## Tags
#agent-harness #harness-recursion #multi-agent #long-context-reasoning #code-as-action #oolong #dynamic-workflows #subagent-orchestration
