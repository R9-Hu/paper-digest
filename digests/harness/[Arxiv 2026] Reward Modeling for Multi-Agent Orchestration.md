---
title: "Reward Modeling for Multi-Agent Orchestration"
authors: ["King Yeung Tsang", "Zihao Zhao", "Vishal Venkataramani", "Haizhou Shi", "Zixuan Ke", "Semih Yavuz", "Shafiq Joty", "Hao Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T17:16:24+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13598"
url: "http://arxiv.org/abs/2606.13598v1"
pdf: "paper/harness/[Arxiv 2026] Reward Modeling for Multi-Agent Orchestration.pdf"
---

# Reward Modeling for Multi-Agent Orchestration

*🕒 **Published (v1):** 2026-06-11 17:16 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13598v1)*

## TL;DR
Orch-RM is a self-supervised Bradley-Terry reward model trained on intermediate orchestration artifacts from multi-agent LLM systems, enabling quality scoring of orchestration plans without executing sub-agents. It improves MAS test-time scaling and orchestrator training efficiency by up to 10–46× in token usage while achieving up to 8% accuracy gains over baselines.

## Problem
Training LLM-based orchestrators for Multi-Agent Systems (MAS) requires either expensive human annotations or exhaustive sub-agent rollouts for every training signal. Existing frameworks (e.g., MAS-Orchestra with GRPO) consume over 1B tokens for 100 update steps because reward signals are only available after full trajectory execution. Standard single-agent reward models also fail on MAS due to dynamic role-switching and out-of-distribution conversational structure.

## Method
Orch-RM constructs pairwise orchestration preferences from two self-supervised sources: (1) **specialized-over-base** pairs comparing trained orchestrator πθ outputs against base model π0 outputs, and (2) **correct-over-incorrect** pairs drawn from MAS-Orchestra training logs labeled by final answer correctness. These are mixed at a 3:1 ratio and used to fine-tune a Bradley-Terry reward model (initialized from Skywork-Reward-LLaMA-3.1-8B). The reward model rϕ(x, z) scores orchestration plans z directly — before any sub-agent execution — enabling two downstream applications: (i) Best-of-N selection at inference time by scoring N parallel orchestration samples and running sub-agents only on the winner, and (ii) reward-guided GRPO orchestrator training using normalized advantages computed from Orch-RM scores instead of sparse final-answer rewards.

## Key Contributions
- Orch-RM framework: self-supervised reward model operating at the orchestration level, eliminating the need for human annotations or sub-agent rollouts during scoring.
- Two complementary preference data sources (specialized-over-base, correct-over-incorrect) with ablation showing a 3:1 mix is optimal.
- Integration into MAS test-time scaling via Best-of-N and weighted BoN at the orchestration level.
- Integration into orchestrator training (from scratch and continued) using Orch-RM as the GRPO reward signal.
- Demonstrated that orchestration-level supervision alone can train a competitive orchestrator from scratch (61.67% vs. 63.33% MAS-Orchestra on AIME 24&25 majority vote).

## Results
- **Test-time scaling (AIME 24&25):** Orch-RM Best-of-8 achieves 68.33% accuracy vs. 63.33% majority vote baseline, using 2.38M verification tokens vs. 142.80M for trajectory-level GPT-5-mini judge (17.4% relative gain in accuracy, ~60× token reduction vs. trajectory-level judge).
- **Test-time scaling (BrowseComp+):** 14.00% accuracy, surpassing trajectory-level GPT-5-mini (12.50%) while using 8.26M vs. 142.80M tokens (~17× reduction).
- **Continued orchestrator training (AIME 24&25):** Orch-RM reaches 68.33% majority-vote accuracy vs. 63.33% for MAS-Orchestra baseline, using ~10× fewer training tokens than trajectory-level GRPO.
- **Continued orchestrator training (BrowseComp+):** 11.00% majority-vote accuracy (vs. 9.50% baseline) using ~46× fewer tokens than GRPO.
- **Training from scratch:** Orch-RM lifts base model from 23.33% to 61.67% on AIME 24&25 majority vote, approaching MAS-Orchestra (63.33%) without trajectory-level RL.
- Gains are smaller on HotpotQA and GPQA, where orchestration diversity is limited and orchestration-level discrimination is less effective.

## Limitations
- Reward model quality is bounded by the diversity and quality of available orchestrator checkpoints and sampled trajectories; scaling to larger, more diverse datasets is unresolved.
- Orch-RM is trained domain-specifically; cross-domain or multi-task orchestration reward modeling is unexplored.
- Effectiveness degrades when MAS orchestrations are structurally homogeneous (e.g., HotpotQA), where orchestration-level discrimination provides little signal.
- Depends on access to intermediate training artifacts from a pretrained MAS-Orchestra model, limiting cold-start applicability.

## Relevance to Harnesses / Meta-Harnesses
Orch-RM is directly relevant as a learned meta-level scoring component for multi-agent harnesses: it shows that a reward model operating at the orchestration plan level — above individual agent calls — can replace costly full-trajectory execution as the supervisory signal. For meta-harness designers, this establishes that plan selection (which sub-agent topology to dispatch) can be learned and reused across queries without re-running the full pipeline. The Best-of-N orchestration selection pattern maps cleanly onto harness-level routing decisions, and the self-supervised data construction from intermediate artifacts suggests meta-harnesses can bootstrap their own quality signals from execution logs rather than requiring external oracles.

## Tags
#multi-agent #reward-modeling #orchestration #test-time-scaling #self-supervised #grpo #mas #llm-training
