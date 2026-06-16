---
title: "SING: Synthetic Intention Graph for Scalable Active Tool Discovery in LLM Agents"
authors: ["Qiao Xiao", "Haochen Shi", "Yisen Gao", "Wenbin Hu", "Huihao Jing", "Tianshi Zheng", "Baixuan Xu", "Ziheng Zhang", "Weiqi Wang", "Haoran Li", "Jiaxin Bai", "Yangqiu Song"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T11:37:37+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16591"
url: "http://arxiv.org/abs/2606.16591v1"
pdf: "paper/agentic-ai/[Arxiv 2026] SING Synthetic Intention Graph for Scalable Active Tool Discovery in LLM Agents.pdf"
---

# SING: Synthetic Intention Graph for Scalable Active Tool Discovery in LLM Agents

*🕒 **Published (v1):** 2026-06-15 11:37 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16591v1)*

## TL;DR
SING is an intention-aware active tool discovery framework that builds a heterogeneous graph linking user intentions, tool capabilities, and tool collaboration patterns, enabling LLM agents to dynamically retrieve relevant tools from large-scale MCP ecosystems without exhaustive schema injection. Evaluated on 7,471 tools across 779 MCP servers, SING improves Global Recall@5 by up to 59.8% and downstream task success rate by up to 28.9% over prior retrieval baselines while reducing schema token exposure by 99.8%.

## Problem
Existing approaches to tool selection either inject all available tool schemas into context (infeasible at scale, imposes a closed-world assumption) or rely on one-shot retrieval that matches user utterances against isolated tool descriptions. One-shot retrieval is fragile for long-horizon tasks where required tool capabilities emerge progressively through decomposition, intermediate observations, and newly induced subgoals—a surface query for "distance between two national parks" may superficially match map tools but actually requires geocoding, coordinate extraction, and numerical calculation in sequence.

## Method
SING has three components:

**Intention graph construction (offline):** For each tool, an LLM synthesizes natural-language queries, expands them into multi-tool chains (using type-compatible and LLM-judged tool-next links), and extracts atomic verb-object "intention" phrases. Semantically similar intentions are merged across tools and servers into shared intention nodes. A heterogeneous graph G = (V, E) is built with server, tool, and intention nodes; edges include `has_tool`, `has_intention`, `tool_next` (directed, within chains), and `tool_cooccur` (undirected). Collaboration edges are weighted by log-scaled co-occurrence frequency for Personalized PageRank (PPR).

**Dynamic ReAct framework (online):** The agent interleaves DISCOVER / INVOKE / RESPOND actions. On DISCOVER, the current task state and history are converted to a query, and the accessible tool set grows incrementally—new subgoals trigger additional retrieval rather than being constrained to a one-shot candidate set.

**Hierarchical discovery layer:** Server-level scoring fuses cosine-similarity-based semantic matching with PPR propagation seeded from matched intention nodes and semantically relevant tool nodes. Tool-level scoring within retrieved servers combines description similarity, max-intention similarity, and PPR score with tunable weights λ.

The graph contains 31,756 nodes and 57,524 edges; Qwen3-Embedding-8B is used for embeddings; DeepSeek-V3.2 synthesizes intentions; DeepSeek-V4-Pro runs downstream agents.

## Key Contributions
- Intention-aware tool discovery framing: uses synthesized verb-object intentions as an intermediate abstraction between user goals and low-level tool schemas, enabling goal-level semantic matching beyond schema text.
- Large-scale MCP tool corpus: 779 servers, 7,471 tools across 15 domains, filtered from 1,141 raw servers for reproducible evaluation.
- Intention–tool graph with collaboration edges: captures cross-server functional relations and multi-step tool-chaining patterns via PPR propagation.
- Dynamic, multi-turn retrieval: unlike one-shot methods, SING triggers re-discovery as new subgoals emerge during execution.
- 99.8% reduction in schema token exposure vs. all-tools-in-context (693,574 → 1,298 tokens average), with context cost nearly constant as pool size scales.

## Results
- **Server discovery (Global, Recall@5):** SING vs. MCP-Zero — +0.112 on MCP-Bench (14.2% relative), +0.110 on MCP-Universe (25.3%), +0.119 on MCP-Atlas (59.8% relative).
- **Server discovery (Global, MRR):** improvements of +0.057, +0.214, +0.172 on MCP-Bench, MCP-Universe, MCP-Atlas respectively vs. MCP-Zero.
- **Downstream success rate (MCP-Universe):** SING (Global) 45.1% SR vs. MCP-Zero (Global) 35.0% SR — +10.1 pp absolute, +28.9% relative. SING (Global) also exceeds the default ground-truth-server setting (38.2% SR) by 6.8 pp.
- **MCP-Atlas (Global):** SING pass rate 40.2% vs. MCP-Zero 34.0%; mean coverage 51.0% vs. 47.1%.
- **MCP-Bench (Global):** SING overall score 67.5% vs. MCP-Zero 66.7%.
- **Token efficiency:** schema exposure reduced from 693,574 to 1,298 tokens (99.8%) in the full-corpus setting.

## Limitations
- Downstream evaluation is expensive (multi-turn real tool calls + LLM judging), restricting experiments to a limited set of models; broader agent backbone generalization is untested.
- Real-world MCP execution has inherent variability: live service updates, availability changes, and external content drift can affect results beyond the control of discovery quality.
- The graph is constructed offline with synthetic queries; distribution shift between synthesized intentions and actual deployment queries is not characterized.
- Tool description quality varies (unclear purpose, missing usage guidance, opaque parameters); SING inherits this noise at graph-construction time.
- Error analysis shows that improved discovery shifts—but does not eliminate—failures to downstream execution stages (parameter filling, output parsing, tool sequencing).

## Relevance to Agentic AI / LLM Agents
SING directly addresses the open-world tool-use bottleneck that becomes critical as agent harnesses scale to thousands of MCP-connected APIs—a paradigm increasingly dominant in production agent deployments (OSWorld, ClawBench, WildClawBench). The key insight—that intention-level abstractions synthesized from tool-use trajectories outperform raw schema or description matching—is transferable to any retrieval-augmented agent architecture managing large skill/tool registries. The work also demonstrates empirically that better tool retrieval can raise downstream success *above* the oracle (ground-truth server) baseline, suggesting tool context quality matters as much as tool availability. For researchers tracking LLM agent infrastructure, SING provides both a practical retrieval technique and a 7,471-tool MCP benchmark suite useful for future evaluation.

## Tags
#tool-retrieval #mcp #knowledge-graph #react-agent #retrieval-augmented #tool-discovery #scalable-agents #active-discovery
