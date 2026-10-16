---
name: setup
description: Configure dev-flow for this repo (commands, environments, ticket tracker). Run once per repo, or again when the toolchain changes.
disable-model-invocation: true
---

Write `docs/dev-flow/config.md` so every dev-flow stage knows how this repo is built, tested and shipped.

1. **Detect.** Read whatever the repo has: `package.json`, `pyproject.toml`, `Makefile`, `go.mod`, `Cargo.toml`, `pom.xml`/`build.gradle`, CI workflows, `Dockerfile`, deploy scripts, the README. Done when every field in the template below has a detected value or is marked `ask`.
2. **Ask once.** Put every `ask` field to the user in one numbered round, each with your recommended answer, worded so "yes" accepts it. The ticket tracker and the production deploy are always the user's decision.
3. **Write.** Write the config from the template. A field the user leaves open stays `ask`; the stage that needs it asks then. If `config.md` already exists, keep the user's values and show what you changed.
4. **Prove.** Run the typecheck and full test commands once. Done when both run (passing or failing is fine; a command that cannot start is not).
5. Create `GLOSSARY.md` at the repo root if missing, with the heading `# Glossary`.

Template:

```markdown
# dev-flow config

## Commands
- install: `<cmd>`
- typecheck: `<cmd or "none">`
- lint: `<cmd or "none">`
- test, one file: `<cmd with {file}>`
- test, full suite: `<cmd>`
- build: `<cmd or "none">`
- e2e: `<cmd or "ask">`

## Environments
- staging deploy: `<cmd or "none">`
- staging health check: `<cmd or URL>`
- production deploy: `<cmd or "ask">`
- production health check: `<cmd or URL>`
- rollback: `<cmd or "ask">`

## Tickets
- tracker: `local` (docs/dev-flow/<feature>/tickets/) or `github` (gh issues)

## Standards
- coding standards: `<path, e.g. CLAUDE.md or docs/standards.md>`
- commit style: `<e.g. conventional commits>`
```
