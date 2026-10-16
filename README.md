# agent-workflow-test

`dev-flow` is a Claude Code plugin that runs a software feature from idea to production through a fixed set of agent skills: grill, spec, interface, design, tickets, implement, harden, validate, deploy, e2e, retro.

[繁體中文](README.zh-TW.md)

## Install

In Claude Code:

```
/plugin marketplace add yennanliu/agent-workflow-test
/plugin install dev-flow@agent-workflow
```

On Claude Code 2.1.275 or later, one line does both:

```
/plugin install dev-flow --marketplace yennanliu/agent-workflow-test
```

From a terminal:

```bash
claude plugin marketplace add yennanliu/agent-workflow-test
claude plugin install dev-flow@agent-workflow
```

**For a whole team**, commit this to the project's `.claude/settings.json`. Everyone who trusts the folder gets the plugin offered automatically:

```json
{
  "extraKnownMarketplaces": {
    "agent-workflow": {
      "source": { "source": "github", "repo": "yennanliu/agent-workflow-test" }
    }
  },
  "enabledPlugins": { "dev-flow@agent-workflow": true }
}
```

**Without the plugin system**, copy the skills into your user or project skills folder. Commands are then unprefixed (`/spec` instead of `/dev-flow:spec`):

```bash
git clone --depth 1 https://github.com/yennanliu/agent-workflow-test /tmp/agent-workflow
cp -r /tmp/agent-workflow/plugins/dev-flow/skills/* ~/.claude/skills/
```

## Quick start

```
/dev-flow:setup        # once per repo: detects your commands, writes docs/dev-flow/config.md
/dev-flow:next         # any time: which stage to run next
/dev-flow:grill        # start a feature
```

`setup` reads `package.json`, `pyproject.toml`, `Makefile`, `go.mod`, `Cargo.toml`, CI workflows and deploy scripts, so the same skills work in a Node, Python, Go, Rust or JVM repo. It asks only about what it can't detect.

## Commands

| # | Command | What it does | Leaves behind |
| --- | --- | --- | --- |
| 0 | `/dev-flow:setup` | Records build, test and deploy commands | `docs/dev-flow/config.md` |
| 1 | `/dev-flow:grill` | Interviews you until every decision is settled | terms in `GLOSSARY.md`, ADRs |
| 2 | `/dev-flow:spec` | Writes acceptance criteria and user journeys; you approve | `docs/dev-flow/<feature>/spec.md` |
| 3 | `/dev-flow:interface` | Smallest public interface + pending contract tests | interface code, trace table |
| 4 | `/dev-flow:design` | Modules, data flow, failure modes | `design.md`, ADRs |
| 5 | `/dev-flow:tickets` | Vertical-slice tickets with blocking edges | local ticket files or GitHub issues |
| 6 | `/dev-flow:implement` | One ticket, test-first, reviewed, committed | one commit per ticket |
| 7 | `/dev-flow:harden` | Real contract tests + integration tests at every seam | tests |
| 8 | `/dev-flow:validate` | Two-axis review (standards, spec) in a subagent | `review.md` |
| 9 | `/dev-flow:deploy` | Staging, rollback drill, production after your yes | `release.md` |
| 10 | `/dev-flow:e2e` | Every user journey against the deployed app | `e2e.md`, tickets for failures |
| 11 | `/dev-flow:retro` | Turns mistakes into checks, standards, skill edits | `retro.md` |
| | `/dev-flow:next` | Router: what to run next, what a small change can skip | |

Stages 1 to 5 run in one unbroken conversation. Run `/clear` before each ticket in stage 6, and between later stages.

Small changes skip stages: a bug fix runs `grill → implement → validate → deploy`.

Four model-invoked skills hold the shared discipline and are called by the stages: `grilling`, `tdd`, `code-review`, `codebase-design`. The whole plugin adds about 800 tokens to each session.

## Example

[`ws/demo_project_1`](ws/demo_project_1/) is a small URL shortener built through every stage of the workflow, with each stage's artifact committed. Its two-axis review caught a header-injection bug and four other blocking issues, and its staging rollback drill caught a bug in its own deploy script.

## How it's designed

- [How to Build Your Own Agent Skill](doc/how-to-build-agent-skill.md) ([中文](doc/how-to-build-agent-skill.zh-TW.md)): the principles, based on Matt Pocock's [skills](https://github.com/mattpocock/skills).
- [Agent Skill Workflow for Software Development](doc/dev-workflow-skills.md) ([中文](doc/dev-workflow-skills.zh-TW.md)): why the stages, gates and context boundaries are where they are.

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace "agent-workflow"
plugins/dev-flow/
  .claude-plugin/plugin.json
  skills/<name>/SKILL.md            # 13 user-invoked stages + 4 shared disciplines
doc/                                # design docs, English and 繁體中文
```

Check changes with `claude plugin validate .` before pushing.
