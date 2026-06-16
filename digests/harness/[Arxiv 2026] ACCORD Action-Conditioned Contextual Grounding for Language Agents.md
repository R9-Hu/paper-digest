---
title: "ACCORD: Action-Conditioned Contextual Grounding for Language Agents"
authors: ["Lai Jiang", "Cheng Qian", "Zhenhailong Wang", "Pan Lu", "Heng Ji", "Hao Peng"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T09:05:55+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16432"
url: "http://arxiv.org/abs/2606.16432v1"
pdf: "paper/harness/[Arxiv 2026] ACCORD Action-Conditioned Contextual Grounding for Language Agents.pdf"
---

# ACCORD: Action-Conditioned Contextual Grounding for Language Agents

*🕒 **Published (v1):** 2026-06-15 09:05 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16432v1)*

## TL;DR

ACCORD is a training-free, model-agnostic agent framework that intercepts LLM agent write actions and augments the agent's context with grounded environmental evidence before execution. It addresses two empirically characterized failure modes—acting on information never acquired ("incomplete") and ignoring information already in context ("overlooked")—yielding up to +20.6 TGC improvement on AppWorld over ReAct baselines.

## Problem

LLM agents operating in information-rich environments receive underspecified user instructions whose disambiguation requires environmental context. Current agents fail in two measurable ways: (1) issuing write actions against information never gathered from the environment (incomplete grounding, 26.7–36.7% of failures), and (2) issuing writes that contradict observations already present in the trajectory (overlooked grounding, 33.3–66.7% of failures). Post-hoc self-reflection methods (Self-Refine, Reflexion-style) worsen performance because they ground corrections in the model's own internal beliefs rather than objective environmental signals.

## Method

ACCORD operates at two complementary layers, both training-free:

**Inference-time grounding layer (core):** Before every write action `w ∈ W`, a separate grounding agent intercepts the proposed action, receives `(w, ct, x)`, and constructs an action-ready context `c't` via two moves: (A) re-surfacing decisive evidence already in the trajectory but unattended (addressing overlooked mode); (B) issuing read-only probes to the live environment for facts not yet in context (addressing incomplete mode). The grounding agent then emits APPROVE or REJECT; on REJECT, conflicting environmental evidence is appended to the main agent's history and the main agent re-proposes. Crucially, only objective environmental signals—not the grounding agent's own reasoning—are fed back, preventing opinionated self-correction. The write set `W` is constructed once per environment automatically (via API metadata or a single LLM classification pass).

**Policy-level shaping layer (supporting):** A prompt suffix on the main agent's system prompt instructs it to inspect concrete environmental content before acting and to survey the environment early in the trajectory, biasing it toward observation calls. This enriches the trajectory so the grounding agent has more to re-surface.

## Key Contributions

- Formal taxonomy of agent grounding failures into "incomplete" (information never acquired) and "overlooked" (information present but ignored) modes, with empirical quantification on AppWorld and AlfWorld.
- A two-layer, inference-time-only framework (no training, no task-success signal) that closes both grounding gaps via action-conditioned context augmentation.
- Demonstration that grounding must be conditioned on the specific upcoming write action, not on generic upfront context expansion (PE alone slightly hurts performance).
- Empirical falsification of post-hoc self-correction as a grounding strategy: both Self-Refine and FullCodeReflex degrade below the ReAct baseline.

## Results

- **AppWorld, GPT-5-mini:** +14.3 TGC / +16.1 SGC on test-normal; +20.6 TGC / +18.0 SGC on test-challenge (vs. ReAct baseline of 63.7 / 42.0 TGC).
- **AppWorld, Claude-4.5-sonnet:** +4.2 TGC on test-normal; +10.8 TGC / +10.8 SGC on test-challenge.
- **AppWorld, Qwen3.5-27B-FP8:** +10.1 TGC / +16.1 SGC on test-normal; +6.7 TGC / +6.4 SGC on test-challenge.
- **AlfWorld, GPT-5-mini:** 70.6% → 78.0% success rate (+7.4); Qwen3.5-27B-FP8: 80.7% → 88.1% (+7.4, 96/109 tasks solved).
- API read share increased from 70.4% → 82.7% (test-normal) and 88.2% → 95.3% (test-challenge) under ACCORD, with no increase in write budget—gains come from better-grounded individual writes.
- Self-Refine: −3.6 TGC on test-normal; FullCodeReflex: −20.2 TGC on test-normal (both baselines regress).

## Limitations

- Requires categorizing environment APIs into write vs. read-only; applicable only where this distinction is well-defined or inferrable.
- The grounding agent adds extra read-only calls and additional model rollouts per write action, raising per-task token cost even though the write budget is bounded.
- Policy layer is prompt-based; the authors acknowledge it should ideally be internalized via distillation or RL rather than an external grounding agent.
- Ablation and failure analysis use only 30 sampled trajectories per benchmark, limiting statistical confidence in the failure-mode taxonomy.

## Relevance to Harnesses / Meta-Harnesses

ACCORD is directly relevant as an **inference-time meta-layer** sitting atop an arbitrary base agent—a grounding agent that intercepts, augments, and gates the main agent's write actions without modifying the agent itself. This is architecturally isomorphic to a harness: a controller that wraps agent execution, enforces a verification step before state-mutating operations, and injects enriched context at the point of action. The write-interception pattern (detect action class → pause → probe → approve/reject) is a concrete, evaluated implementation of the kind of pre-action validation and context injection that meta-harnesses for multi-agent pipelines need. The result that generic upfront context expansion fails while action-conditioned augmentation succeeds is a strong design signal for harness builders: grounding/validation hooks must be conditioned on the specific downstream action, not injected once at task start.

## Tags

#llm-agents #contextual-grounding #inference-time-adaptation #action-verification #meta-harness #tool-use #appworld #agent-framework
