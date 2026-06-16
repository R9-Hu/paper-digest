---
title: "AutoRedTeamer: Autonomous Red Teaming with Lifelong Attack Integration"
authors: ["Andy Zhou", "Kevin Wu", "Francesco Pinto", "Zhaorun Chen", "Yi Zeng", "Yu Yang", "Shuang Yang", "Sanmi Koyejo", "James Zou", "Bo Li"]
source: "NeurIPS"
venue: "NeurIPS 2025"
published: "2025-01-01"
year: 2025
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "openreview:xQH4lDLIC0"
url: "https://openreview.net/forum?id=xQH4lDLIC0"
pdf: "paper/harness/[NeurIPS 2025] AutoRedTeamer Autonomous Red Teaming with Lifelong Attack Integration.pdf"
---

# AutoRedTeamer: Autonomous Red Teaming with Lifelong Attack Integration

## TL;DR
AutoRedTeamer is a fully automated, end-to-end red teaming framework for LLMs that combines a dual-agent architecture (red teaming agent + strategy proposer agent) with a memory-guided attack selection mechanism. It achieves 20% higher attack success rates on HarmBench against Llama-3.1-70B while reducing computational cost by 46% compared to prior methods. Unlike static frameworks, it continuously discovers and integrates new attack vectors from research literature ("lifelong" integration).

## Problem
Existing automated red teaming approaches suffer from three compounding weaknesses: (1) they optimize individual attack vectors in isolation, missing synergies between them; (2) they depend on human-curated test cases or specific seed prompts, preventing operation from high-level risk categories alone; (3) they cannot adapt to emerging attacks without manual re-engineering, making evaluations increasingly stale as new jailbreaking techniques are published.

## Method
AutoRedTeamer operates in two interleaved phases:

**Strategy Proposer Agent (lifelong attack integration):** Queries the Semantic Scholar API for recent jailbreaking papers, scores each by novelty, distinctiveness from the current library, and reported performance. Promising candidates enter an Attack Designer that implements each as a Python class inheriting a base attack interface, validates on a HarmBench subset (threshold: ASR ≥ 30%), and adds successful ones to the library with initial performance metrics.

**Red Teaming Agent (evaluation):** A pipeline of four modules—(1) *Risk Analyzer* decomposes high-level risk categories or specific prompts into testable components and scenarios; (2) *Seed Prompt Generator* creates diverse JSON-structured test cases across demographic, technical, and situational dimensions; (3) *Strategy Designer* selects attack combinations from the library using an LLM conditioned on test case content and memory state; (4) *Evaluator + Relevance Checker* judges success and discards off-topic test cases.

**Memory System:** Three-tier architecture—long-term memory (past test cases + selected attacks, retrieved via embedding similarity), attack metrics memory (per-attack and per-combination success rates, query costs, execution counts), and short-term trajectory memory for the current test case. Initialized with prior session data for cross-setting transfer.

## Key Contributions
- Dual-agent framework (red teaming agent + strategy proposer) that is unique in supporting fully automatic prompt generation from both specific behaviors and high-level risk categories.
- Memory architecture that tracks attack combination effectiveness via embedding-based retrieval and running statistics, enabling learned strategy selection rather than manual or random selection.
- Lifelong attack integration: automatic implementation and validation of new attacks discovered from research literature, without human intervention.
- Empirical demonstration of 20% higher ASR on HarmBench at 46% lower query cost, with the only nontrivial ASR on Claude-3.5-Sonnet (0.28 vs. ~0.00–0.05 for all baselines).
- Coverage of all 314 level-4 AIR taxonomy risk categories with prompt diversity (avg. pairwise cosine similarity 0.45) comparable to human-curated AIR-Bench (0.38), without human curation.

## Results
- **HarmBench (Llama-3.1-70B):** AutoRedTeamer ASR 0.82 vs. PAIR 0.60, TAP 0.60, AutoDAN-Turbo 0.67, Rainbow Teaming 0.18; 14 evaluation queries vs. AutoDAN-Turbo's 8 eval + 60k dev queries.
- **HarmBench (GPT-4o):** ASR 0.69 vs. TAP 0.66, AutoDAN-Turbo 0.76 (at 60k dev queries).
- **HarmBench (Mixtral-8x7B):** ASR 0.96, matching AutoDAN-Turbo (0.96) at a fraction of cost.
- **HarmBench (Claude-3.5-Sonnet):** ASR 0.28 vs. all baselines ≤ 0.05; AutoDAN-Turbo required 258 eval queries and still achieved only 0.02.
- **AIR-Bench (risk categories, Llama-3-Instruct-8B):** AutoRedTeamer ASR 0.90 vs. static AIR-Bench 0.21 on the same category set.
- **Ablation—memory removed (random selection):** ASR drops from 0.82 to 0.12 (85% reduction).
- **Ablation—fixed selection (no memory):** ASR 0.43 (48% reduction).
- **Ablation—Strategy Designer removed:** ASR 0.31 (62% reduction).
- **Ablation—Attack Proposer removed:** ASR 0.75 (only human-seeded attacks).

## Limitations
- Attack implementation relies entirely on LLM code generation; errors or hallucinated implementations may produce invalid or ineffective attacks without detection beyond the 30% ASR threshold.
- Strategy proposer may exhibit biases inherited from its LLM backbone in selecting which research to prioritize.
- Evaluation uses LLM-as-a-judge (GPT-4o with HarmBench prompt), which can misclassify borderline outputs.
- Black-box constraint excludes gradient-based attack vectors, limiting the library to semantic and structural transformations.
- Scope is limited to text-based LLMs; extension to agent-based or multimodal targets is noted as future work.

## Relevance to Harnesses / Meta-Harnesses
AutoRedTeamer is directly a *meta-harness* for security evaluation: it orchestrates a modular pipeline of specialized sub-agents (Risk Analyzer, Seed Prompt Generator, Strategy Designer, Attack Proposer, Evaluator) into an end-to-end evaluation workflow, and crucially includes a self-extending mechanism that automatically discovers, implements, and validates new tools (attack modules) to add to its own toolbox. The lifelong attack integration loop—query API → score novelty → implement as code → validate → register—is a canonical harness self-improvement pattern. The three-tier memory system (long-term, metric, short-term trajectory) demonstrates how meta-harnesses can accumulate cross-session operational knowledge to improve strategy selection without retraining. This work is particularly relevant as a model for how safety evaluation harnesses can be designed to remain current without manual curation.

## Tags
#red-teaming #multi-agent #meta-harness #llm-safety #attack-memory #lifelong-learning #jailbreaking #automated-evaluation
