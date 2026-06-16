---
title: "When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime"
authors: ["Wei Wu"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T16:06:55+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14589"
url: "http://arxiv.org/abs/2606.14589v1"
pdf: "paper/agentic-ai/[Arxiv 2026] When Errors Become Narratives A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime.pdf"
---

# When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime

*🕒 **Published (v1):** 2026-06-12 16:06 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14589v1)*

## TL;DR
This paper presents a longitudinal empirical study of 22 production incidents in a continuously running personal-assistant LLM agent runtime, deriving a five-class mechanism-oriented taxonomy of silent failures. The central novel contribution is the "fail-plausible" failure mode (Class D): LLMs actively transform internal errors into fluent, plausible false output delivered to the user rather than signaling failure. Cross-cutting findings show that ~70% of silent failures were caught by a human reading pushed output, not by 4,286 unit tests or 827 governance checks.

## Problem
LLM agent runtimes inherit gray failure (differential observability where the application suffers but automated observers stay green) from distributed systems—but add a strictly worse variant: the system does not merely hide errors, it narrates them. Existing taxonomies (MAST, provider-side incident studies) cover benchmark-trace failures or infrastructure-layer outages; none address longitudinal production silent failures with multi-week latency, discovery-channel distribution, or the LLM-specific fabrication failure class. There is no empirical account of how defenses must evolve under real recurrence pressure.

## Method
Single-system longitudinal case study of `openclaw-model-bridge`, a three-plane agent runtime (control, capability, memory planes) in continuous production on macOS since March 2026 (~40 scheduled jobs, 8 LLM providers, 4,286 unit tests, 827 declarative governance checks). The corpus is 22 incidents over 2026-04-09 to 2026-06-02 meeting three criteria: reached production, had a silent phase while automated indicators stayed green, and received a full postmortem under a mandatory "exception-analysis constitution" requiring causal-chain diagrams, three-layer root cause (trigger/amplifier/concealer), per-minute timeline reconstruction, and condition-combination analysis. Taxonomy was constructed mechanism-first (how the error evaded observation, not which file failed), iteratively stabilized after 9 consecutive incidents without a class split.

## Key Contributions
- **Five-class mechanism taxonomy**: (A) environment/platform quirks, (B) design-assumption mismatches, (C) error swallowing and dilution, (D) chained hallucination and fabrication, (E) operational omission and forensic blind spots—derived from 22 fully postmortem'd incidents with a single meta-pattern manifesting ≥28 times.
- **Fail-plausible failure class** (Class D): four documented production incidents where LLMs converted polluted context (error logs captured by command substitution, stale alerts in chat history, unlabeled context injection) into confident fabricated output—fabricated platform crises, OS remediation instructions, software releases, and review content—with all detectors green.
- **Systems reframing of hallucination**: in all 4 Class D incidents the model behaved correctly; the fault was system-side context pollution (stderr/stdout conflation, alert/conversation context mixing, provenance-free enrichment), making the defense system-side hygiene rather than model-side mitigation.
- **Quantified cross-cutting findings**: ~70% discovery via human user-view; unit tests ≈0% for this failure class; incident latency 13 hours–60 days correlating with mechanism layer not code complexity; audit ex-ante prevention 0/15 but ex-post regression blocking 13/15 (87%).
- **Defense maturation path**: point fix → meta-rule → mechanized scanner; every meta-rule that reached the scanner step has zero recorded recurrences; every recurrence traces to a lesson that stopped at step 1.
- **Complexity argument**: longest-latency failures live in seams (deployment topology, cross-script contracts, observer–observed coupling), motivating a "Sunset Law" prioritizing complexity retirement over defense accretion.

## Results
- 22 incidents, ≥28 silent-failure manifestations across 8 weeks; taxonomy stable over last 9 incidents
- Incident latency range: 13 hours to 60 days; latency tracks mechanism layer, not code complexity
- Discovery channel: ~70% human user-view; target-environment execution catches all Class A; unit tests/preflight ≈0% for this corpus by selection
- Audit retrospective (15 incidents): ex-ante prevention 0% (0/15), partial early warning 13% (2/15), ex-post regression blocking 87% (13/15), root cause of misses was "blank category" (unconceived dimension) in 80% (12/15) of cases
- Adversarial audit: 16/16 destruction scenarios detected after blind-spot remediation (10 replaying known incidents, 6 probing suspected blind spots)
- 23 meta-rules and 14 mechanized scanners by study end; 0 recorded recurrences for any lesson that reached the scanner step
- LLM observer self-audit: found real regressions including a fabrication and two bugs in itself, but also shipped with a Class B path bug and a sampling artifact causing hallucinated truncation

## Limitations
- Single-system case study; no independent annotators for taxonomy classification (author + AI collaborator only; no inter-annotator agreement reported)
- Surviving-silence bias: incidents still silent at study cutoff are by construction absent from the corpus
- 8-week window; the system has been in production only since March 2026
- The system is self-hosted on a single macOS machine with one human operator; generalizability to multi-operator, multi-host, or multi-tenant deployments is unverified
- The AI engineering collaborator (Claude) co-wrote incident postmortems and co-implemented defenses, creating a potential observer–observed coupling in the study methodology itself (acknowledged as a finding in §7)
- Prompt anti-fabrication guards are the last layer and not claimed sufficient; no controlled ablation separates the contribution of individual defense layers

## Relevance to Agentic AI / LLM Agents
This paper is directly foundational for anyone building or operating LLM agent systems in production: it is the first longitudinal taxonomy of silent failures specific to the agent runtime layer, and the fail-plausible class is a novel, dangerous failure mode with no analog in prior reliability literature. The trigger–amplifier–concealer decomposition offers a practical postmortem framework that generalizes beyond the studied system, and the empirical finding that user-view observation dramatically outperforms automated testing for this failure class should reset assumptions about observability stack design. The defense patterns (stderr discipline as the single load-bearing fix for a fabrication chain, declared-state convergence engines, reserved-file unwritability for LLM tool paths) are directly actionable for agent framework developers.

## Tags
#llm-agents #reliability #silent-failures #hallucination #production-systems #observability #fail-plausible #agent-runtime
