---
title: "EvoArena: Tracking Memory Evolution for Robust LLM Agents in Dynamic Environments"
authors: ["Jundong Xu", "Qingchuan Li", "Jiaying Wu", "Yihuai Lan", "Shuyue Stella Li", "Huichi Zhou", "Bowen Jiang", "Lei Wang", "Jun Wang", "Anh Tuan Luu", "Caiming Xiong", "Hae Won Park", "Bryan Hooi", "Zhiyuan Hu"]
source: "HuggingFace"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.13681"
url: "https://huggingface.co/papers/2606.13681"
pdf: "paper/agentic-ai/[HuggingFace 2026] EvoArena Tracking Memory Evolution for Robust LLM Agents in Dynamic Environments.pdf"
---

# EvoArena: Tracking Memory Evolution for Robust LLM Agents in Dynamic Environments

## TL;DR
EvoArena is a benchmark suite evaluating LLM agents under persistent environment evolution across terminal workflows, software repositories, and social preferences—domains where interfaces, rules, codebases, and user preferences change over time. The authors also propose EvoMem, a git-like patch-based memory paradigm that records not just the latest memory state but the full evolution history (what changed, why, and from what prior state). Current strong agents average only 39.6% step accuracy on EvoArena, and EvoMem yields consistent but modest gains (+1.5% on EvoArena, +6.1%/+4.8% on GAIA/LoCoMo).

## Problem
Existing agent benchmarks evaluate on static environment snapshots, but real deployment environments continuously evolve: APIs change, codebases accumulate milestones, and user preferences shift over time. Standard memory systems suffer from *state collapse*—they overwrite prior memory with newer observations, losing context about when earlier behaviors were valid. An agent handling a workflow permission change may discard a still-valid prior rule that applies to an older release or future rollback. No benchmark measured this version-aware adaptation capability, and no memory design preserved the evidence trail needed for it.

## Method
**EvoArena** structures evaluation as version chains—ordered sequences of progressive environment releases sharing the same underlying goal but changing operational details:
- **Terminal-Bench-Evo**: 89 Terminal-Bench tasks evolved into 5-version chains (441 total instances, 352 evolved) with changes spanning I/O protocols, CLI/API, dependency toolchains, workspace structure, and policy constraints.
- **SWE-Chain-Evo**: 50 evolution chains from 12 GitHub repositories, 493 chain-step instances, 145 unique milestones (5–15 steps/chain). Oracle-state progression applies the reference patch after each step, isolating each agent's local adaptation from compounding prior errors.
- **PersonaMem-Evo**: 10 persona conversations, 505 multiple-choice preference-inference questions (avg 174.7K tokens, 597 turns/conversation) requiring agents to track evolving user preferences across implicit multi-turn evidence.

Two metrics: **step accuracy** (per-version correctness) and **chain accuracy** (all steps in a chain solved consecutively).

**EvoMem** augments any base memory system with an append-only patch history. For each non-additive memory update Mt−1 → Mt, EvoMem records a patch containing: summary of changes, reason for the update, difference from prior state, and relevant triggering context. At inference, the agent retrieves the current memory state by default and selectively fetches relevant patches when a query involves overwritten states, version conflicts, or temporal trajectories. The base memory updater is left unchanged.

## Key Contributions
- EvoArena benchmark covering three complementary evolution regimes (workflow, software, social), with step- and chain-level evaluation.
- EvoMem: lightweight, model-agnostic patch-based memory augmentation that makes memory evolution traceable and reusable.
- Empirical finding that even frontier models degrade substantially under persistent evolution (average 39.6% step accuracy).
- Mechanistic analysis showing EvoMem improves row-level evidence capture and retention of complete evolving environment states.

## Results
- Average step accuracy across all EvoArena domains: **39.6%** (all tested frontier models).
- GPT-5.5: **50.8% step / 27.2% chain** accuracy (best step performer).
- Gemini-3.1-Pro: **40.2% step / 29.2% chain** (best chain performer).
- DeepSeek-V4-Pro: **37.3% step / 20.7% chain** (lowest shown).
- EvoMem average gain on EvoArena: **+1.5%** across agents and backbone models.
- EvoMem chain-level accuracy gain on EvoArena: **+3.7%**.
- EvoMem on GAIA: **+6.1%**; on LoCoMo: **+4.8%**.
- EvoMem shows strongest gains on PersonaMem-Evo temporal trajectory and multi-pattern synthesis questions, where agents must track dispersed evolving evidence.

## Limitations
- EvoMem gains on EvoArena are small (+1.5% step average), suggesting the benchmark poses challenges beyond what patch history alone can address.
- Chain accuracy remains extremely low for all tested models (maximum ~29.2%), indicating sustained multi-step reliability is far from solved.
- SWE-Chain-Evo is heavily skewed toward Go (81.9%) and Python (18.1%) repositories with only 12 repositories, limiting language and domain diversity.
- PersonaMem-Evo is built on synthetic persona conversations derived from PersonaHub, which may not capture the full complexity of real longitudinal user interactions.
- Small scale in some domains (10 persona conversations, 89 initial terminal tasks) limits statistical power for fine-grained analysis.
- The paper text is truncated; additional stated limitations in experiments or discussion sections may exist.

## Relevance to Agentic AI / LLM Agents
EvoArena addresses a critical blind spot in agent evaluation: virtually all existing benchmarks freeze the environment at construction time, while deployed agents must operate over environments that continuously evolve. The chain accuracy metric specifically quantifies whether agents can *sustain* correct behavior across linked evolutionary steps—a capability that step-level metrics systematically overestimate. EvoMem operationalizes a "git for agent memory" concept, treating memory updates as versioned, auditable evidence rather than destructive overwrites, which directly informs the design of long-lived, deployment-robust agent memory systems. The finding that frontier models achieve only ~27–29% chain accuracy despite reasonable step-level performance reveals a fundamental reliability gap for agents that must handle real-world versioned environments.

## Tags
#benchmark #memory #dynamic-environments #evaluation #chain-accuracy #software-engineering #personalization #long-horizon
