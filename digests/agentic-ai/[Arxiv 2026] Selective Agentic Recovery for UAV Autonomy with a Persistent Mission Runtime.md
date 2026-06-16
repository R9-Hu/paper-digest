---
title: "Selective Agentic Recovery for UAV Autonomy with a Persistent Mission Runtime"
authors: ["Taewoo Park", "Kyeonghyun Yoo", "Seunghyun Yoo", "Hwangnam Kim"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T07:57:47+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14219"
url: "http://arxiv.org/abs/2606.14219v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Selective Agentic Recovery for UAV Autonomy with a Persistent Mission Runtime.pdf"
---

# Selective Agentic Recovery for UAV Autonomy with a Persistent Mission Runtime

*🕒 **Published (v1):** 2026-06-12 07:57 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14219v1)*

## TL;DR
Persistent Mission Runtime (PMR) integrates an LLM-based agentic reasoner into UAV autonomy as a selective, on-demand recovery module rather than an always-active controller. A learned admission gate (learned-CVI) decides when remote reasoning is worth its latency and token cost. In a 400-run Gazebo/PX4 simulation, PMR raises hard-scenario success from 5% to 95% while cutting remote calls by 16.7% versus the best rule-based baseline.

## Problem
Prior LLM-augmented robot systems invoke remote reasoning either always-on, at static intervals, or via brittle expert-specified triggers—ignoring the latency, token cost, backend uncertainty, and verification burden each call introduces. Physical UAVs demand selective admission: remote reasoning should fire only when its expected recovery value exceeds those combined costs, and outputs must pass through a verified execution boundary before affecting flight.

## Method
PMR wraps a PPO-trained local flight policy with three layers:

1. **Admission gate (learned-CVI):** A lightweight linear classifier operating on an 18-dimensional runtime feature vector (kinematics, progress/no-progress, obstacle risk, query budget, verifier state) estimates whether invoking the remote LLM will yield more short-horizon mission progress than continuing locally. The score is combined with fixed runtime guards (budget, cooldown, terminal-radius suppression) and a hard-stuck override. The gate is trained pre-deployment from 651 labeled runtime states using K=5-step recovery-utility labels (Eq. 6) and held fixed during evaluation.

2. **Recovery-skill contract:** The remote LLM (accessed via an OpenClaw HTTP JSON gateway) is constrained to a closed vocabulary of predefined recovery skills and must return typed JSON. Raw flight commands are entirely outside its authority.

3. **Verification pipeline:** Returned JSON passes through sequential parsing → local verification → safety shielding → fallback checks → executor mapping before any flight action occurs (Eq. 3).

The local PPO policy uses a 10-dim observation and Discrete(32) macro actions; all baselines share this local policy, verifier, shield, and executor—only the admission rule differs.

## Key Contributions
- Formulation of selective remote reasoning for physical UAVs as a cost-aware online admission problem with bounded output authority.
- Learned-CVI: a pre-deployment 18D linear gate trained on short-horizon recovery-utility labels that outperforms rule-based triggers on held-out ROC-AUC (0.9635 vs. degraded alternatives) while being forward-only and transparent.
- Fixed-protocol 400-run Gazebo/PX4 benchmark across 8 scenarios comparing local-only, one-shot, periodic, rule-based, and learned-CVI admission policies.
- Real-world validation on a Crazyflie nano-quadcopter achieving 10/10 Clean Success@1m (vs. 0/10 local-only) with one query per trial.

## Results
- **Hard/ambiguous regime (40 runs):** learned-CVI 38/40 (95.0%) vs. local-only 2/40 (5.0%), one-shot 30/40 (75.0%), periodic 25/40 (62.5%), rule-based 39/40 (97.5%).
- **Nominal regime (40 runs):** learned-CVI 40/40 (100%) with only 0.150 calls/run vs. rule-based 1.200 calls/run — 87.5% fewer calls, 91.2% fewer tokens, identical success.
- **Invocation efficiency vs. rule-based (hard regime):** −16.7% calls, −29.2% tokens logged, within 1 success run.
- **Ablation (hard regime):** hard-stuck guard only 16/40 (40%), learned-CVI score only 25/40 (62.5%), matched-budget rule-based 37/40 (92.5%), full learned-CVI 38/40 (95.0%).
- **Model comparison (held-out ROC-AUC):** learned-CVI linear gate 0.9635 vs. small MLP [32,16] 0.6968 vs. boosted stumps 0.2976 — linear gate generalizes best.
- **Crazyflie real platform:** learned-CVI 10/10 at 0.192m mean final distance, 0 safety events; local-only 0/10 at 1.158m.

## Limitations
- Validated only for single-UAV indoor navigation recovery; outdoor perception, wind disturbance, heterogeneous airframes, and multi-UAV settings untested.
- Two remaining hard-regime failures are an under-query case (threshold sensitivity) and a remote-backend timeout—motivating adaptive thresholds and backend redundancy.
- Learned-CVI is a pre-deployment linear gate trained on a specific simulator distribution; transfer beyond semantic summaries to new sensor payloads requires re-labeling or feature re-mapping.
- Recovery-skill vocabulary is predefined and closed; richer or emergent skills require contract extension.

## Relevance to Agentic AI / LLM Agents
PMR is a concrete instantiation of *selective tool invocation*—a core challenge in deploying LLM agents in latency- and cost-sensitive real-world loops. Rather than treating the LLM as the controller, it positions the agent as a sparse recovery oracle with bounded output authority, directly addressing the safety-verification gap common in embodied agentic systems. The learned-CVI gate operationalizes "when should an agent call a tool?" as a trainable, cost-aware decision—a pattern applicable beyond UAVs to any agent runtime where remote inference is expensive or unreliable. The work also demonstrates that a lightweight linear classifier over compact semantic runtime features can capture most of the admission signal, suggesting that simple learned gates may be sufficient for structured tool-calling decisions in real deployments.

## Tags
#agentic-ai #llm-agents #selective-invocation #embodied-agents #tool-use #uav-autonomy #safety-filtering #cost-aware-reasoning
