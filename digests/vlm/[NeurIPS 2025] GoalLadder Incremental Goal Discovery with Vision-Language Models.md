---
title: "GoalLadder: Incremental Goal Discovery with Vision-Language Models"
authors: ["Alexey Zakharov", "Shimon Whiteson"]
source: "NeurIPS"
venue: "NeurIPS 2025"
published: "2025-01-01"
year: 2025
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "openreview:BiowiwzQaO"
url: "https://openreview.net/forum?id=BiowiwzQaO"
pdf: "paper/vlm/[NeurIPS 2025] GoalLadder Incremental Goal Discovery with Vision-Language Models.pdf"
---

# GoalLadder: Incremental Goal Discovery with Vision-Language Models

## TL;DR
GoalLadder is a VLM-guided RL method that incrementally discovers and ranks intermediate goal states toward a language-specified task objective, using an ELO-based rating system to mitigate noisy VLM feedback and a VAE embedding space to generalize rewards without dense labeling. It achieves ~95% mean success rate on 7 classic control and robotic manipulation tasks, nearly matching an oracle with ground-truth rewards while requiring far fewer VLM queries than prior methods.

## Problem
Existing VLM-based reward specification for RL either (a) relies on non-visual state representations (LLM code-generation approaches), (b) uses CLIP-based embedding rewards that are noisy due to training distribution mismatch, or (c) requires large numbers of VLM preference queries to learn a well-shaped reward function that still contains label noise (RL-VLM-F). No prior method simultaneously addresses robustness to noisy VLM feedback and query efficiency in visual environments without environment modifications.

## Method
GoalLadder operates as a repeating 4-stage loop during SAC training:

1. **Discovery**: Uniformly sampled observations from the latest episode trajectory are compared pairwise against the current top-rated candidate goal via a VLM (Gemini 2.0 Flash) conditioned on the language instruction. Observations judged as closer to the goal are inserted into a ranking buffer $B_g$ (capped at 10 candidates) with a default initial ELO rating.

2. **Ranking**: Pairs $(g_i, g_j)$ are sampled from $B_g$ and compared by the VLM. Ratings are updated via the ELO update rule: $e_i \leftarrow e_i + T(S_i - E_i)$, where $E_i = 1/(1 + 10^{(e_j - e_i)/C})$ is the expected score. This accumulates noisy VLM comparisons into a stable utility estimate without trusting any single query.

3. **Reward definition**: The reward is the negative Euclidean distance to the top-rated candidate's latent representation: $R(s_{t-1}, a_{t-1}) = -\|z_t - z^*\|_2$, where $z = \psi(o)$ and $\psi$ is a VAE encoder trained on unlabeled agent observations. This enables reward generalization to unseen states without additional VLM queries.

4. **Relabeling**: Every $L=5000$ steps, all transitions in the replay buffer are relabeled with the current top-rated goal's reward to handle non-stationarity in SAC.

VLM queries are batched every $K$ steps ($K=2000$ for Gym, $K=500$ for Metaworld) with $M=5$ comparisons per session.

## Key Contributions
- ELO-based candidate goal rating system that is robust to noisy VLM pairwise comparisons
- Incremental goal discovery framing: VLM identifies states of *improving* task progress rather than directly scoring all observations
- VAE-based reward generalization: reward defined as distance in a learned visual embedding space trained on unlabeled data, decoupling reward coverage from VLM query volume
- Demonstration that a single language instruction suffices to train RL agents in visual environments without environment modifications (e.g., robot masking required by RL-VLM-F)

## Results
- **Mean success rate ~95%** across 7 tasks (CartPole, MountainCar, Drawer Open, Drawer Close, Sweep Into, Window Open, Button Press) vs. ~45% for the next best competitor (RL-VLM-F)
- Nearly matches or exceeds oracle (ground-truth reward) on all tested tasks; surpasses oracle on Drawer Open
- **VLM query efficiency**: ~4,500 total queries averaged across Metaworld tasks vs. ~15,000 preference labels required by PEBBLE (ground-truth preference baseline) to reach equivalent performance
- RL-VLM-F fails on most Metaworld tasks at GoalLadder's feedback rate; VLM-RM and RoboCLIP fail on nearly all tasks

## Limitations
- Assumes task success is identifiable from a **single image** (static goal); dynamic or multi-step goal tasks not addressed
- Visual similarity in VAE latent space may be a poor proxy for task progress in environments where state changes are visually subtle
- Experiments limited to 7 environments; VLM API cost constrains broader evaluation
- VLMs have known poor spatial reasoning, which GoalLadder mitigates but does not eliminate; spatial tasks remain harder

## Relevance to Vision-Language Models
GoalLadder demonstrates a principled use of VLMs as noisy oracles for sequential decision-making rather than as direct reward generators, highlighting the importance of noise-robust aggregation (ELO) when deploying VLMs in feedback loops. It is directly relevant to the growing literature on VLMs as reward models (VLM-RM, RL-VLM-F, Eureka), offering a concrete mechanism to reduce query cost and label noise simultaneously. The method's reliance on pairwise comparisons rather than absolute scoring aligns with known VLM strengths and exposes the critical bottleneck of spatial reasoning in vision-language grounding for robotics. For researchers tracking VLMs, this work establishes a practical template for integrating VLM feedback with unsupervised representation learning to bridge the gap between language instruction and dense reward in pixel-based environments.

## Tags
#vlm #reinforcement-learning #reward-learning #goal-discovery #robotic-manipulation #elo-rating #preference-learning #vae
