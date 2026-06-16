---
title: "A Multi-AI-agent Framework Enabling End-to-end Finite Element Analysis for Solid Mechanics Problems"
authors: ["Titu Ranjan Sarker", "Muhammed Jawaad Zulqernine", "Ling Yue", "Shaowu Pan", "Chenxi Wang", "Shiyao Lin"]
source: "HuggingFace"
venue: ""
published: "2026-05-28"
published_time: "2026-05-28T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.00138"
url: "https://huggingface.co/papers/2606.00138"
pdf: "paper/harness/[HuggingFace 2026] A Multi-AI-agent Framework Enabling End-to-end Finite Element Analysis for Solid Mechanics Problems.pdf"
---

# A Multi-AI-agent Framework Enabling End-to-end Finite Element Analysis for Solid Mechanics Problems

*🕒 **Published (v1):** 2026-05-28 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.00138)*

## TL;DR
AbaqusAgent is a six-agent LLM-driven framework that converts natural-language engineering prompts into fully executed Abaqus FEA simulations, covering geometry definition, meshing, boundary conditions, solver execution, iterative error correction, and result visualization. Evaluated on 50 solid mechanics problems spanning static, dynamic, nonlinear, buckling, and composite categories, it achieves 86% simulation success and 86% result accuracy using Claude Opus 4.6. The system couples a 104-case RAG knowledge base with a hierarchical hybrid retrieval strategy to guide input-file generation.

## Problem
FEA in Abaqus requires deep interdisciplinary expertise; API-based automation is rigid (predefined scripts, fixed templates, solver-specific parameters) and fails for novel geometries or boundary conditions. Existing LLM-FEA agents either target open-source solvers (FEniCS, MOOSE, Calculix) with limited validation sets or require domain-specific fine-tuning to reach acceptable success rates. No prior work addressed end-to-end automation for Abaqus—the dominant industrial FEA platform—across a broad, categorically balanced benchmark.

## Method
AbaqusAgent is a directed pipeline of six specialized agents:

1. **Interpreter Agent** — validates user prompts, extracts five key parameters (geometry, material, BCs, loads, output requests), and rephrases incomplete/ambiguous input into structured Abaqus-style specifications.
2. **Architect Agent** — parses the structured prompt into case name, domain, category, and material; runs a two-stage hybrid retrieval (FAISS semantic search → domain hard-filter → weighted re-ranking at 60% name / 30% category / 10% material) over a 104-case FAISS vector store (OpenAI `text-embedding-3-small`).
3. **Input Writer Agent** — generates the Abaqus `.inp` file using the retrieved case as a template plus system-prompt formatting constraints.
4. **Runner Agent** — submits the job to Abaqus; routes the `.odb` output to the Visualizer on success or the error logs to the Reviewer on failure.
5. **Reviewer Agent** — parses error files with LLM reasoning and an Abaqus-expert system prompt; issues targeted corrections back to the Input Writer (Algorithm 2, up to 15 iterations).
6. **Visualization Agent** — post-processes the `.odb` via Abaqus Python API to export deformation contour plots (PNG) and field data (CSV).

The RAG database contains 71 Abaqus benchmark cases and 33 textbook-style problems, each represented as structured metadata, natural-language problem description, and full input-file content.

## Key Contributions
- Six-agent orchestrated pipeline enabling fully automated end-to-end FEA from natural language to post-processed contour plots on Abaqus.
- Curated heterogeneous RAG of 104 solid mechanics cases with a hierarchical hybrid retrieval algorithm (FAISS + domain filter + weighted similarity re-ranking).
- 50-problem benchmark spanning five structural categories with three evaluation metrics: retrieval accuracy, simulation success, and result accuracy.
- Systematic ablation quantifying the independent contribution of RAG, the Reviewer Agent, and underlying LLM choice (Opus 4.6 vs. GPT-5.2).
- Demonstrated generalization to unseen geometries (elliptical/square holes) and complex nonlinear cases (Taylor rod impact, tensile necking) not in the RAG.

## Results
- **Overall**: 86% simulation success, 86% result accuracy across 50 cases (Claude Opus 4.6).
- **RAG cases (40)**: 85% retrieval accuracy, 92.5% simulation success, 92.5% result accuracy; avg. 28,761 tokens and 157 s per successful case.
- **Non-RAG cases (10)**: 60% simulation success, 60% result accuracy; avg. 48,200 tokens and 312 s per successful case.
- **Ablation (20 cases)**:
  - RAG + Reviewer: 90% success, 634,690 tokens, 3,518 s total.
  - No RAG + Reviewer: 80% success, 2,203,778 tokens (+247%), 7,758 s (+121%).
  - RAG + No Reviewer: 45% success, 246,622 tokens, 1,859 s.
- **LLM comparison (20 cases)**: Opus 4.6 — 90% success / 90% accuracy; GPT-5.2 — 65% success / 45% accuracy (with RAG). Gap widens without RAG: Opus 4.6 80%/80% vs. GPT-5.2 55%/35%.
- Outperforms ALL-FEM (71.79% on 39 cases with fine-tuned GPT-OSS 120B) and MechAgents (two validated cases); below MooseAgent (93% on 9 cases, open-source solver).

## Limitations
- No multiphysics simulation support (e.g., thermal-structural coupling beyond single-physics problems).
- Custom mesh workflows not supported; complex geometries require detailed meshing instructions in the prompt, creating residual expert burden.
- Iteration cap of 15 prevents resolution of problems requiring >15 correction cycles (authors note some cases need up to 40 iterations).
- Evaluation set contains 40 modified-RAG cases; generalization to entirely novel problem classes is measured on only 10 cases.
- Results accuracy validated primarily against Abaqus benchmarks and expert review rather than independent analytical solutions across all cases.
- Framework is coupled to closed-source Abaqus, limiting reproducibility and accessibility compared to open-source FEA agents.

## Relevance to Harnesses / Meta-Harnesses
AbaqusAgent is a concrete instance of a domain-specific multi-agent harness: a fixed orchestration graph of specialized agents that together automate a complex, multi-step scientific workflow end-to-end. The Reviewer-loop pattern (iterative self-correction with state history passed back to the writer) is a core meta-harness primitive, and the ablation study quantitatively demonstrates how harness components—RAG retrieval, error-correction loops, and LLM backbone—each contribute to pipeline reliability and cost. The sharp efficiency gap between RAG-guided and RAG-free operation (2.4× token cost, 2× latency) provides a concrete data point on the value of retrieval augmentation as a harness-level design choice. This paper complements work on CFD agents (FoamAgent, MetaOpenFOAM) and chemistry agents (LLM-RDF) as evidence that the multi-agent harness pattern is converging on a common architecture across computational science domains.

## Tags
#multi-agent #harness #rag #llm #finite-element-analysis #scientific-automation #iterative-self-correction #domain-specific-pipeline
