---
title: "TrajGenAgent: A Hierarchical LLM Agent for Human Mobility Trajectory Generation"
authors: ["Siyu Li", "Toan Tran", "Lingyi Zhao", "Khurram Shafique", "Li Xiong"]
source: "Arxiv"
venue: ""
published: "2026-06-10"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12657"
url: "http://arxiv.org/abs/2606.12657v1"
pdf: "paper/harness/[Arxiv 2026] TrajGenAgent A Hierarchical LLM Agent for Human Mobility Trajectory Generation.pdf"
---

# TrajGenAgent: A Hierarchical LLM Agent for Human Mobility Trajectory Generation

## TL;DR
TrajGenAgent is a zero-shot hierarchical LLM-agent framework for synthetic human mobility trajectory generation that decouples macro-level activity planning (LLM orchestrator via in-context learning) from micro-level spatiotemporal grounding (deterministic LangGraph worker workflow), avoiding both the spatial imprecision of pure prompting and the compute cost of fine-tuning. It also introduces an anomaly-detection-based evaluation framework using ICAD and BeSTAD detectors to assess behavioral plausibility beyond aggregate distributional statistics.

## Problem
Existing LLM-based trajectory generators face a trilemma: (1) prompt-only approaches produce semantically plausible but spatiotemporally uncalibrated trajectories; (2) fine-tuned approaches (e.g., Geo-Llama/LoRA) achieve spatiotemporal fidelity but incur high compute cost and erode general reasoning; (3) tool-augmented agent paradigms lack reliable coordination between high-level behavioral planning and low-level visit-level realization—free-form autonomous tool calling is fragile over long-horizon, multi-visit daily sequences due to cascading schema errors. Additionally, standard evaluation metrics (JSD over distance/duration/transition distributions) capture population-level statistics but miss individual-level semantic defects.

## Method
**Stage 1 – Orchestrator:** An LLM (Qwen2.5-32B-Instruct) generates a daily activity-chain scaffold `C_{u,d} = [a1, …, aN]` via in-context learning over individual-conditioned exemplar chains and compact statistical summaries (activity frequencies, transition tendencies, weekday-conditioned start-time priors). A generate–verify loop enforces vocabulary membership and no-adjacent-duplicate constraints, with deterministic fallback to a sampled historical chain on failure.

**Stage 2 – Deterministic Worker Workflow (LangGraph state machine):** For each activity visit, a fixed module order executes:
1. **Location grounding:** Builds a feasible POI candidate set from personal history augmented by a top-K peer-similarity pool. Scores candidates by composite `S(p) = λf · sfreq(p) + λd · sdist(p)`, where `sdist` uses Haversine distance against individual historical transition-distance priors.
2. **Travel-time propagation:** Kinematics-aware; computes `Δt_travel = clip(dist(p_{i-1}, p_i) / v_u(a_{i-1}, a_i), Δ_min, Δ_max)` using historical mean speeds per transition type.
3. **Duration estimation:** An LLM worker conditions on current start time, remaining time budget, remaining activity sequence, and historical duration priors; outputs strict JSON `{"duration_minutes": N}`; lightweight verifier enforces `δi ∈ [δ_min, min(δ_max, budget_left)]` with retry and deterministic fallback.

**Evaluation:** Two anomaly detectors applied post-hoc treat generated trajectories as anomalies against real ones; lower AUROC/AP indicates higher behavioral fidelity (harder to distinguish from real).

## Key Contributions
- Zero-shot hierarchical orchestrator–worker agent architecture implemented as a deterministic LangGraph state machine; no parameter updates required.
- Activity-chain intermediate scaffold that decouples semantic planning from spatiotemporal realization, reducing long-horizon error accumulation.
- Peer-augmented, distance-aware POI retrieval and kinematics-aware travel-time propagation without LLM involvement in physics calculations.
- Behavior-aware evaluation framework combining ICAD (visit-level local anomaly detection) and BeSTAD (individual-level behavioral shift detection).

## Results
All metrics are JSD (lower is better) for distributional statistics; anomaly results are AUROC/AP (closer to 0.5 = better generation quality).

**NumoSim dataset vs. baselines:**
- Distance JSD: TrajGenAgent **0.0006** vs. Geo-Llama 0.0075, Geo-CETRA 0.0093, best non-LLM (Transformer) 0.0082
- G-radius JSD: **0.0993** vs. Geo-Llama 0.2361, best baseline (SeqGAN) 0.0998
- Duration JSD: **0.0155** vs. Geo-Llama 0.0028, Geo-CETRA 0.0060 (Geo-CETRA/Geo-Llama better here)
- G-rank JSD: **0.0002** vs. Geo-Llama 0.0001, Geo-CETRA 0.0002 (comparable)
- Transition Frobenius: **0.0075** vs. Geo-Llama 0.0087, best non-LLM 0.0088

**MobilitySyn dataset:**
- Distance, DailyLoc, Transition: TrajGenAgent achieves **0.0000** (perfect match)
- G-radius: **0.0051** vs. Geo-Llama 0.5528, SeqGAN 0.0738
- Geo-Llama collapses on MobilitySyn (G-radius 0.5528, Distance 0.0268), suggesting fine-tuning over-specializes to NumoSim distribution

*(Anomaly-detection AUROC/AP results table was not included in the provided text excerpt.)*

## Limitations
- Evaluation is conducted entirely on synthetic datasets (NumoSim is a benchmark simulation; MobilitySyn is author-generated); no real GPS trajectory dataset is used.
- Stage 2 peer-augmented retrieval still requires a sufficiently populated historical dataset per individual and a peer pool for similarity matching—cold-start behavior for users with sparse history is not thoroughly analyzed.
- Qwen2.5-32B-Instruct requires substantial inference-time compute (vLLM server), which may not be cheaper than LoRA fine-tuning at large scale.
- Duration estimation by LLM may still drift for highly context-dependent activities; the paper does not quantify how often verifier retries or fallbacks trigger.
- Anomaly-detection results (AUROC/AP tables) are absent from the provided text, preventing verification of the behavioral plausibility claims numerically.

## Relevance to Harnesses / Meta-Harnesses
TrajGenAgent is a canonical task-specific agent harness: a deterministic LangGraph state machine that orchestrates heterogeneous components—an LLM semantic planner, a rule-based retrieval module, a physics calculator, an LLM duration estimator, and lightweight verifiers—with explicit control flow, bounded termination, and schema-enforced fallbacks. The paper's explicit argument for deterministic workflow management over free-form tool calling (reliability, termination guarantees, control flow stability) directly articulates a core design rationale for agent harnesses over autonomous agents. The orchestrator–worker decomposition mirrors meta-harness patterns where a high-level planner delegates to specialized sub-workers with well-scoped state interfaces. The verifier-guarded fallback mechanism is a concrete instance of the harness reliability pattern (generate–verify–repair loops), and the intermediate activity-chain scaffold is an example of using a structured intermediate representation to decouple planning from execution, a recurring harness design principle.

## Tags
#agent-harness #orchestrator-worker #langgraph #deterministic-workflow #trajectory-generation #tool-augmented-agent #in-context-learning #spatiotemporal
