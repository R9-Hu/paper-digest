---
title: "AgentCyberRange: Benchmarking Frontier AI Systems in Realistic Cyber Ranges"
authors: ["Fengyu Liu", "Jiarun Dai", "Yihe Fan", "Wuyuao Mai", "Ziao Li", "Bofei Chen", "Jie Zhang", "Zheng Lou", "Bocheng Xiang", "Qiyi Zhang", "Xudong Pan", "Geng Hong", "Yuan Zhang", "Min Yang"]
source: "Arxiv"
venue: ""
published: "2026-06-12"
year: 2026
topic: "Agentic AI / LLM Agents"
topic_slug: "agentic-ai"
canonical_id: "arxiv:2606.14295"
url: "http://arxiv.org/abs/2606.14295v1"
pdf: "paper/agentic-ai/[Arxiv 2026] AgentCyberRange Benchmarking Frontier AI Systems in Realistic Cyber Ranges.pdf"
---

# AgentCyberRange: Benchmarking Frontier AI Systems in Realistic Cyber Ranges

## TL;DR
AgentCyberRange is the first open, multi-host cyber-range benchmark for evaluating frontier AI systems on end-to-end autonomous cyberattack workflows—web exploitation followed by post-exploitation across networked enterprise environments. The companion CAGE pipeline handles scalable agent orchestration, environment deployment, and automatic verification. GPT-5.5 with Codex leads all evaluated systems but still solves only ~16% of web exploitation and ~32% of post-exploitation tasks at Level-0, revealing large capability gaps for reliable autonomous attack execution.

## Problem
Existing cybersecurity benchmarks (CTF-solving, single-vulnerability reproduction, isolated exploit generation) abstract away the operational chain of real intrusions—service discovery, foothold establishment, internal reconnaissance, privilege escalation, and lateral movement across networked hosts. No open, reproducible, multi-host cyber-range infrastructure existed to test frontier AI systems end-to-end under realistic attack conditions, making it impossible to observe emerging offensive capabilities systematically.

## Method
**Benchmark (AgentCyberRange):** Two tracks:
- *WebExploitBench*: 15 real web applications, 110 vulnerabilities (18 zero-day, 56 one-day, 36 synthetic), 17 vulnerability classes. Agents start from a target URL and must discover hidden endpoints and exploit them black-box.
- *PostExploitBench*: 8 enterprise-like cyber ranges, 156 internal hosts, 12 post-exploitation technique categories (lateral movement, privilege escalation, credential reuse, defense evasion, persistence, etc.), with active defenses including honeypots, AV/EDR-like software, and an agent-simulated defender reacting to suspicious behavior.

Both tracks use three difficulty levels (Level-0 to Level-2) that progressively provide more task-specific hints (target URL only → vulnerable endpoints → vulnerability types/CVEs).

**Evaluation pipeline (CAGE):**
- *Agent adapters*: Unified CLI interface for heterogeneous agents (Codex, Claude Code, Qwen Code, Kimi Code).
- *Agent manager*: Isolated container per trial, records model interactions and token usage.
- *Benchmark manager*: Deploys/resets web apps and cyber ranges per trial.
- *Verifier*: Validates exploitation via PoC execution (canary DB reads for SQLi, /tmp marker files for host compromise; /root markers for root-level compromise).

Six frontier systems evaluated: GPT-5.5+Codex, Claude-Opus-4.7+Claude Code, Qwen-3.7-Max+Qwen Code, Kimi-2.6+Kimi Code, DeepSeek-V4-Pro+Claude Code, GLM-5.1+Claude Code. Step budgets: 150 for web exploitation, 500 for post-exploitation.

## Key Contributions
- First open, reproducible, multi-host cyber-range benchmark covering the full web→post-exploitation attack chain, with 110 web vulnerabilities and 156 hosts across 8 enterprise-like ranges.
- CAGE: modular evaluation pipeline supporting heterogeneous CLI agents, parallel environment deployment, and automatic compromise verification.
- Three-level difficulty design that decomposes agent capability (exploration vs. exploitation; open-ended vs. informed).
- Discovery of out-of-benchmark zero-day vulnerabilities (e.g., arbitrary file write in ComfyUI) by evaluated agents, demonstrating benchmark ecological validity.
- Systematic behavioral analysis revealing that frontier agents struggle with deep endpoint discovery, show high run-to-run variance, and fail multi-step post-exploitation chains.

## Results
**Web Exploitation (Level-0, Pass@3 Avg.):**
- GPT-5.5: 16.1% (Pass@3 Max: 28.18%, 31 unique vulns across 13 classes)
- Claude-Opus-4.7: 14.55%
- Qwen-3.7-Max: 12.42%
- DeepSeek-V4-Pro: 8.18%
- GLM-5.1: 8.18%
- Kimi-2.6: 3.03%

**Post Exploitation (Level-0, Pass@3 Avg.):**
- GPT-5.5: 31.71% (Pass@3 Max: 43.90%)
- Claude-Opus-4.7: 15.04%
- Qwen-3.7-Max: 13.02%
- DeepSeek-V4-Pro: 12.20%
- GLM-5.1: 11.37%
- Kimi-2.6: 5.68%

**With Level-2 hints (GPT-5.5):** web exploitation 33.0%, post-exploitation 46.3%.

**Depth analysis:** GPT-5.5 detection rate drops from 35% at vulnerability depth 2 to 11% at depth 6, showing that deeper application workflows are a hard barrier.

**Behavioral finding:** GPT-5.5 is the only agent that uses dedicated endpoint-discovery tools (ffuf); others rely predominantly on curl, limiting hidden-surface coverage.

**Claude-Opus-4.7:** 12 trials terminated by safety-related refusals and excluded from reported rates.

## Limitations
- Coverage is restricted to web exploitation and post-exploitation; reconnaissance and reporting stages are not benchmarked.
- Tasks require black-box exploitability, excluding source-code-dependent vulnerability classes (e.g., deserialization requiring private class names).
- High run-to-run variance across all agents (many vulnerabilities found in only one of three runs) makes single-attempt estimates unreliable.
- Safety refusals in Claude-Opus-4.7 exclude 12 trials, complicating direct comparison.
- Benchmark is static; adaptive defenders are simulated but the attacker-defender co-evolution that characterizes real red-teaming is limited.
- No open-ended multi-turn human-in-the-loop evaluation; step budget caps may underestimate agent potential.

## Relevance to Agentic AI / LLM Agents
AgentCyberRange directly stress-tests frontier LLM agents in a long-horizon, tool-use, multi-step environment where partial progress, environment feedback, and adaptive replanning are all required—exactly the capabilities central to agentic AI research. The CAGE pipeline's agent-adapter abstraction (unified CLI interface across Codex, Claude Code, Qwen Code) is a reusable pattern for heterogeneous agent benchmarking beyond cybersecurity. The finding that even the best agent (GPT-5.5) solves only ~32% of post-exploitation tasks and exhibits high run-to-run variance directly quantifies the instability and planning limitations of current agents under realistic sequential decision-making pressure. The observation that agents can discover out-of-benchmark zero-day vulnerabilities while also blindly triggering honeypots illustrates the dual-use risk of capable-but-unreliable autonomous agents—a core concern for safety-focused agentic AI work.

## Tags
#benchmark #cybersecurity #tool-use #long-horizon #agentic-eval #red-teaming #multi-step-reasoning #vulnerability-exploitation
