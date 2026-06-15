---
title: "LLM Agents Can See Code Repositories"
authors: ["Dongjian Ma", "Silin Chen", "Yufei Yang", "Yulin Shi", "Yanfu yan", "Xiaodong Gu"]
source: "HuggingFace"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14061"
url: "https://huggingface.co/papers/2606.14061"
pdf: "paper/agentic-ai/[HuggingFace 2026] LLM Agents Can See Code Repositories.pdf"
---

# LLM Agents Can See Code Repositories

## TL;DR
SeeRepo augments coding agents with visual dependency-graph renderings of code repositories, enabling MLLMs to consume structural context visually rather than through linearized text. Evaluated on SWE-bench Verified across four frontier models, hybrid text+vision reduces input token cost by up to 46% while maintaining or improving issue-resolution accuracy. Vision-only interaction, by contrast, degrades accuracy and inflates costs.

## Problem
Current coding agents flatten repository structure (dependency graphs, call hierarchies, containment) into sequential text tokens, requiring models to re-infer non-linear structural relationships under tight context budgets. This iterative grep-then-read exploration is both token-expensive and error-prone. While graph-based representations exist, they are invariably linearized before model input, losing 2D spatial and topological cues. No prior work systematically studied whether visual modalities can help MLLMs understand repositories more efficiently.

## Method
SeeRepo extends Mini-SWE-Agent with a query-driven repository visualization tool. A directed heterogeneous graph G = (V, E, A, R) is pre-constructed via AST-based static analysis, capturing four relation types: `contains`, `imports`, `invokes`, and `inherits`. At inference time, the agent calls `graph_query(node, edge_type, depth)`, which performs bidirectional BFS up to depth *k*, renders a distance-aware subgraph via Graphviz DOT (layered left-to-right layout, HTML-table node labels with semantic icons, junction nodes for edge merging), and returns a PNG image. This image is concatenated with standard text tokens in the MLLM's context—the ViT encodes image patches, a learned projection maps them into the LLM embedding space, and cross-modal attention operates jointly. The agent autonomously determines traversal depth per query. Three visual layouts are compared: **Graph** (explicit directed edges), **Nested** (dashed bounding boxes for directory grouping), **Tabular** (color-coded flat list, no topology). Visualization is also ablated across three pipeline stages: fault localization, patch repair, and patch validation.

## Key Contributions
- First systematic empirical study of multimodal (visual) repository representations for repository-level coding agents, across four frontier MLLMs on SWE-bench Verified (500 instances).
- Establishes a clear performance boundary: vision-only input degrades accuracy by 13.6–34.1 points and inflates cost by 27–268%; hybrid text+vision reduces cost up to 46% while preserving or improving accuracy.
- Design and implementation of SeeRepo: AST-derived dependency graph + query-centered Graphviz subgraph rendering integrated into an agentic tool-calling loop.
- Ablations across visual layout (graph/nested/tabular) and invocation stage (localization/repair/validation) identifying optimal configuration.
- Demonstrates transfer: efficiency and accuracy gains hold on SWE-Rebench Leaderboard 2026.03 and SWE-QA.

## Results
- **Vision-only vs. text baseline (SWE-bench Verified):** GPT-5-mini: 55.0%→41.4% (−13.6 pp), cost +42%; Doubao-Seed-2.0-Lite: 51.0%→16.9% (−34.1 pp), cost +268%; Kimi K2.5: 70.3%→55.0% (−15.3 pp), cost +27%.
- **Hybrid text+vision (SeeRepo) vs. text-only (SWE-bench Verified):**
  - GPT-5-mini: Pass@1 55.0%→55.4% (+0.4), input tokens −25%, cost −26%
  - GPT-5.1: Pass@1 51.0%→48.8% (−2.2), cost −46%
  - Kimi K2.5: Pass@1 68.8%→70.6% (+1.8), cost −3%
  - Doubao-Seed-2.0-Lite: Pass@1 51.0%→52.0% (+1.0), cost −6%
- **Visual layout (GPT-5-mini, 500 instances):** Graph: Pass@1 +0.4, cost −26%; Nested: +0.8, cost −18%; Tabular: +1.2, cost −14%; agent-decided depth (SeeRepo default) achieves −25% input tokens and −26% cost, best efficiency.
- **Stage ablation (GPT-5-mini):** Localization: Pass@1 +0.4, cost −26%; Repair: Pass@1 −5.0, cost −5%; Patch Validation: Pass@1 −3.4, cost −4%.
- **SWE-Rebench (110 instances, GPT-5-mini):** Pass@1 25.45%→26.36%, input tokens −34.89%, cost −9.6%.
- **SWE-QA (GPT-5-mini):** Score 66.8→67.2, API calls −35.7%, cost −26.2%.

## Limitations
- GPT-5.1 shows a −2.2 pp accuracy regression: stronger models may be distracted by topologically proximate but semantically tangential dependencies exposed by graph queries.
- Gains are modest in absolute accuracy terms; primary benefit is cost/token efficiency rather than large accuracy improvement.
- Only evaluated on Python repositories (SWE-bench Verified); generalization to polyglot or non-Python codebases is untested.
- AST-based static analysis may miss dynamic relationships (monkey-patching, runtime imports), potentially producing incomplete or misleading graphs.
- Kimi K2.5 evaluated on only 400 of 500 instances in vision-only condition due to compute cost.
- Vision-only results suggest current MLLMs remain fundamentally text-symbolic in their code reasoning; visual modality is useful only as a supplement, not a replacement.

## Relevance to Agentic AI / LLM Agents
This paper directly advances the design of coding agents by demonstrating that the *modality* of tool output—not just the content—significantly affects agent efficiency, a relatively underexplored axis in agentic system design. The finding that visual structural context is most valuable at the **fault localization** stage, and harmful at repair/validation stages, has immediate implications for stage-aware tool provisioning in multi-step agent pipelines. The SeeRepo framework exemplifies a broader pattern of augmenting LLM agents with structured, query-driven external representations that compress multi-step exploration into single tool calls—directly relevant to work on tool design, context management, and agent scaffolding. The token-efficiency gains (up to 46% cost reduction) matter practically for long-horizon agentic tasks where context limits are a hard constraint.

## Tags
#coding-agents #multimodal #repository-understanding #swe-bench #tool-use #context-efficiency #fault-localization #mllm
