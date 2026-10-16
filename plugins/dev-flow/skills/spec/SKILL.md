---
name: spec
description: Turn the grilled conversation into an approved spec with testable acceptance criteria and user journeys.
disable-model-invocation: true
---

Write the spec for the feature this conversation settled. The spec is the destination: when direction changes later, edit the spec, never the history.

1. Pick a short kebab-case feature slug and confirm it. The spec goes to `docs/dev-flow/<feature>/spec.md`.
2. Write it from the template below, using `GLOSSARY.md` terms exactly.
3. Give every acceptance criterion an ID, an observable behaviour, and how to check it. Done when each criterion could become a failing test without asking anyone anything.
4. Give every user journey an ID, the steps a user takes, and the criteria it covers. Done when every user-visible criterion sits in at least one journey.
5. Show the spec and ask the user to approve it. Apply their edits first. Done when they say yes; record the date under **Approved**.

Template:

```markdown
# <Feature name>

**Approved:** <date, or "pending">

## Problem
<who hurts, how, and how we will know it is fixed>

## Acceptance criteria
- **AC-1** <observable behaviour>. Check: <test or measurement>.

## User journeys
- **UJ-1** <name>: <step> → <step> → <outcome>. Covers AC-1, AC-2.

## Out of scope
- <thing we deliberately won't do>

## Trace
| AC | Interface | Module | Ticket | Test |
| --- | --- | --- | --- | --- |
```

Next: `/dev-flow:interface`, in this same conversation. For a small change with no new interface, go to `/dev-flow:tickets`.
