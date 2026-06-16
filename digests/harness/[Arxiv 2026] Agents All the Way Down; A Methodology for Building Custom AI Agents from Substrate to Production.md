---
title: "Agents All the Way Down; A Methodology for Building Custom AI Agents from Substrate to Production"
authors: ["Marc Alier Forment", "Juanan Pereira", "Francisco Jos\u00e9 Garc\u00eda-Pe\u00f1alvo", "Mar\u00eda Jos\u00e9 Casa\u00f1 Guerrero"]
source: "Arxiv"
venue: ""
published: "2026-06-10"
published_time: "2026-06-10T09:44:54+00:00"
year: 2026
topic: "Harnesses / Meta-Harnesses"
topic_slug: "harness"
canonical_id: "arxiv:2606.11869"
url: "http://arxiv.org/abs/2606.11869v1"
pdf: "paper/harness/[Arxiv 2026] Agents All the Way Down; A Methodology for Building Custom AI Agents from Substrate to Production.pdf"
---

# Agents All the Way Down; A Methodology for Building Custom AI Agents from Substrate to Production

*🕒 **Published (v1):** 2026-06-10 09:44 UTC  ·  **Source:** Arxiv  ·  [link](http://arxiv.org/abs/2606.11869v1)*

## TL;DR
This methodology paper codifies a five-phase, framework-free practice for building custom production AI agents — from internalizing the LLM substrate through prototyping with a general-purpose code agent, shipping as a CLI (the "Turtle pattern"), and using a general-purpose agent to test the custom agent ("agent-tests-agent"). It was distilled from a real deployment (the AAC agent on the LAMB educational platform, ~200 users, production since April 2026) and presented as a transferable, language-agnostic engineering practice.

## Problem
No published work chains the recognized pieces of custom-agent construction (function-calling, MCP, agent loop, evaluation, skills) into a single, named, sequential methodology with explicit acceptance criteria. The practice is scattered across vendor docs, leaked system prompts, blog posts, and podcast appearances; the gap is not missing ingredients but a missing recipe.

## Method
The methodology has a structural asymmetry: two preconditions crossed once (P1–P2) and three iterated practices (P3–P5).

- **P1 — Substrate**: Engineer internalizes the LLM as a software component, including the `tools → system → messages` caching hierarchy. Cache discipline is central: tools are immutable at init, system is immutable per session, messages grow append-only; volatile state never pollutes the cached prefix.
- **P2 — Building blocks**: Vocabulary fluency across function calling, MCP vs. CLI vs. the *liteshell pattern* (a CLI-shaped in-process facade for cloud runtimes with no host shell), the agent loop, skills (versioned markdown behavior files), characters (persona), hooks (deterministic pre-tool-use security gates), and instruction sets.
- **P3 — Prototype with a general-purpose agent**: Use Claude Code/OpenCode/Cursor as a pair-programmer to do reconnaissance against the real platform, letting architecture emerge from building rather than pre-specification.
- **P4 — Harvest, fold, ship as CLI (Turtle pattern)**: Collect tools, scaffolding, skills, and characters from P3; fold into a minimal loop with a deterministic `pre_tool_use_hook`; ship as a stateless, session-keyed CLI invocable by humans or other agents.
- **P5 — Agent-tests-agent**: A general-purpose CLI agent drives the custom agent through behavioral scenarios, returning structured evaluations. This is a complementary layer to classical testing (unit/integration/E2E), addressing stochastic scenario-shaped failure modes that deterministic tests cannot reach.

The recursion — "agents all the way down" — lives in P3→P4→P5→P3: the agent that prototyped is the agent that tests; multi-agent orchestration is CLI composition (the "Turtle corollary").

## Key Contributions
- Named, sequential, five-phase methodology with explicit acceptance criteria and anti-mandates for each phase — first to chain substrate → building blocks → prototype → ship → test as a single framework-independent practice.
- **Agent-tests-agent (P5)** as a novel QA discipline: a general-purpose agent drives the custom agent through behavioral scenarios, producing structured evaluation; distinct from and complementary to classical software testing.
- **Turtle corollary**: once an agent is shipped as a CLI (P4), multi-agent orchestration reduces to CLI composition, making supervisor/worker, parallel fan-out, conditional handoff, and Ralph-loop patterns emergent without framework primitives.
- **Liteshell pattern**: named and located a convergent engineering practice — a CLI-shaped in-process facade that exposes a single dispatch tool to the LLM in cloud runtimes lacking a host shell, inheriting the token-cost advantage of CLI over MCP.
- Argument (not demonstrated result) for dependency-aware design as a structural security posture: framework-free construction yields a smaller dependency surface, reducing supply-chain attack exposure.

## Results
- AAC (Agent-Assisted Creator) built on the LAMB educational platform: ~10 developer-days with an AI pair-programmer, in production at two universities with ~200 educator-creators since April 2026.
- MCP vs. CLI token overhead (cited practitioner benchmarks): a controlled matched-task benchmark shows ≈35× more tokens via MCP than CLI, with task-completion dropping from 100% to 72% on harder scenarios (MindStudio 2026); a single GitHub language-check costs ~1,365 tokens via `gh` vs. ~44,026 via the matching MCP server (Vensas 2026); a GitHub MCP server exposing 93 tools adds ~55,000 tokens of registry overhead vs. ~200 for the `gh` equivalent (Reinhard 2026).
- Cache-read pricing across providers is ~0.1× base input cost on Anthropic and OpenAI flagship models; DeepSeek cache-hit multipliers approach 0.02×.

## Limitations
- The supply-chain security posture argument is explicitly flagged as lower evidentiary weight than contributions 1–3; empirical validation (measured dependency counts, attack-surface comparison across matched stacks) is deferred to future work.
- The AAC/LAMB deployment is a single case study in the EdTech domain; generalizability to other verticals is asserted but not empirically demonstrated.
- MCP vs. CLI token benchmarks are all from large-catalogue, many-call conditions — the authors note these represent the upper end of their cost model, not a universal ratio.
- The paper is a methodology paper, not an experimental one; it offers no controlled trial comparing this methodology against framework-based alternatives on build time, defect rate, or operational cost.
- The Turtle pattern's "replay" reproducibility is noted with a caveat (not elaborated in the provided text).

## Relevance to Harnesses / Meta-Harnesses
This paper is directly relevant: its P5 "agent-tests-agent" phase is a meta-harness primitive — a general-purpose agent driving and evaluating a custom agent as an automated behavioral test harness. The Turtle corollary (multi-agent orchestration as CLI composition) is itself a theory of how meta-harnesses compose: any agent shipped as a CLI is both a tool and an orchestrable node, making harness hierarchies compositional by construction. The methodology fills in the engineering substrate that harness builders typically leave implicit — caching discipline, hook-based security gates, skill loading — and formalizes the prototype→harvest→ship cycle that underlies most real harness development. For researchers tracking harnesses and meta-harnesses, this paper provides a practitioner-grounded vocabulary (liteshell, Turtle pattern, pre-tool-use hook, agent-tests-agent) and a structured lifecycle that complements more formal multi-agent coordination frameworks.

## Tags
#agent-harness #meta-harness #agent-methodology #cli-composition #agent-tests-agent #liteshell #mcp-vs-cli #custom-agents
