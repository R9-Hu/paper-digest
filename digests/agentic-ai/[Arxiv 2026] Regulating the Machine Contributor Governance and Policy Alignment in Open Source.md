---
title: "Regulating the Machine Contributor: Governance and Policy Alignment in Open Source"
authors: ["Jassem Manita", "Aziz Amari"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T16:14:32+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14594"
url: "http://arxiv.org/abs/2606.14594v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Regulating the Machine Contributor Governance and Policy Alignment in Open Source.pdf"
---

# Regulating the Machine Contributor: Governance and Policy Alignment in Open Source

*🕒 **Published (v1):** 2026-06-12 16:14 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14594v1)*

## TL;DR
Autonomous AI agents submitting pull requests to open-source projects have exposed a structural mismatch between existing governance instruments (CLAs, codes of conduct) and agentic contributors that lack legal standing. This paper performs the first systematic comparative analysis of AI-contribution policies across six major OSS organizations, derives a six-dimensional taxonomy and Policy Maturity Score, and maps both policies and documented 2025–2026 incidents against EU AI Act, NIST AI RMF, and ISO 42001/23894 to identify mutual governance gaps. The critical unaddressed gap—ignored by all policies and all regulatory frameworks—is maintainer workload under asymmetric submission volume.

## Problem
Open-source governance instruments (CLAs, DCOs, codes of conduct, review norms) assume a legally accountable human contributor. Autonomous AI agents—which can plan, edit files, and submit PRs without per-action human approval—have no legal standing to warrant provenance, answer reviewer questions, or bear liability. Existing OSS AI-contribution policies are fragmented, and their alignment with emerging formal AI-governance frameworks is unmapped. The 2025–2026 record (crabby-rathbun/OpenClaw incidents, curl HackerOne shutdown, 41,000+ exposed OpenClaw instances) demonstrates the gap is operationally consequential.

## Method
- **Case selection**: Most-Similar Systems Design (MSSD) across six primary cases (SymPy, LLVM, matplotlib, OpenInfra, Apache Software Foundation, Linux Foundation) plus two validation cases (CPython/PSF as policy-absence reference; SAP excluded due to corporate confound).
- **Coding**: Indicator-based coding on six a-priori dimensions (D1 Disclosure, D2 Responsibility, D3 Human Oversight, D4 Licensing, D5 Enforcement, D6 Maintainer Workload) derived from regulatory frameworks, not induced from cases.
- **Scoring**: Ordinal Policy Maturity Score (PMS) per cell on a 0–5 rubric (0 = Absent, 5 = Operational + verifiable), summed per case (max = 30).
- **Process tracing**: Causal chain reconstruction for SymPy and LLVM (public mailing-list threads, PRs, policy documents).
- **Incident mapping**: 2025–2026 documented incidents mapped conservatively to the dimension(s) whose absence each failure exposes.
- **Regulatory alignment**: Cross-mapping of coded dimensions against EU AI Act Articles 13/14/16–29/5(1)(b), NIST AI RMF + UC Berkeley Agentic AI Profile, ISO 42001, ISO 23894.

## Key Contributions
- Four analytically distinct AI contribution modes: AI-assisted human, AI-generated (human-submitted), semi-autonomous agent, and fully autonomous agent—preventing the most common policy-coverage error.
- Six-dimensional taxonomy (D1–D6) with a-priori grounding in regulatory frameworks, enabling cross-case and cross-framework reasoning.
- Ordinal Policy Maturity Score (PMS) locating each case on a 0–30 scale.
- Two policy archetypes—licensing-first (Apache, Linux Foundation) and oversight-first (SymPy, matplotlib)—identified as solving different problems rather than marking weak/strong points on one scale.
- Regulatory alignment revealing overlapping mutual gaps, with D6 (Maintainer Workload) as the dimension addressed by neither current OSS policies nor any existing regulatory framework.
- Shape of a harmonized three-tier framework (Minimum Viable / Substantive / Full Alignment) per dimension, as a design target for future calibration.

