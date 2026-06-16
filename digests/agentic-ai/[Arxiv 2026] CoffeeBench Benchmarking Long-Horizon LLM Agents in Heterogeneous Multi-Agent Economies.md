---
title: "CoffeeBench: Benchmarking Long-Horizon LLM Agents in Heterogeneous Multi-Agent Economies"
authors: ["Issa Sugiura", "Daichi Hattori", "Kazuo Araragi", "Keita Ogawa", "Shota Onose", "Taro Makino", "Teppei Usuki", "Takashi Ishida"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T12:04:44+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16613"
url: "http://arxiv.org/abs/2606.16613v1"
pdf: "paper/agentic-ai/[Arxiv 2026] CoffeeBench Benchmarking Long-Horizon LLM Agents in Heterogeneous Multi-Agent Economies.pdf"
---

# CoffeeBench: Benchmarking Long-Horizon LLM Agents in Heterogeneous Multi-Agent Economies

*🕒 **Published (v1):** 2026-06-15 12:04 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16613v1)*

## TL;DR
CoffeeBench is a 90-day multi-agent economic simulation where an LLM-controlled coffee roaster must generate net income by communicating and transacting with two farmers and two retailers, all operated by independent LLM agents. It is the first benchmark combining long-horizon sequential decision-making with heterogeneous multi-agent economic roles. Top performers (GPT-5.5, Claude Opus 4.7) communicate heavily and engage markets actively; Claude Haiku 4.5 exhibits a novel "idle-drift" failure mode—coherent reasoning but persistent inaction.

## Problem
Existing long-horizon agent benchmarks (e.g., Vending-Bench, SWE-bench) evaluate either a single agent against a passive environment or multiple agents in homogeneous roles (e.g., competing vending machines). Real economies consist of heterogeneous firms with distinct supply-chain roles (producers, processors, distributors) that must communicate, negotiate, and transact under financial constraints over extended horizons. No prior benchmark captures this structure.

## Method
CoffeeBench simulates a coffee supply chain with six LLM-driven firms across three heterogeneous roles: two farmers, two roasters, two retailers. The evaluated model is assigned `roaster_A`; the five background firms run independently using Claude Sonnet 4.6 as the reference agent. All agents use the ReAct framework with role-specific tool sets: shared tools (`post_listing`, `make_offer`, `accept_offer`, `pay_invoice`, `send_message`) and role-specific tools (e.g., `roast()` for roasters, `set_retail_price()` for retailers). The simulation runs for 90 days with asynchronous, event-driven interaction—each proactive tool call advances the agent's local clock by 30 minutes; agents can be reactivated mid-day by incoming messages or trade events. Economic constraints include inventory spoilage (0.5%/day), storage caps, net-30 trade credit with late-payment penalties, stochastic logistics, and bankruptcy triggered by negative cash. The KPI is cumulative net income (Revenue − COGS − OpEx − InterestExp + InterestRev), with COGS computed on a weighted-average cost basis to prevent score inflation via self-trading. Histories exceeding 160k tokens are summarized mid-run using the same model. Three independent runs per model are executed; each run costs ~$250 in API spend across all six agents.

## Key Contributions
- First benchmark combining long-horizon, heterogeneous, multi-agent economic roles in a shared supply-chain marketplace.
- Identification and characterization of the **idle-drift failure mode**: agents generating coherent reasoning while repeatedly selecting inaction (`wait_for_next_day()`), observed prominently in Claude Haiku 4.5 (~40/90 days idle).
- Behavioral analysis decomposing performance into tool-use strategy, communication patterns, and inventory/margin discipline; shows that profitability correlates with proactive communication and pricing discipline, not merely transaction volume.
- Exploratory stress test under revenue-maximizing incentives showing current frontier models lack the long-horizon coherence for sophisticated collusion or circular trading.
- Public release of code and full agent trajectories across seven LLMs × three seeds.

## Results
- **GPT-5.5**: +$3,109 ±1,123 net income; 140 ±22 outbound DMs; highest proactive tool-call activity throughout all 90 days.
- **Claude Opus 4.7**: +$2,782 ±2,263; 88 ±13 DMs; concentrates on transaction-execution tools.
- **Claude Sonnet 4.6**: +$2,236 ±1,489; 151 ±25 DMs (highest DM count); 0 idle days.
- **Gemini 3.1 Pro**: +$1,695 ±508; only 16 ±3 DMs sent but reads 90 inbound messages—reactive style with efficient tool use and superior commodity pricing ($11.9/kg vs. Kimi K2.6's $10.8/kg) explains higher income than Kimi K2.6 despite similar revenue.
- **GLM-5.1**: +$1,597 ±1,199; highest revenue ($16,962) but weaker margin discipline.
- **Kimi K2.6**: +$454 ±1,420; high tool-call volume (1,173) but only 14 DMs—volume without coordination yields poor profit.
- **Claude Haiku 4.5**: −$630 ±1,745; 40 ±22 idle days; highest spoilage rate (3.5% of revenue); only model with negative net income.
- **HeuristicRoaster**: −$1,931; **PassiveRoaster**: −$2,765 (no actions).
- Best-observed result (GPT-5.5 at +$3,109) is ~13% of a loose analytical performance ceiling (~$23,800), indicating substantial headroom.
- No horizontal competitor-to-competitor messaging observed (≤1 DM to `roaster_B` across all models).

## Limitations
- Significant simulation-to-reality gap: production via simple tool calls, no financing/regulation/macroeconomic factors, supply chains shallower than real markets.
- Only three runs per model due to ~$250/run cost; high variance means small differences may not be statistically significant.
- Idle-drift root cause unexplained—hypothesized causes (long-context behavioral drift, implicit token-budget conservatism) are unvalidated.
- No manipulation or collusion behaviors emerged under revenue-pressure stress tests; whether this reflects model capability limits or benchmark constraints is unclear.
- Simulation is fully deterministic in structure, which may not capture emergent complexity of real market dynamics.

## Relevance to Agentic AI / LLM Agents
CoffeeBench extends long-horizon agent evaluation beyond single-agent coding/web tasks to a competitive, multi-stakeholder economic environment where sustained planning, proactive communication, and pricing strategy are all required—dimensions that existing benchmarks underexplore. The idle-drift failure mode directly implicates a fundamental reliability problem for deployed agentic systems: models can produce coherent reasoning while systematically failing to act, a failure not captured by task-completion metrics. The finding that communication frequency (not raw transaction volume) is the primary behavioral correlate of profitability has direct design implications for LLM agent architectures targeting real-world economic or operational settings. The controlled economic environment also offers a tractable testbed for studying emergent misalignment risks such as collusion and manipulative trading under altered incentive structures.

## Tags
#benchmark #multi-agent #long-horizon #economic-simulation #tool-use #failure-modes #llm-agents #supply-chain
