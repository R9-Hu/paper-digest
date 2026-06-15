---
title: "The Containment Gap: How Deployed Agentic AI Frameworks Fail Public-Facing Safety Requirements"
authors: ["Md Jafrin Hossain", "Mohammad Arif Hossain", "Weiqi Liu", "Nirwan Ansari"]
source: "Arxiv"
venue: "ICML 2026"
published: "2026-06-11"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12797"
url: "http://arxiv.org/abs/2606.12797v1"
pdf: "paper/harness/[Arxiv 2026] The Containment Gap How Deployed Agentic AI Frameworks Fail Public-Facing Safety Requirements.pdf"
---

# The Containment Gap: How Deployed Agentic AI Frameworks Fail Public-Facing Safety Requirements

## TL;DR
This paper audits three dominant agentic AI frameworks (LangChain, AutoGPT, OpenAI Agents SDK) against six formal containment principles and finds zero native compliance in any of them. A single memory-poisoning write in a LangChain-based government benefits agent achieves 100% targeted corruption across all tested model backends, raising wrongful denial rates to 88.9%. Two deterministic, sub-millisecond interventions (a memory integrity validator and a tool-call policy gate) eliminate both attack vectors entirely.

## Problem
Agentic LLM frameworks compose perception → reasoning → execution → memory update into recursive pipelines, but no major framework enforces structural isolation at inter-layer boundaries by default. Prior safety work focuses on model-level outputs (toxicity, bias) rather than architectural containment, leaving a systematic gap: a single corrupted write can propagate through the entire pipeline and persist across future reasoning cycles, causing cascading harm in high-stakes public deployments (welfare, healthcare, finance).

## Method
The authors derive six containment principles (P1–P6) from a compositional security model grounded in reference-monitor theory and constrained-control projection operators:
- **P1** Reasoning-Execution Separation (policy gate between plan and action)
- **P2** Capability Scoping (per-session deny-all tool allowlist with rate limits)
- **P3** Memory Integrity (validated writes before reaching long-term memory)
- **P4** Layer-Transition Validation (checks at every inter-stage boundary)
- **P5** Authenticated Communication (cryptographic signing of inter-agent messages)
- **P6** Runtime Monitoring (anomaly detection spanning all stages)

They score LangChain, AutoGPT, and OpenAI Agents SDK against these principles using a rubric (✓ = native default / ✓* = requires configuration / ✗ = absent) with two raters (Cohen's κ = 0.81). Empirical validation uses a synthetic LangChain welfare-benefits agent (250 claims, 5 model backends including Qwen-2.5 3B, Claude Haiku 4.5, GPT-4o, Claude Sonnet 4.6, GPT-4o-mini). Two lightweight fixes are implemented as deterministic wrappers: a regex-based memory integrity validator interposing on `ConversationBufferMemory.save_context`, and a deny-all tool-call policy gate with path canonicalization.

## Key Contributions
- First formal audit methodology operationalizing containment principles into a reusable compliance matrix for agentic frameworks
- Empirical proof that zero-native-compliance is exploitable: single memory-poisoning write achieves corruption rate 1.000 across all 5 tested model backends regardless of scale or alignment training
- Demonstration that complex multi-factor policies make attacks harder to detect: overall accuracy stays near baseline while targeted wrongful denials increase 3.5× (aggregate concealment)
- Two backend-agnostic containment mechanisms that reduce corruption and bypass rates from 1.000 to 0.000 with <0.2 ms overhead per call

## Results
- **Compliance audit**: 0 frameworks achieve any ✓ (native default) on any of the 6 principles; AutoGPT is worst (0✓/1✓*/5✗), LangChain intermediate (0✓/4✓*/2✗)
- **Memory poisoning (simple policy)**: corruption rate 1.000 across all seeds and all 3 backends (Qwen-2.5 3B, Claude Haiku 4.5, GPT-4o); mean accuracy drops from 0.908 → 0.558; Region B wrongful denial rate = 0.889
- **Memory validator recovery**: corruption drops to 0.000 across all backends; accuracy recovers to 0.967 (Qwen) / 1.000 (commercial); validator overhead = 0.006–0.016 ms/call
- **Tool bypass**: 100% bypass rate without gate (path traversal, unauthorized API, restricted write); 0% bypass with gate; gate overhead = 0.095–0.129 ms/call
- **Complex 5-factor policy**: corruption rate 1.000 for both Claude Sonnet 4.6 and GPT-4o-mini without guard; detection difficulty metric = 0.167 (aggregate accuracy unchanged while Region B denials spike 3–3.5×); validator reduces corruption to 0.000 (Claude) / 0.167 (GPT-4o-mini)

## Limitations
- Compliance rubric captures mechanism presence, not implementation depth or runtime effectiveness; point-in-time evaluation subject to framework evolution
- Empirical validation uses LangChain only; AutoGPT and OpenAI SDK empirical replication is future work
- Regex-based memory validator is brittle to semantically equivalent adversarial natural language that avoids surface patterns
- Policy gate deny-all allowlist may not generalize to dynamic multi-agent systems requiring flexible tool composition
- Compound attacks (sequences of individually benign operations) are not addressed; trajectory-level analysis (P6) remains an open problem
- Experiments use a simulated scenario; real-world adaptive adversaries and live deployment conditions are untested

## Relevance to Harnesses / Meta-Harnesses
This paper directly characterizes the structural safety properties—and their absence—in the framework layer that harnesses are built on, making it a foundational reference for anyone designing or evaluating meta-harnesses. The six containment principles (P1–P6) constitute an architectural checklist that any harness orchestrating tool-calling agents should enforce at composition boundaries, particularly P1 (policy-gated execution between reasoning and action) and P3 (provenance-validated memory writes). The empirical finding that alignment-trained commercial models (Claude Haiku 4.5, GPT-4o) are equally vulnerable as small local models underscores that safety cannot be delegated to the model layer—it must be enforced structurally within the harness itself. The lightweight, LLM-free interceptor pattern (wrapping `save_context` and tool dispatch) demonstrated here is directly applicable as a harness-level middleware design pattern.

## Tags
#agentic-ai #safety #memory-poisoning #containment #framework-audit #tool-use #langchain #multi-agent
