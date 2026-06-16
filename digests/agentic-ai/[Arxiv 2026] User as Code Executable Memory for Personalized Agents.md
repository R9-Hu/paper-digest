---
title: "User as Code: Executable Memory for Personalized Agents"
authors: ["Bojie Li"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T13:39:41+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16707"
url: "http://arxiv.org/abs/2606.16707v1"
pdf: "paper/agentic-ai/[Arxiv 2026] User as Code Executable Memory for Personalized Agents.pdf"
---

# User as Code: Executable Memory for Personalized Agents

*🕒 **Published (v1):** 2026-06-15 13:39 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16707v1)*

## TL;DR
User as Code (UaC) proposes representing an agent's user model as executable typed Python code rather than unstructured text, knowledge graphs, or fact stores. A two-phase pipeline (append-only fact extraction → periodic structured code generation) converts raw conversation into typed Python dataclasses plus deterministic constraint functions. This enables both competitive factual recall (78.8% on LOCOMO) and capabilities retrieval-based systems cannot support at all: aggregate inference (99% vs. 6–43% for retrieval baselines) and proactive, unsolicited safety alerts.

## Problem
Existing LLM agent memory systems (Mem0, A-MEM, MemMachine, Hindsight, knowledge graphs) store user state as text, extracted facts, or graph nodes—formats that separate *representation* from *verification*. This creates two structural failures: (1) conflicting facts coexist unresolved with no version history, and (2) aggregate queries ("how many international trips did I take last year?") and rule-based proactive alerts ("passport expires before booked departure") are structurally impossible under top-k retrieval, which only ever surfaces a handful of records at once.

## Method
UaC models the user as a self-evolving Python software project consisting of typed dataclasses (state), Python functions (constraints), and a compact manifest (always-loaded summary + `ACTIVE_ALERTS`).

**Phase 1 – Memorize (per session, append-only):** A thinking-enabled LLM (Gemini 3 Flash, budget 8192) extracts ~50–75 atomic facts per session as flat strings with resolved absolute dates, appended to a never-overwritten log. Facts are also indexed in ChromaDB alongside raw conversation chunks.

**Phase 2 – Structure (periodic, full-corpus):** A thinking-enabled LLM (budget 16384) regenerates the entire typed Python state from scratch from all accumulated facts—not incrementally edited—producing dataclass instances (`date()` fields, typed lists, `notes: list[str]` for hard-to-type facts) organized into domain packages (`travel/`, `health/`, `finance/`, …). Regenerating from the full corpus rather than editing incrementally limits information loss to 0.18% of facts.

**Retrieval uses three concatenated channels:** (1) structured code state (full `state.py`, up to 6K chars); (2) fact-vector retrieval (top-20 from ChromaDB over the fact log); (3) raw archive retrieval (top-10 session chunks). The LLM is instructed to prefer the structured channel on conflicts.

**Proactive alerts** emerge from a generate–verify–review loop: the coding agent writes Python constraints against the typed state, the interpreter executes them deterministically in a sandbox, and results are persisted in `ACTIVE_ALERTS` in the manifest, visible at session start without any user query.

