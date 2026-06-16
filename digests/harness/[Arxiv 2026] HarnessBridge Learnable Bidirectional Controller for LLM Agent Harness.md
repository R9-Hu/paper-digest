---
title: "HarnessBridge: Learnable Bidirectional Controller for LLM Agent Harness"
authors: ["Xiaoxuan Wang", "Haixin Wang", "Alexander Taylor", "Jason Cong", "Yizhou Sun", "Wei Wang"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T04:18:37+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.12882"
url: "http://arxiv.org/abs/2606.12882v1"
pdf: "paper/harness/[Arxiv 2026] HarnessBridge Learnable Bidirectional Controller for LLM Agent Harness.pdf"
---

# HarnessBridge: Learnable Bidirectional Controller for LLM Agent Harness

*🕒 **Published (v1):** 2026-06-11 04:18 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.12882v1)*

## TL;DR
HarnessBridge replaces manually engineered LLM agent harnesses with a lightweight, end-to-end learnable bidirectional projection policy (Qwen3.5-0.8B) that compresses agent observations and validates or rejects proposed actions at runtime. On Terminal-Bench 2.0 and SWE-bench Verified, it matches or beats strong specialized harnesses while cutting token usage by 23–91% and generalizes from small open-source generators to large commercial models.

## Problem
Existing harnesses are static, hand-coded scaffolds that manage context, retry logic, summarization, and tool-call validation via fixed heuristics. As task horizons grow, manually engineered harnesses fail to scale: observation trajectories accumulate stale, redundant context that degrades generator decisions, and agents issue repeated unproductive actions that waste environment steps. Prior "auto-harness" methods (e.g., Meta-Harness) optimize the outer scaffold structure rather than learning the runtime policy that mediates bidirectional information flow between generator and environment.

## Method
HarnessBridge parameterizes the agent–environment interface as a learned bidirectional policy πh: (s, q, Ht, at) → (H̃t, a′t).

**Observation projection** (environment→agent): Assigns each history unit hi a decision zi ∈ {Pass, Compress, Drop} and prepends an *active-state index* Ut — a distilled slot recording unresolved errors, open constraints, and pending goals — to make current decision-relevant state immediately visible without requiring the generator to reconstruct it from a long log.

**Action projection** (agent→environment): Maps a proposed action at to either a Pass (executable transition) or Reject with structured feedback ρt = (concern, evidence, suggestion), where rejection requires trajectory-grounded evidence; if no such evidence exists, the action passes by default.

Both projections share a single policy Pθ (initialized from Qwen3.5-0.8B) trained via **unified instruction fine-tuning**. Training data is curated by sampling traces with prompted instruction-tuned models, retaining only successful trajectories, and filtering with an LLM judge for schema consistency, faithful compression, and grounded pass/reject decisions. The raw trajectory Ht is always preserved as an authoritative record; Pθ only decides the projected view, making compression non-destructive and provenance-aware.

## Key Contributions
- First formulation of harness engineering as an end-to-end learnable generation problem over the bidirectional agent–environment interface.
- Unified instruction tuning over a single shared policy for both observation projection (Pass/Compress/Drop + active-state index) and action projection (Pass/Reject with grounded feedback).
- Non-destructive trajectory design: raw history is retained; the harness only decides what view to expose, mitigating hallucinated summaries and accidental detail loss.
- Empirical demonstration that a harness trained on one generator family (Qwen3.5-35B-A3B, SWE-bench traces) generalizes to 6 other generators across 2 benchmarks.

## Results
- **Terminal-Bench 2.0, Qwen3.5-35B-A3B**: HarnessBridge 33.7% SR vs. Terminus 2 baseline 30.3% (+11.2 pp); token usage 1.23M vs. 2.31M (−46.8%). Best SR among all harnesses tested.
- **SWE-bench Verified, Qwen3.5-35B-A3B**: 60.2% SR vs. 61.6% for Terminus 2 (−1.4 pp); token usage 1.13M vs. 1.47M (−23.1%). Lowest token budget among reported harnesses.
- **Terminal-Bench 2.0, GLM-4.7-Flash**: 20.2% SR vs. 19.1% (+5.8 pp); token usage 0.42M vs. 1.87M (−77.5%).
- **Generalization — GPT-5.4-Nano**: SR 22.5% vs. 18.0% (+25%); tokens 0.91M vs. 9.80M (−90.7%).
- **Generalization — GPT-5.4**: SR maintained at 53.9%; tokens 0.99M vs. 9.41M (−89.5%).
- **Generalization — Claude-Opus-4.7**: SR 65.2% vs. 64.0% (+1.9%); tokens 0.19M vs. 0.26M (−26.9%).
- **Ablation**: Removing either projection reduces success rate on both backbone models; efficiency gains without action projection come at consistent SR cost.
- **Outcome-level**: On "Gained" tasks (HarnessBridge succeeds, baseline fails), average trajectory 18 turns vs. 52 (−65%) and token usage −89%.

## Limitations
- Training data derived exclusively from SWE-bench trajectories; Terminal-Bench 2.0 is purely out-of-domain (no in-domain ablation showing the gap from domain-matched training).
- Evaluation restricted to coding-centric long-horizon tasks; generalization to other domains (web navigation, multimodal tasks) is asserted but not tested.
- Data curation relies on LLM judges for quality filtering, introducing a dependency on judge calibration that is not ablated.
- Requires training and deploying an auxiliary 0.8B harness model alongside the generator, adding latency and infrastructure overhead that is not quantified.
- Rejection feedback quality and its downstream effect on the generator are not isolated in ablations.

## Relevance to Harnesses / Meta-Harnesses
HarnessBridge directly advances the harness-as-optimizable-object agenda: where prior meta-harness work (Meta-Harness, Lee et al. 2026) searches over scaffold structure, HarnessBridge learns the *runtime interaction policy* — the per-step decisions about what to expose and what to commit — making it a foundational complement to scaffold-level optimization. Its bidirectional framing (observation compression + action gating) operationalizes the distinction between harness-as-format and harness-as-policy, which is a conceptual clarification with direct design implications for anyone building or studying meta-harnesses. The generalization result — a policy trained on one small generator's trajectories transferring to GPT-5.4 and Claude-Opus-4.7 — suggests that effective harness control patterns are largely generator-agnostic, which has practical implications for harness meta-training pipelines.

## Tags
#harness #meta-harness #agent-environment-interface #context-compression #action-validation #long-horizon-agents #instruction-tuning #swe-bench
