# Skill / Method library (C 技能库)

This is the **self-growing** part of the knowledge base. Each `*.md` file here is a
reusable *methodology* — the prompt + judgment criteria behind one step of the
pipeline — that you can read and **edit without touching Python**. The harness loads
the relevant skill at runtime; if a file is missing or malformed, it falls back to the
built-in default, so nothing breaks.

## File format

```markdown
---
name: <slug>
description: <one line>
placeholders: [topic, title, text]   # the {fields} the prompt expects (documentation)
---

## system
<the system prompt>

## prompt
<the user/template body; use {placeholder} where values are filled in>
```

Either section may be omitted. `{placeholder}` uses Python `str.format` — to write a
literal brace (e.g. JSON), double it: `{{` and `}}`. Edits are picked up on the next
run (no restart).

## The skills

| File | Stage | Used by |
|------|-------|---------|
| `impact-ranking.md` | A 收集 | `fetch._llm_rank` — which papers/groups to download |
| `digest.md` | B 处理 | `digest._produce` — per-paper structured digest |
| `relevance.md` | B 处理 | `digest._relevance` — per-topic "why it matters" |
| `trend-synthesis.md` | D 沉淀 | `trends.analyze_topic_year` — yearly trend map |
| `daily-brief.md` | D 输出 | `trends.summarize_today` — Today's "In brief" |
| `followup-qa.md` | D 输出 | `ask_server` — local Ask-Claude panel |
| `review.md` | E 复盘 | `review.run_review` — weekly review/flowback |
| `what-to-read-next.md` | (optional) | reading-list curation |
| `writing-style.md` | (shared) | house style reference |

User identity/needs live separately in `../profile.md` and are layered on top of a
skill's system prompt at runtime, so skills themselves stay user-agnostic.

To add a skill: drop a new `<name>.md` here and reference it from code via
`skills.load_skill("<name>", defaults=...)`.
