---
title: "RetailBench: Benchmarking long horizon reasoning and coherent decision making of LLM agents in realistic retail environments"
authors: ["Linghua Zhang", "Jun Wang", "Jingtong Wu", "Zhisong Zhang"]
source: "Arxiv"
venue: ""
published: "2026-06-14"
published_time: "2026-06-14T15:30:30+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.15862"
url: "http://arxiv.org/abs/2606.15862v1"
pdf: "paper/harness/[Arxiv 2026] RetailBench Benchmarking long horizon reasoning and coherent decision making of LLM agents in realistic retail environments.pdf"
---

# RetailBench: Benchmarking long horizon reasoning and coherent decision making of LLM agents in realistic retail environments

*🕒 **Published (v1):** 2026-06-14 15:30 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15862v1)*

## TL;DR
RetailBench is a data-grounded POMDP simulation benchmark for evaluating tool-using LLM agents in single-store supermarket operation over 180-day horizons. Seven contemporary LLMs are tested under three agent frameworks; only two survive the full horizon, and the best LLM run achieves less than 19% of the oracle policy's net worth. Three systematic failure modes are identified: incomplete evidence acquisition, surface-level decision making, and absence of a consistent long-horizon policy.

## Problem
Existing agent benchmarks saturate on short-horizon, isolated tasks and do not expose whether agents can maintain coherent, stateful strategies over extended episodes where local errors compound through delayed consequences. Prior retail/supply-chain benchmarks isolate individual subproblems (pricing, inventory, shopping) rather than modeling the closed-loop, coupled dynamics of real business operation.

## Method
RetailBench models store management as a POMDP with latent state factorized across seven coupled modules: Inventory, Suppliers & Orders, Shelf, Customer Demand, Reviews & Returns, News Events, and Finance & Records. Agents interact through three tool groups — read-only queries (`A_read`), auxiliary tools including a memory writer and sandboxed `execute_code` (`A_other`), and state-changing actions (`A_act`). The simulator is grounded in the Dominick's grocery dataset (96 products, 20 categories), Amazon Reviews 2023 for customer feedback, and financial news articles for event dynamics. Customer demand follows a Multinomial Logit (MNL) model with Nakanishi-Cooper power aggregation. Agent performance is evaluated under ReAct, Reflection, and Plan-and-Act frameworks using a survival-first selection protocol over a 180-day horizon and compared against a privileged oracle policy with full structured state access. Behavioral diagnostics cover four axes: query depth/evidence completeness, price-closeness/supplier-quality scores, acted-products-per-day/high-demand coverage, and follow-up action rate/resolved-event rate.

## Key Contributions
- **RetailBench environment**: A data-grounded, 180-day POMDP benchmark coupling pricing, replenishment, supplier selection, shelf assortment, customer reviews, news events, and cash-flow into a single closed-loop evaluation.
- **Multi-model evaluation**: Seven LLMs (DeepSeek-V4-Pro, GPT-5.5, Kimi-K2.6, Grok-4.3, GLM-5.1, MiniMax-M2.5, Qwen3.5-397B-A17B) benchmarked across three agent frameworks with a privileged oracle reference.
- **Systematic failure taxonomy**: Three operationally grounded failure modes identified with quantitative diagnostics rather than qualitative observation.
- **Diagnostic testbed**: Four behavioral metrics provide fine-grained attribution of failure to evidence acquisition, reasoning quality, attention scope, or temporal follow-through.

## Results
- Only DeepSeek-V4-Pro and GPT-5.5 survive the full 180-day horizon; remaining agents terminate between day 58 and 130 (mean ~107 days).
- Oracle policy: net worth 131,510; total sales 267,998.
- Best LLM net worth: GPT-5.5 at 24,350.98 (−107,159 vs. oracle).
- Best LLM sales: DeepSeek-V4-Pro at 164,417 (−103,581 vs. oracle).
- Evidence acquisition: GPT-5.5 query depth 0.9922, evidence completeness 0.9689; Grok-4.3 completeness 0.0000.
- Price closeness: Oracle mean raw price distance 1.98%; best LLM (GPT-5.5) 17.92%.
- Supplier quality: LLM QualityFirst rate 21.5% vs. PriceFirst rate 55.6%; best selected-run QualityFirst only 34.65%.
- Product attention: Oracle acts on 38.00 products/day; LLMs act on 0.95–7.89 products/day, missing 32.86%–88.18% of high-demand opportunities.
- Temporal follow-up: Oracle follow-up rate 0.9936, unresolved-event rate 0.0040; DeepSeek-V4-Pro best LLM follow-up at 0.7316.

## Limitations
- Single-store scope; excludes multi-store coordination, competitive markets, strategic supplier behavior, labor costs, and promotions.
- Reviews, news events, supplier adaptation, returns, and parts of the demand model are synthetic or rule-based — not a full-fidelity retail simulator.
- Only prompting-based agents evaluated; no learning-based or fine-tuned agents.
- Selected-run protocol captures peak behavior, not mean performance across frameworks or seeds.
- Failure diagnostics are correlational, not causal; individual factor contributions are not isolated.
- Fixed environment configuration; generalization across parameter settings untested.

## Relevance to Harnesses / Meta-Harnesses
RetailBench is directly relevant as a controlled harness that defines the agentic loop — tool taxonomy, POMDP state, day-level transitions, and agent framework instantiation — and wraps it in a reproducible evaluation protocol. The three-framework (ReAct / Reflection / Plan-and-Act) instantiation pattern mirrors the meta-harness concern of running the same underlying agent across scaffolding variants to isolate framework effects from model effects. The quantitative behavioral diagnostics (query depth, evidence completeness, follow-up rate) function as harness-level instrumentation probes, showing how to instrument a simulation harness to produce structured per-dimension failure attribution rather than a single scalar score. The survival-first selection protocol is itself a harness design choice with significant impact on reported results, raising questions about how meta-harnesses should aggregate across runs when terminal failure is possible.

## Tags
#benchmark #long-horizon #tool-use #agent-evaluation #pomdp #retail-simulation #failure-analysis #agentic-ai
