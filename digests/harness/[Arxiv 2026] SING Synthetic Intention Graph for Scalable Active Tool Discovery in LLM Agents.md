---
title: "SING: Synthetic Intention Graph for Scalable Active Tool Discovery in LLM Agents"
authors: ["Qiao Xiao", "Haochen Shi", "Yisen Gao", "Wenbin Hu", "Huihao Jing", "Tianshi Zheng", "Baixuan Xu", "Ziheng Zhang", "Weiqi Wang", "Haoran Li", "Jiaxin Bai", "Yangqiu Song"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T11:37:37+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16591"
url: "http://arxiv.org/abs/2606.16591v1"
pdf: "paper/harness/[Arxiv 2026] SING Synthetic Intention Graph for Scalable Active Tool Discovery in LLM Agents.pdf"
---

# SING: Synthetic Intention Graph for Scalable Active Tool Discovery in LLM Agents

*🕒 **Published (v1):** 2026-06-15 11:37 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16591v1)*

## TL;DR
SING is an intention-aware active tool discovery framework that constructs a heterogeneous intention–tool graph over a corpus of 7,471 MCP tools and dynamically retrieves relevant tools via Personalized PageRank and semantic matching during ReAct-style agent execution. It eliminates the need to inject all tool schemas into context, reducing schema token exposure by 99.8% while improving tool retrieval recall and downstream task success rates over prior baselines.

## Problem
As harness-connected MCP tool ecosystems scale to hundreds or thousands of APIs and task-specific skills, exhaustive schema injection into agent context becomes prohibitively expensive, degrades model retention of task-critical information, and imposes a closed-world assumption. Existing retrieval-augmented alternatives use one-shot matching of the initial user utterance against isolated tool descriptions, which fails on long-horizon tasks where required capabilities emerge only through decomposition, intermediate observations, and dynamically induced subgoals.

## Method
SING operates in two phases. **Offline**, it constructs a heterogeneous intention–tool graph G = (V, E) with server, tool, and intention nodes. For each tool, an LLM synthesizes single-tool queries and expands them into multi-tool chains by judging input-output type compatibility and tool-chain coherence; atomic verb-object intention phrases are then extracted from these synthetic queries and globally deduplicated. Edges encode `has_tool` (server→tool), `has_intention` (tool↔intention), directed `tool_next`, and undirected `tool_cooccur` links with log-scaled frequency weights. **Online**, SING uses a dynamic ReAct framework where the agent can issue DISCOVER, INVOKE, or RESPOND actions at each step. On DISCOVER, the current task state is decomposed into a global request and subtasks; server-level discovery fuses cosine-similarity matching with Personalized PageRank (PPR) seeded from matched intention nodes and tool nodes. Tool-level reranking within retrieved servers scores each tool by a weighted sum of description similarity, intention similarity (max cosine over I(t)), and PPR graph score. Retrieved tools are added to the growing accessible tool set incrementally across turns.

## Key Contributions
- **Intention–tool graph**: heterogeneous graph linking 7,471 MCP tools across 779 servers via synthesized atomic intention nodes, capturing both capability semantics and tool collaboration patterns (31,756 nodes, 57,524 edges).
- **Active, state-conditioned discovery**: tools are retrieved incrementally throughout execution as subgoals emerge, not fixed at initialization.
- **Dual retrieval pipeline**: PPR-based graph propagation (Pipeline 1) combined with query semantic matching (Pipeline 2), fused at server and tool levels.
- **Large-scale MCP corpus**: curated 779 servers / 7,471 tools from Glama, Smithery, and MCPHub, filtered to deployable standalone servers across 15 domains.
- **99.8% schema-token reduction**: from 693,574 to 1,298 tokens on average in the full-corpus setting, with context overhead nearly independent of library size.

## Results
- **Global Recall@5** (server discovery): SING improves over MCP-Zero by +11.2 pp on MCP-Bench (0.790→0.902), +10.9 pp on MCP-Universe (0.434→0.544), +11.9 pp on MCP-Atlas (0.199→0.317); relative gains of 14.2%, 25.3%, and 59.8% respectively.
- **MRR** (global): SING improves over MCP-Zero by +5.7 pp on MCP-Bench, +21.4 pp on MCP-Universe, +17.2 pp on MCP-Atlas.
- **Downstream success rate** (MCP-Universe): SING vs. MCP-Zero — +8.1 pp (Restricted), +10.1 pp (Global); relative gains of 20.8% and 28.9%.
- SING under Global discovery (45.1% SR) **exceeds the Default (ground-truth server) setting** (42.0% SR) on MCP-Universe, suggesting subtask-specific tool context reduces irrelevant tool noise.
- On MCP-Atlas (Global): pass rate 40.2% vs. 34.0% (MCP-Zero); mean coverage 51.0% vs. 47.1%.
- On MCP-Bench (Global): overall score 67.5% vs. 66.7% (MCP-Zero).
- Schema exposure: 99.8% reduction (693,574 → 1,298 tokens); SING's token cost grows near-constant as pool size increases, while all-tools-in-context grows linearly.

## Limitations
- Downstream MCP evaluation is expensive (multi-step agent interactions, real tool calls, LLM-based judging), so experiments use a limited model family (DeepSeek-V4-Pro runner, Kimi-K2.5 judge); broader model comparisons are deferred.
- Real-world MCP execution has inherent variability from live service updates, changing external content, and tool availability; SING reduces discovery failures but cannot eliminate execution variability.
- Absolute task success on MCP-Atlas remains below the Default (ground-truth server) setting, consistent with lower retrieval accuracy on that benchmark's broad multi-step tasks.
- Graph construction depends on LLM-synthesized intentions, which can produce generic or poorly-aligned labels if tool schemas are incomplete or ambiguous (a known MCP tooling smell).

## Relevance to Harnesses / Meta-Harnesses
SING directly addresses the tool-management layer inside agent harnesses: rather than pre-loading a static tool registry into context (the canonical harness pattern), it proposes a graph-structured, dynamically updated tool inventory that grows as the task state evolves. This is a concrete architectural alternative for meta-harnesses managing large, heterogeneous MCP ecosystems, showing that intention-graph retrieval can replace or complement static schema injection with measurable context efficiency gains. The paper also formalizes the DISCOVER/INVOKE/RESPOND action abstraction, which is a clean interface point for harness designers separating tool discovery from tool execution. For researchers tracking harness design, the 99.8% schema-token reduction at 7,471-tool scale and the finding that dynamic discovery can outperform ground-truth-server baselines are directly actionable signals for how to architect tool routing in production harness systems.

## Tags
#tool-discovery #mcp #agent-harness #knowledge-graph #retrieval-augmented #personalized-pagerank #intention-modeling #scalable-tool-use
