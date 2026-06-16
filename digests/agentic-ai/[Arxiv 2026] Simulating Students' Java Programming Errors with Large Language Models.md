---
title: "Simulating Students' Java Programming Errors with Large Language Models"
authors: ["Ali Keramati", "Jie Cao", "Iman Mohammadi", "Mark Warschauer", "Yang Shi"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T04:51:49+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14113"
url: "http://arxiv.org/abs/2606.14113v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Simulating Students' Java Programming Errors with Large Language Models.pdf"
---

# Simulating Students' Java Programming Errors with Large Language Models

*🕒 **Published (v1):** 2026-06-12 04:51 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14113v1)*

## TL;DR
This paper evaluates whether LLMs can generate realistic student-like logical errors in Java code, assessing five models under three prompting strategies (IO, CoT, Self-Refine) across 74,000+ authentic submissions from the CodeWorkout dataset. Results show that LLMs produce functionally indistinguishable errors (83.7% deception rate in expert annotation) but face an inherent diversity–fidelity trade-off. Claude Sonnet 4 achieves the best balance between error diversity and alignment to authentic student mistakes.

## Problem
Obtaining representative sets of student programming errors for newly designed tasks requires extensive classroom deployment — authentic submissions accumulate slowly and are costly to collect. Existing LLM prompting tends to produce correct or near-correct code, while random corruption generates artificial bugs lacking pedagogical validity. No prior work systematically compared multiple LLMs on both the diversity and alignment dimensions of logical (not syntactic) error simulation across varying task difficulty.

## Method
The authors use the CodeWorkout dataset (37 introductory Java problems, 74,080 unique compilable-but-incorrect student submissions from 410 undergraduates). Five LLMs (Claude Sonnet 4, GPT-4o, GPT-5, Gemini 2.5 Pro, Grok Code Fast 1) generate multiple erroneous submissions per problem under three prompting strategies:
- **IO**: single-step direct instruction to produce one logical error
- **CoT**: model first writes a 1–3 sentence rationale for the intended slip, then produces buggy code
- **Self-Refine**: iterative loop (up to 4 rounds) where a critic instance evaluates against a rubric and a refiner rewrites flagged outputs

**Diversity** is measured via mean pairwise AST edit distance (Zhang–Shasha algorithm) among generated samples. **Alignment** is measured as mean nearest-neighbor AST edit distance from each generated error to its closest authentic student submission, using Jaccard-based Recall@100 retrieval as a pre-filter. A blinded expert annotation study (N=401; 205 authentic, 196 synthetic) assessed source attribution (Turing test), plausibility on a 5-point Likert scale, and error taxonomy (8 categories: Condition Logic, Boundary, Concept, Method, Infinite Loop, Scope, Type, Other).

## Key Contributions
- Systematic multi-model, multi-strategy evaluation of LLM student error simulation on a large authentic dataset (74K+ submissions)
- Two-dimensional evaluation framework: diversity (AST edit distance within generated set) vs. alignment (nearest-neighbor distance to authentic submissions)
- Demonstration that task struggling level (operationalized as total submission count) moderates both dimensions: harder problems increase diversity but reduce alignment
- Blinded expert annotation confirming LLM-generated errors are largely indistinguishable from authentic ones (83.7% deception rate), yet are "idealized" — concentrated in clean single-fault categories

## Results
**Diversity (RQ1):**
- All models produce non-trivial diversity; Gemini 2.5 Pro (CoT: 72.55 mean edit distance) and Claude Sonnet 4 (IO: 63.33) show highest diversity; GPT-4o is lowest (25–40)
- CoT generally increases diversity; Self-Refine reduces diversity for Claude Sonnet 4 but not for other models

**Alignment (RQ2, structural):**
- Claude Sonnet 4 + Self-Refine achieves mean nearest edit distance of 16.35 (best balanced); Grok Code Fast 1 + Self-Refine achieves 16.22 (absolute minimum) but is inconsistent across prompts (IO: 39.66)
- GPT-5 and Gemini 2.5 Pro diverge substantially (distances often >80)
- GPT-4o is intermediate (CoT: 20.41; Self-Refine: 49.85)

**Alignment (RQ2, human evaluation, N=401):**
- 83.7% deception rate (164/196 synthetic items misclassified as human)
- LLM errors rated higher plausibility (M=4.27) than authentic errors (M=3.78), p<0.001 (Mann-Whitney U)
- LLM errors concentrate on Condition Logic (46.4%) and Boundary (21.9%); authentic errors have 28.3% in the diffuse "Other" category

**Struggling level (RQ3):**
- Higher struggling → greater generated diversity (Gemini 2.5 Pro CoT: low=62.34, medium=82.89, high=74.59)
- Higher struggling → worse alignment across all models; Claude Sonnet 4 most stable but still degrades

## Limitations
- Dataset limited to 37 introductory Java problems from a single institution and two semesters; generalizability to other languages, curricula, or institutional contexts is unknown
- Struggling level operationalized as total submission count, which may conflate difficulty with course policy, assignment placement, or popularity
- Generation constraints (compilable, exactly one logical error) produce an "idealized novice" distribution, underrepresenting multi-fault and structurally messy authentic submissions
- AST edit distance lacks direct interpretability across problems and misses semantic equivalence (structurally distinct code may be functionally identical)
- No execution-based or semantic evaluation (e.g., test-case traces) to complement structural metrics
- Expert annotation was single-coded in the main phase; no formal inter-rater reliability statistic on the full set

## Relevance to Agentic AI / LLM Agents
This paper directly addresses LLM-as-student-agent simulation — a specific instance of the broader challenge of using LLMs to proxy human behavior within intelligent tutoring systems and teachable agent environments. The diversity–fidelity trade-off identified here is a domain-specific instantiation of the general tension in agent simulation between behavioral coverage and distributional fidelity. The Self-Refine prompting strategy, acting as an iterative critic–refiner loop, is an agentic pattern (multi-turn self-correction with structured feedback) evaluated here in an educational domain, providing evidence of where iterative refinement improves alignment vs. where it diverges. These findings also inform how synthetic data pipelines for agent training should be calibrated when the target is human-like error distributions rather than correctness.

## Tags
#llm-agent #student-simulation #synthetic-data #code-generation #educational-ai #prompting-strategies #human-evaluation #iterative-refinement
