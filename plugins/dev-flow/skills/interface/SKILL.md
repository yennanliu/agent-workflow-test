---
name: interface
description: Turn the approved spec into the smallest public interface plus pending contract tests.
disable-model-invocation: true
---

Read `docs/dev-flow/config.md` and the feature's approved `spec.md`. Call the Skill tool with "codebase-design".

1. List the acceptance criteria. Done when the list matches the spec one to one.
2. Write the smallest interface that satisfies them, in the repo's own idiom: types and function signatures, an HTTP/OpenAPI schema, a CLI's flags, a proto, a component's props. A few deep calls beat many shallow ones. Done when every criterion maps to at least one call.
3. Write one contract test per call, skipped or marked pending, in the repo's test framework. Done when the typecheck passes with the stubs in place.
4. Fill the **Interface** and **Test** columns of the spec's Trace table.

Next: `/dev-flow:design`, in this same conversation.
