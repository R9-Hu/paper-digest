---
title: "Skill-to-LoRA: From Using Skills to Learning Behaviors for Token-Efficient LLM Agents"
authors: ["Tianyi Zhang", "Zhonghao Qi"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T14:17:39+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16769"
url: "http://arxiv.org/abs/2606.16769v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Skill-to-LoRA From Using Skills to Learning Behaviors for Token-Efficient LLM Agents.pdf"
---

# Skill-to-LoRA: From Using Skills to Learning Behaviors for Token-Efficient LLM Agents

*🕒 **Published (v1):** 2026-06-15 14:17 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16769v1)*

## TL;DR
Skill-to-LoRA (S2L) replaces runtime SKILL.md injection in LLM agents with skill-specific LoRA adapters trained offline via self-distillation, eliminating per-step skill-document overhead. On a 21-skill SWE-Skills-Bench subset, S2L solves 65/210 tasks vs. 54/210 for Full Skill Text prompting while reducing per-step token cost by 6.6% relative to that baseline.

## Problem
Agent skill libraries are deployed as SKILL.md files injected into every inference-step prompt. This creates redundant context overhead, competition with local repository evidence, and — per SWE-Skills-Bench — frequent neutral or negative effects on task success despite the token cost increase.

## Method
S2L has two stages:

**Offline (Skill-to-LoRA conversion):** For each skill `s` with document `t_s`, two LLM-based data-generation agents synthesize (1) diverse task inputs that would naturally trigger the skill, and (2) target outputs produced by the model conditioned on the full SKILL.md (teacher). A QLoRA adapter (rank 16, α=32, ~6.03M params, ~24MB) is then trained per skill on these (input, teacher-output) pairs using a standard causal LM loss on assistant tokens only — the base model (Qwen3.6-27B) remains frozen.

**Online (LoRA activation):** The runtime prompt retains only lightweight skill metadata for routing; the full SKILL.md body is omitted. The selected skill ID retrieves and dynamically loads the corresponding adapter via vLLM's multi-LoRA serving, steering the frozen base model toward the learned procedural behavior.

## Key Contributions
- Behavior-centric skill representation: models skill-induced behavioral change rather than compressing skill text.
- Skill-based self-distillation pipeline that auto-generates training data from SKILL.md without human annotation.
- Per-skill LoRA adapter library where each adapter encodes one skill's workflow, tool-use, and verification patterns (~0.022% of base model parameters per adapter).
- Introduction of Cost-Normalized Gain (CNG) metric: pass-rate improvement per unit of relative token-cost change.

## Results
- **Aggregate pass rate:** S2L 65/210 > Vanilla LLM 59/210 > Full Skill Text 54/210 on 21-skill SWE-Skills-Bench subset (210 tasks, Qwen3.6-27B).
- **Token cost vs. Vanilla LLM:** Full Skill Text +13.39% tokens; S2L −4.89% tokens.
- **CNG:** S2L +0.58 vs. Full Skill Text −0.18.
- **Skill-level coverage:** S2L matches or exceeds Full Skill Text on 18/21 skills; matches or exceeds Vanilla LLM on 15/21 skills.
- **Retrieval mismatch robustness (7-skill subset):** Under least-similar wrong-skill retrieval, S2L 35.6% vs. Full Skill Text 27.8% vs. Vanilla LLM ~28%.
- **Shared-LoRA ablation:** S2L (skill-specific) outperforms Shared-LoRA on all 6 tested skills (e.g., gitlab-ci-patterns: 7/10 vs. 3/10).
- **Configuration ablation (gitlab-ci-patterns):** rank-16, 64-row setting achieves 93.5; larger rank (32) or more data (128 rows) offers no gain or regresses.

## Limitations
- Effectiveness degrades for skills requiring concrete code examples, flexible syntax transfer, or open-ended reasoning, where runtime text provides richer local context.
- LoRA compression captures dominant behavioral effects; rare edge cases or highly specific configuration patterns may not be retained.
- Reduced interpretability: adapter weights cannot be inspected or edited like human-readable SKILL.md.
- Current design assumes single-skill-per-task activation; multi-skill composition, adapter routing, and behavioral conflict resolution are unaddressed.

## Relevance to Agentic AI / LLM Agents
S2L directly targets the skill/knowledge-injection bottleneck in tool-using LLM agents, proposing that procedural behavioral priors can be stored in model parameters rather than repeated in context — a form of compiled agent memory. This connects to a broader trajectory of moving reusable agent knowledge out of prompts and into weights (PromptIntern, Text-to-LoRA, SKILL0), but S2L is the first to demonstrate this for file-based, benchmark-evaluated SWE agent skills with a self-supervised pipeline requiring no environment rollouts. The dynamic adapter-routing framing is architecturally significant: it recasts skill management as a parameter-routing problem compatible with scalable multi-LoRA serving, pointing toward modular, composable agent skill ecosystems where skills are loadable behavioral modules rather than prompt libraries.

## Tags
#lora #skill-library #token-efficiency #swe-bench #knowledge-distillation #parameter-efficient-finetuning #agentic-ai #tool-use
