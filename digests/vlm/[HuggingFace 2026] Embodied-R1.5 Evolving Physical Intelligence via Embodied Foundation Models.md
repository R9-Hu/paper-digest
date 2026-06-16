---
title: "Embodied-R1.5: Evolving Physical Intelligence via Embodied Foundation Models"
authors: ["Yifu Yuan", "Yaoting Huang", "Xianze Yao", "Yutong Li", "Shuoheng Zhang", "Linqi Han", "Pengyi Li", "Jiangeng Sun", "Wenting Jia", "Zhao Zhang", "Yuhao Liu", "Ruihao Liao", "Yucheng Hu", "Qiyu Wu", "Yuxiao Li", "Zibin Dong", "Fei Ni", "Yan Zheng", "Shuyang Gu", "Yi Ma", "Hongyao Tang", "Han Hu", "Jianye Hao"]
source: "HuggingFace"
venue: ""
published: "2026-06-09"
published_time: "2026-06-09T00:00:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.11324"
url: "https://huggingface.co/papers/2606.11324"
pdf: "paper/vlm/[HuggingFace 2026] Embodied-R1.5 Evolving Physical Intelligence via Embodied Foundation Models.pdf"
---

# Embodied-R1.5: Evolving Physical Intelligence via Embodied Foundation Models

*🕒 **Published (v1):** 2026-06-09 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.11324)*

## TL;DR
Embodied-R1.5 is an 8B-parameter Embodied Foundation Model (EFM) built on Qwen3-VL-8B-Instruct that unifies spatial cognition, task planning/correction, and embodied pointing within a single VLM. Trained on a 15B-token corpus via two-stage SFT+RL with a multi-task balanced reward recipe, it achieves SOTA on 16/24 embodied VLM benchmarks (70.4% average), surpassing Gemini-Robotics-ER-1.5 by 17.0% and GPT-5.4 by 21.7%.

## Problem
Existing embodied models are fragmented: cognition, planning, and grounding are handled by separate specialized models or separate model scales, preventing unified inference. Joint multi-task training suffers from severe convergence conflicts due to heterogeneous output formats (text, coordinates, trajectories). Additionally, most prior EFMs validate only on static embodied QA without testing closed-loop long-horizon autonomy in the physical world.

## Method
**Architecture.** Qwen3-VL-8B-Instruct fine-tuned to output all modalities (language, normalized coordinates in [0,1000], trajectory sequences) as plain-text token sequences. An optional lightweight flow-matching DiT action expert can be attached for continuous action generation (Embodied-R1.5-VLA).

**Data.** Three automated pipelines produce 34 datasets totaling >15B tokens:
1. *ER1.5-Spatial* (~20K): 3D scene graphs from real robot RGB using MoGe-2 depth + Grounded-SAM segmentation + RANSAC plane alignment; programmatically generates spatial QA pairs for tabletop manipulation.
2. *ER1.5-Correction* (~800K): Failure-annotated planning/execution data via five structured perturbation operators (step omission, swap, object error, etc.) applied to correct plans; execution failures simulated via video truncation, description substitution, and physics-engine injection.
3. *ER1.5-Pointing* (~400K): Functional affordance grounding from ManiSkill-PartNet simulation + data restructuring; 2D/3D visual trajectory extraction via projected 3D poses, Detectron2 end-effector tracking, and Co-Tracker3 object tracking.

**Training (two stages).**
- *SFT*: Full-parameter fine-tuning, 1 epoch, AdamW, lr=2×10⁻⁶ cosine, batch=512, context=8192 tokens. Vision encoder unfrozen.
- *RFT (Multi-Task Balanced RL)*: GRPO variant with four key modifications: (i) difficulty-aware filtering retaining ~200K medium-difficulty samples by rollout pass rate; (ii) dynamic masking of degenerate groups (all-same-reward); (iii) global batch reward normalization Â_i = (R_i − μ_group)/(σ_batch + ε), eliminating cross-task reward scale differences without per-task history; (iv) adaptive thinking—no forced reasoning chains, letting the model allocate compute on demand.
- *Reward families*: exact-match (0/1), IoU (bounding box), point-distance decay (φ(d_nn; 40, 150)), trajectory RMSE (φ(RMSE; 50, 120) + depth MAE), semantic similarity (Skywork-Reward-V2-Qwen3-4B mapped via sigmoid).

