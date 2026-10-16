---
name: retro
description: Look back on a feature's sessions and improve the environment (checks, standards, skills), not the code.
disable-model-invocation: true
---

Look back over this session, or the session log the user points to, together with the feature's `review.md` and `e2e.md`.

1. List each moment the agent went wrong or the user had to correct it. Done when every correction in the session is on the list.
2. Give each one a fix in the environment:
   - A mechanical mistake → a **deterministic check**: a lint rule, a type, a test, a CI step.
   - A judgement call → a line in the **coding standards** named in config.
   - A stage that rushed or wandered → an edit to that dev-flow skill: a sharper completion criterion or a stronger leading word.
   - A one-off → drop it, and say so.
3. Write `docs/dev-flow/<feature>/retro.md` with each item and its fix.
4. Ask the user which fixes to apply, then apply them.

Done when every item has a fix or a stated reason to drop it.
