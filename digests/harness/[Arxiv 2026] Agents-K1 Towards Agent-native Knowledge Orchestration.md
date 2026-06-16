---
title: "Agents-K1: Towards Agent-native Knowledge Orchestration"
authors: ["Zongsheng Cao", "Bihao Zhan", "Jinxin Shi", "Jiong Wang", "Fangchen Yu", "Zhijie Zhong", "Zijie Guo", "Tianshuo Peng", "Zhuo Liu", "Yi Xie", "Xiang Zhuang", "Yue Fan", "Runmin Ma", "Shiyang Feng", "Xiangchao Yan", "Anran Liu", "Peng Ye", "Wenlong Zhang", "Shufei Zhang", "Chunfeng Song", "Fenghua Ling", "Jie Zhou", "Liang He", "Bo Zhang", "Lei Bai"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T17:58:35+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13669"
url: "http://arxiv.org/abs/2606.13669v1"
pdf: "paper/harness/[Arxiv 2026] Agents-K1 Towards Agent-native Knowledge Orchestration.pdf"
---

# Agents-K1: Towards Agent-native Knowledge Orchestration

*🕒 **Published (v1):** 2026-06-11 17:58 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13669v1)*

## TL;DR
Agents-K1 is an end-to-end pipeline that converts raw scientific PDFs into agent-native multimodal knowledge graphs by combining a five-module extraction schema, a 4B GRPO-trained model, and a tri-source CLI agent interface. It processes 2.46 million papers across six disciplines to produce Scholar-KG, with a 1M-paper subset released. On research-QA benchmarks it lifts frontier-model accuracy by up to 3× over unaugmented baselines.

## Problem
LLM-based research agents have matured in *agent orchestration* (planning, tool use) but not in *knowledge orchestration*. Three concrete gaps: (1) Graph-augmented retrieval systems (LightRAG, HippoRAG, GraphRAG) build text-only triples from abstracts, discarding figures, tables, equations, mechanisms, and method lineages; (2) scholarly citation graphs use a flat `cites` edge with no argumentative intent (support/contrast/extend); (3) agents re-extract structure from raw PDFs at query time, preventing provenance tracing from answer back to exact evidence spans.

## Method
Three coordinated layers:

**KG Layer** — A MinerU-based multimodal parser decomposes each PDF into typed content units `(type, raw_content, structural_metadata)` covering text, figures, tables, and equations. A unified heterogeneous graph with a *semantic anchor* middle layer bridges modalities without brittle cross-modal entity alignment. Five extraction modules populate the graph: (A) meta/factual entities with provenance; (B) textually mentioned entities (methods, datasets, metrics, theorems) with synonym canonicalization; (C) implicit/abstracted entities (motivations, contributions, limitations, hypotheses) via rhetorical-role tagging; (D) citation edges with typed argumentative role, strength score, and evidence spans; (E) fine-grained entity-to-entity triples (controlled: BUILDS_ON, SOLVES, APPLIED_TO; open: causal, compositional, comparative, domain).

**LLM Layer** — A 4B-parameter extraction backbone trained with Group Relative Policy Optimization (GRPO) under a rule-based reward jointly supervising format compliance, JSON validity, and task-conditioned F1 on NER, relation extraction, and long-form structured extraction.

**CLI Layer (GraphAnything)** — A tri-source agent interface unifying real-time web search, multimodal graph retrieval, and cross-document network traversal. Exposed via CLI/MCP/API; supports graph operators, multi-agent coordination, and an idea→method-spec→code-synthesis pipeline.

**General-KG** uses a *core-then-modes* architecture: a shared two-pass core produces a canonical entity set and binary skeleton; six pluggable views (binary, nary, temporal, person, event, diy) derive from it, with projection modes costing zero additional LLM calls and upgrade modes costing one pass per chunk. A weight-frozen self-improvement loop distils vertical-specific skills from 10–20 gold documents without retraining.

## Key Contributions
- **Agents-K1 unified pipeline** integrating KG construction, RL-trained extraction, and agent CLI under one framework
- **Scholar-KG**: 2.46M papers across CS, chemistry, biology, earth science, physics, materials; 1M-paper subset publicly released
- **4B GRPO extraction backbone** that surpasses an 8B open-source baseline across 10 benchmarks and matches a 32B model on NER
- **GraphAnything CLI** as a tri-source, MCP-compatible agent-facing interface turning the KG into an executable research tool
- **General-KG** schema-adaptive multi-view extension deployable to arbitrary document corpora without weight updates
- **LLM-guided multi-hop QA synthesis** pipeline reusing the structured KG to generate evidence-grounded 3–5-hop QA datasets

## Results
- FrontierScience-Research benchmark: Gemini-3 overall accuracy 7.9% → 24.6%; GPT-5.2 accuracy 25.2% → 39.4%
- Geoscience research questions: Gemini-3 rationale accuracy 52.3% → 69.5%
- Multi-hop QA: state-of-the-art on HotpotQA, 2WikiMultiHopQA, and MuSiQue against nine graph-augmented retrieval baselines (specific numbers not given in provided text)
- 4B extraction model outperforms 8B open-source reference across 10 benchmarks; matches 32B base on NER
- General-KG core-then-modes reduces LLM calls by 50% vs. naïve per-view extraction (96 → 48 calls for all-views, n=8 chunks, 4 upgrade modes)

## Limitations
- QA generation truncates each paper to a fixed context window `L`; content beyond that threshold is excluded from evidence grounding
- The weight-frozen skill loop for new verticals requires 10–20 hand-curated gold documents per domain, which may not be available in low-resource settings
- Cross-domain benchmark results cited in the abstract are not broken down in the provided text excerpt; cross-domain generalization details are cut off
- Numerical results, hyperparameters, and experimental setups are deliberately excluded from the KG entity layer, limiting reproducibility tracing for quantitative claims
- Human-in-the-loop verification is applied only for "high-impact" citation relation cases; the selection criterion is unspecified

## Relevance to Harnesses / Meta-Harnesses
Agents-K1 is structurally a *meta-harness*: it separates the offline harness (KG construction pipeline) from the online agent interface (CLI/MCP layer), exactly the composable, reusable scaffold pattern central to harness research. The core-then-modes architecture in General-KG is itself a canonical meta-harness design — a shared core spawns multiple specialized extraction views without re-running extraction, directly analogous to how harness foundries (e.g., HarnessX) decouple evaluation scaffolding from task-specific probes. The weight-frozen skill library with version-controlled, human-auditable prompt skills addresses harness evolvability and compliance provenance, a concern also raised in compositional shielding and agent governance work. For researchers tracking harnesses, Agents-K1 provides a concrete, deployed example of how to architect an agent-facing knowledge harness at million-document scale with MCP integration.

## Tags
#knowledge-graph #scientific-reasoning #graph-rag #information-extraction #agent-infrastructure #multi-hop-qa #grpo #meta-harness
