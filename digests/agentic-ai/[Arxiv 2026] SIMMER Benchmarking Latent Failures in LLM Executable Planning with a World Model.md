---
title: "SIMMER: Benchmarking Latent Failures in LLM Executable Planning with a World Model"
authors: ["Xiaoxin Lu", "Ranran Haoran Zhang", "Rui Zhang"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T15:53:16+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14574"
url: "http://arxiv.org/abs/2606.14574v1"
pdf: "paper/agentic-ai/[Arxiv 2026] SIMMER Benchmarking Latent Failures in LLM Executable Planning with a World Model.pdf"
---

# SIMMER: Benchmarking Latent Failures in LLM Executable Planning with a World Model

*🕒 **Published (v1):** 2026-06-12 15:53 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14574v1)*

## TL;DR
SIMMER is a benchmark that exposes "latent failures" in LLM-generated executable plans — errors that satisfy all preconditions and produce no immediate exception but silently compromise goal safety through implicit state propagation. Across six frontier and open-weight LLMs on 100 kitchen tasks, fewer than 17% of plans are error-free, and 29–56% contain latent failures, most of which are irreversible. Counterfactual foresight simulation — prompting models to predict state changes before committing each action — reduces latent failures by up to 72%.

## Problem
Existing LLM planning evaluations either use virtual environments that check only precondition violations (immediate failures) or measure surface-level semantic similarity to reference plans. Neither paradigm detects latent failures: errors where every individual action executes legally yet cumulative implicit state changes (contamination spread, appliance left on, missing implicit precondition) silently invalidate the plan's safety or correctness, often irreversibly. The standard plan-execute-replan loop cannot recover irreversible latent failures because no replanning action can undo the state damage.

## Method
SIMMER integrates three components:

1. **Symbolic world model**: PDDL-style definitions for 77 actions and 262 objects, grounded in cooking scripts from wikiHow and Instructables. Each action specifies `⟨args, preconditions, effects⟩`; each object specifies `⟨properties, states, location⟩`. GPT-5.4 extracted candidates; human annotators curated, normalized, and formally annotated them. The model supports ~46,800 semantically realistic interactions — orders of magnitude more than TextWorld (≤260) or VirtualHome (≤2,112).

2. **Failure taxonomy**: Immediate failures violate preconditions and block execution; latent failures satisfy all preconditions but silently propagate bad state (e.g., contamination transferring from unwashed cutting board to vegetables). Latent failures are further split into reversible (e.g., forgotten salt, correctable) and irreversible (e.g., bacterial contamination once served, unrecoverable).

3. **State machine executor** with two-phase detection: Phase 1 (step-by-step) checks preconditions, applies state transitions, and flags contamination propagation events; Phase 2 (post-execution audit) scans the final state for unresolved hazardous conditions (e.g., food served while contaminated, stove left on).

Two open-loop mitigation strategies are evaluated: **Self-Refine** (generate plan, then critique against a safety checklist and rewrite) and **Counterfactual Foresight Simulation** (before each action: predict state changes, self-check for hazards, revise if needed — enforcing step-level mental simulation throughout generation).

## Key Contributions
- SIMMER benchmark: kitchen symbolic world model with 77 actions, 262 objects, ~46,800 interactions, derived from real cooking scripts
- Formal failure taxonomy distinguishing immediate, latent-reversible, and latent-irreversible planning failures
- State machine executor that detects latent failures invisible to precondition-only validators
- First systematic latent failure analysis across six LLMs (GPT-5.4, Gemini 3 Flash, Claude Opus 4.6, Llama 3.3 70B, DeepSeek V3, Qwen 3.5 27B)
- Counterfactual foresight simulation prompting strategy achieving up to 72%/75% reduction in latent/irreversible failures

## Results
- Across all six models, fewer than 17% of plans are error-free; average is 7.2%
- Latent failures: 29% (Claude Opus 4.6) to 56% (GPT-5.4) of plans contain at least one; 0.50–1.73 latent failures per plan
- Irreversible failures: 20% (Gemini 3 Flash) to 45% (Llama 3.3 70B) of plans affected
- Frontier models average 2.12 immediate failures/plan; open-weight models average 4.91
- Self-Refine: ~40% total failure reduction for GPT-5.4 and Claude Opus 4.6; marginal or negative for weaker models
- Counterfactual foresight vs. Self-Refine on GPT-5.4: immediate failures 73% vs. 30% reduction; latent failures 64% vs. 69% reduction; irreversible 45% vs. 27% reduction
- Counterfactual foresight on Claude Opus 4.6: latent −72%, irreversible −75%; Self-Refine: latent −75%, irreversible −75% (comparable on latent, foresight dominates on immediate)
- SIMMER exposes ~46,800 possible interactions vs. 2,112 for VirtualHome (next largest comparable)

## Limitations
- Domain restricted to kitchen cooking; generalizability to other planning domains (e.g., navigation, software task) is untested
- Task dataset is 100 scripts only, though covering all 77 actions and 262 objects
- Counterfactual foresight evaluated only on the two best-performing models (GPT-5.4, Claude Opus 4.6); results for weaker models unknown
- Open-loop evaluation only; no closed-loop comparison against environments providing real execution feedback
- World model is manually curated and may not capture all real-world food-safety constraints or cross-domain implicit norms
- Self-Refine degrades performance for weaker models, and the mechanism (insufficient reasoning capacity) is only hypothesized, not validated

## Relevance to Agentic AI / LLM Agents
SIMMER directly challenges the assumption underlying most LLM agent benchmarks — that task success rate adequately measures agent reliability. By demonstrating that up to 56% of plans from frontier models contain silent, often irreversible failures, it shows that agents can appear to "succeed" on conventional metrics while producing unsafe outcomes. The failure taxonomy (latent vs. immediate, reversible vs. irreversible) is a principled framework applicable beyond cooking to any agent operating in state-dependent environments. Counterfactual foresight simulation is a concrete, deployable prompting technique for improving agent safety without requiring closed-loop environment access — relevant for anyone building planning agents where environment feedback is expensive or unavailable.

## Tags
#benchmark #llm-planning #agentic-ai #embodied-agents #failure-analysis #world-model #safety #prompting
