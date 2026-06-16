---
title: "OmniGameArena: A Unified UE5 Benchmark for VLM Game Agents with Improvement Dynamics"
authors: ["Mingxian Lin", "Shengju Qian", "Yuqi Liu", "Yi-Hua Huang", "Yiyu Wang", "Wei Huang", "Yitang Li", "Fan Zhang", "Zeyu Hu", "Lingting Zhu", "Xin Wang", "Xiaojuan Qi"]
source: "HuggingFace"
venue: ""
published: "2026-06-08"
published_time: "2026-06-08T00:00:00+00:00"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.09826"
url: "https://huggingface.co/papers/2606.09826"
pdf: "paper/vlm/[HuggingFace 2026] OmniGameArena A Unified UE5 Benchmark for VLM Game Agents with Improvement Dynamics.pdf"
---

# OmniGameArena: A Unified UE5 Benchmark for VLM Game Agents with Improvement Dynamics

*🕒 **Published (v1):** 2026-06-08 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.09826)*

## TL;DR
OmniGameArena is a real-time benchmark of twelve custom Unreal Engine 5 games spanning Solo, PvP, and Coop regimes, designed to evaluate VLM agents under matched conditions across heterogeneous agent classes. Beyond single-shot cold-start scores, the paper introduces the Improvement Dynamics Curve (IDC), a multi-round agentic-reflection harness where a tool-using reflector LLM autonomously refines a bounded skill prompt between play rounds. Key findings show no single VLM dominates across games, and origin-task improvement from reflection does not reliably predict transfer to held-out task variants.

## Problem
Existing game benchmarks for VLM agents report a single first-attempt score per (agent, game) pair, making it impossible to measure how agents improve under repeated interaction. They also skew toward single-agent Solo play, underrepresenting adversarial (PvP) and cooperative (Coop) regimes that probe qualitatively different capabilities (opponent modeling, role assignment, recovery from teammate errors). Additionally, most benchmarks reuse commercial titles, exposing evaluations to pre-training contamination.

## Method
**Benchmark construction.** Twelve games were built from scratch in Unreal Engine 5—7 Solo, 3 PvP, 2 Coop—with unified keyboard-mouse and gamepad action interfaces. All scores are normalized to [0,1]. Games are verified against pre-training contamination via a two-test analysis (visual recognition rate, mechanics leakage rate using Gemini as a probe model).

**Per-episode harness.** At each step the environment returns an RGB frame plus metadata; VLMs emit chunked keyboard-mouse actions. A bounded sliding window of L observation-response pairs constitutes the agent's visual-action history.

**Improvement Dynamics Curve (IDC).** An outer reflection loop runs R rounds, each with K episodes. After each round, a reflector LLM (same model as the player) with sandboxed read-only tool access (list_dir, read_text, read_image, grep) autonomously executes four stages: Explore (selects which trajectory content to inspect), Diagnose (commits explicit failure modes via submit_diagnosis), Validate (proposes an updated skill prompt, verified by an independent LLM judge; up to 5 retries), and Distill (finalizes skill prompt mr+1 ≤1200 tokens and optionally edits a 2000-token persistent notebook). Best-skill rollback resets to the cached best skill mr* when the new round score drops below α=0.5 of the historical best. The final output per (agent, game) is the score sequence [S0,...,SR] (the IDC) plus transfer scores on three held-out task variants.

## Key Contributions
- **OmniGameArena**: twelve custom UE5 games spanning Solo/PvP/Coop with unified action interfaces and proactive contamination avoidance (0.0% visual recognition rate vs. 66.7–100% for prior benchmarks).
- **IDC harness**: agentic-reflection framework with autonomous tool-use reflector, four-stage refinement (Explore→Diagnose→Validate→Distill), persistent memory module, and best-skill rollback.
- **Empirical study** across 12 agents (8 commercial VLMs, 2 open-weight Qwen3.5 MoE, 2 specialized game policies) revealing game-specific leadership rotation, a large commercial-vs-open-weight gap, and dissociation between origin-task IDC gain and held-out variant transfer.

## Results
**Cold-start leaderboard (Solo):**
- No single model dominates: GPT-5.5 leads 4/7 games; Claude Opus 4.6 leads CueChase (0.840 vs. next 0.580); Gemini 3.1 Pro leads MonsterShoot (0.710 vs. next 0.464).
- Newer ≠ better: Claude Opus 4.6 outperforms Opus 4.7 on 5/7 Solo games; GPT-5.4 exceeds GPT-5.5 on SceneEscape.
- Open-weight VLMs (Qwen3.5-397B-A17B, 122B-A10B) score below 0.15 on every Solo game, exactly 0.00 on several.
- Specialized policies (NitroGen gamepad, Open-P2P keyboard-mouse) collapse to near zero on nearly all games.

**PvP:** SkyDuel and CrystalGuard show transitive dominance tracking Solo rankings; MidlineClash is non-transitive (Kimi K2.5 beats Claude Opus 4.6 at 1.00 win rate despite Claude's superior Solo ranking).

**Coop:** GPT-5.5 leads both games; best scores are 0.368 (SharedFloor) and 0.184 (HandoffRun); both Qwen3.5 checkpoints score exactly 0.000 on both Coop games.

**IDC (LastStand, SharedFloor; R=10, K=5 per round, 4 agents):**
- All four agents improve over Round 0 baseline on both games.
- LastStand best-round gains: +0.54 to +0.70 in survival fraction (+130% to +437% relative).
- SharedFloor best-round: 1–4 additional completed orders per episode (+5% to +50% relative).
- Peak performance reached mid-curve, not at Round 10; Opus models lose 0.40–0.52 between best and final round on LastStand.

**Transfer (IDC best skill → 3 held-out variants):**
- SharedFloor: 16/16 variant scores positive (+6% to +56%), as skills encode coordination heuristics rather than spatial memory.
- LastStand: highly variable; GPT-5.5 transfers positively on all 3 variants (+79% on VAR2) despite the smallest origin gain (+130%); Opus 4.7 gains +201% on origin but transfers negatively on every variant.
- VAR2 (cluster tile drops) causes Opus models to collapse (−72%, −76%) due to movement-minimizing policies that exploit single-tile structure.

## Limitations
- IDC experiments cover only 2 of 12 games (LastStand and SharedFloor) and 4 of 12 agents due to compute constraints.
- Only 3 held-out variants per game; broader variant diversity is untested.
- Reflector and player use the same underlying model; asymmetric setups (weak player + strong reflector) are unexplored.
- Single bounded skill prompt replaces the prior skill each round rather than accumulating a skill library (Voyager-style library extensions are noted as future work).
- PvP games excluded from IDC, so reflection under adversarial pressure is unmeasured.

## Relevance to Vision-Language Models
OmniGameArena provides a contamination-controlled, multi-regime testbed that stress-tests capabilities VLMs are increasingly expected to exhibit in agentic deployment: real-time visual grounding, spatial navigation, planning under delayed rewards, opponent modeling, and multi-agent coordination. The IDC framework directly measures whether frozen-weight VLMs can leverage agentic self-reflection for skill acquisition—a key question for the field—and reveals that origin-task improvement and out-of-distribution transfer are dissociable, challenging the assumption that a single leaderboard score characterizes an agent's adaptability. The finding that commercial VLMs hold a large gap over open-weight models and specialized policies, combined with non-transitive PvP rankings and near-zero Coop performance even for top models, provides concrete diagnostic signal for where current VLM architectures and training regimes fall short in interactive, embodied settings.

## Tags
#vlm #benchmark #game-agents #agentic-reflection #self-improvement #multi-agent #embodied-ai #evaluation
