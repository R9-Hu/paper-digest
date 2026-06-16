---
title: "Infant Spontaneous Movement Noise Improves Exploration in Deep RL"
authors: ["Francisco M. L\u00f3pez", "Markus R. Ernst", "Francisco Cruz", "Matej Hoffmann", "and Jochen Triesch"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T11:35:06+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16590"
url: "http://arxiv.org/abs/2606.16590v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Infant Spontaneous Movement Noise Improves Exploration in Deep RL.pdf"
---

# Infant Spontaneous Movement Noise Improves Exploration in Deep RL

*🕒 **Published (v1):** 2026-06-15 11:35 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16590v1)*

## TL;DR
This paper characterizes the power spectral density (PSD) of infant spontaneous end-effector movements and finds that the noise color exponent β increases linearly with age (8–30 weeks). Translating this developmental pattern into a scheduled action noise for deep RL—starting at β=0.7 and linearly annealing to β=0.9—yields more consistent exploration improvement than fixed-color noise baselines across 12 continuous-control environments.

## Problem
Exploration in deep RL defaults to temporally uncorrelated Gaussian (white) noise. While fixed colored noise (especially pink, β=1) has been shown to improve exploration, no prior work has derived a principled, developmentally grounded schedule for annealing noise color during training, nor quantitatively characterized the PSD dynamics of infant spontaneous movements.

## Method
1. **Infant movement analysis**: 2D keypoints (wrists, ankles) extracted via OpenPose from 19 longitudinal video sessions of 4 infants (ages 8–30 weeks). Velocities are computed from keypoint differences; PSDs estimated via Welch's method with FFT over 1,024-frame windows. Linear regression in log-log space yields β per session; a second regression fits β as a linear function of age (β(w) = 0.617 + 0.00869·w, R=0.70, p<0.001).
2. **Baby noise schedule**: Colored noise blocks (length L=10,000) are generated via spectral shaping (FFT scaling). β is annealed linearly during training: β(t) = 0.7 + 0.2·(t/T), matching the empirically derived infant developmental range. A new block is sampled whenever the previous one is exhausted.
3. **RL integration**: Baby noise replaces white noise in TD3 (additive policy perturbation) and SAC (reparametrization trick). Hyperparameters are held fixed across all noise types; 10 seeds per condition.

## Key Contributions
- First quantitative PSD characterization of infant spontaneous movement noise color across development, showing β increases significantly (R=0.70, p<0.001) from ~0.69 at 8 weeks to ~0.88 at 30 weeks.
- A developmental noise schedule (Eq. 4) that linearly anneals β from 0.7 to 0.9 over training, inspired directly by infant motor statistics.
- Demonstration that this schedule achieves the highest average normalized AUC across 24 conditions (12 environments × 2 algorithms) and is the only noise type with a win rate significantly above chance vs. white noise (56%, p<0.05).

## Results
- **Overall normalized AUC** (z-scored across all algorithms and environments): Baby noise = 0.24 (highest), rose (β=0.75) = 0.17, blush (β=0.5) = 0.13, pink (β=1) = 0.12, white = 0.07, red (β=2) = −0.38, OU = −0.40.
- **Win rate vs. white noise** (paired runs, binomial test): Baby noise = 56% (p<0.05, only noise type significantly above chance); blush, rose, and pink win rates were not significantly above chance despite higher aggregate AUC.
- **Per-algorithm**: Baby noise achieves highest aggregate AUC for both SAC (0.21) and TD3 (0.24 across all environments per Table I aggregate).
- Evaluated on 12 Gymnasium/Gymnasium-robotics environments: 4 classic control, 4 locomotion (Hopper, Swimmer, HalfCheetah, Ant), 4 PointMaze tasks.

## Limitations
- Infant data covers only ages 8–30 weeks from 4 infants (19 sessions); the β schedule beyond this range is extrapolated assuming β=1 as an adult upper bound.
- Baby noise is best on average but achieves the best score in only 1 of 24 individual conditions; blush noise dominates maze environments with SAC.
- Win rate advantage over white noise is modest (56%) and not assessed against other fixed colored noises.
- Only continuous-control environments evaluated; discrete-action or high-dimensional visual RL not tested.
- The biologically motivated β range (0.7–0.9) is narrow; whether wider schedules or non-linear annealing would improve results is unexplored.

## Relevance to Agentic AI / LLM Agents
This work is tangential to LLM-based agents but directly relevant to embodied and RL-based agents: it provides a biologically grounded principle for scheduling exploration noise, which is a core challenge in training autonomous agents. The developmental curriculum analogy—progressively increasing temporal structure during training—parallels ideas in curriculum learning and exploration scheduling that appear in agentic RL pipelines. For researchers building agents that learn through interaction (e.g., robot manipulation, navigation, or game-playing), infant-inspired noise schedules offer a low-overhead, parameter-light improvement over the white-noise default. The broader thesis—that human developmental trajectories can inform artificial agent design—connects to ongoing work on intrinsic motivation and embodied developmental AI.

## Tags
#reinforcement-learning #exploration #colored-noise #developmental-ai #embodied-agents #continuous-control #curriculum-learning #biologically-inspired
