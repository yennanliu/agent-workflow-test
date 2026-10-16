# agent-workflow-test

`dev-flow` 是一個 Claude Code plugin，用一組固定的 agent skill 帶著一個功能從想法走到上線：grill、spec、interface、design、tickets、implement、harden、validate、deploy、e2e、retro。

[English](README.md)

## 安裝

在 Claude Code 裡：

```
/plugin marketplace add yennanliu/agent-workflow-test
/plugin install dev-flow@agent-workflow
```

Claude Code 2.1.275 以上版本可以一行完成：

```
/plugin install dev-flow --marketplace yennanliu/agent-workflow-test
```

在終端機：

```bash
claude plugin marketplace add yennanliu/agent-workflow-test
claude plugin install dev-flow@agent-workflow
```

**整個團隊一起用**：把下面這段 commit 到專案的 `.claude/settings.json`，信任這個資料夾的人都會自動被提示安裝：

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

**不用 plugin 系統**：把 skill 複製到使用者或專案的 skills 資料夾。指令就沒有前綴（`/spec` 而不是 `/dev-flow:spec`）：

```bash
git clone --depth 1 https://github.com/yennanliu/agent-workflow-test /tmp/agent-workflow
cp -r /tmp/agent-workflow/plugins/dev-flow/skills/* ~/.claude/skills/
```

## 快速開始

```
/dev-flow:setup        # 每個 repo 一次：偵測指令，寫入 docs/dev-flow/config.md
/dev-flow:next         # 隨時：下一步該跑哪個階段
/dev-flow:grill        # 開始一個功能
```

`setup` 會讀 `package.json`、`pyproject.toml`、`Makefile`、`go.mod`、`Cargo.toml`、CI workflow 和部署腳本，所以同一套 skill 在 Node、Python、Go、Rust、JVM 專案都能用。它只會問偵測不到的部分。

## 指令

| # | 指令 | 做什麼 | 留下什麼 |
| --- | --- | --- | --- |
| 0 | `/dev-flow:setup` | 記錄建置、測試、部署指令 | `docs/dev-flow/config.md` |
| 1 | `/dev-flow:grill` | 訪問你，直到每個決策都定案 | `GLOSSARY.md` 的術語、ADR |
| 2 | `/dev-flow:spec` | 寫驗收條件與 user journey，由你核准 | `docs/dev-flow/<feature>/spec.md` |
| 3 | `/dev-flow:interface` | 最小的公開 interface + pending 的 contract test | interface 程式碼、追蹤表 |
| 4 | `/dev-flow:design` | 模組、資料流、失敗模式 | `design.md`、ADR |
| 5 | `/dev-flow:tickets` | vertical slice 的 tickets，含阻擋關係 | 本地 ticket 檔或 GitHub issue |
| 6 | `/dev-flow:implement` | 一張 ticket：先寫測試、review、commit | 每張 ticket 一個 commit |
| 7 | `/dev-flow:harden` | 真正的 contract test + 每個接縫的整合測試 | 測試 |
| 8 | `/dev-flow:validate` | 在 subagent 做兩軸 review（規範、需求） | `review.md` |
| 9 | `/dev-flow:deploy` | 上 staging、演練 rollback、你同意後上 production | `release.md` |
| 10 | `/dev-flow:e2e` | 在部署環境跑每條 user journey | `e2e.md`、失敗就開 ticket |
| 11 | `/dev-flow:retro` | 把錯誤變成檢查、規範或 skill 修改 | `retro.md` |
| | `/dev-flow:next` | Router：下一步跑什麼、小改動可以跳過哪些 | |

階段 1 到 5 在同一個不中斷的對話裡跑完。階段 6 每張 ticket 之前先 `/clear`，之後的階段之間也是。

小改動可以跳過階段：修 bug 只跑 `grill → implement → validate → deploy`。

四個 model-invoked skill 承載共用的紀律，由各階段呼叫：`grilling`、`tdd`、`code-review`、`codebase-design`。整個 plugin 每個 session 約佔 800 tokens。

## 設計說明

- [如何打造你自己的 Agent Skill](doc/how-to-build-agent-skill.zh-TW.md)（[English](doc/how-to-build-agent-skill.md)）：設計原則，參考 Matt Pocock 的 [skills](https://github.com/mattpocock/skills)。
- [軟體開發的 Agent Skill 工作流程](doc/dev-workflow-skills.zh-TW.md)（[English](doc/dev-workflow-skills.md)）：為什麼階段、關卡和 context 邊界放在那裡。

推送前用 `claude plugin validate .` 檢查。
