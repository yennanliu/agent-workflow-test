---
name: code-review
description: Review a diff on two separate axes, coding standards and the spec, in a fresh subagent. Use after implementing a change, before a commit or merge, or when the user asks for a review.
---

Dispatch a fresh subagent for the review. The agent that wrote the code is the worst one to judge it. Give it the diff, the spec or ticket it should satisfy, and the coding standards file.

The subagent reports two **axes**, side by side, never merged or re-ranked. "Meets every convention but builds the wrong thing" and "builds the right thing but breaks conventions" are both common, and a merged list lets one hide the other.

```markdown
## Standards
| # | File:line | Finding | Blocking |
| --- | --- | --- | --- |

## Spec
| AC | Verdict (met / partly / missing) | Evidence (test, file:line) |
| --- | --- | --- |
```

Blocking means it breaks behaviour, security, data, or a written standard. Everything else is a suggestion.

Done when every acceptance criterion in scope has a verdict with evidence, and every standards finding cites a line.
