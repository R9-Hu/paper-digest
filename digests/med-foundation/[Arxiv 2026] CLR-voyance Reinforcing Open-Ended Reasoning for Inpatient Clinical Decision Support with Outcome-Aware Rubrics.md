---
title: "CLR-voyance: Reinforcing Open-Ended Reasoning for Inpatient Clinical Decision Support with Outcome-Aware Rubrics"
authors: ["Aishik Nagar", "Arun-Kumar Kaliya-Perumal", "Yu-Hsuan Han", "Andrew Sheng-Han Huang", "Kristen Kee", "Yushi Cao", "Yiming Chen", "Hongchao Jiang"]
source: "Arxiv"
venue: ""
published: "2026-05-10"
published_time: "2026-05-10T14:51:31+00:00"
year: 2026
topic: "Foundation Models in Medicine"
topic_slug: "med-foundation"
canonical_id: "arxiv:2605.09584"
url: "http://arxiv.org/abs/2605.09584v1"
pdf: "paper/med-foundation/[Arxiv 2026] CLR-voyance Reinforcing Open-Ended Reasoning for Inpatient Clinical Decision Support with Outcome-Aware Rubrics.pdf"
---

# CLR-voyance: Reinforcing Open-Ended Reasoning for Inpatient Clinical Decision Support with Outcome-Aware Rubrics

*🕒 **Published (v1):** 2026-05-10 14:51 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2605.09584v1)*

## TL;DR
CLR-voyance reformulates inpatient clinical reasoning as a Partially Observable Markov Decision Process (POMDP) and trains small language models (8B/4B) via GRPO with per-case, outcome-grounded rubrics derived from real EHR future trajectories. The resulting 8B model (84.91% on CLR-POMDP) outperforms GPT-5 (77.83%) and MedGemma-27B (66.66%) on inpatient clinical decision support, has been deployed at a partner hospital for 6+ months, and has processed 1.03T+ tokens.

## Problem
Existing clinical-LLM evaluations collapse the inherently sequential, partially observable structure of inpatient reasoning into one of three flawed paradigms: (1) closed-form exam-style MCQ benchmarks that frontier models have saturated and that don't predict real-world performance; (2) longitudinal-EHR benchmarks that leak the full admission (including the answer) into the input; or (3) reward signals grounded in static clinical references rather than in the patient's actual downstream care trajectory. No prior work jointly provides outcome-grounded training, clinician-aligned evaluation, and real hospital deployment for open-ended inpatient reasoning.

## Method
**CLR-POMDP formulation.** Each MIMIC-IV admission is treated as a POMDP `M = (S, A, O, T, Z, r)`. A temporal split at `k ~ N(n/2, n/6)` divides a chronologically ordered event stream into a policy-visible *past* and an oracle-only *future* (~65K-token context, raw JSON event-level EHR, no pre-summarisation). Four clinical action-space categories are instantiated per split: Diagnosis, Treatment, Procedural Decision, Uncertainty/Risk-Benefit.

**Grounded Judge.** An oracle LLM with access to the full future generates (query `q`, reference answer `y*`, reference reasoning `ρ*`, supporting future events `src`, per-case rubric `R`). The rubric has pass/fail criteria weighted in `[-10, +10]` on five axes: Accuracy, Completeness, ContextAwareness, CommunicationQuality, InstructionFollowing. The scalar reward is `r_rub = clip[0,1](Σ_{i: j_i=true} p_i / Σ_{i: p_i>0} p_i)` — normalised by positive weights so negative safety criteria drive the score down without inflating the ceiling.

**Post-training.** Qwen3-8B and MedGemma-4B are post-trained with GRPO (G=4/8 completions per prompt, group-relative advantage, KL penalty). Total reward: `r_total = r_rub + r_format + r_tag`. After GRPO, weight-space merging (DELLA-Linear or Breadcrumbs, optionally composed with Activation-Informed Merging) recovers generalist capabilities eroded by domain-specialized RL.

## Key Contributions
- **CLR-POMDP**: first POMDP-style inpatient EHR benchmark built from MIMIC-IV that functions as both training distribution and evaluation harness, with strict past/future isolation.
- **Grounded Judge + per-case adaptive rubrics**: first rubric-as-reward signal for open-ended clinical decision tasks conditioned on a real patient's downstream care trajectory; eliminates static reference grounding.
- **CLR-voyance-8B**: GRPO + DELLA-Linear merging on Qwen3-8B achieves 84.91% on CLR-POMDP, outperforming GPT-5 by 7.08 pp and MedGemma-27B by 18.25 pp.
- **Large-scale clinician validation**: 4 board-certified physicians across 2 specialty cohorts (spine/orthopaedic, general medicine/obesity) validate rubric quality, judge alignment, and blinded model preferences; GPT-5 is worst-aligned judge due to 100% self-preference.
- **Production hospital deployment**: 6+ months, thousands of daily inpatient notes, 1.03T+ tokens processed; only clinical decision support system directly integrated into routine inpatient workflows at this scale.

