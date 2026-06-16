---
title: "SkillAdaptor: Self-Adapting Skills for LLM Agents from Trajectories"
authors: ["Zhuoyun Yu", "Xin Xie", "Wuguannan Yao", "Chenxi Wang", "Lei Liang", "Xiang Qi", "Shumin Deng"]
source: "HuggingFace"
venue: ""
published: "2026-05-31"
published_time: "2026-05-31T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.01311"
url: "https://huggingface.co/papers/2606.01311"
pdf: "paper/harness/[HuggingFace 2026] SkillAdaptor Self-Adapting Skills for LLM Agents from Trajectories.pdf"
---

# SkillAdaptor: Self-Adapting Skills for LLM Agents from Trajectories

*🕒 **Published (v1):** 2026-05-31 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.01311)*

## TL;DR
SkillAdaptor is a training-free framework that improves LLM agent skill libraries via step-level fault attribution rather than coarse trajectory-level reflection. Given a failed execution trace, it localizes the earliest accountable fault step, links blame to specific retrieved skills, and applies targeted revisions under an explicit qualification gate. It plugs into OpenClaw-class agent harnesses without modifying the backbone model.

## Problem
Existing training-free skill adaptation methods update skills from full-trajectory outcomes or session-level summaries, which diffuses failure signals across unrelated steps and produces overly broad or misdirected revisions. In long-horizon tasks a single early error invalidates many downstream actions, making outcome-level credit assignment unreliable and skill updates unstable.

## Method
SkillAdaptor maintains a frozen skill collection K of structured SKILL.md records (title, principle, applicability conditions). At runtime, skills are retrieved via Qwen3-Embedding-8B cosine similarity (top-10, threshold 0.45) then reranked by the backbone LLM. After a failed trajectory, adaptation proceeds in three stages:

1. **Attribution**: A *Localizer* identifies the earliest accountable fault step t* and failure type (skill_wrong vs. skill_missing); a *Linker* assigns weighted responsibility scores to the retrieved candidate skills and routes to REVISE or GENERATE.
2. **Modification**: The *Reviser* surgically rewrites the highest-weight skill in-place; the *Generator* synthesizes a new skill anchored at t*. Duplicate suppression uses cosine similarity with threshold θdup = 0.95.
3. **Qualification**: Candidate and original skill collections are re-executed on the task set; the update is committed only if ∆ ≥ 0 in execution metric, otherwise discarded.

Iteration runs for up to 10 rounds with early stopping after 3 rounds of no accepted changes. Skill initialization bootstraps K₀ from successful trajectories before any retrieval-augmented execution.

## Key Contributions
- Step-level fault attribution pipeline (Localizer + Linker) that identifies the earliest causally responsible step and responsible skill(s), replacing trajectory-level aggregation.
- Explicit qualification gate that accepts skill updates only when re-execution confirms non-negative performance delta, suppressing harmful updates.
- Modular plug-in design compatible with OpenClaw-class harnesses, with no backbone fine-tuning.
- Ablation evidence isolating the contributions of attribution (Localizer+Linker) and qualification independently, showing both are necessary for stable adaptation.

## Results
**WebShop** (vs. strongest skill baseline EvoSkill, Kimi-K2.5):
- Score: 41.6 vs. 40.4 (+1.2); Succ%: 33.0 vs. 31.3 (+1.7 pp)
- Largest cross-model gain: +2.3 Score on GLM-5

**PinchBench** (vs. OpenSpace):
- Avg Score%: 67.2 vs. 66.0 (Kimi-K2.5); largest gain +1.5 pp on GLM-5

**Claw-Eval** (vs. OpenSpace):
- Avg Score: 75.8 vs. 74.0 (Kimi-K2.5), +1.8 largest gain; Pass@3%: 77.4 vs. 75.9

**Ablation** (Kimi-K2.5, WebShop): removing Localizer+Linker drops Succ% from 33.0 to 28.6; removing Qualifier drops Succ% to 26.3 with variance rising (±2.6 vs. ±1.0).

**Adaptation dynamics**: ~75% of accepted skill writes occur in rounds 1–2; gains plateau by round 5–6, consistent with dominant failure modes being addressed early.

**Token/step tradeoff**: mean input tokens increase (13.9k→16.9k on PinchBench, Kimi-K2.5) while mean interaction steps decrease (10.4→9.8 PinchBench, 7.3→5.8 Claw-Eval), indicating computation shifts from environment interactions to richer per-step context.

## Limitations
- Effectiveness degrades under sparse or delayed feedback and when required tool interfaces are unavailable—conditions where intermediate signals cannot be observed.
- Evaluated only on three public benchmarks (WebShop, PinchBench, Claw-Eval); long-term deployment stability and behavior under distribution shift are untested.
- Gains are task-type dependent: Data/Code tasks (clear procedural traces) benefit most; Research, Memory, and Security tasks benefit least due to persistent state and external knowledge dependencies.
- Adds per-step context to prompts (up to +20% tokens on desktop benchmarks), increasing inference cost even as interaction steps decrease.

## Relevance to Harnesses / Meta-Harnesses
SkillAdaptor is explicitly designed as a plug-in post-execution adaptation module for OpenClaw-class harnesses, making it a direct example of meta-harness infrastructure: it operates above the task-execution layer to evolve the skill library that the harness injects. The qualification gate and step-level attribution logic are architectural patterns directly applicable to any harness that maintains a reusable skill/tool store. The paper also benchmarks on PinchBench and Claw-Eval, which are themselves harness-native evaluation frameworks, grounding its findings in the OpenClaw ecosystem. For researchers building or studying meta-harnesses, SkillAdaptor demonstrates a concrete credit-assignment mechanism that improves over session-level reflection without requiring harness-level architectural changes.

## Tags
#agent-harness #skill-adaptation #credit-assignment #training-free #openClaw #llm-agents #tool-use #continual-learning
