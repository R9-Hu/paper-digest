---
title: "From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails"
authors: ["Yuguang Zhou", "Xunguang Wang", "Pingchuan Ma", "Zhantong Xue", "Zhaoyu Wang", "Shuai Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T14:49:00+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14517"
url: "http://arxiv.org/abs/2606.14517v1"
pdf: "paper/agentic-ai/[Arxiv 2026] From Shield to Target Denial-of-Service Attacks on LLM-Based Agent Guardrails.pdf"
---

# From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails

*🕒 **Published (v1):** 2026-06-12 14:49 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14517v1)*

## TL;DR
LLM-based guardrails protecting autonomous agents are vulnerable to a novel denial-of-service attack that exploits their schema-following behavior: adversarial payloads mimicking a guardrail's own analytical template trap it in unbounded reasoning loops. A beam-search optimization framework crafts transferable natural-language payloads achieving 13–63× token amplification on standalone guardrails and up to 148× latency amplification in end-to-end agent deployments.

## Problem
LLM-based guardrails have become the dominant runtime safety layer for autonomous agents (e.g., OpenAI Codex, Anthropic Claude Code), but their availability has been treated as a given. Because guardrails sit on the critical path of every agent action and ingest raw, unsanitized third-party content, an attacker who can inject text into any agent-fetched resource can force the guardrail into pathologically long reasoning — blocking forward progress and starving co-located agents in shared infrastructure. Prior LLM DoS methods achieve only 1.1–1.2× amplification on guardrails because they rely on off-task distractions that a task-confined guardrail ignores.

## Method
The attack exploits the guardrail's **schema-following behavior**: injecting content that mirrors the guardrail's own structured analytical template (risk categories, enumeration depth, anti-shortcut clauses, evidence ledgers) causes the guardrail to treat the injected scaffold as a legitimate continuation of its analysis, entering a self-reinforcing attention cycle rather than reaching a verdict.

Two instantiations of a **beam-search optimization framework** find maximally effective payloads:
- **LLM-as-Proposer**: an LLM proposer iteratively mutates candidate payloads guided by a strategy bank that tracks which structural patterns (e.g., "categorical exhaustion," "anti-convergence clauses") score highest on the surrogate guardrail TS-Guard-8B. The proposer observes the guardrail's full reasoning output as feedback.
- **Mechanism-Aware**: lightweight structural mutation operators directly manipulate named template slots (risk categories, enumeration depth, anti-shortcut clauses), with an attention-cycling score and entropy filter as the fitness signal — no LLM proposer needed.

Payloads optimized on one open-source surrogate (TS-Guard-8B) transfer black-box to closed-source targets. For end-to-end deployments, scenario-specific adaptations handle surface constraints: hidden DOM attributes (web), code comments (code agents), contradiction-inducing ambiguity for integrated guardrails, and transform-resilient optimization for multi-agent pipelines where intermediate rewriting can degrade payloads.

The mechanistic signature of a successful attack: response-token attention to schema headers is **9.6× higher** than baseline, and per-token entropy collapses from 0.264 bits to 0.132 bits as the model enters mechanical template-filling rather than genuine reasoning.

## Key Contributions
- Identification and formal characterization of **reasoning-extension DoS** as a new vulnerability class in LLM-based guardrails, distinct from prior DoS or jailbreak attacks.
- Beam-search optimization framework with two instantiations (LLM-as-Proposer with strategy bank; Mechanism-Aware with attention-guided structural mutation) that craft fluent, transferable NL payloads.
- Scenario-specific adaptations for four real-world agent frameworks: conflict-based ambiguity for integrated guardrails (code agents), transform-resilient optimization for multi-agent pipelines.
- Empirical demonstration that existing mitigations (perplexity filters, hard token budgets with fail-open/fail-closed policies, more capable guardrail models) fail to resolve the vulnerability — more capable models are actually more susceptible because they follow injected schemas more faithfully.

## Results
- **Standalone transferability**: Payloads optimized on TS-Guard-8B transfer to 8 guardrail models achieving **13–63× token amplification**; prior DoS baselines (ENGORGIO, OverThink, ReasoningBomb, CRABS, RECUR, ThinkTrap) achieve only **1.11–1.20×**.
- Peak standalone ratios: DeepSeek-V3.2 at **63.4×** (ASB, Inst. I); TS-Guard-8B at **50.2×** (AgentDojo, Inst. II); Qwen3.5-9B at **521,697 chars** absolute output.
- Closed-source models: Claude-3.5-Haiku **27.7×**, Gemini-3-Flash **22.1×**, GPT-4o-mini **20.6×** (AgentDojo, Inst. I).
- **End-to-end deployments**: LangGraph (multi-agent) **148×** peak latency + head-of-line throughput degradation; BrowserGym (web) **131×**; OpenHands (code) **36.3×**; OSWorld (desktop) **18×**.
- Ablation: removing beam search drops fitness 88% (greedy k=1: 7,220 vs. full 59,182); removing anti-shortcut clauses drops fitness 83%; removing category enumeration drops 74%.
- Mechanism-Aware (no LLM proposer) achieves 33,895 fitness — still **16.5×** amplification without any LLM call during optimization.

## Limitations
- Payload injection requires the agent to naturally fetch attacker-controlled content (same capability as indirect prompt injection); no active exploitation of the guardrail service directly.
- End-to-end amplification ratios vary widely by deployment scenario (18× to 148×), and integrated guardrails require richer scenario-specific adaptation.
- Evaluated mitigations are all shown to fail, but the paper does not propose a concrete positive defense — identifying the design space for cost-bounded, reasoning-robust guardrails is left as future work.
- Experiments use a specific surrogate (TS-Guard-8B) and proposer (GPT-5.2); generalizability of the strategy bank's accumulated patterns to future guardrail architectures is untested.
- Sustained reasoning loops (marked * in tables) would be unbounded without generation length limits; behavior beyond enforced limits depends on operator configuration.

## Relevance to Agentic AI / LLM Agents
This paper exposes a fundamental tension in the current agentic safety stack: the same structured-reasoning capability that makes LLM guardrails effective against sophisticated prompt injection and jailbreaks makes them a resource-exhaustion target. For researchers building or deploying agentic systems, the key takeaway is that **availability is an orthogonal safety property** that current guardrail designs do not address — a guardrail can correctly block harmful actions while still being DoS'd. The shared-guardrail infrastructure finding (head-of-line blocking in LangGraph) is particularly relevant to multi-agent system architects, since a single poisoned document in any co-located agent's fetch trajectory can degrade the entire system. This work also directly challenges the assumption that deploying stronger guardrail models increases safety, since more instruction-following capability amplifies the schema-hijack effect.

## Tags
#agent-safety #guardrails #denial-of-service #prompt-injection #multi-agent #adversarial-attacks #llm-reasoning #benchmark
