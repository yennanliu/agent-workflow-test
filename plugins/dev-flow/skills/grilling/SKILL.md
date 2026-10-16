---
name: grilling
description: Grill the user relentlessly about a plan, design or decision until every branch is settled. Use when the user wants to stress-test an idea, says "grill me", or a plan has unresolved choices.
---

Interview the user relentlessly until you share one understanding of the plan. Map it as a **design tree**: each decision branches into the decisions that depend on it.

Work in **rounds**. The **frontier** is every open decision whose prerequisites are settled. Each round, ask the whole frontier at once:

```
**Q1. <title>** <the question, with options when there are any>
→ Recommended: <your answer and a one-line reason>
```

Word each question so "yes" accepts your recommendation. Wait for the answers, recompute the frontier, ask the next round. A question that depends on another open question waits for a later round.

Facts are your job; decisions are the user's. When a question needs a fact from the code, docs or tools, look it up (in a subagent when it takes a while) and keep asking the questions that don't depend on it.

The session is done when the frontier is empty: every branch visited, nothing silently assumed, and the user confirms the shared understanding.
