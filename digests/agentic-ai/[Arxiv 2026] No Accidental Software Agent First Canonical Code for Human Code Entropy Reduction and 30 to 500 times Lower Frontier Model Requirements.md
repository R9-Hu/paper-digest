---
title: "No Accidental Software Agent First Canonical Code for Human Code Entropy Reduction and 30 to 500 times Lower Frontier Model Requirements"
authors: ["Jepson Taylor"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14357"
url: "http://arxiv.org/abs/2606.14357v1"
pdf: "paper/agentic-ai/[Arxiv 2026] No Accidental Software Agent First Canonical Code for Human Code Entropy Reduction and 30 to 500 times Lower Frontier Model Requirements.pdf"
---

# No Accidental Software Agent First Canonical Code for Human Code Entropy Reduction and 30 to 500 times Lower Frontier Model Requirements

## TL;DR
Raw human code repositories force LLM coding agents to spend training and inference budget on "accidental representation" — framework churn, naming drift, CI dialects, and duplicated encodings of identical behavior — rather than on verified software change. This paper proposes "agent-first canonical code": a governed, proof-carrying substrate that collapses behavior-equivalent encodings into canonical representatives, with hypothesized 30×–150× training-token efficiency gains (central estimate). All headline efficiency ranges are explicitly labeled hypotheses, not measured frontier results; only preliminary QLoRA learnability evidence is reported.

## Problem
Frontier coding models train on human software archives built for humans, not agents. The archives mix durable behavioral content (product judgment, incident scars, edge cases, migration history) with accidental representation (language fashion, framework drift, folder folklore, naming inconsistency, CI dialect heterogeneity, copy-pasted generated artifacts). A coding agent pays this "accidental representation tax" four times: during pretraining, during context gathering, during reasoning/tool/retry loops, and during human review. The result is "agent sprawl": the model becomes a repository cartographer, build engineer, and migration archaeologist before it can safely edit behavior. Existing remedies — larger context windows, deduplication, synthetic tasks, more data curation — address surface symptoms but leave the underlying distribution wrong.

## Method
The core theoretical move is **behavior-equivalence quotienting**: define an oracle O (tests, contracts, traces, security policies, migration replay) and the equivalence relation p₁ ~O p₂ ⟺ O(p₁) = O(p₂). A raw corpus samples many syntactic representatives from the same behavior class (Python/FastAPI, Java/Spring, Go/Gin, etc.). Rather than training on the full orbit, the proposal is to learn a canonical normal-form map κ: [p]O → (s, e, r, d) where s is the shortest accepted canonical specification, e is the evidence bundle, r is the renderer/generator, and d is the disposition ledger for non-preserved behaviors, legal risk, and security defects.

This yields a set of structured substrate objects: **canonical profiles** (versioned limited-stack product profiles with enforced file grammar, named ownership roles, and generated boundaries), **behavior cells** (versioned proof-carrying primitives with interface, tests, migration obligations, and repair memories), **semantic patch cells** (typed change archetypes), **proof lanes** (standard validation routes with exact commands and acceptance rules), **constrained edit grammars** (machine-checkable legal file/edit/migration/dependency operations), **reasoning digests** (compact repository knowledge summaries), and **proof-carrying change objects** (structured accepted-patch bundles). The theoretical compression objective is **Minimum Functional Description Length (MFDL)**: the shortest canonical specification + evidence bundle + renderer that satisfies the declared oracle.

Preliminary evidence: QLoRA fine-tuning of Qwen2.5-Coder-14B on 64,088 canonically translated trajectories shows convergence and suppression of forbidden-language markers. This does not establish behavior preservation, scaling economics, or verified-change cost.

The decisive falsification test is a **same-model paired ablation**: identical model, same issue lineage, same hidden tests, same reviewer rubric, on a raw repository versus its canonical port — measuring files opened, planning tokens, tool calls, failed repair loops, and dollars per accepted change.

## Key Contributions
- Formalization of **human-code entropy** as conditional representational uncertainty given behavior, contracts, and environment (H_human = H(representation | behavior, contracts, environment)), and the **Accidental Representation Tax** (ART = log|E_{y,τ}| − log|C_{y,τ}|)
- **Correct-change information theory**: mutual information preservation condition I(Φ(x); Δ | i, O) ≈ I(x; Δ | i, O) with H(Φ(x) | Δ, i, O) ≪ H(x | Δ, i, O) as the canonical map's learning-theoretic justification
- Fourteen distinct efficiency ratio denominators (R_source, R_entropy, R_action, R_train, R_cost, etc.), with explicit prohibition on multiplying them
- **MFDL** as the theoretical compression floor — the product-software analogue of Minimum Description Length
- Agent-first canonical profile architecture (versioned 2026 P²⁰²⁶_app) with nine explicit assumptions each paired with falsification criteria
- Front-door measurement ledger with primary denominators, first tests, and failure modes for each claim
- Preliminary QLoRA evidence of trajectory learnability on 64K canonical examples

## Results
All efficiency ranges are **reported as hypotheses, not measured frontier results**; the paper is explicit that they must not be multiplied.

- **Training-token efficiency (R_train)**: conservative 10×–30×; central 30×–150×; aggressive 150×–1,000×
- **Context/reasoning/tool/retry tokens per verified change (R_reason, R_retry)**: conservative 3×–10×; central 10×–100×; aggressive 100×–10,000×
- **Cost per verified correct change (R_cost)**: conservative 3×–10×; central 10×–50×; aggressive 50×–1,000×
- **Dense-active serving speed**: conservative 3×–5×; central 8.3×–10×; aggressive 10×–20×
- **Action/representation space (R_action)**: conservative 10×–40×; central 40×–150×; aggressive 100×–300×
- **Dense-active infrastructure cost/token**: conservative 67%–80% lower; central 88%–90% lower
- **Preliminary measured**: 64,088 QLoRA trajectories converge; zero measured forbidden-language markers. Behavior preservation, scaling economics, and verified-change cost are **not established**

## Limitations
- All headline efficiency figures are theoretical hypotheses with no paired raw/canonical frontier measurement
- Preliminary QLoRA evidence establishes only learnability and forbidden-language suppression on a small trajectory set — explicitly not behavior preservation or cost reduction
- The decisive same-model paired ablation experiment has not been run
- Foundry amortization costs (porting, provenance, governance, verification infrastructure) are not measured and could consume efficiency gains
- Scope is deliberately narrow: the primary profile targets web/SaaS/backend/product applications; kernels, compilers, GPU code, embedded, and HPC are excluded or deferred to secondary profiles
- Behavior preservation under canonical porting is asserted as a design goal but not empirically validated
- The oracle O (tests, traces, contracts) may itself be incomplete or misspecified, causing silent behavior loss during porting
- The theoretical framework assumes behavior-equivalence classes are well-defined and tractable to compute; realistic software has partial observability and undecidable equivalences

## Relevance to Agentic AI / LLM Agents
This paper addresses a structural inefficiency that affects every LLM-based coding agent: the mismatch between the training/inference substrate (raw human repositories) and what agents actually need (unambiguous behavioral primitives with constrained legal edit surfaces). The concepts of "agent sprawl" and the "accidental representation tax" give precise names to why agents on SWE-bench and similar benchmarks expend large token budgets on repository archaeology rather than behavior change, which connects directly to resource-constrained agent evaluation work. The proposed constrained edit grammars, proof lanes, and reasoning digests would, if validated, reduce both the branching factor during agent planning and the failure rate of repair loops — the two largest drivers of per-task token cost in agentic coding pipelines. The falsification-first framing (nine explicit assumptions with measurement tests) is methodologically sound and provides a roadmap for the community to verify or refute claims, making this a substantive research program proposal rather than benchmark-chasing.

## Tags
#code-agents #training-efficiency #canonical-code #software-engineering #data-curation #agent-infrastructure #llm-efficiency #agentic-coding
