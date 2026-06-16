---
title: "VeriGeo: Controllable Geometry Question Generation with Numerical and Analytical Verification"
authors: ["Xiaoxian Duan", "Zequn Liu", "Yingce Xia"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T06:59:44+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14176"
url: "http://arxiv.org/abs/2606.14176v1"
pdf: "paper/agentic-ai/[Arxiv 2026] VeriGeo Controllable Geometry Question Generation with Numerical and Analytical Verification.pdf"
---

# VeriGeo: Controllable Geometry Question Generation with Numerical and Analytical Verification

*🕒 **Published (v1):** 2026-06-12 06:59 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14176v1)*

## TL;DR
VeriGeo is a controllable geometry question generation framework that uses an Author agent and a Solver agent, both grounded in executable action sequences, to synthesize multimodal geometry problems with mutual consistency guaranteed by a three-stage verification pipeline. Raw LLM generations fail verification at high rates (average direct-pass rate 29.02%), but verification-guided reflection repairs a substantial fraction. Fine-tuning Qwen2.5-VL-7B on only 8.7k verified examples achieves state-of-the-art GeoQA accuracy among end-to-end MLLM-based solvers.

## Problem
Synthesizing high-quality geometry problems is hard because the problem statement, diagram, symbolic constraints, and solution must be mutually consistent. Existing approaches trade off controllability against verifiability: diagram-first methods improve validity but cannot easily satisfy arbitrary user constraints, while seed-based LLM rewriting is flexible but silently introduces cross-modal inconsistencies that are difficult to detect or repair.

## Method
VeriGeo frames geometry generation as a closed-loop agentic pipeline with two LLM agents sharing a unified executable action representation:

- **Author Agent** receives user constraints (difficulty, target concepts), generates a blueprint from a curated concept library (426 Euclidean/vector/function concepts across 3 difficulty levels), synthesizes a natural-language problem statement, then emits an executable action sequence `{op, type, args}` that constructs the diagram step-by-step.
- **Solver Agent** independently generates a proof-aligned solution and its own action sequence over the same representation.

Both agents pass through a **three-stage verification pipeline**:
1. **Numerical verification**: executes the action sequence, checking geometric constraints (collinearity, perpendicularity, etc.) within floating-point tolerance using exact rational/radical representations.
2. **Analytical verification**: compiles geometric constraints into an algebraic system and solves it with SymPy, using gauge-fixing and rank-aware filtering to handle over/under-determined systems; a successful solve certifies geometric realizability.
3. **Logical verification**: LLM-as-a-judge checks global consistency among problem text, diagram, action sequence, and solution for contradictions and unsupported inferences.

Failures at any stage trigger a **self-reflection** step: the error signal (failing step + reason) is fed back to the LLM to diagnose and repair the generation. At most one reflection round is allowed per attempt.

## Key Contributions
- Unified executable action representation connecting natural language, diagram construction, geometric constraints, and proof steps into a single verifiable artifact.
- Three-stage (numerical → analytical → logical) verification pipeline with complementary failure-detection coverage and automated repair via reflection.
- Controllable generation over user-specified difficulty levels and geometry concepts, including seed-conditioned variant generation.
- 8.7k verified synthetic examples that yield best-reported GeoQA accuracy among end-to-end MLLM solvers when used for SFT, despite being far smaller than competing datasets (vs. 65K–8.6M examples in prior work).

## Results
- **Direct-pass rate** across five LLM backbones averages 29.02%; Gemini 3.1 Pro is highest at 54.22%, GPT-5.4-mini lowest at 2.44%.
- **Repair rate** averages 25.78%; Gemini 3.1 Pro repairs 36.00%, Qwen3.5-Plus 30.67%, Claude Opus 4.6 20.22%.
- **Failure detection by module** (Claude Opus 4.6 example): numerical 55.30%, analytical 23.25%, logical 8.36% — modules are complementary.
- **Diversity**: VeriGeo covers 354 distinct geometry concepts in 100 samples vs. 116–201 for all prior datasets (manually curated, diagram-first, seed-based).
- **Difficulty controllability**: target-difficulty matching rate 93–98% for easy/medium, 78–87% for hard.
- **Downstream SFT** (Qwen2.5-VL-7B-Instruct on 8.7k examples):
  - GeoQA: **82.74%** (best among end-to-end MLLM solvers; prior best TR-CoT: 79.20%)
  - PGPS9K: **59.40%** (prior best among SFT-only generation methods: GeoGen-SFT-7B 54.30%)
  - MathVista-GPS: **75.96%** (prior best among comparable methods: GeoGen-SFT-7B 74.00%)

## Limitations
- Maximum of one reflection round per attempt; unrecoverable failures (up to 88% for GPT-5.4-mini) are simply rejected, wasting generation budget.
- Logical verification relies on an LLM-as-a-judge, which is itself imperfect and may miss subtle higher-level inconsistencies.
- Reinforcement learning and process-level optimization are explicitly left for future work; current training is SFT-only.
- Hard problems show lower difficulty-matching rates (78–87%), suggesting difficulty boundaries are ambiguous or harder to control precisely.
- Evaluation covers Euclidean, vector, and function-augmented geometry; generalization to other mathematical domains is untested.
- Analytical verification with SymPy may struggle on highly nonlinear or large constraint systems not addressed in the paper.

## Relevance to Agentic AI / LLM Agents
VeriGeo is a concrete example of a **multi-agent closed-loop system** where Author and Solver agents operate over a shared executable representation, with structured external verification replacing unchecked LLM self-assessment — directly relevant to the broader agenda of grounding agentic reasoning in verifiable, executable artifacts. The verification-guided reflection loop (error signal → diagnosis → repair) instantiates a principled self-correction mechanism that goes beyond naive retry, showing measurable yield improvement across diverse LLM backbones. The finding that raw LLM generation fails verification ~71% of the time on average, and that repair contributes more verified data than direct pass for many backbones, quantifies the necessity of external verification in agentic synthesis pipelines. This work thus provides empirical grounding for the design principle that agentic systems generating structured outputs (code, proofs, diagrams) should couple generation with complementary verification stages rather than rely on LLM confidence alone.

## Tags
#multi-agent #verification #synthetic-data #mathematical-reasoning #multimodal #geometry #self-reflection #executable-reasoning
