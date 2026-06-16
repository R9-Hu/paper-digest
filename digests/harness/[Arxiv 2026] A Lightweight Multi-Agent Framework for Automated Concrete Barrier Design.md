---
title: "A Lightweight Multi-Agent Framework for Automated Concrete Barrier Design"
authors: ["Wanting Wang", "Xiye Ma", "Yuyang He", "Minghui Cheng", "Ran Cao"]
source: "Arxiv"
venue: ""
published: "2026-06-10"
published_time: "2026-06-10T13:06:11+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12040"
url: "http://arxiv.org/abs/2606.12040v2"
pdf: "paper/harness/[Arxiv 2026] A Lightweight Multi-Agent Framework for Automated Concrete Barrier Design.pdf"
---

# A Lightweight Multi-Agent Framework for Automated Concrete Barrier Design

*🕒 **Published (v1):** 2026-06-10 13:06 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.12040v2)*

## TL;DR
This paper proposes a closed-loop multi-agent framework (MAF) built on AutoGen for automating reinforced concrete highway barrier design per AASHTO-LRFD specifications. The framework orchestrates Designer, Validator, and Optimizer agents in a generation-evaluation-optimization loop, achieving >98% design precision versus ≤11.7% for standalone LLMs. A key finding is that an 8B-parameter model inside the MAF outperforms an unconstrained 671B-parameter model.

## Problem
Manual barrier design requires iterative yield-line analysis to satisfy AASHTO-LRFD Section 13 constraints — a trial-and-error process prone to error. Standalone LLMs applied directly to this task exhibit severe hallucination and lack physical grounding, producing resistance values ranging from critically unsafe (~200 kN) to grossly over-designed (>4000 kN) against a target of 336–384 kN for TL-4.

## Method
The framework is implemented in AutoGen as five coupled modules:
1. **Designer Agent** — interprets natural language specs (test level, geometric bounds) and emits a structured JSON parameter set (height H, widths B_top/B_bottom, material properties fc/fy, bar diameter dz/dk, spacing s, count n).
2. **Message Parser & Validator** — regex-based extraction and sanitization of the JSON; enforces hard feasibility bounds and imputes missing fields.
3. **Mechanics Calculator** — deterministic external tool computing ultimate transverse resistance R_w via AASHTO yield-line equations (Eq. 1–2); classifies output as UNSAFE (R_w < F_t), WASTEFUL (R_w > 1.6·F_t), or OPTIMAL (1.4·F_t ≤ R_w ≤ 1.6·F_t).
4. **Optimizer Agent** — receives structured error context (deviation from target band) and applies mechanics-informed adjustments (increase reinforcement/dimensions for UNSAFE; reduce for WASTEFUL); re-enters the validator in a closed loop until convergence or iteration cap.
5. **Drafting Module** — generates parametric AutoLISP scripts for direct CAD execution.

## Key Contributions
- Closed-loop "generation-evaluation-optimization" agentic architecture grounding LLM outputs in deterministic AASHTO-LRFD mechanics.
- Demonstration that structured multi-agent orchestration decouples task precision from model scale: MAF-DS-8B (98.3%) outperforms standalone DS-671B (8.3%).
- Quantitative metric for "dimensional hallucination" via interval-based MSE (Eq. 4–5).
- Automated CAD drawing generation (AutoLISP) as end-to-end engineering output.
- Blueprint for integrating physical guardrails into safety-critical, code-compliant AI design workflows.

## Results
- **MAF-DS-8B**: 98.3% average precision across TL-3/TL-4/TL-5 (100%/100%/98.3%); average MSE ≈ 0 (×10⁴).
- **MAF-DS-32B**: 88.3% average precision (80%/90%/95%); average MSE = 0.15 (×10⁴).
- **Standalone DS-8B**: 6.7% average precision; average MSE = 331.97 (×10⁴).
- **Standalone DS-32B**: 11.7% average precision; average MSE = 21.85 (×10⁴).
- **Standalone DS-671B**: 8.3% average precision; average MSE = 4.86 (×10⁴).
- MAF-DS-8B achieves near-zero MSE versus DS-671B standalone MSE of 4.86×10⁴, confirming the framework dominates scale.

## Limitations
- Evaluation restricted to single-slope barrier geometry; other profiles (New Jersey, F-shape) not tested.
- Only DeepSeek model family evaluated; generalizability to other LLM families (GPT, Llama, etc.) not established.
- Optimization relies on heuristic rule-based adjustments within the Optimizer Agent rather than gradient-based or formal constraint satisfaction.
- No finite element validation of generated designs; physical correctness is verified only against the analytical yield-line formula, not simulation.
- Maximum iteration cap behavior (best-available fallback) not characterized quantitatively.
- Framework tested only on one national code (AASHTO-LRFD); portability to Eurocode or other standards undemonstrated.

## Relevance to Harnesses / Meta-Harnesses
This paper is a concrete domain-specific instantiation of the generation-evaluation-optimization harness pattern: a Designer agent generates candidates, a deterministic validator enforces schema and physical constraints, and an Optimizer agent closes the loop — structurally identical to code-generation harnesses that wrap LLM output in a test executor and retry loop. The key transferable insight is that injecting a *deterministic physics oracle* as the evaluation layer can substitute for model scale, reducing backbone requirements by ~80× (671B→8B) without accuracy loss — a cost-reduction principle directly applicable to any harness that can formalize its evaluation criterion. The work also demonstrates regex-based structured-output sanitization as a practical reliability layer between LLM generation and downstream tools, a pattern common to robust agent harnesses.

## Tags
#multi-agent #autogen #domain-specific-harness #generation-evaluation-optimization #structural-engineering #hallucination-mitigation #model-efficiency #closed-loop
