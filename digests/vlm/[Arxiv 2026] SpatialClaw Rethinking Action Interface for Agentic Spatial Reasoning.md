---
title: "SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning"
authors: ["Seokju Cho", "Ryo Hachiuma", "Abhishek Badki", "Hang Su", "Byung-Kwan Lee", "Chan Hee Song", "Sifei Liu", "Subhashree Radhakrishnan", "Seungryong Kim", "Yu-Chiang Frank Wang", "Min-Hung Chen"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Vision-Language Models"
topic_slug: "vlm"
canonical_id: "arxiv:2606.13673"
url: "http://arxiv.org/abs/2606.13673v1"
pdf: "paper/vlm/[Arxiv 2026] SpatialClaw Rethinking Action Interface for Agentic Spatial Reasoning.pdf"
---

# SpatialClaw: Rethinking Action Interface for Agentic Spatial Reasoning

## TL;DR
SpatialClaw is a training-free framework that replaces single-pass code execution and structured tool-call interfaces in spatial reasoning agents with a persistent, multi-turn Python kernel. A VLM-backed agent writes one executable cell per step, inspects intermediate outputs (masks, depth maps, plots), and revises its geometric analysis before committing an answer. Evaluated on 20 spatial benchmarks with six backbone models, it achieves 59.9% average accuracy, outperforming the prior best spatial agent by +11.2 points.

## Problem
Existing tool-augmented spatial agents are bottlenecked by their action interface. Single-pass code execution commits to a complete analysis strategy before observing any intermediate result; structured tool-call interfaces (JSON/XML) cannot express test-time compositions (e.g., chaining segmentation masks with KD-tree nearest-neighbor search) because those compositions are not anticipatable by a fixed API. Neither interface supports the open-ended, multi-step geometric reasoning that 3D/4D spatial tasks require.

## Method
SpatialClaw instantiates "code as the action interface" via a five-stage agentic loop over a persistent Python kernel:

1. **Persistent kernel workspace**: Initialized once per example, pre-loaded with `InputImages`, `Metadata`, perception tools (`tools.Reconstruct` wrapping Depth Anything 3, `tools.SAM3` for segmentation), scientific libraries (NumPy, SciPy, Matplotlib), a `show()` hook for visual feedback, a `vlm` sub-session for grounding/commonsense queries, and `ReturnAnswer()` for termination.
2. **Planning (Stage I)**: A separate LLM session (no images, no code) generates an analysis plan; it is injected into the main agent's system prompt.
3. **Code generation (Stage II)**: The main VLM writes one Python cell per step (purpose / reasoning / next-goal / code fields), conditioned on all prior stdout, variable summaries, and intermediate images.
4. **Code execution (Stage III)**: AST-level static checker rejects unsafe modules; validated cell runs in the persistent kernel.
5. **Feedback assembly (Stage IV)**: stdout, tracebacks, variable type/shape summaries, and `show()`-registered images are appended to the model context for the next step.
6. **Answer submission (Stage V)**: Loop terminates when `ReturnAnswer()` produces a format-valid answer or step count reaches $N_{\max}=30$.

The system prompt encodes general spatial reasoning discipline (prefer metric computation over pixel-level impression, visually verify masks, sanity-check magnitudes) without benchmark- or model-specific templates.

## Key Contributions
- Identification of the **action interface** as a critical, underexplored axis for spatial reasoning agent performance, distinct from tool coverage or model capacity.
- **SpatialClaw**: a training-free persistent-kernel agent that enables iterative composition, inspection, and revision of perception outputs using arbitrary Python/NumPy/SciPy operations.
- **Comprehensive evaluation** across 20 spatial reasoning benchmarks spanning single-image, multi-view, video/4D, and general video understanding categories, with six open-source VLM backbones (Qwen3.5/3.6 27B–397B, Gemma4 26B–31B).
- **Ablation and analysis** isolating the action interface contribution (+2.7 pp over no-tool even without perception tools) and showing spontaneous, task-adaptive primitive selection without prompt engineering.

## Results
- **Overall**: 59.9% average accuracy across 20 benchmarks (Gemma4-31B backbone); +11.2 pp over SpaceTools-Toolshed (best prior spatial agent using same backbone).
- **vs. No-tool baseline**: consistent gains across all six backbone models; largest on video spatial & 4D reasoning (e.g., DSI-Bench avg. +18.3 pp) and multi-view reasoning (MindCube avg. +14.3 pp).
- **Action interface comparison** (same toolset, same backbone):
  - No-tool: 53.4% | Single-pass code: 55.2% | Structured tool-call: 56.7% | SpatialClaw: **59.9%**
- **vs. specific baselines** (Gemma4-31B): VADAR ~38% (no video support), pySpatial 48.7%, SpaceTools 48.7% → SpatialClaw 59.9%.
- **Win rate**: SpatialClaw wins 11/13 task meta-categories over both single-pass code and structured tool-call; largest gains on Camera motion (+9.0 pp over structured, +7.2 pp over single-pass), Multi-view/viewpoint (+7.7 pp / +9.1 pp), Relative direction (+6.3 pp / +9.1 pp).
- **Ablation**: Removing utility wrappers (keeping only SAM3/DA3 + numpy/scipy) loses <1 pp on average (52.5% vs. 56.0% on subset), confirming kernel expressiveness compensates for absent wrappers. Removing perception tools entirely still yields +2.7 pp over no-tool baseline.

## Limitations
- No training or fine-tuning; performance is bounded by the backbone VLM's code generation quality and the quality of underlying perception tools (Depth Anything 3, SAM3).
- Large models required: backbones range from 26B to 397B parameters, making deployment expensive.
- Gains are smaller on tasks already near-saturated by the backbone (visual recognition: +0.1–1.7 pp over structured tool-call); the interface cannot compensate for perception saturation ceilings.
- Evaluation caps samples at 1,000 per benchmark for large benchmarks, potentially underrepresenting tail distributions.
- Spatial planning and size estimation show small or negative margins over structured tool-call (−1.3 pp and −4.7 pp respectively), suggesting the interface is not universally superior.
- The persistent kernel incurs multi-step inference overhead (up to $N_{\max}=30$ turns), which is not analyzed in terms of latency or cost.

## Relevance to Vision-Language Models
SpatialClaw directly addresses a known failure mode of VLMs in geometric and spatial reasoning, demonstrating that the action interface—not just model scale or tool availability—determines agent capability. For VLM researchers, this is a clean empirical result: a code-as-interface design yields +11.2 pp over structured tool-call agents across 20 benchmarks and six backbone families without any fine-tuning, isolating the interface as the explanatory variable. The finding that gains are consistent across Qwen3.5/3.6 and Gemma4 architectures (27B–397B) is directly relevant to practitioners evaluating which VLM backbone to deploy for agentic spatial tasks. The work also raises an open question about how future VLMs might internalize similar iterative geometric reasoning natively rather than via external kernel scaffolding.

## Tags
#vlm #spatial-reasoning #tool-augmented-agents #code-as-action #agentic-reasoning #3d-understanding #video-understanding #benchmark
