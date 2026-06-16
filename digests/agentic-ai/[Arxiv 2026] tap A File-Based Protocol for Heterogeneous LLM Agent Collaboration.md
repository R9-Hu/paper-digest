---
title: "tap: A File-Based Protocol for Heterogeneous LLM Agent Collaboration"
authors: ["Minseo Kim"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T13:28:34+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14445"
url: "http://arxiv.org/abs/2606.14445v1"
pdf: "paper/agentic-ai/[Arxiv 2026] tap A File-Based Protocol for Heterogeneous LLM Agent Collaboration.pdf"
---

# tap: A File-Based Protocol for Heterogeneous LLM Agent Collaboration

*🕒 **Published (v1):** 2026-06-12 13:28 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14445v1)*

## TL;DR
`tap` is a file-based communication protocol enabling heterogeneous LLM agents (Claude and Codex) to collaborate on a shared codebase without a common runtime or central server. It uses markdown files in a shared `inbox/` directory as the canonical message store, supplemented by environment-specific real-time notification paths. A 27-day self-hosted operation produced 209 merged PRs and showed heterogeneous model pairings detected defects in 69.8% of reviews vs. 53.1% for homogeneous pairings.

## Problem
Existing multi-agent coding frameworks (ChatDev, MetaGPT, AutoGen) assume a common runtime, single vendor API family, or central conversation server, preventing direct collaboration between agents from different vendors (e.g., Claude + Codex). This also creates a "popularity trap" where homogeneous model ensembles share error tendencies and fail to catch each other's mistakes.

## Method
`tap` implements a two-tier message delivery system built on the local file system:

- **Tier 1 (File communication):** `tap_reply` writes a markdown file with YAML metadata to `inbox/` — this is the canonical, durable message. MCP tools read these files directly for inspection and recovery.
- **Tier 2 (Real-time communication):** After the file write completes, environment-specific notifications are dispatched — Claude MCP channel notifications and a WebSocket bridge for Codex. Receivers always re-read the original file rather than trusting the notification payload, making real-time delivery a latency optimization, not a reliability dependency.
- **Workspace isolation:** Each agent operates in a separate git worktree (keyed by `instanceId`) to prevent file conflicts.
- **Per-environment config:** The `tap add` command configures each agent's native config file (`.mcp.json` for Claude, `config.toml` for Codex, JSON for Gemini) without forcing a single API.

Operational artifacts (findings, retrospectives, handoffs, reviews) accumulate as files and serve as external memory for subsequent agent generations when context resets.

## Key Contributions
- Design of a file-first heterogeneous agent collaboration protocol requiring no shared runtime or central coordination server
- Demonstration that Claude and Codex can divide development/review roles on one repository across 37 agent generations over 27 days
- Empirical finding that heterogeneous model pairings yield higher defect detection rates than homogeneous pairings (69.8% vs. 53.1% across 375 review artifacts)
- Self-applied bootstrap: tap was used to develop and review tap itself, producing 209 merged PRs and 717 operational artifacts
- Open-source npm package `@hua-labs/tap` (v0.5.2)

## Results
- **Duration / scale:** 27 days, 37 agent generations, 209 merged tap-related PRs, 717 operational artifacts
- **Review detection rate (heterogeneous pairs):** 69.8% (183/262 artifacts recorded ≥1 defect or requested change)
- **Review detection rate (homogeneous pairs):** 53.1% (60/113 artifacts)
- **Breakdown by pair:** Codex-reviews-Claude: 71.0% (174/245); Codex-reviews-Codex: 62.1% (36/58); Claude-reviews-Claude: 43.6% (24/55); Claude-reviews-Codex: 52.9% (9/17)
- **Security-relevant findings:** 12 security or security-adjacent cases identified manually, including an `execSync` shell injection and a local write endpoint CSRF

## Limitations
- Observational data only; reviewer assignment was not randomized, and the dataset is dominated by Codex-reviews-Claude (245/375 artifacts), entangling model identity, reviewer role, cross-OS, and execution environment effects
- Review artifact is the unit of analysis, so repeated re-reviews of the same PR may inflate counts; detection rate ≠ independent defect count
- Real-time collaboration limited to Claude and Codex; Gemini participated only experimentally via polling
- Single organizational context and repository; generalization unvalidated
- Protocol itself evolved across generations, so early and late operating conditions differ
- LLM performance varies with base model updates, breaking longitudinal comparability

## Relevance to Agentic AI / LLM Agents
`tap` directly addresses the vendor lock-in problem in multi-agent software engineering systems, offering a lightweight, file-system-based interoperability layer that avoids the HTTP-based infrastructure assumed by protocols like Google A2A. The finding that heterogeneous model pairings improve defect detection aligns with ensemble diversity research and has practical implications for how multi-agent coding pipelines should be composed. The use of accumulated file artifacts as cross-generation external memory is a concrete mechanism for maintaining operational continuity when individual agents have bounded context windows — a key challenge for long-horizon agentic tasks. This work provides one of the first empirical, longitudinal accounts of heterogeneous LLM agent collaboration in a real production repository.

## Tags
#multi-agent #software-engineering #agent-interoperability #heterogeneous-llm #file-based-protocol #code-review #external-memory #agent-collaboration
