---
name: harden
description: After all tickets land, turn the pending contract tests into real ones and test every seam between modules.
disable-model-invocation: true
---

Read `docs/dev-flow/config.md`, the feature's `spec.md` (with its Trace table) and `design.md`. Call the Skill tool with "tdd".

1. Turn every pending contract test into a real one. Done when none is skipped or pending.
2. Add an integration test at each seam the design names, through the real dependency when it starts locally in seconds (database, queue, HTTP service in a container), through a fake only when it can't. Done when every seam has a test.
3. Run the full suite. Done when it is green and every AC in the Trace table points at at least one passing test.

Commit, then next: `/dev-flow:validate`.
