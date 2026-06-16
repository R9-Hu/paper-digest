---
title: "INFRAMIND: Infrastructure-Aware Multi-Agent Orchestration"
authors: ["Ahasan Kabir", "Jiaqi Xue", "Mengxin Zheng", "Qian Lou"]
source: "Arxiv"
venue: ""
published: "2026-06-09"
published_time: "2026-06-09T20:50:12+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.11440"
url: "http://arxiv.org/abs/2606.11440v1"
pdf: "paper/harness/[Arxiv 2026] INFRAMIND Infrastructure-Aware Multi-Agent Orchestration.pdf"
---

# INFRAMIND: Infrastructure-Aware Multi-Agent Orchestration

*🕒 **Published (v1):** 2026-06-09 20:50 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.11440v1)*

## TL;DR
INFRAMIND is an infrastructure-aware multi-agent LLM orchestration framework that closes the "infrastructure blindness" gap in existing routers by conditioning topology planning, per-step model/strategy selection, and queue scheduling on real-time serving metrics (queue depths, KV-cache pressure, latencies). Formulated as a hierarchical constrained MDP and trained end-to-end via RL, it delivers up to +7.6 pp accuracy and 7× lower latency at low load, and sustains 99.9% SLO compliance under high load where all baselines collapse below 50%.

## Problem
Existing multi-agent orchestration systems (MoA, GPTSwarm, MasRouter) select models and topologies from static task features alone, ignoring runtime infrastructure state on shared GPU clusters. This causes systematic load imbalance: preferred models accumulate deep queues (>130 pending requests) while capable alternatives sit idle, translating to avoidable latency that compounds across every downstream agent step in a pipeline. Under high concurrent load, this causes SLO compliance to collapse across all prior methods.

## Method
INFRAMIND inserts infrastructure awareness at three decision layers, jointly trained as a single hierarchical RL policy:

1. **Infra-aware planner**: At query arrival, a cascaded controller (task classifier → topology → agent count → roles) is conditioned on a system summary vector `z₀ = [budget, queue_depths, E2E_latencies, KV_utilizations]` via Feature-wise Linear Modulation (FiLM), biasing toward simpler graphs under congestion and richer topologies when capacity is available.

2. **Infra-aware executor**: At each agent step, a dual-pathway neural policy reads a semantic pathway (query + role embeddings via Sentence-BERT) and a resource pathway (remaining budget + live per-model metrics polled from vLLM's `/metrics` endpoint). The joint action head selects both a target model and a reasoning strategy (Flash / Concise / DeepThink) from a 5-model × 3-strategy action space.

3. **Budget-aware EDF scheduler**: Each model's request queue is reordered by deadline (`t_arrive + β`), so tight-budget requests are not head-of-line blocked by relaxed ones.

Training uses hierarchical policy gradient: executor via PPO, planner via REINFORCE on episode return, with a shared Lagrange multiplier λ enforcing the latency budget constraint via dual updates. A System Monitor continuously polls vLLM telemetry to provide real-time state.

## Key Contributions
- Identifies and empirically quantifies "infrastructure blindness" as a systematic failure mode of multi-agent LLM orchestration on shared GPU clusters.
- First end-to-end infrastructure-aware multi-agent orchestrator with awareness at all three layers (planning, execution, scheduling).
- Hierarchical constrained MDP formulation trained jointly via RL, automatically learning the quality–latency trade-off across load regimes without hand-coded rules.
- Budget-aware EDF scheduler that propagates query deadlines into each model's serving queue.
- Blackbox/hybrid extension using client-side proxies (EMA latency, RPM-derived congestion signal) that extends infrastructure awareness to API-only pools without server-side access.

## Results
- **Low load (10 req/min)**: +7.6 pp on MATH (82.0% vs. 74.4% MoA), +7.4 pp on GSM-Hard (62.0% vs. 54.6% MASRouter); up to 14× lower latency on HumanEval (5 s vs. 70 s MASRouter).
- **High load (100 req/min)**: Up to 99.9% SLO compliance (HumanEval); all baselines drop below 50% SLO on 4/5 benchmarks; MoA and GPTSwarm exceed 1,000 s mean latency on several benchmarks.
- **Ablations**: Disabling infra-aware routing increases mean queue depth 25.1→40.6 and step latency 2.3–3.6×; replacing EDF with FCFS doubles mean latency (68→134 s); forcing Flash-only reasoning drops MMLU-Pro accuracy 9.5 pp (59.5%→50.0%).
- **Budget sensitivity**: On MATH at low load, accuracy rises from 62.6% to 82.0% (+19.4 pp) as budget increases from 10 s to 300 s, emerging from RL without hand-coded budget rules.
- **Hybrid/API pools (GSM-Hard)**: At 100 req/min, INFRAMIND achieves 54.4% SLO (hybrid) and 50.4% SLO (pure-API) vs. MASRouter at 11.6% and 30.6%.

## Limitations
- Topology is committed once at planning time; mid-workflow revision under changing load is not supported.
- Assumes a fixed, static model pool; no adaptation to elastic/autoscaling or hot-swap configurations.
- Blackbox proxy signals (EMA latency, RPM ratio) are approximations; accuracy degrades if provider rate limits are opaque or inconsistent.
- Training requires simulated Poisson load across budget tiers, which may not match all production arrival distributions.

## Relevance to Harnesses / Meta-Harnesses
INFRAMIND directly addresses a gap in meta-harness design: existing orchestration harnesses (including learned routers like MasRouter) treat the underlying serving infrastructure as a black box, making topology and routing decisions that are unaware of runtime system state. This paper demonstrates that a harness operating on shared GPU clusters must incorporate live infrastructure telemetry as a first-class input to avoid compounding queue delays across multi-step pipelines. For researchers building or evaluating meta-harnesses, the hierarchical constrained MDP formulation—where a planner sets structure once and an executor adapts step-by-step—is a concrete architectural pattern showing how to decouple planning-time and execution-time adaptation within a single jointly-trained policy. The blackbox extension is also directly relevant: it shows that infrastructure-aware harnesses can be built without privileged server access, lowering the bar for adoption in any deployment environment.

## Tags
#multi-agent #orchestration #routing #infrastructure-aware #reinforcement-learning #latency #slo #harness
