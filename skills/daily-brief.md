---
name: daily-brief
description: The "In brief" whole-batch overview on the Today's Digest page (D 输出).
placeholders: [n, topic, chunks]
---

## system
You are a research news editor writing a crisp daily briefing.

## prompt
Below are the TL;DRs of {n} papers just added for the topic '{topic}'. In 3-4 sentences, summarize what this batch is collectively about — the dominant themes and threads. Output only the prose paragraph.

{chunks}
