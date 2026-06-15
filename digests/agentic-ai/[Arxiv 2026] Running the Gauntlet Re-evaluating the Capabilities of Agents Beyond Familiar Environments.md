---
title: "Running the Gauntlet: Re-evaluating the Capabilities of Agents Beyond Familiar Environments"
authors: ["Mykola Vysotskyi", "Runqi Lin", "Grzegorz Biziel", "Michal Zakrzewski", "Sebastian Montagna", "Damian Rynczak", "Shreyansh Padarha", "Kumail Alhamoud", "Zihao Fu", "William Lugoloobi", "Kai Rawal", "Hanna Yershova", "Xander Davies", "Taras Rumezhak", "Guohao Li", "Fazl Barez", "Baoyuan Wu", "Arkadiusz Drohomirecki", "Yarin Gal", "Chris Russell", "Christopher Summerfield", "Adam Mahdi", "Volodymyr Karpiv", "Philip Torr", "Adel Bibi"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14397"
url: "http://arxiv.org/abs/2606.14397v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Running the Gauntlet Re-evaluating the Capabilities of Agents Beyond Familiar Environments.pdf"
---

# Running the Gauntlet: Re-evaluating the Capabilities of Agents Beyond Familiar Environments

## TL;DR
GauntletBench is a web-based agent benchmark targeting three underexplored capabilities—temporal perception, graphical understanding, and 3D reasoning—across five professional applications. State-of-the-art agentic systems achieve only 19.1% success rate versus >80% for non-expert humans, exposing a critical generalisation gap invisible in existing saturated benchmarks.

## Problem
Existing web agent benchmarks (WebArena, MiniWoB++, WorkArena) are built on familiar consumer applications with form-filling and navigation tasks, leading to benchmark saturation and failure to expose genuine capability limitations. They neglect temporal perception, graphical understanding, and 3D spatial reasoning—capabilities increasingly demanded in real professional software—and lack compatibility with both open- and closed-source agent frameworks.

## Method
GauntletBench provides a modular pipeline: a unified web environment (state space S, action space A, observation space O, transition T, reward R) where agents interact via high-level browser commands (click, type, scroll) through Playwright. Five custom professional web applications are built with React/Next.js and canvas-based rendering: Video Editor, Workflow Builder, 3D Modeller, Flight Analyser, and Circuit Designer. Canvas-only interfaces for three apps force visual perception with no accessibility tree fallback, preventing agents from exploiting DOM shortcuts. Tasks are structured at three difficulty tiers (2 easy / 9 medium / 9 hard per app, 100 total). Evaluation uses a two-stage engine: per-application tailored objective evaluators (with task-aware tolerances, e.g., ±100 ms for video timestamps, fuzzy color matching) plus an MLLM-judge (GPT-5.1) for partial-credit progress rate (1–5 scale). Efficiency metrics (consumed tokens, consumed steps) are also reported.

## Key Contributions
- GauntletBench benchmark: 5 professional web apps × 20 tasks = 100 vision-intensive tasks targeting temporal perception, graphical understanding, and 3D reasoning.
- Modular evaluation pipeline compatible with open-source MLLM agents, API-based agents, and closed-source frameworks (e.g., Claude Computer Use, Gemini Enterprise).
- Tailored per-application evaluators with human-aligned tolerances, validated against human annotations (GPT-5.1 judge achieves κ=0.73 average agreement).
- Empirical evaluation of 14 frontier systems revealing a 60+ percentage-point human–agent gap.

## Results
- Best agent (Claude-Opus-4.6 Computer Use): **19.1% success rate**; Gemini Enterprise: 13.7%; GPT-5.4 CU: 4.3%.
- All open-source MLLM agents: ≤1.7% success rate on any single application; most achieve 0.0%.
- Best API-based agent (Claude-Opus-4.6): 13.2%; Gemini-3.1-Pro High-reasoning: 13.2%.
- Non-expert human annotators: **>80% success rate** across all applications, using ~30% fewer steps than the best agent.
- Ablation—model scale: Claude-Haiku-4.5 → Sonnet-4.6 → Opus-4.6 yields 1.7% → 8.7% → 12.3% SR; larger models also consume fewer tokens despite higher per-step cost.
- Ablation—extended reasoning: helps sufficiently capable models (Gemini-3.1-Pro: 6.3% → 13.2% with high reasoning); no improvement for Qwen-3-VL; Claude-Opus-4.6 Thinking slightly regresses (12.3% → 10.3%).
- Vision modality: enabling visual input improves progress rate by 43.5% (Qwen family) and 15.5% (GPT family) on text-exposed apps, confirming tasks are genuinely vision-intensive.
- Divide-and-conquer step strategy (Claude CU: more fine-grained steps) appears more efficient than high-token single-step reasoning (Qwen-Max: highest token cost, lower SR).

## Limitations
- Only five specialised domains; may not capture full diversity of real-world scenarios or interaction paradigms.
- Constraining agents to visual-only interaction (no DOM/CDP access) may understate capabilities in hybrid observation settings.
- 100 tasks total is a relatively small evaluation set, though each is human-validated as feasible.
- Closed-source framework internals are opaque, making it difficult to fully attribute performance differences to model vs. framework design.

## Relevance to Agentic AI / LLM Agents
GauntletBench directly addresses benchmark saturation—a critical infrastructure problem for the agent research community—by introducing professional, vision-intensive tasks where frontier agents fail dramatically despite near-human performance on existing benchmarks. The finding that agents make meaningful intermediate progress (progress rate >1 for nearly all systems) but collapse under accumulating long-horizon complexity has direct implications for agent architecture research (planning, error recovery, self-monitoring). The compatibility with closed-source computer-use frameworks (not just raw MLLMs) makes it one of the few benchmarks that evaluates end-to-end agentic systems as deployed, rather than model APIs in isolation. The empirical evidence that divide-and-conquer step strategies outperform high-token deliberation offers a concrete design signal for agent scaffolding.

## Tags
#benchmark #web-agents #computer-use #visual-grounding #3d-reasoning #temporal-perception #evaluation #generalisation
