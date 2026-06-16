---
title: "TVIR: Building Deep Research Agents Towards Text--Visual Interleaved Report Generation"
authors: ["Xinkai Ma", "Zhiqi Bai", "Dingling Zhang", "Pei Liu", "Yishuo Yuan", "He Zhu", "Jiakai Wang", "Qianqian Xie", "Yifan Zhao", "Xinlong Yang", "Hao Cong", "Zhiheng Yao", "Fengxia Xie", "Zihao Xu", "Haoran Xu", "Zhaohui Wang", "Minghao Liu", "Shirong Lin", "Yingshui Tan", "Yuchi Xu", "Wenbo Su", "Zhaoxiang Zhang", "Bo Zheng", "Jiaheng Liu"]
source: "HuggingFace"
venue: ""
published: "2026-06-01"
published_time: "2026-06-01T00:00:00+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.02320"
url: "https://huggingface.co/papers/2606.02320"
pdf: "paper/harness/[HuggingFace 2026] TVIR Building Deep Research Agents Towards Text--Visual Interleaved Report Generation.pdf"
---

# TVIR: Building Deep Research Agents Towards Text--Visual Interleaved Report Generation

*🕒 **Published (v1):** 2026-06-01 00:00 UTC  ·  **Source:** HuggingFace  ·  [link](https://huggingface.co/papers/2606.02320)*

## TL;DR
TVIR introduces a benchmark (TVIR-Bench, 100 expert-curated tasks) and a hierarchical multi-agent framework (TVIR-Agent) for generating research reports that interleave retrieved images and code-generated charts with narrative text. Existing deep research agents treat visuals as decorative; TVIR enforces evidential grounding with traceable provenance. TVIR-Agent outperforms six commercial deep research systems on the benchmark including Manus-1.6 and Claude-4.5-Sonnet w/Search.

## Problem
Deep Research Agents (DRAs) produce text-centric reports where visuals, when present, lack factual grounding, source provenance, and semantic alignment with surrounding analysis. No benchmark exists that evaluates end-to-end text-visual interleaved report generation with fine-grained visual quality metrics, leading systems to optimize for aesthetic completeness over evidential rigor.

## Method
**TVIR-Bench construction**: Expert proposes topic → Grok-4.1-Thinking drafts the task → three domain experts review (design compliance, factual accuracy, logical coherence, multimodal validity) → evaluation checklist compiled. Result: 100 tasks across 10 domains, three complexity levels, 50 Chinese / 50 English.

**TVIR-Agent** is a four-stage hierarchical multi-agent pipeline built on MiroThinker:
1. **Research-Grounded Planning**: Planner invokes Google Search and web scraping iteratively, then synthesizes a structured outline where each section carries planned visual requirements (`V_i^req`) and citation-annotated research notes (`N_i`).
2. **Visual Asset Instantiation**: Two specialized agents execute in parallel — Image Searcher retrieves candidates via Google Image Search, filters heuristically, and uses a VQA tool for relevance verification; Chart Generator retrieves data, cross-validates across sources, generates Python plotting code, and executes in a sandbox. Source URLs are preserved for all assets.
3. **Context-Aware Sequential Writing**: Writer generates sections sequentially, conditioning on a dynamically updated global context `C_{i-1}` (titles + summaries of prior sections) plus section research notes; invokes additional search if notes are insufficient.
4. **Global Index Polishing**: Polisher deduplicates and renumbers references globally by URL and normalized content, then renumbers figures across sections with consistent in-text labels.

**Evaluation** uses a dual-path LLM-as-judge framework (GPT-5.2, T=0):
- *Textual Assessment (TA)*: Citation Support (CS), Instruction Alignment (IA), Writing Quality (WQ), Analytical Depth & Breadth (ADB), Factual & Logical Consistency (FLC).
- *Visual Assessment (VA)*: Multimodal Composition (MC), Figure Quality (FQ, combining CV-based metrics + LLM checklist), Figure Caption Quality (FCQ), Figure–Context Integration (FCI), Chart–Source Consistency (CSC).

Report preprocessing extracts reference entries, fact-citation pairs, and figure elements (with base64 content) via LLM, then retrieves referenced webpages via Serper API (96.53% retrieval success rate).

## Key Contributions
- **TVIR-Bench**: first benchmark for end-to-end multimodal deep research evaluation enforcing semantic grounding of visuals; fine-grained dual-path metrics rather than coarse holistic scores.
- **TVIR-Agent**: hierarchical multi-agent framework with explicit visual planning, specialized Image Searcher and Chart Generator agents, and a post-hoc Polisher that enforces global citation and figure consistency.
- **Dual-path evaluation framework** with near-perfect LLM extraction fidelity (F1 ≈ 100%) and strong human alignment (Overall OPC 99.73, PAR 78.39), robust across two judge LLMs (GPT-5.2 vs. Gemini-2.5-Pro).
- Empirical finding that current DRAs systematically prioritize decorative over evidential visuals.

## Results
- **TVIR-Agent (Claude-4.5-Sonnet)**: best Overall 73.53, best VA 76.75; best commercial is Manus-1.6 at Overall 69.73.
- **TVIR-Agent (GLM-4.7)**: best TA 72.62; lowest total structural error count.
- **Citation Support gap**: TVIR-Agent (GLM-4.7) scores 68.64 CS vs. best commercial (Claude-4.5-Sonnet w/Search) at 47.53 (+21.11 points).
- **Chart Generator ablation**: removing it drops VA from 78.62 → 60.91 and Overall from 73.92 → 63.84 (largest single-component effect).
- **Chart fulfillment rate**: TVIR-Agent (Claude-4.5-Sonnet) achieves 94.61% vs. GLM-4.7 at 38.45%, attributable to GLM-4.7's heavier retrieval usage exhausting the agent-turn budget before chart generation.
- **Structural errors**: TVIR-Agent variants produce substantially fewer traceability, consistency, and completeness errors than all commercial systems.
- **Task complexity**: as complexity increases, IA declines while ADB improves across all systems tested.
- **Domain difficulty** (ranking-based): Technology & Intelligence and Finance & Business are hardest; History & Society and Education & Culture easiest.

## Limitations
- Traceability errors (facts/figures without accessible sources) persist across all TVIR-Agent variants, not just commercial systems.
- Only 100 benchmark tasks; domain and language balance may not generalize.
- FLC (factual/logical consistency) remains weak for longer, more detailed reports — a systemic challenge not specific to TVIR-Agent.
- GLM-4.7 backbone causes severe chart under-generation (38.45% fulfillment) when retrieval dominates the agent-turn budget — the pipeline does not dynamically reallocate budget between retrieval and generation.
- Evaluation requires Serper API webpage retrieval; ~3.5% of referenced pages are unreachable, introducing minor evaluation gaps.
- TVIR-Bench tasks are not bilingual translations but parallel slices, complicating cross-language comparison.

## Relevance to Harnesses / Meta-Harnesses
TVIR-Agent is itself a production-grade multi-agent harness: specialized sub-agents (Planner, Image Searcher, Chart Generator, Writer, Polisher) are orchestrated in a fixed pipeline with tool-use (search, scraping, VQA, Python sandbox), a shared structured outline as inter-agent state, and a dedicated post-processing agent (Polisher) that enforces global consistency — a pattern directly analogous to meta-harness architecture. The paper demonstrates how agent-turn budget allocation between sub-agents determines end-to-end pipeline performance (GLM-4.7's retrieval overrun crowding out chart generation), a key harness-level failure mode. The dual-path evaluation framework is a reusable harness-evaluation template: automated preprocessing + LLM-judge scoring across multiple quality dimensions with validated human alignment, applicable to any report-generation harness.

## Tags
#deep-research #multi-agent #report-generation #multimodal #benchmark #evaluation #visual-grounding #hierarchical-agents
