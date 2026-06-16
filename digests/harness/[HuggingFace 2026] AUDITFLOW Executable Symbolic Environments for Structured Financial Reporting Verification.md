---
title: "AUDITFLOW: Executable Symbolic Environments for Structured Financial Reporting Verification"
authors: ["Yan Wang", "Xuguang Ai", "Jaisal Patel", "Xueqing Peng", "Fengran Mo", "Yupeng Cao", "Haohang Li", "Mingyu Cao", "Lingfei Qian", "V\u00edctor Guti\u00e9rrez-Basulto"]
source: "HuggingFace"
venue: ""
published: "2026-06-02"
published_time: "2026-06-02T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.03031"
url: "https://huggingface.co/papers/2606.03031"
pdf: "paper/harness/[HuggingFace 2026] AUDITFLOW Executable Symbolic Environments for Structured Financial Reporting Verification.pdf"
---

# AUDITFLOW: Executable Symbolic Environments for Structured Financial Reporting Verification

*🕒 **Published (v1):** 2026-06-02 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.03031)*

## TL;DR
AUDITFLOW is a graph-grounded multi-agent framework for verifying XBRL financial filings against US-GAAP taxonomy constraints. It separates LLM-driven search from deterministic symbolic verification via a dual-graph environment and typed tool interface. On a 67-instance FinAuditing-derived benchmark, it reaches 82.09% joint audit accuracy under GPT-5.5, outperforming the strongest baseline by 14.93 points.

## Problem
LLMs cannot reliably perform structured XBRL audit verification because correctness requires traversing taxonomy calculation/dimensional graphs, recomputing expected values, and applying DQC rules—operations that depend on structured evidence, not text retrieval. The strongest prior model achieves only 13.86% on numerical-consistency tasks; existing financial-agent systems do not treat the taxonomy and filing as a unified executable environment.

## Method
AUDITFLOW constructs a symbolic environment from two graphs: a static US-GAAP taxonomy graph (concept metadata, calculation/dimensional/presentation edges) and a dynamic XBRL filing graph (reported facts, contexts, units, dimensional assignments), linked by bridge edges. Agents interact with this environment exclusively through typed deterministic tools organized into three categories: static taxonomy tools, dynamic filing tools, and deterministic DQC rule checkers (sign consistency DQC.US.0015, dimensional aggregation DQC.US.0117, calculation-tree consistency DQC.US.0126).

A three-agent protocol runs two role-specialized junior auditors in parallel: the Compliance Auditor (A1) starts from taxonomy constraints (static tools only), and the Forensic Auditor (A2) starts from filing evidence (static + dynamic tools). Both must pass a **required-tool gate**—mandatory deterministic checker calls—before their reports are accepted. A Senior Auditor reads both reports; if they disagree, it issues targeted feedback and re-dispatches the juniors for up to K rounds. Final verdicts are produced via **Dempster-Shafer evidential aggregation** (ER fusion) of the two junior mass functions, yielding a verdict, expected value, evidence trail, and trustworthiness score τ.

## Key Contributions
- Formal definition of **graph-grounded numerical consistency verification** for XBRL, with a structured output tuple (verdict, reported value, expected value, action path, evidence, trustworthiness score).
- **Dual-graph symbolic environment** combining static US-GAAP taxonomy and dynamic filing graphs, exposed through a deterministic typed tool interface that prevents LLMs from short-circuiting verification.
- **Three-agent protocol** with role-specialized search policies, a required-tool gate enforcing evidence collection, and bounded senior-feedback refinement.
- **Evidential aggregation** (ER fusion) over junior mass functions instead of LLM confidence scores, producing conflict mass K and trustworthiness τ as interpretable signals.
- Ablation demonstrating that removing deterministic checks collapses accuracy from 82.09% to 17.91% and raises invalid outputs from 1.49% to 35.82%.

## Results
- AUDITFLOW (GPT-5.5): **82.09% Joint ACC**, +14.93 pts over Single Agent (strongest baseline); VAcc 98.51%.
- AUDITFLOW (GPT-4o, Claude Sonnet 4.6, Qwen-397B): **80.60% Joint ACC**, ~95% VAcc each.
- AUDITFLOW (Qwen-27B): 73.13% Joint ACC, 85.07% VAcc.
- AUDITFLOW (Fino1-14B): 31.34% Joint ACC, 59.70% VAcc (model fails before reaching deterministic checks).
- Ablation (no deterministic checks, GPT-5.5): 17.91% Joint ACC, 35.82% invalid outputs; DQC.US.0117 and DQC.US.0126 drop to 0.00%.
- Ablation (no required-tool gate): 74.63% Joint ACC, 17.91% invalid outputs.
- Ablation (no ER fusion): 77.61% Joint ACC.
- On Qwen-27B, pre-senior disagreement cases have 36.4% final accuracy vs. 80.4% for consensus cases.
- LLM-only and vanilla RAG baselines remain substantially weaker; GraphRAG/TreeRAG improve over RAG but fall short of tool-based agents.

## Limitations
- Evaluation covers only 67 instances and 3 DQC rule families from one benchmark (FinMR/FinAuditing); does not generalize to the full XBRL rule set or diverse filing types/years.
- Requires well-tagged XBRL filings parseable into reliable graphs; cannot directly handle scanned reports, incomplete tags, or unstructured disclosures.
- Framework still depends on the LLM backbone following the tool protocol—weak models (e.g., Fino1-14B) fail before reaching deterministic checks.
- LLM-as-a-judge evaluation protocol (gpt-5-mini) may introduce judge errors despite fixed configuration and caching.
- Not validated for real-world audit deployment; intended as a research system.

## Relevance to Harnesses / Meta-Harnesses
AUDITFLOW is a concrete instantiation of the **harness pattern**: it wraps deterministic symbolic infrastructure (dual-graph environment, typed tools, DQC checkers) with an LLM orchestration layer, explicitly separating what the model decides (search trajectory, tool selection) from what the environment computes (verification verdicts). The **required-tool gate** is a harness-level enforcement mechanism—analogous to pre/post-condition hooks—that prevents agents from bypassing mandatory computation steps, a design choice directly relevant to any meta-harness that needs to guarantee coverage or correctness of sub-agent behavior. The ablation result (deterministic checks account for the bulk of accuracy; their removal causes near-total collapse) provides strong empirical grounding for the meta-harness principle that symbolic/deterministic components should own verification, not LLMs.

## Tags
#multi-agent #symbolic-environment #tool-use #financial-ai #xbrl #harness #neuro-symbolic #deterministic-verification
