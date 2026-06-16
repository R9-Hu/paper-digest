---
title: "Semantic Flip: Synthetic OOD Generation for Robust Refusal in Embodied Question Answering and Spatial Localization"
authors: ["Dongbin Na", "Chanwoo Kim", "Giyun Choi", "Dooyoung Hong"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T16:07:24+00:00"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.16898"
url: "http://arxiv.org/abs/2606.16898v1"
pdf: "paper/agentic-ai/[Arxiv 2026] Semantic Flip Synthetic OOD Generation for Robust Refusal in Embodied Question Answering and Spatial Localization.pdf"
---

# Semantic Flip: Synthetic OOD Generation for Robust Refusal in Embodied Question Answering and Spatial Localization

*🕒 **Published (v1):** 2026-06-15 16:07 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16898v1)*

## TL;DR
Semantic Flip is a framework that synthesizes out-of-distribution (OOD) training pairs for embodied agents by independently corrupting either the language query (Q-Flip) or the visual memory (V-Flip), then training a lightweight MLP rejection gate on top of a frozen VLM to detect unanswerable queries. It achieves F1=0.7110 on AbstainEQA and F1=0.9559 on the newly introduced SpaceReject benchmark, outperforming 32B prompted baselines using only a frozen 7B encoder.

## Problem
Embodied VLMs (e.g., memory-augmented navigation agents like ReMEmbR and Meta-Memory) hallucinate confident answers—including navigation coordinates—for queries that lack visual grounding. Existing approaches (prompt-based refusal, supervised fine-tuning, CoT) fail: prompting is brittle, fine-tuning requires curated OOD annotations that don't exist at deployment, and CoT tends to rationalize plausible answers rather than abstain. The core gap is learning to detect ungroundability without any manually labeled unanswerable training examples.

## Method
Given an answerable in-distribution pair (Q, V), Semantic Flip constructs two synthetic OOD distributions:
- **Q-Flip**: Keeps video V intact, rewrites Q via a frozen LLM into an ungroundable variant—referential underspecification (ambiguous head noun), false premise, or subjective judgment. A coarse variant requires no taxonomy assumption; the fine variant targets three of five AbstainEQA categories to test generalization.
- **V-Flip**: Keeps Q intact, removes the target referent from every video frame via a spaCy parse → Grounding-DINO detection → LaMa inpainting pipeline.

Both corrupted pairs receive label `abstain=1`. A frozen Qwen2.5-VL-7B encoder produces joint (Q,V) embeddings; only a 3-layer MLP classification head is trained with class-weighted binary cross-entropy over `D_ID ∪ D_Q-Flip ∪ D_V-Flip`. At inference, the gate triggers abstention when `g_θ(Q,V) > 0.5`. For spatial localization, the gate is inserted as a fourth in-loop tool inside Meta-Memory's reasoning cycle (configuration C2).

## Key Contributions
- **Semantic Flip framework**: annotation-free synthetic OOD generation via single-axis modality corruption (Q-Flip + V-Flip) with a frozen-encoder lightweight rejection gate.
- **SpaceReject benchmark**: extends SpaceLocQA with 135 unanswerable queries (68 Object-Absent, 67 Visually-Unavailable) over six campus video sequences for spatial-localization refusal evaluation.
- **SpaceReject Extra**: large-scale extension with 2,520 OOD queries across all six sequences, covering all five AbstainEQA abstention categories (84 queries/category/sequence).
- Zero-shot generalization: gate trained on three abstention categories achieves 0.89 recall on unseen "Information Unavailability" category, suggesting structural rather than lexical abstention signal.

## Results
- **AbstainEQA (HM3D-380)**:
  - Semantic Flip (7B + MLP head): F1=0.7110, BalAcc=0.6684, Recall=0.8158, Spec=0.5211
  - Best prompt baseline (Qwen-32B-Coarse): F1=0.6746 — Semantic Flip exceeds by +3.6 pp
  - Naive CoT (Qwen-32B-Fine + CoT): collapses Recall from 0.95→0.20, F1=0.3099
- **SpaceReject (135 ID + 135 OOD)**:
  - Semantic Flip (Q-Flip+V-Flip): F1=0.9559, BalAcc=0.9563, Recall=0.9467, Spec=0.9659
  - Best prompt baseline (C2 Tool, Qwen3-8B): F1=0.8874 — Semantic Flip exceeds by ~+0.07
  - Q-Flip alone: F1=0.9494; V-Flip alone: F1=0.6867 (V-Flip adds calibration, Q-Flip dominates)
- Spatial navigation baselines before Semantic Flip: ReMEmbR mean Euclidean error 28.5 m, Meta-Memory 21.7 m on NaVQA.

## Limitations
- The fused (Q,V) embedding produces a single consistency signal—cannot attribute abstention to an ungrounded query vs. a missing visual referent, limiting cause-specific user feedback.
- Weakest abstention categories remain at 0.68–0.69 recall (Referential Underspecification, Actionability Limitation).
- V-Flip quality depends on detector (Grounding-DINO) and inpainter (LaMa) accuracy; inpainting artifacts can weaken the perceptual signal.
- SpaceReject is limited to campus indoor/outdoor environments (six sequences); generalization to other deployment domains is untested.

## Relevance to Agentic AI / LLM Agents
Robust abstention—knowing when not to act—is a foundational safety property for embodied agents that physically operate in the world; a navigation agent that commits to an arbitrary coordinate is a safety hazard, not merely a QA error. Semantic Flip offers a practical, plug-in solution that requires no modification to the underlying reasoning pipeline and no curated OOD data, making it directly deployable on top of existing memory-augmented agents (e.g., Meta-Memory, ReMEmbR). The finding that CoT reasoning actively degrades abstention is an important negative result for the broader agentic AI community, which has broadly adopted CoT as a reliability tool. The freeze-encoder + lightweight head paradigm generalizes to any VLM-backed agent pipeline, connecting to the growing line of work on selective prediction and uncertainty-aware LLM agents.

## Tags
#embodied-agents #abstention #ood-detection #vlm #spatial-reasoning #robot-navigation #selective-prediction #benchmark
