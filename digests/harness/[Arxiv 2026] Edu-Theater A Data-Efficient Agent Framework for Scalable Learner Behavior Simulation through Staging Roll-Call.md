---
title: "Edu-Theater: A Data-Efficient Agent Framework for Scalable Learner Behavior Simulation through Staging Roll-Call"
authors: ["Weibo Gao", "Qi Liu", "Linan Yue", "Zheng Zhang", "Yichao Du", "Fangzhou Yao", "Ao Yu", "Zhenya Huang", "Shijin Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-13"
published_time: "2026-06-13T09:48:25+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.15225"
url: "http://arxiv.org/abs/2606.15225v1"
pdf: "paper/harness/[Arxiv 2026] Edu-Theater A Data-Efficient Agent Framework for Scalable Learner Behavior Simulation through Staging Roll-Call.pdf"
---

# Edu-Theater: A Data-Efficient Agent Framework for Scalable Learner Behavior Simulation through Staging Roll-Call

*🕒 **Published (v1):** 2026-06-13 09:48 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.15225v1)*

## TL;DR
Edu-Theater is an LLM-powered multi-agent framework that simulates learner behavior in educational settings using a cohort-aware "roll-call" paradigm instead of per-learner private tutoring. A central teacher agent clusters learners into cohorts, builds population-level priors, then refines individual states via a small number of retrospective log queries, dramatically reducing LLM calls and data requirements while matching or exceeding existing simulators' accuracy.

## Problem
Existing learner simulators pair one agent per learner and replay dense interaction histories to infer latent knowledge states — this is data-intensive, computation-intensive, and brittle under cold-start (sparse history) conditions. There is no mechanism to exploit group-level regularities across learners with similar histories.

## Method
Three-stage pipeline ("theatrical" abstraction):

**Stage I — Casting:** Learners are embedded via task-wise status encoding and clustered into K cohorts. Each cohort gets a dedicated teacher agent sharing parameters but with an independent memory state.

**Stage II — Rehearsal (two acts):**
- *Act I (Whole-class diagnosis):* A coverage-based probe set E^cov is constructed (p tasks per knowledge concept). The teacher agent queries each learner's static log database retrospectively, aggregates cohort-level interaction summaries into cohort memory M_k via LLM, and fine-tunes a NeuralCD cognitive diagnosis model on the retrieved records.
- *Act II (Individualized informative probing):* Over R rounds, for each learner the teacher computes disagreement D_u(c) between its own mastery estimate µ̃_u(c) and the NeuralCD estimate µ_u(c), plus ambiguity U_u(c) = µ_u(c)(1 − µ_u(c)). The highest-scoring task is selected (score = Σ_c [D_u(c) + U_u(c)]), its historical record retrieved, cohort memory updated, and — if warranted — the learner reassigned to another cohort via cross-teacher broadcast.

**Stage III — Final Performance:** The teacher generates simulated responses conditioning on target task, cohort memory, learner interaction history, and NeuralCD mastery estimates. Learners remain passive log databases throughout.

Total LLM invocations: K(R+1), vs. O(|U|·T_avg²/2) for individual-centric baselines.

## Key Contributions
- Cohort-aware roll-call simulation paradigm that treats learner groups as informative priors, reducing reliance on dense per-learner histories
- Edu-Theater framework: teacher-as-orchestrator architecture with learners as indexed static log databases (not full agents), plus NeuralCD and a task retriever as auxiliary "props"
- Discrepancy-driven probing rule that combines teacher–diagnostic disagreement with diagnostic uncertainty to select maximally informative retrospective queries
- Cross-cohort discussion mechanism: teacher agents exchange cohort summaries and vote on learner reassignment
- Demonstrated downstream utility: synthetic data from Edu-Theater improves IRT-based Computerized Adaptive Testing (CAT) F1 by up to +3.27 points

## Results
- **Data-available scenario (DBE-KT22, correctness ACC):** Edu-Theater (GPT-4.1-mini) 73.03% vs. Agent4Edu (GPT-4.1-mini) 71.30%, EduAgent (GPT-4.1-mini) 69.95%; best supervised baseline (EERNN) 69.32%
- **Cold-start (0% history):** Edu-Theater (Llama3-8b) 66.50% vs. Agent4Edu 65.83%, EduAgent 63.25%; supervised models inoperable
- **Monetary cost (DBE-KT22, GPT-4.1-mini):** Edu-Theater $39.3 vs. Agent4Edu $59.0, EduAgent $44.7; wall-clock 4h24m vs. 6h55m and 4h53m
- **Data efficiency:** uses only 63.4% (DBE-KT22) / 69.5% (EduHS) of available data at rehearsal vs. 100% for baselines
- **CAT downstream (DBE-KT22, test length 5):** KLI F1 +3.27, FSI +1.54, MAAT +1.31 after augmenting with Edu-Theater synthetic data
- **Ablation:** removing Casting or Act II causes the largest accuracy drops; inter-cohort discussion contributes marginally

## Limitations
- Learner representations (task-wise status encoding) are high-dimensional and sparse; LLM-summary fallback for logs-unavailable case is noted but not deeply evaluated
- Cross-cohort reassignment is local (first better cohort found), not globally optimal; exhaustive search would incur prohibitive token cost
- K, p, R are dataset-specific hyperparameters requiring tuning
- Evaluated only on multiple-choice exercise datasets; generalizability to open-ended or sequential skill tasks is unvalidated
- EduHS dataset is not yet publicly released (pending acceptance)
- Monetary/time savings depend heavily on Tavg (sequence length); advantage narrows for learners with short histories

## Relevance to Harnesses / Meta-Harnesses
Edu-Theater is a concrete multi-agent harness with a fixed three-stage pipeline, typed roles (teacher agent, log-database learner, NeuralCD prop, task retriever), and explicit inter-agent communication protocols (cross-cohort broadcast and binary reassignment vote). The structured separation of orchestration phases — cohort construction, iterative diagnostic refinement, and final generation — mirrors the phase/stage model common in meta-harnesses, where a coordinator agent manages sub-agent lifecycles and information flow. The discrepancy-driven probing loop (compare two assessors → select query → update shared memory → repeat) is an instance of the adversarial-verify-and-refine pattern used in research and review harnesses. For practitioners building harnesses, this paper offers a worked example of how to bound LLM invocations via population priors and budget-limited iterative probing rather than dense per-instance replay.

## Tags
#multi-agent #orchestration #educational-ai #llm-agent #simulation #data-efficiency #pipeline #benchmark
