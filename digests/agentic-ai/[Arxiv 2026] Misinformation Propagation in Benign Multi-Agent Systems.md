---
title: "Misinformation Propagation in Benign Multi-Agent Systems"
authors: ["Jonas Becker", "Jan Philip Wahle", "Terry Ruas", "Bela Gipp"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T13:40:01+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16710"
url: "http://arxiv.org/abs/2606.16710v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Misinformation Propagation in Benign Multi-Agent Systems.pdf"
---

# Misinformation Propagation in Benign Multi-Agent Systems

*🕒 **Published (v1):** 2026-06-15 13:40 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16710v1)*

## TL;DR
This paper studies how contextual misinformation injected into one or more agents propagates through fully benign multi-agent debate (MAD) systems, degrading task accuracy. Multi-agent debate partially mitigates the harm relative to single-agent prompting, but robustness depends critically on group composition (ratio of informed to misinformed agents) and the decision protocol (voting vs. consensus).

## Problem
Prior work on misinformation in LLM systems either studies isolated single models or adversarial/malicious multi-agent settings where agents intentionally deceive. The effect of contextual misinformation on *benign* MAD—where all agents follow the protocol honestly but some receive misleading context—is underexplored. This gap matters because real deployments encounter misinformation from RAG, web search, and hallucinations, not only from adversarial agents.

## Method
The authors inject LLM-generated, intent-tagged misinformation into a subset of agents participating in turn-based multi-agent debate using the MALLM framework (3–5 agents, 5 turns). Misinformation is appended to the prompt as ostensibly genuine context; agents are not told it may be false. Three factors are varied: (1) misinformation relevance (task-relevant vs. irrelevant), (2) group composition (0–5 misinformed agents out of 5), and (3) decision protocol (consensus vs. majority voting). Tasks span reasoning (WinoGrande), factual knowledge (Complex Web Questions), and ethical alignment (Ethics benchmark). They also construct and release **MINT** (Misinformation INTents): 10,278 LLM-generated misinformation texts across nine intent categories (neutral, clickbait, hoax, rumor, satire, propaganda, framing, conspiracy, other) aligned to 1,142 task samples. Models evaluated: Llama-3.3-70B-Instruct and GLM-4.7-Flash.

## Key Contributions
- Controlled study of contextual misinformation propagation in fully benign MAD, isolating it from adversarial manipulation or defense mechanisms.
- Quantified comparison of single-agent vs. multi-agent robustness: MAD degrades −2.2% to −10.3% under misinformation vs. −12.9% to −17.2% for single agents.
- Analysis of opinion persistence across turns by misinformation category (hoaxes and unconstrained "other" most persistent; framing and rumors least persistent for Llama-3.3).
- Analysis of group composition effects: misinformed-agent self-correction jumps from 8.0% with 2 uninformed agents to 20.5% with 3, revealing a majority-threshold effect.
- Release of MINT dataset (HuggingFace: `jonasbecker/MINT`) and all experimental code.

## Results
- **Single-agent accuracy drop (Llama-3.3):** −26.75% on CWQ, −25.71% on Ethics, −19.51% on WinoGrande under relevant misinformation; irrelevant misinformation causes −12.96%, −0.45%, +0.68% respectively.
- **Multi-agent vs. single-agent degradation:** MAD reduces misinformation-induced accuracy drop to −2.2%–−10.3% vs. −12.9%–−17.2% for single-agent setups (Figure 1).
- **Opinion persistence (Llama-3.3):** misinformed answers persist at −10.4% delta on CWQ and −7.7% on WinoGrande (negative = misinformed answers retained more); Ethics shows +1.3% (agents resist misinformation on ethical judgments).
- **Voting vs. consensus (WinoGrande, 5 agents):** voting starts higher (0.938 vs. 0.729 uninformed) but degrades to 0.857 fully misinformed; consensus stays stable (0.729–0.758). The advantage of voting over consensus shrinks from 0.208 to 0.099.
- **Self-correction threshold:** initially misinformed agents correct to the right answer 8.0% of the time with 2 uninformed peers, but 20.5% with 3 uninformed peers—a majority flip.
- GLM-4.7 shows weaker susceptibility overall; both voting and consensus remain highly stable across misinformation levels (gap 0.008–0.025).

## Limitations
- Only two open-weight model families tested (Llama-3.3, GLM-4.7); conclusions are not model-family-general.
- MINT uses machine-generated misinformation; human-written or adversarially optimized misinformation may behave differently.
- Llama-3.3 was used both to generate MINT and as an experimental agent, which may amplify self-preference effects and overestimate persistence for same-family models.
- Fixed MAD structure (up to 5 agents, 5 turns, voting/consensus only); excludes tool use, long-term memory, dynamic roles, retrieval, and source verification.
- Human annotation agreement on MINT is only fair (Fleiss' κ = 0.24–0.26), indicating category boundaries are sometimes ambiguous.

## Relevance to Agentic AI / LLM Agents
Multi-agent debate is increasingly used as a robustness mechanism in agentic pipelines, but this work reveals a concrete failure mode: contextual misinformation from upstream tools (RAG, web search) can propagate through agent interactions even when no agent acts adversarially. The finding that robustness is sensitive to group composition (uninformed majority needed for self-correction) and decision protocol (consensus more stable under peer pressure, voting better in clean conditions) has direct implications for how production multi-agent systems should be designed and monitored. The MINT dataset and MALLM-based experimental framework provide a reusable testbed for evaluating reliability of agentic architectures under realistic noisy-context conditions.

## Tags
#multi-agent #misinformation #robustness #llm-agents #debate #benchmark #information-propagation #reliability
