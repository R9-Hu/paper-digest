---
title: "Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks"
authors: ["Mengyu Zheng", "Kai Han", "Boxun Li", "Haiyang Xu", "Yuchuan Tian", "Wei He", "Hang Zhou", "Jianyuan Guo", "Hailin Hu", "Lin Ma", "Chao Xu", "Guohao Dai", "Lixue Xia", "Yunchao Wei", "Yunhe Wang", "Yu Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-10"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12344"
url: "http://arxiv.org/abs/2606.12344v1"
pdf: "paper/harness/[Arxiv 2026] Claw-SWE-Bench A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks.pdf"
---

# Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks

## TL;DR
Claw-SWE-Bench is a multilingual SWE-bench-style benchmark and adapter protocol that treats the agent harness as a controlled experimental variable, enabling heterogeneous "claws" (agent harnesses) to be compared under fixed tasks, prompts, budgets, and scoring pipelines. It includes 350 GitHub issue-resolution instances across 8 languages and 43 repositories, plus an 80-instance cost-aware Lite subset. Results show harness choice alone spans 27.4 pp Pass@1 under a fixed model—comparable to or exceeding the effect of swapping model tiers.

## Problem
Existing SWE-bench evaluations conflate three causally distinct factors—the LLM, the agent harness, and the task set—making it impossible to attribute performance differences to harness design. General-purpose agents (e.g., OpenClaw) also cannot enter SWE-bench scoring directly due to contract mismatches: the evaluator requires a `model_patch` diff, not an agent session transcript. No prior benchmark has made the harness a controlled experimental variable while simultaneously reporting end-to-end cost alongside accuracy.

## Method
**Two-layer architecture:**
1. **Adapter protocol** — each harness implements five lifecycle methods (`create_agent`, `send_task`, `backup_session`, `delete_agent`, `get_docker_args`). A shared orchestrator drives all harnesses through this interface; patch collection is done from repository Git state (not parsed from agent output), making it output-format-agnostic.
2. **Standardized execution pipeline** — fixes task prompt template, Docker workspace (SWE-bench evaluation images with `/testbed` mount), per-instance 3600 s wall-clock timeout, worker concurrency (3), patch extraction, and upstream SWE-bench evaluator. Future-commit visibility in non-Python SWE-bench-Multilingual containers is removed by stripping reachable Git history past `base_commit`.

**Lite-80 subset selection** — formulated as a binary selection problem with hard constraints (10 instances/language, 2/3/3/2 difficulty-quartile quota) and a three-term objective: resolve-rate parity (L1 vs. full-350 across 17 calibration columns), pairwise ranking hinge (penalty if Lite reverses pairs differing by >3 pp on full-350), and log-cost parity. Solved via per-language 200-restart 1-swap local search.

**Evaluation metrics:** Pass@1, total API cost (USD), mean wall-clock duration, input/output tokens, turn count, and cache hit rate (`#cache_read_tokens / (#input_tokens + #cache_read_tokens)`).

## Key Contributions
- A unified adapter protocol enabling heterogeneous harnesses (general-purpose and coding-specific) to enter SWE-bench scoring under identical conditions.
- Full 350-instance multilingual benchmark (8 languages, 43 repos) drawn from SWE-bench-Multilingual + SWE-bench-Verified-Mini with future-commit leak fix.
- Claw-SWE-Bench Lite: 80-instance cost-aware, rank-aware subset at ~22.9% of full-run cost, with mean Pass@1 deviation of +0.4 pp from full-350 across 17 calibration columns.
- Empirical decomposition of harness vs. model contribution: harness spread reaches 27.4 pp (Qwen 3.6-flash), model spread reaches 29.4 pp (fixed OpenClaw across 9 LLMs).
- Cost-aware Pareto analysis showing that accuracy and API cost are not monotonically aligned across claw–model combinations.
- Quantification of future-commit leakage: cleanup drops Pass@1 by up to 8.0 pp (Claude Opus 4.7) with no model showing an increase.

## Results
**Adapter diagnostic (GLM 5.1, full-350):**
- Bare adapter (model writes unified diff directly): 19.1% Pass@1
- Full adapter (model edits files; runner exports patch from Git): 73.4% Pass@1; apply failures <1.5%

**LLM sweep (fixed OpenClaw, 9 models, full-350):**
- GPT 5.5: 78.0% Pass@1, $1399.1 total cost
- Claude Opus 4.7: 77.1%, $1082.0
- GLM 5.1: 73.4%, $277.0
- DeepSeek-V4 Flash: 70.3%, $8.2 (highest cache hit rate: 98.5%)
- Seed 2.0-mini: 48.6% (lowest)
- Model spread: 29.4 pp

**Claw sweep (fixed GLM 5.1 and Qwen 3.6-flash, 5 claws, full-350):**
- GLM 5.1: OpenClaw 73.4% ($277) → NanoBot 60.9% ($768.8); spread 12.5 pp
- Qwen 3.6-flash: OpenClaw 66.0% ($71.5) → GenericAgent 38.6% ($14.5); spread 27.4 pp
- Pareto-dominant points: OpenClaw × GLM 5.1 (73.4%, $277), OpenClaw × Qwen 3.6-flash (66.0%, $71.5), ZeroClaw × Qwen 3.6-flash (58.3%, $49.3)

**Lite-80 validation:**
- Mean Pass@1 full-350: 0.639; Lite-80: 0.643 (+0.4 pp)
- Cross-claw mean absolute deviation: 1.88 pp; max: 3.68 pp (NanoBot × Qwen 3.6-flash)
- Lite-80 cost: ~22.9% of full run across input tokens, output tokens, cache-read tokens, and wall-clock

## Limitations
- The adapter diagnostic compares bare vs. full adapter as a whole; individual adapter components (workspace prep, shared prompt, Git-based extraction, patch cleaning) are not ablated separately.
- Token statistics are not uniformly exposed across all five claws, preventing cross-harness token-level cost attribution.
- Wall-clock duration conflates remote API latency with local compute, reducing its precision as a harness efficiency signal.
- The five evaluated claws are all presented as an OpenClaw-family or related systems; broader coverage of architecturally distinct harnesses is not demonstrated.
- Lite-80 C/C++ and Ruby deviations (+2.94 pp and +2.65 pp) are the largest; the subset is less faithful for these languages.
- Single-run evaluation (no variance estimates); stochastic harness behavior is not characterized.

## Relevance to Harnesses / Meta-Harnesses
Claw-SWE-Bench directly operationalizes the concept of a harness as an experimental variable rather than an incidental implementation detail—the core concern of meta-harness research. The adapter protocol is itself a lightweight meta-harness: a thin orchestration layer that normalizes lifecycle, workspace, and output contracts across heterogeneous inner harnesses without dictating their internal agent loops. The finding that harness choice moves Pass@1 by 27.4 pp under a fixed model is a quantitative grounding for claims that scaffold design is a first-order factor, complementing qualitative taxonomies in the broader harness literature. The cost-aware Pareto framing and Lite subset methodology offer transferable patterns for any meta-harness evaluation that must balance coverage, reproducibility, and evaluation budget.

## Tags
#benchmark #agent-harness #swe-bench #meta-harness #coding-agents #evaluation-protocol #cost-aware #multilingual
