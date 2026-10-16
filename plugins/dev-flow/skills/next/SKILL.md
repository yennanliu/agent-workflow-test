---
name: next
description: Which dev-flow stage to run next for a feature, and which stages a small change can skip.
disable-model-invocation: true
---

Tell the user which dev-flow stage to run next, and why, in three lines or fewer.

Look in `docs/dev-flow/` for the feature's artifacts, then find the first stage whose artifact is missing or unfinished:

| # | Command | Artifact it leaves | Context |
| --- | --- | --- | --- |
| 0 | `/dev-flow:setup` | `docs/dev-flow/config.md` | once per repo |
| 1 | `/dev-flow:grill` | terms in `GLOSSARY.md`, ADRs | plan window |
| 2 | `/dev-flow:spec` | `<feature>/spec.md`, approved | plan window |
| 3 | `/dev-flow:interface` | interface code, contract stubs, trace table | plan window |
| 4 | `/dev-flow:design` | `<feature>/design.md` | plan window |
| 5 | `/dev-flow:tickets` | tickets, each a vertical slice | plan window |
| 6 | `/dev-flow:implement <ticket>` | one commit per ticket | fresh per ticket |
| 7 | `/dev-flow:harden` | contract + integration tests | fresh |
| 8 | `/dev-flow:validate` | `<feature>/review.md` | subagent |
| 9 | `/dev-flow:deploy` | `<feature>/release.md` | fresh |
| 10 | `/dev-flow:e2e` | `<feature>/e2e.md` | fresh |
| 11 | `/dev-flow:retro` | `<feature>/retro.md` | same session as the work |

Stages 1 to 5 belong in one unbroken conversation. Each ticket in stage 6 starts after `/clear`.

Match the task size:

| Task | Stages |
| --- | --- |
| Bug fix or small change, no new interface | grill → implement → validate → deploy |
| Feature inside one module | grill → spec → tickets → implement → harden → validate → deploy → e2e |
| New service, public API, or cross-team feature | all |

A failed e2e journey goes back to tickets. A spec-axis review finding goes back to implement, or to spec when the spec itself was wrong.
