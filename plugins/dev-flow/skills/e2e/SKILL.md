---
name: e2e
description: Run every user journey in the spec against a deployed environment and turn failures into tickets.
disable-model-invocation: true
---

Read `docs/dev-flow/config.md` and the feature's `spec.md`. If the e2e command is `ask`, recommend a runner that fits the project (Playwright for web UIs, scripted HTTP checks for APIs, the CLI itself for CLIs), confirm it, and write it to the config.

1. Write or update one e2e test per **user journey** (`UJ-n`), named after its ID. Done when every journey has a test.
2. Run them against staging, or against a local production build when there is no staging. Done when every journey has a result.
3. Run the journeys tagged smoke (or the first step of each journey) against production. These must be read-only or use a test account.
4. Write `docs/dev-flow/<feature>/e2e.md`: one row per journey, environment, pass or fail, and evidence (a screenshot path, a response, a log line).
5. Turn each failure into a ticket carrying the failing step, the expected result and the actual result.

Done when every journey passed on staging and the production smoke passed, or every failure has a ticket.

Next: `/dev-flow:retro`, in the session that did the work.
