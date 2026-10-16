---
name: tickets
description: Split the spec and design into vertical-slice tickets with blocking edges, each sized for one context window.
disable-model-invocation: true
---

Read `docs/dev-flow/config.md`, the feature's `spec.md`, and `design.md` if it exists.

Split the work into **vertical slices**: each ticket is one thin path through every layer it touches, demoable on its own. The first ticket is a **tracer bullet** through the whole stack.

1. Draft the tickets. Each one carries: title, the ACs it covers, the modules it touches, what it is blocked by, and a two-line **Done when**. A ticket whose Done when needs more than two lines splits in two.
2. Order them by blocking edges. Done when every ticket's blockers come before it.
3. Write them to the tracker named in config:
   - `local`: `docs/dev-flow/<feature>/tickets/NN-<slug>.md`, with `Status: todo` on the first line.
   - `github`: `gh issue create` with the label `dev-flow:<feature>` and a `Blocked by #N` line per blocker.
4. Fill the **Ticket** column of the spec's Trace table. Done when every AC appears in at least one ticket.

Next: `/clear`, then `/dev-flow:implement <first unblocked ticket>`.
