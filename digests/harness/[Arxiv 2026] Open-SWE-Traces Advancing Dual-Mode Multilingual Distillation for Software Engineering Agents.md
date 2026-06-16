---
title: "Open-SWE-Traces: Advancing Dual-Mode Multilingual Distillation for Software Engineering Agents"
authors: ["Wasi Uddin Ahmad", "Nikolai Ludwig", "Somshubra Majumdar", "Boris Ginsburg"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T22:10:06+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16038"
url: "http://arxiv.org/abs/2606.16038v1"
pdf: "paper/harness/[Arxiv 2026] Open-SWE-Traces Advancing Dual-Mode Multilingual Distillation for Software Engineering Agents.pdf"
---

# Open-SWE-Traces: Advancing Dual-Mode Multilingual Distillation for Software Engineering Agents

*🕒 **Published (v1):** 2026-06-14 22:10 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16038v1)*

## TL;DR
Open-SWE-Traces is a corpus of 207,489 agentic software engineering trajectories across nine programming languages, synthesized by running two frontier LLMs through two agent harnesses (OpenHands and SWE-agent) on real-world PRs from SWE-rebench-v2. The dataset is explicitly structured for **dual-mode distillation**—pairing "thinking" (chain-of-thought) traces from MiniMax-M2.5 with "non-thinking" execution traces from Qwen3.5-122B. Fine-tuning Qwen3-Coder-30B-A3B on this corpus yields a model reaching 61.7% on SWE-bench Verified.

## Problem
The SWE agent field has outpaced its training infrastructure: multilingual evaluation benchmarks (Multi-SWEbench, SWE-PolyBench) now exist, but the community lacks large-scale, diverse **interaction traces** and pre-built containerized environments to train models against them. Existing datasets are either Python-only, too small, or lack the thinking/non-thinking modality split needed for switchable-reasoning agents.

## Method
The pipeline has four stages:

1. **Repository selection** — 20,000 real-world PRs filtered from SWE-rebench-v2 (20 languages → 9 permissively licensed languages: Python, Go, TS, JS, Rust, Java, PHP, C, C++).
2. **Trajectory synthesis** — MiniMax-M2.5 (thinking mode) and Qwen3.5-122B-A10B (non-thinking mode) are run inside both **OpenHands** and **SWE-agent** harnesses, producing heterogeneous traces across model architectures and scaffolds.
3. **Multi-stage quality filtering** — Stage 1 discards corrupted/incomplete runs; Stage 2 prunes task-incomplete, structurally invalid (empty patches, test-suite cheats), and malformed tool-use trajectories.
4. **TrajectoryScanner (git-hacking detection)** — AST-based auditor categorizes every Bash command into a risk hierarchy; trajectories using banned git introspection commands (`reflog`, `blame`, `log`, `diff` outside safe contexts) are removed.

Distillation trains Qwen3-30B-A3B variants (Thinking, Instruct, Coder) on the full corpus with SFT (lr=1e-5, batch=32, ctx=131k, 3 epochs). Dual-mode inference is controlled via `/think` and `/no_think` prompt triggers.

## Key Contributions
- **Open-SWE-Traces corpus**: 207,489 trajectories across 9 languages and 4 harness×modality combinations; ~40.6% of traces contain a verified-passing patch (65,244 resolved).
- **Dual-mode distillation strategy**: explicit separation of thinking vs. non-thinking trajectories enabling a single model to switch reasoning modes at inference time.
- **Open-SWE-Agent**: Qwen3-Coder-30B-A3B fine-tuned model achieving 61.7% SWE-bench Verified, 57.1% SWE-bench Multilingual, 36.8% SWE-bench Pro.
- **TrajectoryScanner**: AST-based git-hacking detector that filters adversarial trajectory shortcuts from training data.
- **Ablation study** isolating effects of harness choice, Python-only vs. multilingual data, resolved-only vs. full corpus filtering, and thinking vs. non-thinking modality.

## Results
- **SWE-bench Verified**: Open-SWE-Agent `/no_think` achieves **61.7%** (MSWEA) / 60.2% (MOH); `/think` achieves 59.3% / 59.1%. Base Qwen3-Coder-30B-A3B: 51.6%.
- **SWE-bench Multilingual**: Open-SWE-Agent `/no_think` achieves **57.1%** (MSWEA) / 48.4% (MOH). Base: 33.5%.
- **SWE-bench Pro**: Open-SWE-Agent `/think` achieves **36.8%** (MSWEA). Base: 28.4%.
- Ablation — cross-lingual transfer: Python-only → full corpus gains +14% absolute on SWE-M (no-think: 43.1% → 57.1%).
- Ablation — data filtering: resolved-only → full corpus gains +7.5% on SWE-M no-think (49.6% → 57.1%).
- Thinking traces reduce avg. assistant turns per trajectory by 38% (94.08 → 58.22) in OpenHands; non-thinking is superior at inference for resolved rate in most settings.
- Cross-harness generalization: MSWEA-trained models transfer to MOH more cleanly than MOH-trained models to MSWEA.

## Limitations
- Student models inherit biases and errors of teacher models (MiniMax-M2.5, Qwen3.5-122B); no mitigation beyond ensemble diversity.
- Environmental stochasticity introduces score variance; triple-run averaging only partially mitigates this.
- MOpenHands integration issues cause 5–10% loop-exhaustion failures for Open-SWE-Agent, suppressing MOH scores on SWE-M.
- MOpenHands excluded entirely from SWE-bench Pro evaluation due to persistent integration failures.
- Coverage limited to nine languages despite SWE-rebench-v2 spanning twenty; C and C++ are heavily underrepresented (983 combined trajectories vs. 48k for Python).
- Dual-mode advantage in resolved rate favors no-think at current training scale; authors hypothesize think-mode gains require more data.

## Relevance to Harnesses / Meta-Harnesses
This paper is directly relevant because it treats **agent harnesses as first-class experimental variables**: it runs the same LLMs through both OpenHands and SWE-agent, quantifies cross-harness generalization gaps, and identifies harness-specific failure modes (loop exhaustion in MOpenHands, patch rendering bugs in MSWEA for Go). The finding that harness choice causes consistent, framework-structural performance degradation—independent of language—is a concrete empirical result for anyone designing or comparing harness scaffolds. The multi-stage filtering pipeline (TrajectoryScanner, execution aggregation, schema normalization across heterogeneous harness logs) is itself a **meta-harness** layer that unifies outputs from multiple scaffolds into a common format for downstream training.

## Tags
#swe-agent #trajectory-dataset #distillation #harness-evaluation #multilingual #benchmark #agent-scaffolding #data-pipeline
