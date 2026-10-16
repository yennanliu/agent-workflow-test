# Release: url-shortener 0.1.0

**Rollback:** `scripts/rollback.sh staging` points `.deploy/staging/current` at the previous release and restarts. The SQLite file is kept.

## Shipped
Tickets 01–07: shorten and follow, bad input and unknown codes, idempotent shorten, stats and hits, CLI and restart persistence, review fixes, re-validation on follow.

## Migrations
None. The schema is created on first start (`CREATE TABLE IF NOT EXISTS`).

## Environments
- **staging:** `http://127.0.0.1:8081`, a local process managed by `scripts/deploy.sh`.
- **production:** none in this demo, so there is no production approval gate. In a real project, `/dev-flow:deploy` stops here and asks before production.

## Outcome
2026-10-16: deployed to staging and healthy. The rollback drill went deploy → deploy → rollback → deploy, and every step passed its health check.

The first drill found a bug in `scripts/deploy.sh`: two deploys in the same second got the same release ID, so `src` was copied into the existing release folder (`src/src`). The fix adds a numeric suffix (`.1`, `.2`, …) when an ID is taken. The drill was re-run from a clean `.deploy/` and passed.

Live release: `20261016192643-da9ad36`. History: `20261016192642-da9ad36`, `20261016192643-da9ad36`.