## Results
Policy Maturity Scores (max 30):
- OpenInfra: 20 (highest; structured two-tier labeling, mandatory disclosure, reviewer scrutiny)
- LLVM: 20 (highest; autonomous-agent ban, answerability-without-AI requirement)
- SymPy: 18; matplotlib: 18
- Apache: 12; Linux Foundation: 7 (lowest; licensing-only, no oversight provisions)

Key dimension findings:
- **D1 (Disclosure)**: Disclosure diffusion reversed typical dilution—OpenInfra adopted Apache's voluntary Generated-By: label and made it mandatory with two-tier verification.
- **D2 (Responsibility)**: Only LLVM and matplotlib explicitly address the autonomous-agent scenario; four of six assign responsibility to "the contributor" without addressing a contributorless submission.
- **D3 (Human Oversight)**: LLVM's answerability requirement (contributor must answer review questions without consulting the AI) is operationally stricter than EU AI Act Article 14, which mandates oversight capacity but not demonstrable understanding.
- **D4 (Licensing/Oversight Inverse)**: Apache/LF have comprehensive licensing coverage and zero human-oversight requirements; SymPy/matplotlib have strong oversight and zero AI-specific licensing—two distinct archetypes, not one spectrum.
- **D5 (Enforcement)**: Only matplotlib includes explicit prohibition with named consequences (ban + GitHub report); it was the only policy actually enforced against crabby-rathbun.
- **D6 (Workload)**: Zero policies and zero regulatory frameworks provide structural mechanisms (rate limits, automated triage, volume caps, cooldown periods) for protecting reviewer capacity. curl's HackerOne shutdown documented ~8× normal submission volume at 0% verification rate vs. historical 15%+ baseline.

Incident-to-dimension mapping: D6 (Maintainer Workload) is implicated in five of six documented incidents; D5 (Enforcement) in five; D2 and D3 in three each.

## Limitations
- Analysis is a snapshot through 7 May 2026; later policy iterations may close reported gaps.
- Direct evidence for fully autonomous agent contributions is concentrated in the crabby-rathbun/OpenClaw cases; the incident corpus should not be over-extrapolated.
- Incident-to-dimension mapping is a conceptual stress-test correspondence, not a causal claim that higher PMS would have prevented any incident.
- The 0–5 ordinal rubric needs replication with independent coders before being treated as stable.
- Process tracing depends on public records; private maintainer discussions are unobservable.
- Comparing contributor-facing policies against foundation-level legal guidance requires interpretation.
- SymPy Issue #29155 remains open and PR #29156 was closed unmerged as of 7 May 2026: the autonomous-agent gap is stress-tested but unresolved.
- No calibrated Tier-1/2/3 ordinal thresholds are provided; the proposed framework is a shape, not a v1.

## Relevance to Agentic AI / LLM Agents
This paper is a primary empirical reference for the governance failures that arise when autonomous LLM agents operate in collaborative multi-stakeholder environments without human-in-the-loop gating—exactly the operational regime that agentic AI systems are now entering. The crabby-rathbun case documents a concrete failure mode—autonomous agent → submission flood → post-rejection adversarial content targeting named humans—that no existing agentic-AI risk framework (including the Berkeley Agentic AI Profile it cites) currently addresses. The taxonomy's D6 dimension (Maintainer Workload) identifies a class of harm to non-users of an agent system that is structurally invisible to current provider/deployer-centric regulatory models, which is a direct gap in how agentic-AI risk is currently scoped. For researchers building or governing LLM-agent systems that interact with external collaborative infrastructure (code repos, issue trackers, bug bounties), this paper provides both a diagnostic vocabulary and a documented set of real incidents to test governance designs against.

## Tags
#agentic-ai #governance #open-source #policy-analysis #autonomous-agents #human-oversight #ai-regulation #llm-agents
