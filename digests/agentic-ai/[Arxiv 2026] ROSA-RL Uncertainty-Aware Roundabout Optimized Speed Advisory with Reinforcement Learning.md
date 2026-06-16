---
title: "ROSA-RL: Uncertainty-Aware Roundabout Optimized Speed Advisory with Reinforcement Learning"
authors: ["Anna-Lena Schlamp", "Jeremias Gerner", "Klaus Bogenberger", "Werner Huber", "Stefanie Schmidtner"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T11:00:08+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16558"
url: "http://arxiv.org/abs/2606.16558v1"
pdf: "paper/agentic-ai/[Arxiv 2026] ROSA-RL Uncertainty-Aware Roundabout Optimized Speed Advisory with Reinforcement Learning.pdf"
---

# ROSA-RL: Uncertainty-Aware Roundabout Optimized Speed Advisory with Reinforcement Learning

*🕒 **Published (v1):** 2026-06-15 11:00 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16558v1)*

## TL;DR
ROSA-RL couples a Transformer-based probabilistic conflict-zone occupancy predictor with a PPO reinforcement learning agent to issue uncertainty-aware speed advisories for vehicles approaching roundabouts in mixed traffic. By encoding prediction confidence directly into the RL state, it outperforms model-based baselines under partial observability while matching ground-truth performance under full observability.

## Problem
Roundabout entry in mixed traffic is a partially observable sequential decision problem: human driving intentions (yield vs. circulate vs. exit) are unknown, making conflict zone availability uncertain. Prior model-based speed advisory systems (e.g., ROSA) deterministically infer conflicts from trajectory predictions and ignore prediction uncertainty, which degrades performance when occupancy is ambiguous. Prior RL approaches to speed optimization were limited to deterministic, fully observable settings (e.g., signalized intersections with known phase timing).

## Method
Two components are stacked end-to-end:

1. **Zone-centric occupancy prediction**: A shared Transformer encoder processes 3 s of historical agent states (position, velocity, acceleration, heading, class) for all scene agents jointly, producing contextualized token embeddings. Five horizon-specific Transformer encoders then refine these per prediction step (1–5 s), followed by attention-based pooling and per-horizon MLP heads that output scalar occupancy scores trained with binary cross-entropy plus logit regularization. Uncertainty per horizon is derived as `u = 1 − 2|ô_h − 0.5|`.

2. **Uncertainty-aware PPO agent**: The RL state includes ego speed, distance to conflict zone, expected arrival times, binarized occupancy predictions per horizon, and the signed distance of each occupancy score from the 0.5 threshold (encoding both predicted state and confidence magnitude). A reward function penalizes stops (weight 5), speed oscillations (weight 0.5), and per-step delay (weight 1). Training uses SUMO microsimulation replaying real-world trajectories from the openDD dataset.

## Key Contributions
- A conflict-zone–centric Transformer occupancy predictor covering a 5 s horizon with horizon-wise uncertainty quantification, avoiding full-scene rasterization or per-agent trajectory regression.
- An uncertainty-aware PPO speed advisory framework that encodes probabilistic occupancy confidence into the RL state, approximating the POMDP as a belief-MDP with minimal overhead.
- Systematic ablation across six conditions (MB-GT, RL-GT, MB-TP, MB-OP, RL-OP, UA-RL-OP) separating the contributions of observability, prediction modality, and uncertainty awareness.

## Results
- **Occupancy prediction**: ROC-AUC 0.997 / PR-AUC 0.984 at 1 s; ROC-AUC 0.927 / PR-AUC 0.647 at 5 s. Outperforms trajectory-based ROSA baseline from 4 s onward (F1: 0.72 vs. 0.70 at 4 s) with more balanced precision–recall at longer horizons.
- **Under full observability (RL-GT vs. MB-GT)**: RL matches model-based ground-truth — waiting time −90.7% vs. −91.3%, stops −80% vs. −78%.
- **Under partial observability (UA-RL-OP vs. MB-TP)**: UA-RL-OP achieves −89.9% waiting time vs. −78.9% and −80% stops vs. −60%; BEV energy −85.6% vs. −56.0%; ICE emissions −17.5% vs. −28.0% (minor drawback due to speed oscillations).
- In non-optimizable scenarios UA-RL-OP introduces no additional stops, showing robustness to false positives.

## Limitations
- Evaluated on a single-lane roundabout entry (rdb1, northern entry) from one dataset (openDD); generalization to multi-lane or geometrically diverse roundabouts is asserted but not demonstrated.
- Minor ICE emission increase in UA-RL-OP (−17.5% vs. −28.0% for MB-TP) due to residual speed oscillations from the RL policy.
- Practical deployment assumes V2X infrastructure or roadside sensing for trajectory aggregation; V2X latency and communication uncertainty are not modeled.
- Single ego-vehicle formulation; cooperative multi-vehicle control and high fleet penetration scenarios are left to future work.
- Only simulation validation; no real-world driving experiments.

## Relevance to Agentic AI / LLM Agents
ROSA-RL exemplifies the class of **uncertainty-aware sequential decision-making agents** operating in partially observable environments — a core challenge shared by agentic AI systems that must act on imperfect world models. The design pattern of encoding an explicit uncertainty signal into the agent's state (belief-MDP approximation without full Bayesian inference) is a lightweight technique directly applicable to any RL-based agent facing stochastic, intent-uncertain environments. The ablation framework (full vs. partial observability, deterministic vs. probabilistic inputs) also provides a reusable evaluation template for benchmarking agent robustness under partial observability. While domain-specific to traffic, the architecture — Transformer world model feeding a PPO policy with calibrated uncertainty features — maps cleanly onto broader agentic decision loops where environmental state must be inferred rather than observed.

## Tags
#reinforcement-learning #uncertainty-aware #partial-observability #autonomous-driving #multi-agent #transformer #sequential-decision-making #pomdp
