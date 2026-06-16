---
title: "Under What Conditions Can a Machine Be Called Genuinely Creative?"
authors: ["Yong Zeng"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T11:02:08+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13196"
url: "http://arxiv.org/abs/2606.13196v2"
pdf: "paper/harness/[Arxiv 2026] Under What Conditions Can a Machine Be Called Genuinely Creative.pdf"
---

# Under What Conditions Can a Machine Be Called Genuinely Creative?

*🕒 **Published (v1):** 2026-06-11 11:02 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13196v2)*

## TL;DR
This paper proposes a ten-requirement framework for "genuine machine creativity" grounded in Designics — the science of meaning-bearing intentional change — organized through three laws: perception, conflict, and capability. It argues that creativity should be evaluated by a system's participation in recursive intervention dynamics (perceive → scope → conflict-identify → intervene → observe consequences → update → rescope), not by output novelty alone. Contemporary AI systems (foundation models, agentic workflows, automated discovery) are treated as "pressure cases" that partially instantiate but do not fulfill these requirements.

## Problem
Existing benchmarks and evaluations of machine creativity are output-centered (novelty, usefulness, surprise), which conflates generating creative-looking artifacts with genuine creative participation. No principled, architecture-independent framework exists for evaluating when a machine is truly creative versus merely generative; additionally, AI ethics is typically applied as an external filter after generation rather than embedded in the creative process.

## Method
The paper derives requirements from Designics theory rather than from any specific AI architecture. Three Designics laws organize ten requirements:

- **Law of Perception** → R1 (environment representation), R2 (scoped perception), R5 (consequence observation), R7 (rescoping), R9 (value-based scoping)
- **Law of Conflict** → R3 (conflict identification)
- **Law of Capability** → R4 (intervention capability), R6 (knowledge/environment update), R8 (local-to-global unfolding), R10 (human–AI co-living)

The core mechanism is **recursive intervention dynamics**: a situation is perceived under constrained scope → conflicts/insufficiencies are identified → an intervention is introduced into the environment → consequences are observed → knowledge and environment representations are updated → scope is revised → next cycle begins. Selected cyber-physical studies (recursive mesh generation, autonomous element extraction) and cyber-biological studies (neurophysiological tracking, workload reallocation, human capacity zone analysis) are mapped to individual requirements to show computational tractability.

## Key Contributions
- Reframes machine creativity from output generation to structural participation in recursive intervention dynamics
- Derives a stable, architecture-independent ten-requirement framework from Designics
- Operationally grounds each requirement via existing computational and empirical studies
- Repositions contemporary AI paradigms (agentic workflows, self-modifying agents, foundation models) as partial instantiations, not definitions, of genuine creativity
- Internalizes proactive AI ethics (value-based scoping, human–AI co-living) as core requirements rather than post-hoc compliance layers

## Results
This is a purely theoretical/framework paper; no quantitative benchmarks, ablations, or comparative evaluations are reported. Validation is illustrative: existing cyber-physical and cyber-biological studies are cited as evidence of computational tractability for individual requirements, not as an empirical validation of the full framework. Mathematical formalization is explicitly deferred to future work.

## Limitations
- No measurement criteria or degrees of satisfaction defined for any requirement; framework is explicitly not a "pass/fail checklist"
- No empirical evaluation of the framework against existing systems
- Mathematical formalization absent; claims of tractability rely on loose mappings to existing studies
- Framework is derived from a single theoretical tradition (Designics / Environment-Based Design), creating potential circularity
- Requirement interdependencies are described qualitatively; no formal model of their mutual constraints
- Domain coverage of illustrative studies is narrow (mesh generation, workload reallocation) relative to the framework's broad scope

## Relevance to Harnesses / Meta-Harnesses
The recursive intervention dynamics loop (scope → conflict-identify → intervene → observe → update → rescope) is structurally isomorphic to the control loop that agent harnesses implement: a harness sets context (scope), dispatches agents (intervention), collects outputs (consequence observation), updates state (knowledge update), and re-invokes with revised context (rescoping). The ten requirements effectively function as a design checklist for evaluating whether a meta-harness transcends mere agent orchestration to support emergent, consequence-sensitive behavior. R8 (local-to-global unfolding) directly addresses how harnesses that compose many local agent calls can produce global creative or scientific structure — a core design challenge for meta-harnesses in automated discovery pipelines. The framework's insistence that architectures should instantiate rather than define creativity aligns with the harness paradigm of placing stable orchestration logic over interchangeable backend models.

## Tags
#recursive-agent #agentic-workflow #requirement-framework #machine-creativity #human-ai-collaboration #scientific-discovery #autonomous-agent #proactive-ethics
