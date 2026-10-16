---
name: design
description: Design the modules behind the interface, their data flow and failure modes, and record hard-to-reverse decisions.
disable-model-invocation: true
---

Read the feature's `spec.md` and the interface. Call the Skill tool with "codebase-design".

1. Give each interface call one owning module, reusing existing modules first. Done when no call is unowned.
2. For each new or changed module, write its inputs, outputs, data flow, and failure modes (bad input, timeouts, partial writes, concurrency). Done when every module lists all four.
3. Record an ADR in `docs/adr/` for each decision that is hard to reverse, surprising without context, and a real trade-off.
4. Write `docs/dev-flow/<feature>/design.md`: the module map as a Mermaid diagram, then one short section per module. Fill the **Module** column of the spec's Trace table.

Next: `/dev-flow:tickets`, in this same conversation.
