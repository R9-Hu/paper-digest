---
title: "When More Documents Hurt RAG: Mitigating Vector Search Dilution with Domain-Scoped, Model-Agnostic Retrieval"
authors: ["Nabaraj Subedi", "Ahmed Abdelaty", "Shivanand Venkanna Sheshappanavar"]
source: "Arxiv"
venue: ""
published: "2026-06-09"
published_time: "2026-06-09T18:26:24+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.11350"
url: "http://arxiv.org/abs/2606.11350v1"
pdf: "paper/harness/[Arxiv 2026] When More Documents Hurt RAG Mitigating Vector Search Dilution with Domain-Scoped, Model-Agnostic Retrieval.pdf"
---

# When More Documents Hurt RAG: Mitigating Vector Search Dilution with Domain-Scoped, Model-Agnostic Retrieval

*🕒 **Published (v1):** 2026-06-09 18:26 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.11350v1)*

## TL;DR
RAG pipelines degrade severely as heterogeneous corpora scale — a phenomenon the authors formalize as *vector search dilution* — because dense similarity loses discriminative power across domain boundaries. They propose MASDR-RAG, a multi-agent framework where each agent is a domain-scoped retrieval tool, and its lightweight variant HYBRID-ROUTED (regex + single LLM router + single synthesis call). The core finding is that domain scoping lifts P@10 from 0.77 to 0.86, but naïve multi-agent orchestration collapses faithfulness from 0.61 to 0.35 — the *precision–faithfulness paradox* — with severity depending on whether the generator is open-source or commercial.

## Problem
Standard RAG pipelines embed–index–retrieve–generate over a monolithic vector store; as the corpus grows to thousands of heterogeneous documents, the top-k retrieved chunks become semantically plausible but contextually wrong (wrong domain). The authors observe this empirically in a deployed Wyoming DOT chatbot where expanding from 54 to 1,128 documents (88,907 chunks) dropped accuracy from 75% to below 40%, even with hybrid dense+sparse retrieval. No prior work provides a deployable, corpus-intrinsic measurement of this degradation or a retrieval-architecture fix that avoids amplifying faithfulness errors.

## Method
**Dilution formalization:** Define dilution factor δ(q, k★) = 1 − P_global(q)/P_scoped(q), where P_global is the fraction of the top-m retrieval set belonging to the target category over the full corpus and P_scoped is the same fraction when retrieval is restricted to that category's sub-index (≈1 by construction). δ=0 means no dilution; δ→1 is severe.

**MASDR-RAG architecture:**
1. *Domain-scoped retrieval*: Nine domain agents, each filtering the Neo4j knowledge graph on `document_series` metadata, reducing the effective search space 85–98% per agent.
2. *Hybrid routing*: A fast regex matcher runs first; on failure, a zero-shot LLM classifier routes to the correct agent scope.
3. *Multi-agent orchestration*: A function-calling orchestrator dispatches to up to five tool-call rounds across scoped agents.

**HYBRID-ROUTED** collapses orchestration to at most two LLM calls (one router, one synthesizer), eliminating multi-round synthesis.

Both systems run hybrid vector+BM25 search within the scoped sub-index, merging results with priority deduplication (vector wins on ties).

## Key Contributions
- Formal definition and empirical measurement of *vector search dilution* (δ), with corpus-intrinsic measurement requiring no labeled queries.
- MASDR-RAG framework: single reasoning agent with K domain-scoped retrieval tools; explicit distinction from genuinely autonomous multi-agent RAG (MA-RAG, SCOUT-RAG).
- HYBRID-ROUTED: regex + LLM router + single scoped synthesis, pareto-optimal on the latency–correctness frontier.
- Discovery and root-cause analysis of the *precision–faithfulness paradox*: multi-agent orchestration improves retrieval precision but degrades faithfulness under commercial generators (Claude-Haiku: 0.250→0.010; GPT-5-mini: 0.378→0.241) but not under open-source generators (Qwen-7B: 0.347→0.391).
- Cross-DOT replication: dilution mechanism transfers to Caltrans and CDOT corpora when scope axis matches producer-level topical granularity (`document_series` for WY/CO, `section` for CA).
- Controlled ablations ruling out routing noise, within-scope reranking, retriever family, and index implementation as sole causes; residual cause is context fragmentation from near-duplicate passages under commercial synthesizers.

## Results
- **P@10**: Monolithic 0.77 → MASDR-RAG 0.86 (p<0.05, WYDOT Gemini stack, n=200).
- **Faithfulness**: Monolithic 0.61 → MASDR-RAG 0.35 (p<0.01); HYBRID-ROUTED recovers to 0.62.
- **Correctness**: MASDR-RAG 33.5% vs. Monolithic 25.5%; HYBRID-ROUTED 24.5% (WYDOT Gemini).
- **ReAct efficiency on Llama-3-8B**: 5.9× more tokens (39.2k vs. 6.6k), 2.2× higher p50 latency, 143.8s vs. 51.0s p95 vs. HYBRID-ROUTED.
- **Cross-domain generalization (Composite-9, Qwen-7B)**: Regex-Scoped correctness 90.0% vs. Monolithic 90.0%; MASDR-RAG drops to 74.0%; Custom ReAct reaches 94.4% at 4.48s p50 vs. 1.94s Monolithic.
- **Genuine multi-agent baselines (WYDOT Qwen)**: Regex-Scoped 35.1% correctness beats MA-RAG 11.0% and SCOUT-RAG 24.1% at 1/22× and 1/10× the LLM-call budget, respectively.
- **Cross-DOT dilution correlation**: ρ_CDOT = −0.95, ρ_WYDOT = −0.68, ρ_Caltrans-section = −0.85.
- **ColBERTv2 scoped**: Faithfulness 0.860 vs. unscoped 0.780 on Composite-9, confirming scoping benefit extends beyond single-vector encoders.

## Limitations
- The precision–faithfulness paradox is measured with an LLM-as-judge (Qwen-7B); RAGAS-style faithfulness metrics assume a single context window and may over-penalize multi-agent responses, so the measured drop is an upper bound.
- Open-source evaluation is limited to 7–8B parameter models; ≥70B models are untested.
- Routing taxonomy (nine WYDOT scopes, Composite-9 source types) is manually crafted and requires explicit organizational metadata at corpus ingestion time — assumes structured document provenance.
- The adaptive scope-axis recommendation (chunks-per-doc heuristic to choose `document_series` vs. `section`) is proposed but not ablated end-to-end.
- Evaluation is on government/enterprise corpora; generalization to knowledge bases without explicit hierarchical metadata is unverified.

## Relevance to Harnesses / Meta-Harnesses
This paper is directly relevant as a *deployed harness case study*: MASDR-RAG is an agent harness where domain-scoped retrieval tools are registered in an `AGENT_REGISTRY` and dynamically dispatched by an orchestrator, closely mirroring the tool-routing patterns studied in meta-harness research. The *precision–faithfulness paradox* is a concrete, quantified failure mode of multi-agent orchestration that any harness designer must account for — specifically, that multi-round synthesis with near-duplicate retrieved evidence degrades output quality, and that this effect is strongly backbone-dependent (commercial vs. open-source generators). The recommendation to "scope first, single synthesis call" is an empirically grounded design principle for RAG harnesses, and the controlled ablation methodology (isolating routing noise, reranking, retriever family, index, fragmentation, and backbone) provides a template for diagnosing harness-level failures beyond the retrieval layer.

## Tags
#rag #multi-agent #agent-harness #retrieval #vector-search #orchestration #enterprise-rag #benchmarking
