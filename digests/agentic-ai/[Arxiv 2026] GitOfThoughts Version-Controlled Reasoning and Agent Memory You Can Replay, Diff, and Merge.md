---
title: "GitOfThoughts: Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge"
authors: ["Pavan C Shekar", "Abhishek H S", "Aswanth Krishnan"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14470"
url: "http://arxiv.org/abs/2606.14470v1"
pdf: "paper/agentic-ai/[Arxiv 2026] GitOfThoughts Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge.pdf"
---

# GitOfThoughts: Version-Controlled Reasoning and Agent Memory You Can Replay, Diff, and Merge

## TL;DR
GitOfThoughts stores an LLM agent's reasoning tree as a git repository, mapping scored thoughts to commits, scores to git notes, and outcomes to tags, enabling replay, diff, and cross-agent memory merge at near-zero cost. A rigorous pre-registered evaluation across five memory substrates, two benchmarks, and two model scales finds that no memory format reliably improves accuracy on novel problems. Memory only helps when retrieved cases are near-duplicates of the test problem (cosine ≥ 0.8); the value of git-as-substrate is therefore auditability and provenance, not retrieval quality.

## Problem
LLM reasoning is ephemeral: chain-of-thought traces vanish with the context window, pruned tree-search branches leave no record, and existing memory stores (vector, graph, markdown) cannot be diffed, merged, or audited. This blocks reproducibility, incident review, memory transfer across agents, and detection of train–test leakage. Every other complex software process is version-controlled; reasoning is not.

## Method
GitOfThoughts maps the reasoning DAG directly onto git primitives: each scored thought is a `git commit` (with `thought.md`, `scores.json`, `trace.jsonl`, `metadata.json`), scores are `git notes`, validation outcomes are `git tags` (`success_*` / `failed_*`), and cross-problem memory lives on a long-lived `memory` branch. Retrieval is entirely stock git: keyword search via `git log --grep`, content search via `git log -S` (pickaxe), outcome filtering via `git tag -l`. A pluggable `MemoryBackend` interface lets the agent be held fixed while only the substrate changes, enabling controlled ablation across five backends: none, markdown, vector (all-MiniLM-L6-v2 + Chroma), graph (networkx spread-activation), and git. The outer reasoning loop is a depth-1 branching-factor-4 Tree-of-Thoughts with MCQ-aware expansion (four root children = four answer options); each node runs a ReAct inner loop with calculator, sympy, and LP solver tools. Experiments are pre-registered before model calls; hypotheses are committed to git before runs execute.

## Key Contributions
- Git-as-reasoning-substrate: one-to-one mapping of reasoning DAG onto git primitives, providing replay, line-level diff, signed authorship, and three-way merge at ~15 ms/write and ~48 ms/read overhead.
- **Copyability threshold (τ ≈ 0.8):** the first precisely bounded condition under which retrieved memory helps — near-duplicate retrieval (cosine ≥ 0.85) yields +12 to +13.5 pp on 7B and +22.5 to +28.5 pp on 32B; below τ, all substrates are null.
- Pre-registered null result: across GPQA-Diamond, MATH-500, five substrates, two backbones (Qwen3.5-9B, Qwen2.5-7B-Instruct), and n=500, no memory format reliably improves accuracy on novel problems.
- Retraction documented: an apparent +15 pp git trend at n=40 collapsed to +1.0 pp [−10.2, +11.2] at n=98 under its own pre-registered replication.
- Scale does not unlock method transfer: a 4.5× larger model (Qwen2.5-32B) steepens the copyability step (doubles near-duplicate payoff) but still yields null on method-transfer arms (−3.6 [−8.7, +1.5]).
- Functional distributed merge demonstration: two agents accumulated lessons on disjoint branches; five injected contradictory lessons surfaced as genuine git merge conflicts; concatenation silently retained all five contradictions.

## Results
- **GPQA-Diamond, system comparison (9B):** GitOfThoughts 47.0% vs. vanilla 33.0% vs. ReTreVal 34.0% — but arms run different compute budgets (600 s vs. 60 s vs. 180 s) and the gain is attributed to MCQ-aware expansion + compute, not memory.
- **MATH-500, n=500 (7B):** self-consistency (+3.4 pp [+0.6, +6.2]∗) is the only arm whose CI clears zero; git −0.8 pp, vector +1.6 pp, markdown +0.2 pp, static few-shot +0.4 pp — all within noise.
- **Copyability sweep, n=200 hard MATH seeds (7B/32B):** identical (cos 1.00): +28.5 pp∗ (32B); paraphrase (cos 0.95): +13.5 pp∗ (7B), +22.5 pp∗ (32B); method band (cos 0.72): −4.1 pp (7B), −3.6 pp (32B); same-subject/unrelated: null on both scales.
- **Cross-model robustness (GPQA, n=98, 7B):** none 40.8%; all substrates negative or null; vector worst on both models; null holds across both backbones.
- **Substrate cost:** git write ~15 ms, read ~48 ms, storage 191 KB (40 lessons); vector read ~20 ms, storage 656 KB; markdown write ~0.5 ms.

## Limitations
- System headline confounded by compute budget: GitOfThoughts runs 600 s/question vs. 60 s for vanilla; a compute-matched control is listed as future work.
- Evaluation limited to two adjacent open-weight backbones (7B–9B range for full suite; 32B only on the method-transfer arm); frontier-class models not tested.
- Memory encoded as short distilled lessons, not full episodic traces; richer memory formats may behave differently.
- ScienceWorld cross-episode arm is inconclusive due to a floored agent (~12% vs. SwiftSage's 84.7%), not a valid null for cross-episode transfer.
- Merged-memory accuracy phase (pre-registered) not yet run; the functional merge demonstration used stub lessons.
- Conflict surfacing in git merge requires a keyed file layout (one file per topic); content-hashed filenames defeat conflict detection, silently co-locating contradictions.
- AWQ int4 quantization on 32B may shift absolute accuracy levels; paired within-model deltas are unaffected but absolute comparisons to 7B are confounded.

## Relevance to Agentic AI / LLM Agents
The paper directly attacks agent memory persistence and auditability — two of the most cited structural weaknesses in production LLM agent systems. The copyability threshold finding (τ ≈ 0.8) provides a concrete, empirically derived boundary that should inform when retrieval-augmented agent memory is worth engineering at all: recurring/near-duplicate workloads justify it; novel-problem generalization does not, regardless of substrate. The git-as-substrate proposal offers a practical, zero-new-infrastructure path to the reproducibility and audit properties that agent deployment increasingly requires (incident review, leakage detection, multi-agent memory merge). The documented retraction — a promising result killed by its own pre-registered replication — also models the evaluation discipline the field needs as agent benchmarks proliferate with small-n single-run comparisons.

## Tags
#agent-memory #reasoning #tree-of-thoughts #benchmark #retrieval-augmented #reproducibility #evaluation #multi-agent
