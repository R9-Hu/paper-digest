---
title: "Trajectory-Level Redirection Attacks on Vision-Language-Action Models"
authors: ["Gokul Puthumanaillam", "Vardhan Dongre", "Pranay Thangeda", "Hooshang Nayyeri", "Dilek Hakkani-T\u00fcr", "Melkior Ornik"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
published_time: "2026-06-11T07:12:17+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.12978"
url: "http://arxiv.org/abs/2606.12978v1"
pdf: "paper/vlm/[Arxiv 2026] Trajectory-Level Redirection Attacks on Vision-Language-Action Models.pdf"
---

# Trajectory-Level Redirection Attacks on Vision-Language-Action Models

*🕒 **Published (v1):** 2026-06-11 07:12 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.12978v1)*

## TL;DR
This paper formalizes **command-preserving trajectory redirection**: a single near-benign text perturbation (median 3.4 character edits) issued once before a robot episode can redirect a frozen VLA policy to an adversary-specified physical goal while appearing to still specify the intended task. An on-policy prompt search algorithm (analogous to DAgger) discovers such prompts by matching closed-loop rollout actions to a target teacher, achieving >90% attack success rate on 7 of 9 evaluated VLA architectures.

## Problem
Prior VLA adversarial work (e.g., GCG-style suffix attacks) shows that adversarial prompts can elicit targeted *individual* actions or sustain them across changing images, but this is strictly weaker than controlling the robot's **final physical outcome**. A prompt optimized on fixed, pre-collected observations is evaluated on the wrong state distribution—because the candidate prompt itself alters which observations are visited—leaving the trajectory-level threat unaddressed.

## Method
The authors formalize a threat model **Tcp(τb, Γe)** requiring that the attack prompt: (1) stays within character edit distance ε of the benign instruction, (2) is a valid readable string, (3) leaks no target-task words/synonyms, and (4) is still interpretable as the benign command. Attack success requires the rollout to fail the benchmark predicate *and* satisfy the attacker's target predicate simultaneously.

To find such prompts, they introduce **on-policy teacher-matching prompt search**:
- A frozen VLA is queried under both the benign prompt τb and the target prompt τt (used only during construction) to produce per-observation "teacher" action chunks Ab(o) and At(o).
- Candidate prompts (generated via character-level text perturbations and GCG-style mutations) are scored by a **target-vs-benign margin loss** (Eq. 4) that measures whether the candidate's actions are closer to At than Ab at the same observation.
- Top candidates are rolled out in closed loop; visited observations are relabeled with teacher actions and added back to the scoring dataset (DAgger-style aggregation). Rollouts are ranked by a weighted combination of target success, benchmark failure, target-action distance, and edit cost (Eq. 6).
- A greedy token-pruning step finds the minimal perturbation that still satisfies constraints and achieves success.
- A Lipschitz tracking bound (δK ≤ Lu Σ α^(K-1-k) ε^τ_k) formally connects per-step action mismatch to final-state target success.

## Key Contributions
- Formal definition of **command-preserving trajectory redirection** as a closed-loop, prompt-only threat model with mathematically specified admissibility constraints.
- **On-policy prompt search** algorithm that discovers redirection prompts using VLA rollouts as training signal, avoiding distribution shift from offline datasets.
- Lipschitz-based **tracking bound** connecting on-trajectory action mismatch to terminal physical-state success.
- Broad empirical evaluation across 9 VLA families (OpenVLA, MolmoAct, π0.5, Octo, SmolVLA, GR00T-N1, OpenVLA-OFT, π0-FAST, VLA-0) in simulation (LIBERO) and on physical hardware (SO-100 6-DoF arm).
- **Causal analysis** localizing the attack mechanism to the residual-stream activations of corrupted destination-phrase tokens.
- Defense evaluation showing that **nearest-task canonicalization** reduces Attack ASR from 95.1% to 7.4%, while lightweight preprocessing (whitespace, punctuation, Unicode normalization) is largely ineffective.

## Results
- **Attack ASR >90%** on 7 of 9 VLA architectures (Table 1); π0.5 reaches 97.5%, GR00T-N1 96.8%, SmolVLA 94.7%, OpenVLA 91.8%, Octo 88.6%, VLA-0 82.8%.
- Median character edit distance of **3.4 characters** across all models (range 2.4–5.4).
- Benchmark failure rate matches or exceeds ASR (e.g., π0.5: 98.4% bench fail, 98.1% target final).
- **Hardware (SO-100)**: benign prompt achieves reliable task success; adversarial near-benign prompt collapses original-task success to ~3–6% across SmolVLA and GR00T-N1.
- **Causal trace** on π0.5: patching corrupted destination-token residual states back to benign counterparts removes target-like action; patching non-destination tokens ("put", "bowl") has negligible effect.
- **Defense hierarchy** on π0.5 LIBERO-Goal: no defense 95.1% ASR → spell correction 31.8% ASR → nearest-task canonicalization **7.4% ASR** (with 94.2% clean SR retained).
- Larger perturbation budgets reduce required policy queries to find successful attacks (Figure 5).

## Limitations
- Evaluation is confined to tabletop manipulation (LIBERO benchmark, SO-100 arm); generalization to navigation, mobile manipulation, or long-horizon tasks is untested.
- The search assumes **white-box query access** to the frozen VLA (rollouts + action-chunk queries), which may overestimate attacker capability in fully locked-down deployments.
- The tracking bound assumes Lipschitz dynamics and a Lipschitz task-predicate function h; real manipulation environments may violate these assumptions at contact events.
- Defense evaluation covers preprocessing strategies only; certified or learning-based defenses (e.g., randomized smoothing, adversarial fine-tuning) are not explored.

## Relevance to Vision-Language Models
VLAs represent the frontier of language-conditioned embodied AI, and this paper exposes a fundamental security gap in how language grounding interacts with closed-loop control: unlike static NLP tasks, text perturbations in VLAs propagate through time by reshaping the observation stream itself, making standard single-query robustness metrics insufficient. The formal command-preserving threat model and on-policy search method are directly applicable to any VLM architecture used as a persistent conditioning signal (e.g., RT-2, π0, OpenVLA), motivating a new class of trajectory-aware robustness evaluation. The finding that nearest-task canonicalization—mapping free-form instructions to a validated command set before inference—is the only effective defense has direct implications for how VLM-based robot pipelines should be architected for deployment. For VLM researchers, the causal tracing result that attack effects are localized to destination-phrase token representations offers a concrete mechanistic target for future alignment and robustness work.

## Tags
#vla #adversarial-attacks #robot-safety #trajectory-level #prompt-perturbation #closed-loop-control #vlm-robustness #embodied-ai
