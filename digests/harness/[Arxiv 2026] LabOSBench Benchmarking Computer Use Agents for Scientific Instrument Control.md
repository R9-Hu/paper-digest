---
title: "LabOSBench: Benchmarking Computer Use Agents for Scientific Instrument Control"
authors: ["Anqi Zou", "Han Deng", "Chengyu Zhang", "Junquan Hu", "Yu Wang", "Yuxiang Xing", "Aokai Zhang", "Hanling Zhang", "Zhaoyang Liu", "Ben Fei", "Zhihui Wang", "Wanli Ouyang"]
source: "Arxiv"
venue: ""
published: "2026-06-15"
published_time: "2026-06-15T14:42:33+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.16802"
url: "http://arxiv.org/abs/2606.16802v1"
pdf: "paper/harness/[Arxiv 2026] LabOSBench Benchmarking Computer Use Agents for Scientific Instrument Control.pdf"
---

# LabOSBench: Benchmarking Computer Use Agents for Scientific Instrument Control

*🕒 **Published (v1):** 2026-06-15 14:42 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.16802v1)*

## TL;DR
LabOSBench is a browser-based benchmark of 96 subtasks across eight simulated scientific instrument GUIs (SEM, TEM, FIB, XRD, SPM, LFM, EDS, APT) for evaluating multimodal computer-use agents without OS-level virtualization. It reveals that current agents handle discrete GUI subtasks reasonably well but collapse on feedback-driven closed-loop control and long-horizon workflows, with GPT-5.5 via GTA1 achieving the best subtask score (0.814) yet only 26.3% end-to-end success.

## Problem
Existing computer-use benchmarks (OSWorld, WebArena) either require heavy VM virtualization or cover only generic web navigation—neither captures the procedural dependencies, dense domain-specific controls, continuous parameter tuning, and feedback-driven visual adjustment required for scientific instrument operation. Directly evaluating agents on physical instruments is impractical due to cost, safety, and reproducibility constraints.

## Method
LabOSBench runs entirely in a standard browser via Playwright, eliminating VM overhead. Eight high-fidelity JavaScript/HTML instrument simulators are instrumented with per-instrument benchmark scripts (e.g., `benchmark_xrd.js`) that record subtask completion, control attempts, and step-level traces. A Python coordinator drives a closed-loop observe–act–execute protocol: agent receives screenshot + NL instruction → outputs a GUI action (click, drag, type, scroll, key, wait) → Playwright executes it → coordinator captures next screenshot and queries in-page state. Evaluation runs in two modes: (1) **full-episode** from initial state within a step budget, and (2) **subtask-level** with fast-forward initialization to the canonical pre-subtask state (e.g., `XRD_fast_forward_to_subtask(Sk)`). Subtask success rates are averaged per instrument; image-producing tasks also report PSNR against a reference micrograph.

## Key Contributions
- Browser-native, OS-virtualization-free benchmark infrastructure using Playwright + in-page JS hooks + JSON Schema episode contracts
- 96 subtasks decomposed from real scientific operating procedures across 8 instrument simulators spanning microscopy, diffraction/spectroscopy, and micro-nanofabrication paradigms
- Dual evaluation protocol (subtask-level with fast-forward isolation vs. full end-to-end episode) enabling separation of local grounding failures from long-horizon error accumulation
- PSNR-based intermediate scientific-state quality metric for image-producing tasks beyond binary success
- Systematic evaluation of 12 agents: general VLMs, specialized GUI models (UI-TARS-1.5-7B, GUI-Owl-7B), and agentic frameworks (GTA1, VLAA-GUI, Hippo Agent)

## Results
- **Best subtask average**: GTA1 w/ GPT-5.5 at 0.814; human baseline at 0.924
- **Best single model**: Seed-1.6 at 0.763 among general-purpose VLMs
- **End-to-end (GPT-5.5, 10 runs/workflow)**: 26.3% average vs. ~72.6% subtask-level — severe error accumulation; non-zero success only on EDS (70%), APT (80%), XRD (60%); zero on SEM, SPM, TEM, LFM, FIB
- **Easiest instruments**: EDS and XRD (structured, short workflows, clear feedback)
- **Hardest instruments**: FIB (longest workflow, lowest average model SR), LFM (largest human–model gap due to feedback-driven optical adjustment)
- VLAA-GUI w/ Opus-4.5 (0.456) underperforms plain Opus-4.5 (0.620), showing agent loops hurt when recovery strategies conflict with instrument semantics
- Specialized GUI models (UI-TARS-1.5-7B: 0.659, GUI-Owl-7B: 0.640) do not outperform strong VLMs overall

## Limitations
- Simulators cannot replicate hardware latency, calibration uncertainty, safety interlocks, or real failure modes of physical instruments
- Coverage restricted to eight instruments from microscopy, spectroscopy, diffraction, and tomography; excludes wet-lab, robotic manipulation, chemical synthesis, or multi-instrument planning
- Evaluation relies on screenshots and logged simulator states; excludes richer multimodal sensor signals or domain-knowledge bases that may be needed for harder tasks
- Subtask success is binary; partial-credit or trajectory-quality metrics are absent except for PSNR on SEM

## Relevance to Harnesses / Meta-Harnesses
LabOSBench is itself a harness: a Python coordinator wraps per-instrument JS benchmark scripts under a unified CLI-configurable observe–act–execute loop with structured JSON Schema episode contracts, making it a concrete example of a domain-specific evaluation harness layered over browser automation. The fast-forward initialization mechanism—programmatically teleporting simulator state to a subtask entry point—mirrors harness-level state injection patterns relevant to meta-harnesses that need to isolate sub-agent capabilities. The dual-mode design (subtask-isolated vs. full-episode) is a direct precedent for harnesses that must both unit-test individual agent steps and run full end-to-end orchestration, a core design tension in meta-harness architecture.

## Tags
#benchmark #computer-use-agents #gui-agents #evaluation-harness #browser-automation #scientific-workflows #multimodal #long-horizon
