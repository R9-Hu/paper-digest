---
title: "When the Tool Decides: LLM Agents Defer Blindly to Graph Neural Network Tools, and Stronger Backbones Defer More"
authors: ["Zhongyuan Wang", "Pratyusha Vemuri"]
source: "Arxiv"
venue: "TMLR"
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14476"
url: "http://arxiv.org/abs/2606.14476v1"
pdf: "paper/agentic-ai/[Arxiv 2026] When the Tool Decides LLM Agents Defer Blindly to Graph Neural Network Tools, and Stronger Backbones Defer More.pdf"
---

# When the Tool Decides: LLM Agents Defer Blindly to Graph Neural Network Tools, and Stronger Backbones Defer More

## TL;DR
LLM agents given a frozen GNN as a callable tool do not exercise judgment over its outputs — they adopt the tool's prediction 97.6–99.2% of the time, functioning as "GNN parrots." Stronger backbone models defer more completely, not less, and the accuracy cost of this blind deference grows with capability because stronger agents have better alternatives they never use.

## Problem
Prior graph–LLM agent systems assume the agent acts as a discerning caller that trusts the tool when appropriate and falls back to other evidence otherwise. This assumption has not been empirically tested. If agents simply obey tool outputs wholesale, claimed "agent+tool" gains are actually raw GNN gains, and the evaluation framing is misleading.

## Method
A frozen 2-layer GCN is exposed to a ReAct-style LLM agent as an explicit tool on ogbn-arxiv (169k nodes, 40 classes) and WikiCS. The tool returns three separate signals: predicted label+confidence, reconstruction anomaly score, and link probabilities. Four arms are compared under a matched per-query budget (5,000 tokens, 6 tool calls): A1 agent+GNN-tool, A2 agent+neighbour-label-lookup, A3 raw GNN alone, A4 agent with no graph tool. Backbone capability is swept across Qwen2.5-Instruct 0.5B–7B. Deference is measured as prediction-level agreement Pr[A1=A3]; cost is measured as the per-node oracle gap (accuracy of best-action selector minus A1). Test nodes are stratified by local homophily (low/mid/high) as an analysis axis. A selective-invocation gate (purity-threshold routing to A2 when τ>0.4) and a learned 4-feature router are evaluated post-hoc, with information-ceiling analysis via held-out kNN and cell estimators.

## Key Contributions
- Empirical evidence that agent+GNN-tool collapses into a GNN parrot: agreement 0.976–0.992 across homophily regimes (7B, 5 seeds, ogbn-arxiv).
- Demonstration that deference increases with backbone capability among tool-using models (agreement 0.60→0.98, Qwen2.5 1.5B→7B), disconfirming the intuition that stronger models are more skeptical.
- Quantification that the oracle gap (cost of deference) does not shrink with capability and roughly doubles at high homophily (3B→7B: 0.12→0.22), because the parrot is pinned to a frozen GNN while the agent's alternatives strengthen (neighbour-label tool overtakes GNN at high homophily at 7B: 0.81 vs. 0.71).
- Analysis of a selective-invocation gate: recovers ~half the high-homophily gap (0.71→0.83) but hurts in other regimes for no net global gain (0.481→0.475), and information-ceiling analysis shows standard uncertainty features can recover only one-sixth to one-third of the oracle headroom.
- Replication on WikiCS confirms the parrot effect (agreement 0.96–1.00) and positive oracle gap across all seed×bin pairs.
- Cross-family boundary condition: Mistral-7B and OLMo-2-7B show partial deference (agreement 0.53/0.60), not wholesale collapse, so extreme parroting (≥0.97) appears partly Qwen-specific, though majority deference generalises.

## Results
- **Parrot effect (7B, ogbn-arxiv):** A1 agreement with raw GNN = 0.976 (low), 0.976 (mid), 0.992 (high homophily); agreement with agent's own tool-free reasoning only 17–37%.
- **Capability scaling:** Agreement rises 0.60→0.97→0.98 (1.5B→3B→7B); 0.5B cannot reliably invoke the tool.
- **Oracle gap (7B):** 0.120 (low), 0.184 (mid), 0.220 (high); gap doubles at high homophily from 3B (0.12) to 7B (0.22), paired t=9.1.
- **Neighbour-label arm at 7B:** Overtakes GNN at high homophily (0.81 vs. 0.71) yet agent still defers to GNN.
- **Selective gate:** High homophily 0.71→0.83 (oracle 0.93); global accuracy 0.481→0.475 (slightly negative).
- **Information ceiling (ogbn-arxiv):** Best held-out gate over 4 features recovers 0.027–0.056 above parrot (≈one-sixth to one-third of oracle headroom of 0.175).
- **WikiCS replication:** Agreement 0.96–1.00; oracle gap positive in all 9 seed×bin pairs; ceiling analysis recovers only 12–14% of oracle headroom.

## Limitations
- Results scoped to ogbn-arxiv and WikiCS with the Qwen2.5 family and a 2-layer GCN; magnitude claims do not generalise by design.
- Backbone sweep limited to ≤7B due to single-GPU constraint; behaviour beyond 7B is unknown.
- The mechanism driving deference (e.g., tool output dominating context) is not isolated.
- Scaffold instructs the agent to consult tools before answering, so invocation is compliance; the study measures post-call adoption, not the decision to invoke.
- Scaffold is in Chinese for Qwen; cross-family results required a separate English scaffold experiment, complicating direct comparison.
- Extreme parroting (≥0.97 agreement) is partly Qwen-specific; other families show majority but not wholesale deference.
- Selective invocation remains an open problem; no gate tested achieves net global gain.

## Relevance to Agentic AI / LLM Agents
This paper directly challenges a foundational assumption in tool-augmented agent design: that the agent contributes meta-level judgment over when and how much to trust a learned tool. The finding that stronger models defer *more* is a counter-intuitive capability-scaling result relevant to anyone studying how agentic behaviour changes with model size. The work also operationalises a general evaluation failure mode — "agent+tool" systems may be silently reporting raw tool performance — which applies beyond the graph domain to any pipeline that calls a learned predictor as a black-box tool. The information-ceiling analysis provides a methodological template for bounding how much selective-invocation can theoretically recover, useful for researchers designing tool-routing mechanisms in agentic pipelines.

## Tags
#tool-augmented-agents #llm-agents #gnn #tool-overreliance #capability-scaling #selective-invocation #graph-learning #evaluation
