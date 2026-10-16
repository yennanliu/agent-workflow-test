---
name: implement
description: Implement one ticket test-first, review it, and commit it.
disable-model-invocation: true
---

Read `docs/dev-flow/config.md`, the ticket the user names, and the feature's `spec.md` and `design.md`. If no ticket is named, take the first unblocked `todo` ticket and say which.

1. State the ticket's title and the ACs it covers.
2. Call the Skill tool with "tdd" and build the ticket one red-green slice at a time. Run the one-file test command after each slice and the typecheck often.
3. Run the full test suite and lint. Done when both pass.
4. Call the Skill tool with "code-review" on this ticket's diff. Fix every blocking finding.
5. Commit with the config's commit style, naming the ticket. Mark the ticket done: `Status: done` for local tickets, or close the GitHub issue with the commit hash.

Done when the ticket's tests went red then green, the full suite passes, and the commit exists.

Next: `/clear`, then the next unblocked ticket. After the last ticket: `/dev-flow:harden`.
