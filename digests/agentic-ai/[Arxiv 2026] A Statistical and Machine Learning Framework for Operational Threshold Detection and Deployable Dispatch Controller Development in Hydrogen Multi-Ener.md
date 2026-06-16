---
title: "A Statistical and Machine Learning Framework for Operational Threshold Detection and Deployable Dispatch Controller Development in Hydrogen Multi-Energy Systems"
authors: ["Shadi Heenatigala", "Hasanika Samarasinghe"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T16:23:33+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14601"
url: "http://arxiv.org/abs/2606.14601v1"
pdf: "paper/agentic-ai/[Arxiv 2026] A Statistical and Machine Learning Framework for Operational Threshold Detection and Deployable Dispatch Controller Development in Hydrogen Multi-Ener.pdf"
---

# A Statistical and Machine Learning Framework for Operational Threshold Detection and Deployable Dispatch Controller Development in Hydrogen Multi-Energy Systems

*🕒 **Published (v1):** 2026-06-12 16:23 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14601v1)*

## TL;DR
This paper applies a six-method statistical and machine learning pipeline — including Kruskal-Wallis tests, multiple regression, Random Forest, LSTM, and DDPG — to one year of five-minute operational data from a hydrogen multi-energy system (H-MES) to characterize dispatch dynamics and train a deployable electrolyzer controller. The central finding is that solar irradiance acts as a binary activation threshold (ε² = 0.457) rather than a continuous driver, and wind output carries unique non-linear predictive information (45.16% %IncMSE) invisible to parametric regression. A DDPG agent trained offline on 14,999 transitions learns a continuous hydrogen revenue-maximizing dispatch policy.

## Problem
H-MES research relies on simulation tools (HOMER, MATLAB/Simulink) that report aggregate averages without statistical inference, concealing distributional structure (zero-inflation, bimodality, threshold effects) that governs real operational performance. No prior work applies formal non-parametric group comparisons with effect sizes or combines statistical characterization with ML-derived controllers on the same H-MES dataset.

## Method
Four sequential analytical phases on a 20,000-observation, five-minute-resolution Kaggle H-MES dataset:
1. **Statistical (R):** Shapiro-Wilk normality, Pearson/Spearman correlation matrices, Kruskal-Wallis group tests with Dunn's post-hoc (Benjamini-Hochberg FDR correction), rank ε² effect sizes, multiple regression with VIF-based multicollinearity screening, and Random Forest (500 trees, %IncMSE + IncNodePurity) for variable importance.
2. **LSTM (MATLAB):** Two stacked LSTM layers (128→64 units) with a 288-step (24-hour) sliding window, dropout, Adam optimizer with piecewise LR decay, early stopping; targets the 81.3%-zero-inflated electrolyzer power signal.
3. **DDPG (MATLAB):** MDP with 7-dimensional state (solar, wind, demand, heat demand, net H₂ balance, electricity price, H₂ price), continuous action a ∈ [0, 0.625 MW], reward = H₂ revenue − electrolyzer energy cost. Actor uses LayerNorm; all 14,999 transitions preloaded offline before gradient updates; exploration noise suppressed.

## Key Contributions
- First formal non-parametric group comparison (Kruskal-Wallis + Dunn's + ε²) applied to H-MES operational data.
- Identification of a solar threshold effect: Low and Medium solar groups produce statistically indistinguishable H₂ output (Dunn's z = 0.000, p = 1.000); activation only during peak solar periods.
- Discovery that wind output ranks first in RF permutation importance (%IncMSE = 45.16%) despite weak bivariate correlation (r = 0.167), revealing non-linear dynamics undetectable by parametric regression.
- LSTM and DDPG controllers operationalized from statistically-derived structural insights, with DDPG formulated as a deployable continuous dispatch policy.

## Results
- Kruskal-Wallis solar effect: χ²(2) = 8,241.3, ε² = 0.457 (very large); demand effect: ε² = 0.126.
- Multiple regression: R² = 1.000 train and test (RMSE = 0.0003 kg/step); electrolyzer power is near-exclusive predictor (β* = 1.000); driven by physical determinism (r = 1.000 bivariate).
- Random Forest (R): OOB R² = 0.9975; CV R² = 0.9999 (RMSE = 0.000594 kg/step).
- Random Forest (MATLAB): OOB MSE ≈ 8.5×10⁻⁴ MW² (RMSE ≈ 0.029 MW); stabilizes within 50 trees.
- Wind %IncMSE = 45.16% vs. electrolyzer 34.74% and PV 26.45%.
- No baseline controller comparison reported for DDPG; grid violation fraction of original controller = 0.0% (used as feasibility baseline only).

## Limitations
- Single synthetic/Kaggle dataset; no real-world deployment or cross-site validation.
- R² = 1.000 in regression is an artifact of physical determinism (H₂ production is a direct function of electrolyzer power, r = 1.000), not a modeling achievement.
- Regression violates OLS assumptions: heteroscedasticity (Breusch-Pagan BP = 6,268.8) and strong autocorrelation (Durbin-Watson = 0.855) acknowledged but unaddressed.
- DDPG is offline-trained only; no online interaction, sim-to-real gap unquantified, and no comparison against rule-based or MPC baselines.
- LSTM and DDPG results reported without confidence intervals or statistical tests.

## Relevance to Agentic AI / LLM Agents
This paper is peripheral to the LLM agent line of work. Its DDPG component is a classical continuous-control RL agent — predating and architecturally distinct from LLM-based autonomous agents — applied narrowly to electrolyzer dispatch in an energy domain. The offline pre-training protocol (preloading a fixed replay buffer before any gradient updates) is conceptually adjacent to offline RL / behavior cloning discussions relevant to safe agentic deployment, but the paper does not engage with that literature. Researchers tracking agentic AI may find the MDP formulation and offline-RL training constraints marginally relevant as a domain case study, but the paper makes no contribution to agent architecture, planning, tool use, or LLM-based reasoning.

## Tags
#reinforcement-learning #ddpg #lstm #offline-rl #energy-systems #dispatch-optimization #time-series #non-llm-agent
