---
name: validate
description: Two-axis review of the whole feature branch (standards and spec) in a fresh subagent, before deploying.
disable-model-invocation: true
---

Review the whole feature, not one ticket. Find the diff from the branch point to `HEAD`, the feature's `spec.md`, and the coding standards named in `docs/dev-flow/config.md`. Call the Skill tool with "code-review", passing all three.

Write the result to `docs/dev-flow/<feature>/review.md` with the two axes side by side, never merged or re-ranked.

Done when every AC has a verdict, every finding is marked blocking or not, and the user has seen the blocking ones.

A blocking spec finding goes back to `/dev-flow:implement` as a new ticket, or to `/dev-flow:spec` when the spec itself was wrong. With nothing blocking, next: `/clear`, then `/dev-flow:deploy`.
