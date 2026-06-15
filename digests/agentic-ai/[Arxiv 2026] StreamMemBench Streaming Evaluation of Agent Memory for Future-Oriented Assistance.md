---
title: "StreamMemBench: Streaming Evaluation of Agent Memory for Future-Oriented Assistance"
authors: ["Guanming Liu", "Yuqi Ren", "Hansu Gu", "Peng Zhang", "Weihang Wang", "Jiahao Liu", "Ning Gu", "Tun Lu"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14571"
url: "http://arxiv.org/abs/2606.14571v1"
pdf: "paper/agentic-ai/[Arxiv 2026] StreamMemBench Streaming Evaluation of Agent Memory for Future-Oriented Assistance.pdf"
---

# StreamMemBench: Streaming Evaluation of Agent Memory for Future-Oriented Assistance

## TL;DR
StreamMemBench is a streaming benchmark that evaluates whether personal-agent memory systems can translate egocentric observations and interaction feedback into future-oriented assistance — not just storage. Built on the EgoLife lifelog dataset, it exposes a systematic gap: current memory systems often retain evidence but fail to use it in tasks or consolidate feedback for later reuse.

## Problem
Existing memory benchmarks test dialogue recall or task improvement in isolation using scripted/synthetic dialogues, bypassing the core streaming challenge: identifying what matters from continuous egocentric observations and applying it to a future task without being explicitly prompted. Neither evidence use (grounding responses in observed facts) nor experience reuse (generalizing from user feedback to future similar tasks) is evaluated end-to-end with traceable, verifiable evidence.

## Method
StreamMemBench constructs evaluation around **evidence anchors** extracted from EgoLife's 7-day continuous egocentric video streams (3,347 five-minute segments, ~200 timestamped observations each). An anchor agent (`A_anchor`) extracts one piece of user-specific evidence per segment and pairs it with two downstream queries (T1, T2) sharing the same anchor but testing different application scenarios. A review agent (`A_review`) enforces three constraints: Leak=0 (query does not reveal the evidence), Need=1 (correct answer requires the evidence), Natural=1 (plausible personal-assistant request).

Evaluation runs each memory system chronologically through the stream prefix up to the anchor segment, then executes a fixed trajectory: T1 → R1 → feedback F → post-feedback response RF → memory commit Φ → T2 → R2. Four metrics are scored:
- **Fidelity** (`Fid_k`): evidence preserved in memory delta after ingestion (process-level)
- **IEU** (Initial Evidence Use): R1 uses anchor evidence (task-level)
- **FI** (Feedback Incorporation): RF incorporates corrective feedback (task-level, correction cases only)
- **FUR** (Follow-up Reuse): R2 reuses evidence/experience from initial interaction (task-level)

Eight systems are evaluated: RAGraw, RAGext, Mem0, EverMemOS, A-Mem, MemOS, MemoryOS, MemSkill, across DeepSeek-V4-Flash and Gemini-3-Flash backbones.

## Key Contributions
- StreamMemBench: a streaming benchmark with 8,107 evidence anchors and 16,214 queries grounded in real egocentric lifelogs, covering task assignment, activity planning, social communication, and other natural assistance types
- A four-metric evaluation trajectory (Fidelity → IEU → FI → FUR) that traces evidence from first observation to task behavior, localizing where failure occurs
- A lifecycle failure taxonomy with five mutually exclusive labels: formation failure, initial evidence use failure, feedback incorporation failure, correction consolidation failure, evidence-use persistence failure
- Empirical evaluation showing that high Fidelity does not imply high IEU or FUR, and high FI does not imply high FUR, across all eight tested systems

## Results
(DeepSeek-V4-Flash / Gemini-3-Flash)

- **RAGraw**: Fidelity 100%† / 100%†, IEU 27.95% / 41.98%, FUR 60.96% / 43.96% — evidence accessible but increasingly unused in initial response as stream grows
- **A-Mem**: Fidelity 100%†, IEU ~35% / 30%, FUR ~65% / 56% — among strongest on FUR despite high token cost (38.57k tokens/segment)
- **MemOS**: Fidelity 67.97% / 39.51%, IEU 2.94% / 3.96%, FUR 3.96% / 5.97%, FI 77.25% / 68.83% — dominated by correction consolidation failure; high FI does not carry into FUR
- **MemoryOS**: Fidelity 100%†, IEU 23.93% / 35.94%, FUR 61.95% / 53.96%
- **MemSkill**: lowest IEU (18.94% / 13.96%) across systems; procedural memory design poorly suited to evidence-grounded personal assistance
- Temporal drift: RAGraw's IEU falls steadily from early to late stream anchors despite flat Fidelity; Mem0 shows stable IEU/FI but weakening FUR on late anchors
- Human audit on N=100 anchors: T1 plausibility 90.0%, feedback plausibility 93.5%; Cohen's κ=0.336 (T1) and κ=0.424 (F)

## Limitations
- Evaluates 8 representative systems; does not cover the full space of commercial or research memory agents
- Benchmark scope limited to EgoLife; not tested on longer streams or other egocentric datasets
- FI is only computed on correction cases (where R1 fails), not confirmation cases
- Inter-annotator agreement for human audit is moderate (κ < 0.5), suggesting plausibility judgments have some subjectivity
- Privacy risks inherent in egocentric lifelog benchmarks; deployment implications for persistent memory systems not addressed in the benchmark itself

## Relevance to Agentic AI / LLM Agents
StreamMemBench directly addresses a critical open problem in personal LLM agents: that storing memory is necessary but not sufficient for useful future behavior. The benchmark's four-metric trajectory (Fidelity → IEU → FI → FUR) provides a diagnostic framework that the community can use to identify where specific memory architectures break down — storage, retrieval, feedback consolidation, or cross-session reuse. The finding that FI ≫ FUR (systems can correct locally but not generalize) is a concrete, actionable failure mode for agent memory designers. For researchers building agentic systems with long-horizon memory (RAG, hierarchical consolidation, procedural memory), this benchmark establishes a more demanding and ecologically valid evaluation target than existing dialogue-recall benchmarks.

## Tags
#benchmark #agent-memory #long-term-memory #egocentric #streaming #personal-agent #retrieval-augmented #evaluation
