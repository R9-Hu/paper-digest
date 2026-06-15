---
title: "The Emergence of Autonomous Penetration Capabilities in Large Language Model-Powered AI Systems"
authors: ["Jiaqi Luo", "Jiarun Dai", "Zhile Chen", "Jia Xu", "Weibing Wang", "Yawen Duan", "Brian Tse", "Geng Hong", "Xudong Pan", "Yuan Zhang", "Min Yang"]
source: "Arxiv"
venue: ""
published: "2026-06-11"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.13079"
url: "http://arxiv.org/abs/2606.13079v1"
pdf: "paper/harness/[Arxiv 2026] The Emergence of Autonomous Penetration Capabilities in Large Language Model-Powered AI Systems.pdf"
---

# The Emergence of Autonomous Penetration Capabilities in Large Language Model-Powered AI Systems

## TL;DR
This paper constructs a realistic evaluation framework for assessing autonomous penetration capabilities of LLM-powered AI systems, addressing methodological gaps in prior work (opacity, CTF-style objectives, excessive prior knowledge). Evaluating 19 models across 300 target servers with real CVE vulnerabilities, the paper finds success rates of 10.7%–69.3%, with capability strongly correlated to general model quality (Pearson r ≈ 0.88).

## Problem
Existing autonomous penetration evaluations suffer from three compounding flaws: (1) opaque agent scaffolding and evaluation protocols (e.g., OpenAI/Anthropic system cards) that resist reproducibility; (2) CTF-style "flag-finding" objectives on single-service targets that do not reflect real-world servers hosting multiple services, most non-vulnerable; (3) excessive task-specific priors (service names, entry-point hints, exploitation paths) given to the LLM, inflating apparent capability. Together these prevent accurate assessment of genuine end-to-end autonomous penetration ability.

## Method
**Framework architecture:** Two-component design — agent scaffolding and target servers.

**Agent scaffolding:** A lightweight, general-purpose architecture with three modules: (1) *Thinking module* — LLM given only a role specification plus attacker/victim IP addresses, no penetration hints; (2) *Memory module* — sliding-window + recursive summarization to manage context overflow while preserving task history; (3) *Tools module* — Nmap, WhatWeb, and Metasploit exposed to the LLM via Model Context Protocol (MCP) servers, with tool descriptions taken directly from their `--help` output.

**Target servers:** 30 CVEs (2015–2025) selected for affecting open-source software and enabling RCE. Two environment tiers: Tier 1 (1 vulnerable + 1 secure service) and Tier 2 (1 vulnerable + 3 secure services). Five Tier 1 and five Tier 2 instances per CVE (different secure-service compositions sampled from 14 real-world services), yielding 300 total targets. Success criterion: agent maintains an active reverse shell on the target. Each model–target pair runs 3 trials; success if ≥1 trial succeeds.

## Key Contributions
- Publicly released general-purpose penetration agent scaffold and evaluation dataset (WhitzardAgent/LLMPentest), enabling reproducible AI safety evaluation.
- 300-target benchmark grounded in real CVEs with realistic multi-service noise (Tier 1/2 complexity tiers), replacing CTF-style flag-hunting.
- Black-box evaluation protocol: no service names, entry points, or exploitation guidance provided; agent receives IP address only.
- Empirical evidence across 19 open-weight and proprietary LLMs that autonomous penetration success correlates strongly with general capability (LiveBench score), Pearson r = 0.886 (Tier 1), r = 0.830 (Tier 2).
- Finding that for frontier models, insufficient/improper tool usage — not intrinsic reasoning — is the primary bottleneck.
- Demonstration that MCP-enabled agents can exploit post-knowledge-cutoff CVEs by discovering and invoking Metasploit modules without any CVE database access.

## Results
- Success rates on Tier 1: 12.0%–69.3%; Tier 2: 10.7%–68.7% across 19 models.
- Top performers (Gemini 3 Pro Preview, Claude Opus 4.5): ~70% success on both tiers.
- Models released as early as September 2024 exceed 10% success rate.
- Strong positive correlation between penetration success rate and LiveBench global average score (r = 0.886 Tier 1, r = 0.830 Tier 2).
- Tier 1 vs. Tier 2 degradation is modest, suggesting additional secure-service noise does not catastrophically reduce performance for capable models.
- Agents successfully exploited CVE-2025-3248 (disclosed April 2025) despite model knowledge cutoffs at January 2025, using Metasploit module discovery alone.

## Limitations
- Success metric is binary shell access on a single host; does not capture post-exploitation (lateral movement, privilege escalation), which real attacks require.
- Active defenses (honeypots, IDS) are absent from target environments, likely inflating success rates vs. real-world deployments.
- Only 30 CVEs (all RCE, open-source software); does not cover proprietary software, web-app logic flaws, or chained multi-vulnerability paths.
- Time/step limits (40 min / 40 steps) may undercount capability of slower-reasoning models.
- Dual-use risk acknowledged but not fully mitigated by selective release; responsible disclosure does not prevent scaffold reuse by adversaries.

## Relevance to Harnesses / Meta-Harnesses
The agent scaffolding is a direct instance of a domain-specific agent harness: a think-memory-tools loop wired to external MCP servers, deliberately kept minimal to avoid confounding evaluation with task-specific prompt engineering. This illustrates the core harness design tension — how much scaffolding structure is "infrastructure" versus "capability leakage" — and operationalizes it as an experimental variable. The recursive-summarization memory module is a practical pattern for long-horizon agentic loops that will recur in any harness operating beyond single-context tasks. The paper also stress-tests the MCP tool-integration layer at scale, providing empirical data on how general-purpose tool harnesses degrade (or don't) as environmental complexity increases, which is directly relevant to meta-harness designers choosing between task-specific and general-purpose scaffolding.

## Tags
#agent-scaffolding #mcp #penetration-testing #llm-evaluation #agentic-loop #memory-module #cybersecurity #benchmarking
