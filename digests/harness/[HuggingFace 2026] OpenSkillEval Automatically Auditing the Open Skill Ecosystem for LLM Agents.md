---
title: "OpenSkillEval: Automatically Auditing the Open Skill Ecosystem for LLM Agents"
authors: ["Jiahao Ying", "Boxian Ai", "Wei Tang", "Siyuan Liu", "Yixin Cao"]
source: "HuggingFace"
venue: ""
published: "2026-05-28"
published_time: "2026-05-28T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2605.23657"
url: "https://huggingface.co/papers/2605.23657"
pdf: "paper/harness/[HuggingFace 2026] OpenSkillEval Automatically Auditing the Open Skill Ecosystem for LLM Agents.pdf"
---

# OpenSkillEval: Automatically Auditing the Open Skill Ecosystem for LLM Agents

*🕒 **Published (v1):** 2026-05-28 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2605.23657)*

## TL;DR
OpenSkillEval is an automatic evaluation framework that audits both skill-augmented LLM agent systems and the open-source skills themselves, using dynamically generated real-world task instances rather than static benchmarks. It evaluates 30 community-contributed skills across 677 tasks in five artifact-production categories, revealing that skill availability does not guarantee usage and that skill benefit is strongly model- and framework-dependent.

## Problem
The open-source skill ecosystem (structured workflow instructions for LLM agents) has expanded rapidly, but there is no systematic way to evaluate: (1) whether agents actually use injected skills, (2) how agent framework × model × skill interactions affect performance, or (3) how to select skills given cost-performance trade-offs. Static benchmarks fail to capture evolving real-world task distributions.

## Method
OpenSkillEval has three automated pipelines:

1. **Artifact-driven case generation**: For five task categories (PPT generation, web design, poster generation, data visualization, report generation), existing high-quality artifacts are collected from external repositories; LLMs reverse-engineer them into structured task specifications and natural-language instructions; a verifier LLM filters incoherent instances. Result: 677 dynamically generated instances using Claude-4.6-Opus and GPT-5.2 as generators.

2. **Skill collection**: 30 skills curated from public repositories (clawhub.ai, skills.sh, openskills.space, skillsmp.com), filtered by community download count, organized per task category.

3. **Evaluation pipeline**: Two complementary tracks — (a) *trajectory trace analysis* using the Agent Trajectory Interchange Format (ATIF) with an agent-as-judge that decomposes skills into workflow steps and checks follow/skip/contradict rates against actual execution traces; (b) *artifact analysis* using task-specific rubrics (VLM-as-judge, agent-as-judge, code-based data accuracy checks, interaction simulation for web design) on a 1–5 scale across dimensions such as completeness, content quality, visual design, and fidelity.

## Key Contributions
- Dynamic benchmark of 677 task instances auto-generated from evolving real-world artifacts across five categories, enabling continuous refresh.
- Systematic trajectory-level audit revealing that agents read skill files in only ~48% of cases under default settings (as low as 20% for Claude Opus 4.6), even when the skill is accessible.
- Quantified step-level adherence: even under forced skill usage (~94% read rate), agents still skip or contradict prescribed workflow steps at measurable rates.
- Per-task, per-model, per-skill performance × cost analysis across 9 agent systems (Claude Code + Claude 4.6 series, Codex + GPT-5.x, Gemini CLI, Kimi Code CLI, DeepSeek V4 Pro, GLM-5.1, MiniMax M2.7).
- Empirical finding that many high-download skills fail to outperform the no-skill baseline, and that a weaker model with good skills and framework can match a stronger base model.

## Results
- Under default deployment, average skill read rate across agents: **~48%**; Claude Opus 4.6 specifically: **~20%**.
- Force-using setting raises average read rate to **94%** and shifts first skill access from step 4.4 to step 3.3.
- Top overall performers: **Claude Opus 4.6 (Claude Code framework, avg 4.51/5)** and **GPT-5.5 (Codex, avg 4.47/5)**; lowest: DeepSeek V4 Pro (3.76) and GLM-5.1 (4.03) when run in adapted frameworks.
- GPT-5.5 under Codex achieves best efficiency: lowest token consumption while maintaining top-tier performance; GPT-5.3-codex uses fewer tokens than GPT-5.2.
- Poster generation and presentation generation are the hardest categories (visual design subscores typically <4.0) and most token-intensive; web design interactive functionality is already near ceiling for most models.
- Skill augmentation is heterogeneous: GPT-5.3-codex frequently performs *worse* with skills than without; some skills (e.g., ppt-master) provide consistent gains; many popular skills yield no meaningful improvement over the no-skill baseline.

## Limitations
- Skill set is a time-sensitive snapshot; community repositories evolve, so rankings may shift.
- Filtering skills by download count introduces popularity bias; low-download but high-quality skills are excluded.
- Evaluation relies on LLM/VLM-as-judge scoring, which inherits model-specific biases.
- Force-using setting (explicit directive to read skill file) departs from realistic deployment; it artificially inflates skill-read rates and may not reflect organic user behavior.
- Only five task categories covering artifact-generation tasks; findings may not generalize to tool-use, planning, or dialogue-centric agent settings.
- Adaptation of non-native models (e.g., GLM-5.1) into Claude Code framework introduces framework-model mismatch confounds.

## Relevance to Harnesses / Meta-Harnesses
OpenSkillEval is itself a meta-harness: an automated orchestration layer that wraps multiple agent frameworks, drives them through dynamically constructed task instances, collects execution traces via ATIF, and applies multi-modal judges to produce cross-system evaluation reports. Its trajectory interchange format (ATIF) is a direct analog to the kind of unified observation interface that meta-harnesses need to inspect sub-agent behavior uniformly across heterogeneous backends. The finding that agents autonomously decide whether to follow injected workflow instructions is directly relevant to harness designers who rely on skills or system-prompt procedures to steer sub-agents — skill compliance cannot be assumed and must be enforced or verified at the harness level. The cost-performance scatter analysis across 30 skills × 9 models provides an empirical template for how a production meta-harness should instrument and compare pluggable workflow modules.

## Tags
#benchmark #llm-agents #skills #workflow-instructions #dynamic-evaluation #agent-trajectory #meta-harness #evaluation-framework
