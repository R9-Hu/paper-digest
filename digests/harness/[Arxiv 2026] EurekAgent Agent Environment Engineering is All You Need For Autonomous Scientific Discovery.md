---
title: "EurekAgent: Agent Environment Engineering is All You Need For Autonomous Scientific Discovery"
authors: ["Amy Xin", "Jiening Siow", "Junjie Wang", "Zijun Yao", "Fanjin Zhang", "Jian Song", "Lei Hou", "Juanzi Li"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T17:56:35+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13662"
url: "http://arxiv.org/abs/2606.13662v2"
pdf: "paper/harness/[Arxiv 2026] EurekAgent Agent Environment Engineering is All You Need For Autonomous Scientific Discovery.pdf"
---

# EurekAgent: Agent Environment Engineering is All You Need For Autonomous Scientific Discovery

*🕒 **Published (v1):** 2026-06-11 17:56 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.13662v2)*

## TL;DR
EurekAgent reframes autonomous scientific discovery as an *environment engineering* problem rather than a workflow-prescription problem, arguing that as general-purpose CLI agents (e.g., Claude Code) grow more capable, the binding constraint is the surrounding environment—its permissions, artifacts, budgets, and oversight interfaces. The system coordinates off-the-shelf CLI agents through a prepare→propose→implement loop with four environment engineering layers, achieving new state-of-the-art results across mathematics, kernel engineering, and ML engineering benchmarks.

## Problem
Existing autonomous research systems encode fixed, domain-specific agentic workflows (evolutionary search, solution trees, debate modules), but evidence shows that strong general-purpose CLI agents already match or exceed these when given clear tasks and metrics. The gap is *reliability*: unconstrained agents reward-hack evaluators, contaminate result files, consume unbounded compute, and produce non-reproducible artifacts. No prior system treats the environment itself—evaluation integrity, shared memory, resource limits, human oversight—as the primary design object.

## Method
EurekAgent engineers the agent environment along four orthogonal dimensions, while leaving the agent's internal research strategy entirely unconstrained:

1. **Permissions Engineering**: Docker-containerized runs; hidden evaluator exposed only through a secure grading service (agents submit, receive scores, cannot inspect or modify grader); read-only controller-owned result files enforced via filesystem hooks; same-round isolation prevents parallel sessions from copying each other; GPU access gated through a helper API with exclusive-lock semantics.

2. **Artifact Engineering**: Filesystem + Git as shared long-term memory. Stage deliverables (prep summaries, proposal manifests, ranked solution histories, web-search caches, session transcripts) persist under a run directory. Agents write structured Git commits describing both the standalone solution and the delta from the prior version.

3. **Budget Engineering**: Separate wall-clock time limits for proposal and implementation sessions (`t_propose`, `t_implement`). Agents query a time-checker helper API (active awareness) and receive injected deadline warnings when deliverables are missing (passive). API cost is tracked globally; when the limit is hit the run aborts and preserves the workspace. Interrupted runs resume from filesystem state under remaining budget.

4. **Human-in-the-Loop Engineering**: Terminal UI showing live session outputs with a chat input box; web monitor showing score-evolution curves, per-round and global-best approaches, and complete session transcripts.

The outer loop is: one Prepare stage (runtime validation, dependency setup) → R rounds of [Propose (one session reads prior artifacts + web search → generates up to P hypotheses) → Implement (P parallel sessions, each in isolated workspace, iteratively submitting to the hidden evaluator)].

## Key Contributions
- **Environment engineering framing**: articulates that as agent capability scales, the bottleneck shifts from workflow design to environment design; introduces four concrete engineering dimensions as a principled taxonomy.
- **EurekAgent system**: open-source implementation coordinating off-the-shelf CLI agents (Claude Code + GLM-5.1) with no task-specific workflow prescription.
- **New SOTA on 26-circle packing**: score 2.635999 vs. prior AI best 2.635986 (AlphaEvolve, R1-Distill-Qwen3-8B), achieved training-free for <$11 API cost.
- **New SOTA on Erdős' minimum overlap and 1st autocorrelation inequality**: beats prior AI best (gpt-oss-120b test-time training) while remaining training-free.
- **Kernel engineering SOTA**: top 4 TriMul solutions all beat prior human leaderboard top entry (2005 µs vs. 2096 µs); 10.8% improvement over TTT-Discover.
- **MLE-Bench Lite**: 85.71% any-medal rate, 71.43% gold-medal rate with open-source LLM, surpassing all baselines using commercial models.

## Results
- **Circle Packing (26 circles)**: 2.635999 (EurekAgent) vs. 2.635986 (AlphaEvolve, prev. AI best), 2.634 (prev. human best); <$11 API cost.
- **Erdős' Minimum Overlap**: 0.380870 vs. 0.380876 (prev. AI); 0.380927 (prev. human).
- **1st Autocorrelation Inequality**: 1.502861 vs. 1.502863 (prev. AI).
- **TriMul kernel**: median 2005.03 µs (EurekAgent-CUDA Graph) vs. 2096.04 µs (top human leaderboard), 2247.78 µs (TTT-Discover); top 4 EurekAgent solutions all rank above prior leaderboard submissions.
- **MLE-Bench Lite (7-task subset)**: 85.71% any-medal, 71.43% gold vs. 71.43% / 57.14% for best baseline (AIBuildAI, Claude-Opus-4.6).
- Average API cost for three math tasks: <$17; all results training-free.

## Limitations
- Evaluation scope is restricted to **metric-driven tasks with executable evaluators**; applicability to open-ended or qualitative scientific domains is undemonstrated.
- MLE-Bench evaluation uses a **curated 7-task subset** (not the full Lite split), and selects tasks by tractability estimates, which may introduce selection bias.
- TriMul results use a **local re-evaluation protocol** rather than official leaderboard submission (leaderboard was closed), so absolute scores may not be directly comparable to originally reported results.
- The system is tested with a single (Claude Code + GLM-5.1) agent configuration; sensitivity to CLI agent or base LLM choice is not ablated.
- Budget engineering aborts at cost limit without graceful partial-result handling beyond filesystem snapshot.

## Relevance to Harnesses / Meta-Harnesses
EurekAgent is a direct instance of a **meta-harness**: an outer orchestration layer that wires together multiple off-the-shelf agent sessions without modifying them internally, analogous to how meta-harnesses in software testing or ML pipelines coordinate heterogeneous workers through standardized interfaces. The four engineering dimensions—permissions, artifacts, budgets, human-in-the-loop—map cleanly onto the canonical meta-harness concerns of sandbox isolation, shared state management, resource governance, and observability. The paper's central thesis (that environment engineering, not workflow prescription, is the key design lever as agent capability scales) is highly relevant to anyone building harnesses: it argues that a well-designed harness *affords* reliable behavior rather than *prescribing* it, shifting design effort from agent prompts to environmental constraints and shared memory schemas.

## Tags
#meta-harness #agent-environment #autonomous-research #scientific-discovery #sandbox-isolation #artifact-management #budget-engineering #human-in-the-loop
