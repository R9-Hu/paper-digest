---
title: "Crafter: A Multi-Agent Harness for Editable Scientific Figure Generation from Diverse Inputs"
authors: ["Haozhe Zhao", "Shuzheng Si", "Zhenhailong Wang", "Zheng Wang", "Liang Chen", "Xiaotong Li", "Zhixiang Liang", "Maosong Sun", "Minjia Zhang"]
source: "HuggingFace"
venue: ""
published: "2026-05-28"
published_time: "2026-05-28T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2605.30611"
url: "https://huggingface.co/papers/2605.30611"
pdf: "paper/harness/[HuggingFace 2026] Crafter A Multi-Agent Harness for Editable Scientific Figure Generation from Diverse Inputs.pdf"
---

# Crafter: A Multi-Agent Harness for Editable Scientific Figure Generation from Diverse Inputs

*🕒 **Published (v1):** 2026-05-28 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2605.30611)*

## TL;DR
CRAFTER is a multi-agent harness that wraps an arbitrary image-generation backend with a shared evolving structured specification, enabling reliable cross-type scientific figure generation without architectural changes to the underlying generator. A companion system, CRAFTEDITOR, applies the same harness pattern to convert raster outputs into editable SVGs. Both are evaluated on the newly introduced CRAFTBENCH, a 279-sample benchmark spanning three figure types and four input conditions.

## Problem
Existing scientific figure generators are narrow: they target a single figure type (typically text-to-methodology-diagram), accept only text input, and produce static rasters that cannot be locally revised. High inter-sample output variance on structured layouts and prompt degradation from accumulated free-text corrections make iterative repair with existing systems unreliable.

## Method
CRAFTER formalizes a four-role harness loop—Designer (D), Executor (E), Verifier (V), Reviser (R)—over a shared, evolving structured specification S. At each round t: D proposes a plan pₜ from Sₜ₋₁; E renders an artifact aₜ; V emits a *directive* diagnostic dₜ (per-dimension scores, identified defects, suggested corrections—not a scalar); R writes *typed edits* (structured operations: add layout constraint, ban artifact category, resize named element) back into S, keeping it internally consistent rather than appending free text. Three mechanisms address specific failure modes:

1. **Diversity-driven plan exploration**: D proposes K candidate plans in parallel; the convergence judge picks the best before refinement begins, escaping structurally unsuitable framings early.
2. **Structured corrective layer**: typed edits replace free-text revision instructions, preventing the contradictory-directive accumulation that erodes faithfulness silently.
3. **Verify-then-refine with a directive critic**: up to T=3 refinement rounds with best-so-far reversion; an early-exit gate bypasses the loop when the first output already meets acceptance thresholds.

CRAFTEDITOR reuses the same four-role harness for raster-to-SVG conversion via three phases: (1) instruction-driven canvas cleaning (a VLM designer authors a keep/delete plan; an image editor executes it; a verifier loops up to T=3); (2) element captioning, grounding, and classification; (3) iterative SVG composition with a hybrid critic (VLM for global layout fidelity + programmatic checkers for text overflow, arrow endpoints, element overlap).

CRAFTBENCH is a 279-sample benchmark drawn from arXiv preprints (18 subject areas), award-tier conference posters, and research blogs, with four tasks (text-to-image, mask-completion, key-element composition, sketch-conditioned) across three figure styles, curated through multi-stage filtering and unanimous graduate-level annotation for reference-conditioned samples.

## Key Contributions
- A formal harness abstraction (D/E/V/R loop over a shared evolving specification) instantiated in CRAFTER (figure generation) and CRAFTEDITOR (raster-to-SVG), forming the first end-to-end generation-to-editing pipeline for scientific figures.
- Three targeted mechanisms: diversity-driven plan exploration, structured corrective layer (typed edits vs. free-text), and verify-then-refine with directive critic—each independently validated by ablation.
- CRAFTBENCH: first benchmark covering three figure types × four input conditions (279 samples) with human annotation, paired with a per-image VLM-as-judge evaluation protocol that removes pairwise position bias.

## Results
- **PaperBanana-Bench**: CRAFTER (w/ Nano Banana 2) scores 50.34% overall vs. 33.73% for PaperBanana (same backbone, +16.61 pt) and 15.07% for standalone Nano Banana 2 (+35.27 pt).
- **CRAFTBENCH**: CRAFTER (w/ Nano Banana 2) scores 50.20% overall vs. 28.00% for PaperBanana (same backbone, +22.20 pt); CRAFTER is the only method to improve over its backbone uniformly across every dimension and every task on both benchmarks.
- Backbone substitution (Nano Banana 2 → Pro) shifts CRAFTER's score by only 0.34 pt on PaperBanana-Bench and 2.10 pt on CRAFTBENCH, confirming harness-vs-executor independence.
- **Ablations on PaperBanana-Bench**: removing plan exploration −8.56 pt; removing corrective layer −8.90 pt; removing refinement loop −5.48 pt; removing directive critic −5.04 pt.
- **CRAFTEDITOR** (80-sample held-out set, 3-VLM ensemble): overall 8.04 vs. AutoFigure-Edit 6.91 and Edit-Banana 3.69; removing iterative composition −2.15 pt; removing agentic cleaning −0.33 pt.

## Limitations
- CRAFTER is not uniformly successful; failure cases analyzed in Appendix K–L but not detailed in the main text.
- CRAFTBENCH covers only three figure types; broader coverage (e.g., charts, plots, equations) is not addressed.
- Evaluation relies on VLM-as-judge (Gemini 3.5 Flash), which may have its own biases despite the human-study validation.
- GPT-Image-2 returned valid outputs for only 260/279 CRAFTBENCH inputs due to instability and content-safety refusals, limiting baseline comparability.
- Computational cost scales with K (candidate plans) and T (refinement rounds); cost analysis is deferred to Appendix D.

## Relevance to Harnesses / Meta-Harnesses
CRAFTER is a direct, worked instantiation of the harness pattern—explicitly citing Young (2025) and Pan et al. (2026) on agent harnesses—and provides one of the clearest formal accounts of the D/E/V/R loop structure with a shared evolving specification as memory. The paper's central empirical claim is that the harness layer, not backbone strength, is the primary driver of quality and generalization, quantified by showing that backbone swaps shift scores by <3 points while harness ablations shift scores by 5–9 points. For researchers tracking harness and meta-harness design, the structured corrective layer (typed edits vs. free-text accumulation) and the pluggable executor architecture are the most transferable design principles, directly addressing a known failure mode (prompt contradiction accumulation) in any iterative agentic loop.

## Tags
#harness #multi-agent #scientific-figures #structured-specification #iterative-refinement #benchmark #svg-generation #agentic-pipeline
