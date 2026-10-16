---
name: grill
description: Relentless interview to sharpen a feature idea before any spec, recording agreed terms and hard decisions as it goes.
disable-model-invocation: true
---

Grill the user on the feature they describe. Call the Skill tool with "grilling".

While the session runs:

- Settle facts from the code yourself. Put only decisions to the user.
- Each time a project term is agreed, add it to `GLOSSARY.md` straight away: the term as a heading, a one-sentence definition, and an `Avoid:` line listing the synonyms not to use.
- Record an ADR in `docs/adr/NNNN-<slug>.md` only for a decision that is hard to reverse, surprising without context, and a real trade-off. Most sessions record none.

Next: `/dev-flow:spec`, in this same conversation.
