---
title: "How Far Can Machine Translation Quality Take You? Extrinsic Discourse Evaluation in Goal-Oriented Setups"
authors: ["Wafaa Mohammed", "Kata Naszadi", "Vlad Niculae"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T11:44:02+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16596"
url: "http://arxiv.org/abs/2606.16596v1"
pdf: "paper/agentic-ai/[Arxiv 2026] How Far Can Machine Translation Quality Take You Extrinsic Discourse Evaluation in Goal-Oriented Setups.pdf"
---

# How Far Can Machine Translation Quality Take You? Extrinsic Discourse Evaluation in Goal-Oriented Setups

*🕒 **Published (v1):** 2026-06-15 11:44 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16596v1)*

## TL;DR
Standard MT quality metrics (COMETQE) correlate weakly with downstream task success in discourse-sensitive applications. This paper introduces two goal-oriented extrinsic evaluation regimes—a controlled entity-counting probe and a multilingual multi-agent Diplomacy game—to expose discourse failures invisible to intrinsic metrics. Even top-scoring MT systems exhibit persistent coreference errors and coordination failures that compound in interactive settings.

## Problem
MT evaluation is predominantly intrinsic: metrics like COMETQE measure fluency and adequacy in isolation but fail to capture discourse-level errors (coreference inconsistency, negation mistranslation, formality shifts, acronym misrendering) that silently degrade downstream task performance in multi-turn, goal-oriented pipelines such as legal interpretation, asylum processing, and collaborative communication.

## Method
Two complementary evaluation regimes:

**Static (entity counting):** 360 controlled single-entity narratives (English→Arabic/Russian/Romanian) sourced from a pronoun-fidelity dataset. Human annotators count distinct referents in MT output; deviations from ground-truth count of 1 directly expose coreference/gender-agreement failures. Four MT models tested (ayaexpanse 8B, gemma3 12B, llama3.1 8B, eurollm 22B).

**Interactive (Welfare Diplomacy):** Seven LLM agents (gemma-4-31B) play the Welfare Diplomacy strategic game across four configurations—monolingual, multilingual (MT-mediated cross-group communication), no-press, and random-press—over 5 seeds × 3 target languages (German, French, Arabic) × 5 MT models (adding llama2 7B). Game metrics: mean welfare, Nash welfare, miscoordination (invalid/failed orders), and conflicts. Discourse phenomena in game messages are tracked via automatic proxies: length mismatch, assistant preface, digit/acronym mismatch, mood change (question marks), dis/armament mistranslation, and formality shift.

## Key Contributions
- Framework for extrinsic discourse MT evaluation using two complementary goal-oriented environments (static interpretation + interactive coordination)
- Entity-counting task as a controlled probe of referential consistency; human-annotated because LLMs proved unreliable as judges
- Empirical demonstration that COMETQE rankings do not transfer to downstream welfare/coordination outcomes (Pearson r ≈ 0.16–0.19 for welfare, not significant for miscoordination/conflicts)
- Identification of game-specific discourse phenomena (acronym mismatch, disarmament mistranslation, formality increase) that correlate with interaction outcomes but are largely invisible to COMETQE
- Qualitative finding that German↔English translation raises formality, which paradoxically improves coordination in that language pair

## Results
- **Entity counting accuracy:** gemma3 12B achieves highest accuracy across languages (87.2% Arabic, 88.6% Russian, 88.1% Romanian); eurollm 22B and ayaexpanse 8B—despite top COMETQE scores—show higher rates of coreference errors (>1 entity counts)
- **COMETQE vs. accuracy correlation:** High COMETQE does not predict entity-counting accuracy; gemma3 12B slightly lower COMETQE but strongest discourse coherence
- **Welfare Diplomacy:** COMETQE–welfare Pearson r = 0.160 (p=0.17); COMETQE–miscoordination r = −0.048 (p=0.68)—no significant correlation between MT quality metric and game outcomes
- **Discourse phenomena:** Length mismatch, preface, digit/mood errors strongly correlate with COMETQE (r = −0.83 to −0.77); acronym mismatch and disarmament mistranslation correlate with miscoordination (r = 0.32, p<0.05) and conflicts (r = 0.28–0.34) but not COMETQE
- **Language variation:** Arabic and French multilingual setups degrade coordination vs. monolingual; German improves it (linked to formality increase)

## Limitations
- Correlational analysis only; no causal claims between specific discourse phenomena and game outcomes
- MT models receive no task-specific context or instructions during translation, which may understate achievable performance
- Entity-counting annotation subject to annotator bias and language/cultural conventions in gender morphology
- Only COMETQE used as intrinsic metric; other metrics (MetricX) may reveal different patterns
- Diplomacy power-to-language assignment is fixed; variance from different permutations unexplored
- Small number of game runs (5 seeds) limits statistical power for game-level comparisons

## Relevance to Agentic AI / LLM Agents
This paper directly evaluates LLM agents in a multi-agent, multi-turn strategic communication game, making it immediately relevant to researchers building or assessing agentic systems that operate in multilingual or cross-lingual environments. The finding that COMETQE is a poor proxy for coordination success in Welfare Diplomacy underscores a broader principle: task-agnostic quality metrics can mislead when agents interact over sequential turns where errors compound. The discourse-phenomenon taxonomy (acronym misrendering, negation mistranslation, formality drift) provides actionable failure modes for any agentic pipeline that relies on MT as an intermediate component. The Welfare Diplomacy setup itself is a reproducible, automated benchmark for evaluating how information fidelity in inter-agent communication affects collective goal achievement.

## Tags
#multi-agent #evaluation #machine-translation #discourse #benchmark #coordination #llm-agents #extrinsic-evaluation