## Results
- **CLR-voyance-8B aggregate: 84.91%** vs. GPT-5 77.83% (+7.08 pp), Qwen3-8B GRPO (no merge) 77.95%, GPT-4.1 75.74%, MedGemma-27B 66.66%, HuatuoGPT-o1-7B 51.24%; Wilcoxon p < 10⁻³⁰⁰.
- Per-axis over GPT-5: +21.36 pp Completeness (80.93 vs. 59.57), +11.08 pp Accuracy (80.73 vs. 69.65), +4.05 pp ContextAwareness (86.16 vs. 82.11); GPT-5 retains +3.38 pp CommunicationQuality, +0.98 pp InstructionFollowing.
- Action-space gains over GPT-5: +8.0 pp Procedural, +7.6 pp Uncertainty, +6.5 pp Treatment, +2.7 pp Diagnosis.
- Weight-space merging adds +6.96 pp over GRPO-alone on Qwen3-8B; all four merge variants within 0.7 pp of each other (84.25–84.91%).
- SFT on oracle references regresses Qwen3-8B from 75.32% base to 52.36% (policy collapse onto single reference); GRPO reaches 77.99%.
- CLR-voyance-4B (MedGemma-4B + GRPO + DELLA-Linear): +36.34 pp over MedGemma-4B base, with +43.54/+46.38/+42.50 pp on Accuracy/Completeness/ContextAwareness.
- External benchmarks (n=200 each): CLR-voyance-8B improves over Qwen3-8B base by +1.0–9.0 pp on MedCalc, MedMCQA, DDXPlus, Mimic-Instr; on DDXPlus (48.5%) outperforms GPT-5 and HuatuoGPT-o1 at 8B scale; HealthBench: +0.051 (8B), +0.072 (4B).
- Clinician blinded preference: CLR-voyance-8B preferred over GPT-5 at 85.6% (spine) / 48.0% (obesity) win rate; over HuatuoGPT-o1-7B at 94.2% / 82.2%.
- Rubric curation (n=2,496 rater-criterion pairs): 89.1% AI-generated criteria accepted as-is; Grounded Judge achieves κ=0.42 against clinician verdicts (substantial agreement).
- DeepSeek-R1-Distill-Qwen-7B scores 11.99% (near-zero clinical transferability from math/code GRPO).

## Limitations
- CLR-POMDP is derived exclusively from MIMIC-IV (a single US academic hospital system); generalizability to other EHR systems, languages, and healthcare contexts is unverified.
- The Grounded Judge (oracle LLM) is a proprietary or large open model; rubric quality is partially bounded by that model's clinical knowledge and generation artifacts.
- Test split evaluation of 7,927 admissions uses the same Grounded Judge for both rubric generation and grading, creating a potential circularity in the reward/evaluation pipeline.
- CLR-voyance-8B is constrained to 8B parameters by on-premise GPU infrastructure; larger models that would be superior are excluded from deployment comparisons.
- Weight-space merging benefits are substantially weaker for the 4B model family, suggesting the approach is not uniformly beneficial across model scales.
- Recurring clinical failure modes observed in production: DDI hazards from failure to cross-reference existing medications, over-inference of acute cardiac events, patient-info contamination (n=16 obesity cases), and occasional Chinese-character intrusions from the Qwen3 base.
- Clinician preference is cohort-specific (spine vs. obesity gap on Table 2), suggesting persona-centric policy training is needed for clinical utility across specialties.
- The obesity cohort blinded preference over GPT-5 (48.0% win rate) indicates near-parity, not superiority, in that domain.

## Relevance to Foundation Models in Medicine
CLR-voyance directly addresses a core open problem for clinical foundation models: replacing exam-style closed-form evaluation with outcome-grounded, open-ended reasoning evaluation and training signals that mirror actual clinical decision-making under uncertainty. The POMDP + per-case adaptive rubric paradigm offers a replicable blueprint for anchoring RL post-training to real patient outcomes rather than static references, applicable to any EHR-linked cohort. The model merging strategy (GRPO task vector + base interpolation) is a practical recipe for specializing small clinical LMs without capability regression, directly relevant to on-premise hospital deployment constraints. The clinician alignment study's finding that LLM-as-a-judge selection is dominated by cohort×judge interaction rather than model size challenges the standard practice of using a single large judge for clinical evaluation.

## Tags
#clinical-decision-support #rlhf #grpo #ehr #pomdp #rubric-reward #model-merging #inpatient-reasoning