**PGC Framework.** A single Embodied-R1.5 instance asynchronously serves Planner (long-horizon decomposition + next-step planning), Grounder (pointing/OFG/VTG for spatial grounding), and Corrector (process detection, error localization, replanning) via a minimal FIFO memory buffer, enabling closed-loop long-horizon execution without multi-model cascading.

## Key Contributions
- Single 8B VLM unifying all three embodied capability dimensions (cognition/spatial, planning/correction, pointing/location) via multi-task balanced RL
- Three automated data construction pipelines generating proprietary embodied training data targeting critical gaps (~20K spatial, ~800K correction, ~400K pointing samples)
- Global batch reward normalization scheme (batch-level σ, group-level μ) that resolves inter-task gradient imbalance without per-task moving averages
- PGC closed-loop framework enabling autonomous long-horizon real-robot execution from a single model
- EmbodiedEvalKit: unified four-layer evaluation framework supporting 25+ embodied benchmarks and 20+ models with standardized coordinate parsing and metric computation
- Open-source model weights, training data, training code, and evaluation framework

## Results
- **Embodied VLM benchmarks**: SOTA on 16/24 benchmarks; 70.4% average on 21 main accuracy benchmarks vs. Gemini-Robotics-ER-1.5 (53.4%, +17.0%) and GPT-5.4 (48.7%, +21.7%)
- **Planning & Correction** (RoboVQA / EgoPlan-2 / Cosmos / RoboFAC): 65.3% avg vs. best prior embodied model Mimo-Embodied 54.1%; 61.0 / 53.8 / 69.3 / 77.2 per benchmark
- **Pointing & Location**: outperforms all baselines across 9 pointing benchmarks (table truncated, full numbers not provided in excerpt, but claimed SOTA)
- **Robotic manipulation (VLA)**: 92.4% on SimplerEnv Google Robot Visual Matching, surpassing π0.5 by >20%; outperforms ManipLLM by 11% on PartNet-Mobility (ManiSkill affordance benchmark); LIBERO and RoboTwin2.0 results referenced but not fully excerpted
- **Zero-shot real-robot**: demonstrated on ARX Lift2s, XArm6, RealMan RM75 across instruction following, tool affordance, articulated object manipulation, and long-horizon tasks (qualitative demonstrations)

## Limitations
- FIFO memory buffer in PGC is acknowledged as a minimalist design; more sophisticated memory strategies would likely improve closed-loop performance
- VLA extension still requires some action-specific fine-tuning data, even if "small"; the exact quantity threshold is not quantified
- Zero-shot real-robot evaluation is demonstration-scale (qualitative/selected tasks) rather than large-scale statistically rigorous quantitative evaluation
- Pointing benchmark table is truncated in the excerpt; full comparative numbers not fully visible
- PGC relies on external low-level skill executors for actuation; the framework is not end-to-end from pixels to motor commands

## Relevance to Vision-Language Models
Embodied-R1.5 advances the embodied VLM subfield by demonstrating that a single 8B VLM can internalize physically grounded spatial reasoning, planning, and precise coordinate prediction without architectural specialization—challenging the prevailing assumption that embodied capabilities require separate expert modules or model cascades. The multi-task balanced RL recipe (global batch normalization + difficulty-aware filtering) addresses a fundamental problem for VLMs trained on heterogeneous output formats, with direct implications for any multi-task VLM training effort. The finding that strong embodied reasoning internalization dramatically reduces downstream action data requirements (small-data VLA outperforming large-pretrain baselines like π0.5) is significant for the broader question of how to leverage pretrained VLMs for robotics. EmbodiedEvalKit fills a standardization gap analogous to VLMEvalKit for general VQA, providing reproducible infrastructure for the embodied VLM evaluation community.

## Tags
#vlm #embodied-ai #reinforcement-learning #grounding #vla #multi-task-learning #spatial-reasoning #robotics