## Key Contributions
- **Two-phase memory architecture** (append-only log + periodic full-corpus code regeneration), reaching 78.8% on LOCOMO (within 1.0pp of full-context upper bound; McNemar p=0.65) and 83.0% on LongMemEval (tied with MemMachine and Full Context).
- **Active Service benchmark**: 60 scenarios across 5 constraint categories—first benchmark measuring memory-triggered proactive alerts without a user query; UaC achieves 100% on 40 standard and 85% on 20 hard scenarios.
- **Analytical inference benchmark**: 100 cases, 10 record types, N∈{20,50,100,200,500} records; UaC 99% vs. MemMachine 43% and Mem0 6%; cost pays back after 3–11 repeated queries via pre-structured state.
- **Ablation suite**: append-only extraction identified as the decisive recall mechanism (+19pp over code-only baseline); two-phase separation adds +12.3pp over incremental code rewriting; modularity/progressive disclosure cuts prompt-token cost 14.9× with no accuracy loss at N=500.
- **Cross-LLM robustness**: substituting GPT-5.4 throughout yields statistical tie (p=0.82) vs. Gemini; re-judging with Claude Opus 4.7 preserves rankings (Cohen's κ ≥ 0.74).
- Open-source implementation with same-backbone comparisons against five memory systems on five benchmarks.

## Results
- **LOCOMO (n=600):** UaC 78.8% vs. Full Context 79.8% (p=0.65, tied), MemMachine 72.7% (p=0.003), Hindsight 69.7% (p=1.5×10⁻⁵), EverMemOS 55.5%, A-MEM 51.8%, Mem0 29.3%.
- **LongMemEval (n=500):** UaC 83.0%, statistically tied with MemMachine 84.8% (p=0.33) and Full Context 85.4% (p=0.19); ahead of EverMemOS 76.4% (p=0.002), Hindsight 73.0%, A-MEM 49.6%, Mem0 23.8%.
- **Analytical inference:** FC+REPL 100%, UaC 99%, Full Context (no tool) 94%, MemMachine 43%, Mem0 6%; gap widens at higher N—at N=500, UaC 95% vs. MemMachine 25%.
- **Active Service:** UaC 100% (standard 40 scenarios), 85% (hard 20 scenarios); no retrieval-based baseline reported as capable.
- **Token cost:** UaC structuring amortizes to ~15× cheaper than reloading raw records after 3–11 queries; wall time for structuring stays at 30–40s across 19–200 session corpora.
- **Cross-LLM:** UaC (GPT-5.4) 80.8% on 120-QA LOCOMO subset vs. 82.5% Gemini (p=0.82).

## Limitations
- **Input cap at ~500K characters:** cost flattens around n=100 sessions; authors acknowledge this motivates hierarchical structuring for production scale.
- **Temporal reasoning gap:** UaC lags Full Context on LongMemEval temporal-reasoning subcategory (65% vs. 74%), where extraction occasionally drops timestamps needed for multi-session date arithmetic.
- **Multi-session contiguous-span retrieval:** MemMachine outperforms UaC on multi-session (88% vs. 81%) and temporal-reasoning (69% vs. 65%) subcategories where the answer is a coherent contiguous span and contextual expansion helps.
- **Benchmarks evaluated are relatively small:** LOCOMO uses 10 conversations, and the Active Service benchmark is 60 scenarios—larger-scale user studies absent.
- **Same-backbone reimplementations may underrepresent baselines:** published SOTA numbers (e.g., EverMemOS 93.05%, Hindsight 91.4%) used stronger backbones and richer retrieval stacks; direct comparison is confounded.
- **Structured phase is LLM-driven and mildly stochastic:** fact extraction varies across runs (~1–2% variance in fact count audited).
- **No user study or real deployment data:** evaluation is entirely LLM-as-judge on benchmark conversations.

## Relevance to Agentic AI / LLM Agents
UaC directly addresses the persistent-memory problem that limits long-running personalized agents: how to accumulate, organize, and act on a growing user model across sessions without paying full-context costs every turn. The paper's core insight—that executable code is a better medium than text for agent memory because it collapses representation and verification into one interpreter-runnable artifact—connects to a broader trend in agentic AI (CodeAct, Voyager, Program-of-Thoughts) of using code as a first-class substrate for reasoning and state. The proactive alerting capability is particularly significant for agents tracking real-world obligations (health, travel, finance), since it demonstrates a memory system that initiates consequential actions rather than waiting for user queries—a core requirement for autonomous, long-horizon agents. The append-only log + periodic structured checkpoint pattern is also directly compatible with RL-based memory policy training (Memory-R1, AgeMem), making UaC an interesting foundation for future learned memory management.

## Tags
#agent-memory #personalization #executable-memory #long-term-memory #proactive-agents #code-as-representation #benchmark #rag
