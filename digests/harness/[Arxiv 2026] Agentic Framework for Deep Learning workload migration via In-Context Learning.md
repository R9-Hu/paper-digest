---
title: "Agentic Framework for Deep Learning workload migration via In-Context Learning"
authors: ["Qiyue Liang", "Steven Ingram", "George Vanica", "Andi Gavrilescu", "Newfel Harrat", "Hassan Sipra", "Sethuraman Sankaran"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T19:41:57+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.15994"
url: "http://arxiv.org/abs/2606.15994v1"
pdf: "paper/harness/[Arxiv 2026] Agentic Framework for Deep Learning workload migration via In-Context Learning.pdf"
---

# Agentic Framework for Deep Learning workload migration via In-Context Learning

*🕒 **Published (v1):** 2026-06-14 19:41 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15994v1)*

## TL;DR
This paper presents a fully autonomous agentic pipeline for migrating PyTorch deep learning code to JAX, combining In-Context Learning (ICL) structural anchors with a dynamic execution oracle for oracle-conditioned self-debugging. The system achieves 91% numerical equivalence on neural modules (Level 2) versus 9% for a baseline LLM and 27% for self-debugging without oracle grounding. It has been validated on 10 real-world repositories including SAM, T5, and StyleGAN2.

## Problem
Manual PyTorch→JAX migration is error-prone due to fundamental framework differences (eager vs. JIT, mutable vs. stateless/functional, NCHW vs. NHWC layout, fp32 vs. bfloat16, PRNG routing). Vanilla LLMs hallucinate syntactically plausible but numerically incorrect translations, and self-debugging loops without a mathematical ground truth enable reward hacking (passing trivial tests while leaving numerical equivalence broken).

## Method
Four-phase autonomous pipeline:
1. **ICL Anchoring (Phase 1):** A tightly curated context containing source PyTorch module, idiomatic JAX translation, and test cases is provided to the LLM. RAG over the full MaxText repo was rejected because retrieved fragments introduced distributed-computing noise ("Lost in the Middle" degradation).
2. **Dynamic Execution Oracle (Phase 2):** A profiling script runs the source PyTorch module with random inputs, extracts weights (`state_dict`), input tensors, and output activations, and serializes them into an immutable `.pkl` artifact ("the Oracle"). This captures runtime behaviors (silent padding, shape changes) invisible to static analysis.
3. **Oracle-Conditioned Test Generation (Phase 3):** The agent generates JAX code (flax.linen) and custom "Silver" test harnesses that deserialize the Oracle `.pkl`, map weights into the JAX model, and assert numerical equivalence with `numpy.allclose` at ε = 1×10⁻⁷. Three-stage evaluation: compilation → shape correctness → numerical equivalence.
4. **Iterative Self-Debugging (Phase 4):** When a test fails, full execution feedback (stderr, stack traces, numerical diffs) is fed back to the LLM context alongside ICL templates for iterative repair. Final metrics are measured against a held-out human-crafted test suite (disjoint from ICL examples) to prevent reward hacking contamination.

## Key Contributions
- **Structural anchoring via ICL:** Demonstrates that a small, dense set of reference translations is sufficient to anchor generation and suppress hallucination, outperforming broad RAG retrieval.
- **Dynamic Execution Oracle:** An immutable, serialized runtime artifact that grounds test generation in real computation rather than LLM arithmetic, bypassing the known limitation of transformers on high-dimensional tensor operations.
- **Oracle-conditioned self-debugging loop:** Closes the feedback loop with objective mathematical truth, preventing the reward-hacking failure mode observed when self-debugging operates without an oracle.
- **Ablation guidance:** Systematic ablation isolating instruction prompting, ICL, and oracle-conditioned debugging, offering actionable design principles for agentic code-translation harnesses.
- **Level 3 repository-scale validation:** Human expert evaluation on 10 full GitHub repositories, reporting completeness, numerical equivalence, and readability (Likert 1–5).

## Results
- **Level 1 (9 mathematical ops):** Full pipeline achieves 100% completeness, 100% shape, 100% numerical equivalence vs. baseline 9% / instruction-only 44% / instruction+self-debug 89%.
- **Level 2 (11 neural modules):** Full pipeline achieves 91% completeness, 91% shape, 91% numerical equivalence vs. baseline 9% / instruction-only 18% / instruction+self-debug 27%.
- **Level 3 (10 full repos, human eval):** 100% completeness on 9/10 repos (SAM2: 86%); numerical equivalence 100% on 4 repos; fell below 85% on two large Facebook Research repos (SAM2: 80%, DETR: 57%); average readability 4.21/5 across repos.
- Self-debugging without oracle stalls at 27% numerical equivalence on Level 2 despite reaching 73% compilation, confirming reward-hacking without mathematical grounding.

## Limitations
- Repository-level (Level 3) migration is not fully automatic; human experts were permitted 1–2 minor edits to guide the agent.
- ICL sensitivity is unexplored: no systematic ablation over which or how many reference examples are selected.
- Large, foundational models (DETR: 57%, SAM2: 80% numerical equivalence) reveal that structural dependency management at full-repository scale remains unsolved.
- Evaluation tolerance (ε = 1×10⁻⁷) is calibrated for fp32; behavior under mixed-precision or bfloat16-dominant JAX configurations is not systematically studied.

## Relevance to Harnesses / Meta-Harnesses
This paper is a direct instantiation of an agentic harness pattern: a multi-phase orchestration loop where tool use (profiling scripts, test execution, traceback capture) provides grounded feedback to an LLM, replacing pure model reasoning with execution-backed verification. The "Oracle + Silver test harness" architecture is a concrete example of how meta-harnesses can separate internal debugging scaffolding from final evaluation to prevent reward hacking — a design principle applicable to any harness that lets an agent self-generate its own tests. The ablation study provides rare empirical data on the marginal value of each harness component (prompt instructions, ICL, oracle grounding, iterative debugging), which is directly informative for harness design trade-offs.

## Tags
#agentic-framework #code-migration #in-context-learning #self-debugging #execution-oracle #pytorch-to-jax #test-harness #llm-code-generation
