---
name: relevance
description: Per-topic "why this matters" framing (B 处理) for papers shared across topics.
placeholders: [title, tldr, topic]
---

## system
You explain, concisely and concretely, why a paper matters to a specific research topic.

## prompt
Paper: {title}
TL;DR: {tldr}

In 2-4 sentences, explain this paper's relevance to the research topic "{topic}" — why it matters for someone tracking it and how it connects to the broader line of work. Output only prose.
