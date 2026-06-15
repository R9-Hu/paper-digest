---
title: "Hy-Embodied-0.5-VLA: From Vision-Language-Action Models to a Real-World Robot Learning Stack"
authors: ["He Zhang", "Lingzhu Xiang", "Haitao Lin", "Zeyu Huang", "Minghui Wang", "Dingyan Zhong", "Yubo Dong", "Yihao Wu", "Yongming Rao", "Dongsheng Zhang", "Wanjia He", "Ling Chen", "Kai Huang", "Jiahao Chen", "Sichang Su", "Xumin Yu", "Ziyi Wang", "Chengwei Zhu", "Xiao Teng", "Yuchun Guo", "Yufeng Zhang", "Yuandong Liu", "Rui Wang", "Zisheng Lu", "Han Hu", "Zhengyou Zhang"]
source: "HuggingFace"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14409"
url: "https://huggingface.co/papers/2606.14409"
pdf: "paper/vlm/[HuggingFace 2026] Hy-Embodied-0.5-VLA From Vision-Language-Action Models to a Real-World Robot Learning Stack.pdf"
---

# Hy-Embodied-0.5-VLA: From Vision-Language-Action Models to a Real-World Robot Learning Stack

## TL;DR
HyVLA-0.5 is an end-to-end Vision-Language-Action system from Tencent that covers the full robot learning stack: custom data collection hardware, a 4B MoT-based VLM backbone with a flow-matching action expert, two SFT tracks for intra- and cross-embodiment transfer, and a reward-free offline RL stage (FlowPRO) that converts operator interventions into policy improvements. The system is pre-trained on 10K hours of egocentric bimanual demonstrations collected with sub-millimeter optical motion capture, then deployed across five heterogeneous real-robot platforms using an asynchronous inference pipeline with Bézier chunk stitching for C¹-continuous control.

## Problem
Existing VLA approaches treat model design in isolation, leaving three compounding gaps: (1) conventional teleoperation and SLAM-based handheld rigs provide coarse or noisy action labels ill-suited for dexterous manipulation; (2) general-purpose VLM backbones lack spatial priors for dense robot control, and standard imitation learning stalls at last-mile dexterity; (3) high-quality policies are rarely co-designed with deployment constraints (cross-embodiment transfer, real-time closed-loop frequency), causing the embodiment gap, control gap, and perception gap to remain unaddressed in a unified way.

## Method
**Data.** A custom fingertip UMI gripper is tracked by an external optical motion-capture cage, labeling each 6-DoF trajectory at sub-millimeter precision in a global Cartesian frame—replacing SLAM-based pose estimation. The gripper uses finger-attached actuation with optional 6-DoF force-torque sensors at the tips. This produces the Hy-UMI-10K corpus: >1M episodes, >10K hours, 70 tasks across six scene families.

**Architecture.** The backbone is Hy-Embodied-0.5-MoT, a 4B Mixture-of-Transformers VLM with modality-adaptive QKV/FFN parameters and native-resolution Hy-ViT 2.0 encoding. A dual-tower flow-matching action expert (370M parameters) generates continuous action chunks via conditional flow matching with block-wise causal attention separating perception, state, and noisy-action token blocks. A parameter-free compact memory encoder inserts factorized temporal-spatial attention every L layers to compress a K-frame history into single-frame token counts without adding new weights.

**Action representation.** Delta-chunk: incremental 10-D end-effector poses (3-D translation + 6-D rotation + 1-D gripper) per arm, expressed relative to the current EEF frame. This decouples policy learning from robot-specific kinematics.

**SFT.** Two tracks from the UMI pre-trained checkpoint: Track-A (intra-embodiment, teleoperation on the target robot) and Track-B (cross-embodiment, UMI-only fine-tuning deployed to morphologically different robots without target-robot teleoperation). K=6 frames used at SFT.

