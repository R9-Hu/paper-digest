---
title: "Encoder Winners Do Not Reliably Transfer Across VLA Backbone Scale: A Frozen-Backbone Grafting Diagnostic"
authors: ["Qingping Zeng", "Fei She"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
published_time: "2026-06-12T06:27:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.14153"
url: "http://arxiv.org/abs/2606.14153v1"
pdf: "paper/vlm/[Arxiv 2026] Encoder Winners Do Not Reliably Transfer Across VLA Backbone Scale A Frozen-Backbone Grafting Diagnostic.pdf"
---

# Encoder Winners Do Not Reliably Transfer Across VLA Backbone Scale: A Frozen-Backbone Grafting Diagnostic

*🕒 **Published (v1):** 2026-06-12 06:27 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.14153v1)*

## TL;DR
Vision-language-action (VLA) policies inherit their vision encoders from upstream VLM releases without backbone-specific ablations; this paper asks whether a small-backbone encoder winner transfers to a larger backbone. Using a frozen-backbone grafting diagnostic across SmolVLA-450M and π0.5-3.3B, the authors show that the top-1 encoder choice is backbone-dependent and cannot be safely inferred from small-scale results.

## Problem
Prior VLA encoder studies (e.g., VLM4VLA, SmolVLA-EdgeBench) co-train the encoder with the rest of the policy, confounding encoder quality with backbone-encoder co-adaptation. Practitioners inheriting a released VLA checkpoint (e.g., π0.5) have no controlled evidence about whether the small-VLA top-1 encoder selection holds at larger backbone scale — an expensive wrong choice wastes pretraining compute and corrupts downstream fine-tune curves.

## Method
**Frozen-backbone grafting protocol:** Given a pretrained VLA, the language model, action expert, and original vision tower are all frozen. A candidate encoder is attached via: (1) a frozen pretrained vision encoder (run at 224×224), (2) deterministic AdaptiveAvgPool2d to 8×8 (SmolVLA, 64 tokens) or 16×16 (π0.5, 256 tokens), and (3) a token-wise LayerNorm plus a single trainable linear projector (0.37M–1.58M parameters). Only the projector is trained — AdamW, lr=1e-4, 2,000 steps, effective batch size 8, BF16. Evaluation uses offline action MSE on an episode-split held-out LIBERO validation set (6,457 windows). Closed-loop success is deliberately excluded due to embodiment mismatch (SO-100 checkpoint vs. Franka LIBERO). Four encoders (SigLIP-base/16, DINOv2-small, FastViT-SA12, RepViT-M1) × two backbones (SmolVLA-450M, π0.5-3.3B) × two LIBERO suites (libero_spatial, libero_object) × 2–3 seeds = 40 training runs total.

## Key Contributions
- Demonstrates that the small-backbone encoder winner (SigLIP on SmolVLA) does not reliably select the large-backbone top tier (DINOv2-small leads on π0.5-spatial; π0.5-object is an unstable near-tie band); 3 of 4 backbone-suite comparisons and 11 of 12 seed-level cells support backbone-dependent rankings.
- Releases an open encoder-swap grafting harness for SmolVLA and π0.5 that hooks the vision pathway at a single point, enabling cheap per-target-backbone encoder selection before committing at scale.
- Establishes offline action-MSE on episode-split held-out windows as a usable diagnostic signal when closed-loop rollout is blocked by embodiment mismatch, a common regime as VLAs ship without matched simulators.
- Shows that standard encoder metadata (ImageNet accuracy, parameter count, latency) cannot identify the top-1 encoder across both backbones — DINOv2 wins π0.5-spatial despite being neither largest nor slowest; ImageNet accuracy even flips sign across π0.5 suites.

## Results
- **SmolVLA (450M), libero_spatial:** SigLIP best (MSE 0.0706 ± 0.0020), DINOv2 +0.0028, FastViT +0.0223, RepViT +0.0850.
- **SmolVLA (450M), libero_object:** SigLIP best (0.0628 ± 0.0022), DINOv2 +0.0047.
- **π0.5 (3.3B), libero_spatial:** DINOv2 best (0.0256 ± 0.0016), SigLIP +0.0011 (+4% relative), FastViT +0.0027 — rank order inverts vs. SmolVLA.
- **π0.5 (3.3B), libero_object:** Near-tie band — SigLIP 0.02149, DINOv2 0.02166, FastViT 0.02206 (all within 2.7% relative); top-1 identity unstable to seed perturbation.
- **Native anchor comparison:** Grafted SigLIP is +30–32% higher MSE than SmolVLA's native tower; grafted DINOv2/SigLIP is −42–43% lower MSE than π0.5's native PaliGemma SigLIP-So400m tower — the sign flips across backbones.
- **Cross-backbone Spearman ρ:** +0.800 (spatial), +1.000 (object) — positive because the bottom (RepViT worst on both) transfers; top-1 does not.
- **P2 LoRA ablation:** Run to check whether projector-only training inflates ranking sensitivity; results confirm the main-matrix pattern (details suppressed here due to text truncation).
- **Compute:** SmolVLA cell ≈ 9 min / 1.85 GB GPU; π0.5 cell ≈ 5 GPU-hours / 14.7 GB GPU.

## Limitations
- Evaluation is offline action-MSE only; no closed-loop success rates are reported due to embodiment mismatch (SO-100 checkpoint vs. Franka LIBERO), so deployment relevance is indirect.
- Only 2–3 seeds per cell; with N=4 encoders, rank correlations and sign tests have very low power and are reported descriptively only.
- The grafting harness itself is non-neutral: the fixed adaptive-avg-pool + single-projector protocol penalizes SmolVLA grafts (+45–56% MSE over native) and coincidentally benefits π0.5 grafts (−50–52% vs. native), so all rankings are conditional on this protocol rather than encoder quality in isolation.
- All encoders use a unified 224×224 preprocessing path, not their official per-encoder preprocessing; rankings may shift under per-encoder input pipelines.
- Only four sub-100M encoders tested; larger encoders (DINOv2-Giant, SigLIP-Large) are excluded to keep compute manageable.
- Only two VLA backbones and two LIBERO suites; generalization to other backbones, tasks, or real-world rollouts is untested.
- Native-vs-grafted sign reversal cannot be attributed causally to backbone scale — SmolVLA and π0.5 differ in language backbone, action expert, hidden size, native vision tower architecture, and pretraining data.

## Relevance to Vision-Language Models
This paper directly interrogates a core engineering assumption in VLA construction: that a vision encoder validated on one VLM-derived backbone transfers across backbone scales. For researchers tracking VLMs, the finding that SigLIP (the dominant VLM vision encoder, used in PaliGemma and inherited by π0.5) is not the top-1 encoder when grafted onto the larger π0.5 backbone challenges the common practice of inheriting upstream VLM encoder choices without ablation. The frozen-grafting diagnostic methodology is immediately applicable to any VLM-derived architecture that exposes a single visual entry point, and the negative result on encoder metadata predictivity (ImageNet accuracy, parameter count, latency all fail to predict top-1) underscores that VLM-scale encoder rankings do not automatically transfer to downstream grounded tasks like robot manipulation.

## Tags
#vla #vision-encoder #encoder-selection #backbone-scale #transfer #robotics #siglip #dinov2
