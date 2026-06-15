---
title: "Communication Policy Evolution for Proactive LLM Agents"
authors: ["Xinbei Ma", "Jiyang Qiu", "Yao Yao", "Zheng Wu", "Yijie Lu", "Xiangmou Qu", "Jiaxin Yin", "Xingyu Lou", "Jun Wang", "Weiwen Liu", "Weinan Zhang", "Zhuosheng Zhang", "Hai Zhao"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14314"
url: "http://arxiv.org/abs/2606.14314v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Communication Policy Evolution for Proactive LLM Agents.pdf"
---

# Communication Policy Evolution for Proactive LLM Agents

## TL;DR
LLM agents operating under partial task information must decide not only *what* to ask users but *how* — via free-text or structured HTML forms. This paper formalizes this as a "Communication Policy," shows text and UI channels have complementary strengths, and proposes Communication Policy Evolution (CPE), a training-free prompt self-evolution method that achieves best task success across all evaluated configurations.

## Problem
Proactive LLM agents interact with users to recover missing task information, but prior work focuses exclusively on *what* to ask, ignoring the interaction channel. Free-text (`ask_question`) and structured UI (`generate_ui`) have different properties: text supports richer, flexible exchange while structured forms reduce ambiguity and improve persona compliance. Without a principled channel-selection strategy, hybrid access can hurt performance relative to single-channel baselines (negative "regret").

## Method
The paper formalizes a **Communication Policy** `πcomm = (system_prompt, examples, appendixes)` that governs when an agent uses `ask_question` vs. `generate_ui`. Three modes are defined: `Mtext`, `Mui`, and `Mhybrid`. Two evaluation settings isolate different sources of information asymmetry:
- **User–Agent**: agent faces partial spec `z̃`, must elicit missing info from a persona-conditioned LLM user simulator.
- **Planner–Executor**: agent-to-agent setting where a Planner holds full spec `z` and discloses cooperatively; removes persona effects.

**CPE** optimizes `πcomm` without model fine-tuning via iterative rollout-based prompt refinement: (1) evaluate current policy on a training batch, (2) prompt an LLM to propose a JSON patch `∆π` based on scores, trajectories, task specs, and patch history, (3) mutate policy with the patch, (4) accept only if the candidate beats the current policy on the batch *and* beats the global best on a held-out validation set, ensuring monotonically non-decreasing best-policy quality.

## Key Contributions
- Formal definition of **Communication Policy** as a first-class design variable for LLM agents, covering channel selection between text and generative UI.
- Systematic empirical comparison of text-only, UI-only, and hybrid interaction across four benchmarks (SWE-bench, TravelGym, τ²-bench, WebArena), four agent models, and four user personas.
- **CPE**: a training-free, self-evolving prompt optimization framework with two-stage gating (train + validation) that guarantees monotonic improvement on held-out data.
- Evidence that communication channel choice matters equally in agent–agent (Planner–Executor) settings as in user-facing settings.

## Results
- `Mhybrid` achieves best productivity in 8/14 User–Agent pairs; most consistent in SWE-bench (4/4), absent in WebArena (0/2).
- `Mui` dominates personalization (10/14 pairs) and proactivity (8/14 pairs); strongest in τ²-bench and TravelGym (8/8 for personalization).
- `Mtext` outperforms `Mui` on raw productivity in 9/14 pairs.
- Oracle (full-information injection) improves productivity 2.3×–10.6× over `Mtext`, confirming information gap is the primary bottleneck, not execution capability.
- **CPE improves productivity in all 9 configurations** where hybrid underperformed a single-channel baseline, e.g., DeepSeek-V3.2 on SWE-bench: `Mhybrid` 0.140 → `MCPE` 0.214; DeepSeek-V3.2 on TravelGym: 1.233 → 1.533; GPT-5-mini on WebArena: 0.180 → 0.275.
- CPE also improves proactivity (6/9) and personalization (6/9) relative to `Mhybrid`, showing no pure tradeoff.
- Planner–Executor: `Mhybrid` leads in 7/10 pairs, confirming channel flexibility benefits even cooperative, deterministic information exchange.

## Limitations
- Evaluation relies on LLM-based user simulators rather than real humans; may not capture true variability in user behavior and disclosure.
- Cost annotation follows a predefined sensitivity schema; real-world disclosure is more context-dependent and messy.
- Evaluation space covers four benchmarks, two settings, and four personas — the broader design space of channel types (voice, multimodal beyond HTML forms) is unexplored.
- CPE is applied only where `Mhybrid` underperforms a single-channel baseline; optimization across always-succeeding hybrid settings is not studied.

## Relevance to Agentic AI / LLM Agents
This paper addresses a concrete, under-studied bottleneck in real-world agent deployment: how to structure the communication interface, not just the content of queries, when agents operate under partial information. The CPE framework is directly applicable to any agent loop that uses interactable UI (e.g., tool-calling agents that generate forms or dialogs) and provides a training-free path to better channel policies via prompt evolution with gated rollout feedback. The complementary-strengths finding — text drives task completion, UI drives compliance and precision — has immediate design implications for agentic systems targeting heterogeneous users or multi-agent pipelines. The Planner–Executor framing also extends naturally to hierarchical multi-agent architectures where sub-agents must query orchestrators.

## Tags
#proactive-agents #communication-policy #human-agent-interaction #generative-ui #prompt-optimization #test-time-evolution #multi-agent #information-asymmetry
