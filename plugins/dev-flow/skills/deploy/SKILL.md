---
name: deploy
description: Ship a validated feature to staging, prove the rollback, then deploy to production after the user approves.
disable-model-invocation: true
---

Read `docs/dev-flow/config.md` and the feature's `review.md`. For any deploy, health check or rollback field marked `ask`, ask the user and write the answer back to the config.

1. Write `docs/dev-flow/<feature>/release.md`: version, the tickets shipped, the migrations, and the **rollback** command. Done when the rollback command is written down before anything ships.
2. Deploy to staging and run the staging health check. Done when every check is green.
3. Run the rollback on staging, confirm the previous version is serving, then redeploy. Done when both directions worked.
4. Ask the user to approve production, showing the release notes and the staging results. Continue only on a yes.
5. Deploy to production and run the production health check. If any check fails, run the rollback and report.

With no staging environment, skip steps 2 and 3, and say so in the approval request.

Done when production health checks are green, or the rollback has run. Record the outcome and time in `release.md`.

Next: `/dev-flow:e2e`.