**RL post-training (FlowPRO).** An iterative offline RL loop using Proximalized Preference Optimization (PRO) adapted for flow matching. An operator performs teleoperated intervention-and-rollback during policy rollouts to produce paired (positive, negative) trajectory segments. Smooth Interpolation synthesizes missing per-state counterparts via cubic Bézier/Slerp to form dense (s, aʷ, aˡ) tuples. The RPRO loss = λ_PRO · L_PRO + λ_SFT · L_SFT, where L_PRO contains a contrastive term and a symmetric proximal regularizer that prevents reward hacking. No reward or critic model is trained.

**Deployment.** A producer-consumer asynchronous loop decouples VLM inference from servo execution. Successive delta chunks are stitched with a latency-aware cubic Bézier connector enforcing C¹-continuous transitions. A platform mapper converts delta-EEF outputs to embodiment-specific joint commands via IK.

## Key Contributions
- Custom fingertip UMI rig with optical motion-capture achieving sub-millimeter action labeling, producing Hy-UMI-10K (>10K hours, 70 tasks).
- Compact memory encoder extending a single-image ViT to video via parameter-free factorized temporal-spatial attention; reduces to the pretrained ViT when K=1.
- Delta-chunk EEF action representation enabling embodiment-agnostic policy learning and cross-embodiment deployment.
- FlowPRO: reward-free, critic-free offline RL algorithm adapting PRO to continuous flow-matching policies with a proximal regularizer that structurally prevents reward hacking.
- Two-track SFT protocol (Track-A intra-embodiment, Track-B cross-embodiment UMI-only transfer) evaluated on five real-robot platforms.
- Asynchronous inference + Bézier stitcher enabling high-frequency closed-loop control despite VLM backbone latency.

## Results
- **RoboTwin 2.0 simulation (50 tasks, Aloha-AgileX bimanual):** HyVLA-0.5 is evaluated against benchmark baselines on the RoboTwin 2.0 suite; specific aggregated scores are referenced but not fully enumerated in the provided text excerpt.
- **Track-A real-robot (Dobot X-Trainer, 4 tasks):** Results reported in Sec. 6 (not included in the provided excerpt).
- **Track-B cross-embodiment (JAKA K1, Astribot S1):** Deployed from UMI-only fine-tuning without target-robot teleoperation; qualitative success reported.
- **FlowPRO (4 bimanual tasks: Bottle, Cap, USB, Zip):** Drives success rates toward "near-ceiling" in Sec. 6.3; specific per-task numbers not included in the provided excerpt.
- Pre-training corpus: >1M episodes, 10K hours; action expert: 370M parameters; action chunk horizon H=50 at 10 Hz during pre-training, 50 Hz at deployment.

## Limitations
- Optical motion-capture cage is lab-bound: superior label accuracy comes "at the cost of inconvenient in-the-wild deployment."
- Depth (RGB-D) data captured but not used in the current training version; reserved for future work.
- Cross-embodiment Track-B heuristically infers chassis/torso frames for humanoids rather than predicting them, and the 24 head/torso DOFs are not learned by the policy.
- FlowPRO requires a human operator to perform intervention-and-rollback during real-robot rollouts; scalability of this data pipeline is not quantified.
- Specific benchmark numbers (success rates per task, comparison to named baselines) are in sections not fully provided in the text excerpt, limiting external reproducibility assessment from this report alone.

## Relevance to Vision-Language Models
HyVLA-0.5 demonstrates how a VLM backbone (Mixture-of-Transformers, 4B parameters) can be efficiently adapted for physical control by adding a co-trained flow-matching action head while preserving VQA and spatial grounding capabilities via auxiliary next-token prediction—directly relevant to the question of how VLMs transfer to embodied settings without catastrophic forgetting. The delta-chunk EEF representation and modality-adaptive MoT design provide a concrete recipe for decoupling language/vision understanding from action generation within a single transformer, advancing the VLA-as-specialized-VLM paradigm. The FlowPRO post-training method offers a reward-free alternative to RLHF-style alignment for continuous-action VLMs, complementing preference optimization work in language-only settings. For VLM researchers, the cross-embodiment transfer results (Track-B) substantiate that strong spatiotemporal VLM representations can generalize across robot morphologies without task-specific robot data collection.

## Tags
#vla #vlm #embodied-ai #robot-learning #flow-matching #preference-optimization #cross-embodiment #manipulation
