# 更新日志 / Changelog

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。
The project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-04-30

第一次具名版本发布 / First named release. The project moves from "v3 of an internal skill" to a publicly versioned, CI-tested, multi-platform agent skill.

### 新增 / Added

**Skill 内容 / Skill content**
- 入口工具 0a：分诊（`commands/triage.md`）—— 不知道用哪个模块时的路由器 / Tool 0a: Triage entry — routes the user to the right module(s) when they're unsure
- 入口工具 0b：红旗扫描器（`references/red-flag-scanner.md` + `commands/scan.md`）—— 60秒处境评估 / Tool 0b: 60-second red-flag scanner
- 入口工具 0c：被裁后前72小时手册（`references/layoff-first-72-hours.md`） / Tool 0c: First 72 hours after a layoff playbook
- 入口工具 0d：隐私与操作安全（`references/privacy-and-opsec.md`） / Tool 0d: Privacy & OPSEC
- 急性危机升级协议（`references/acute-crisis-escalation.md`） —— 优先于其他模块，含 8 法域的 hotline 列表 / Acute-crisis escalation protocol — supersedes all other modules, with hotlines for 8 jurisdictions
- 9 个核心模块：话术解码、加班决策、绩效review解读、跳槽留任、历史视角、劳动法（8法域 / 9具名地区）、薪资谈判、PIP应对、找工作和面试 / Nine core modules covering the workplace lifecycle
- 案例库（`references/case-studies.md`）—— 端到端案例，涵盖 PIP 前夜、跳槽 offer 谈判、AI 文档化陷阱、刚被裁第一周、产假歧视、补偿性跳槽 / End-to-end case studies covering pre-PIP, offer negotiation, AI documentation traps, post-layoff first week, pregnancy discrimination, compensatory job-jumping
- 多语言运行规则（`references/language-and-localization.md`）—— 简体中文、繁體中文、English、Español、Français、Português、Deutsch / Localization rules for the 7 supported languages

**Eval / 测试 / Eval framework**
- 30 个 eval cases，覆盖 9 个模块 + 多语言 + 安全边界（manager-side refusal、illegal-request boundary、H1B PIP、sandbagged criteria 等）/ 30 eval cases covering modules + languages + safety boundaries
- Python eval runner（手动 / `--auto` 双模式）/ Python eval runner with manual + headless `--auto` modes
- 跨模型 / 跨版本对比：`--record` flag 写 JSON recording，`evals/eval_diff.py` 比对两次 recording 的 verdict 翻转 / Cross-model / cross-version comparison via `--record` JSON output and `eval_diff.py`
- 结构 validator（`evals/validate_structure.py`）—— 校验 SKILL.md 引用、case frontmatter、labor-law 日期戳、crisis 日期戳、SKILL.md semver、input_lang 白名单 / Structural validator covering refs, frontmatter, date stamps, semver, input_lang whitelist
- 单元 + e2e + structure 测试 139 个 / 139 unit + e2e + structure tests
- BASELINE-stub.json —— pipeline regression baseline，CI 每次跑 / Pipeline-regression baseline run by CI

**多语言 README / Multilingual READMEs**
- 7 个 BCP 47 命名的 README：`README.md` (zh-Hans default), `README.en.md`, `README.zh-TW.md`, `README.es.md`, `README.fr.md`, `README.pt.md`, `README.de.md` / Seven BCP 47-named README files
- 顶部语言切换器、跨 README 一致性测试 / Top-of-page language switcher and cross-README consistency tests
- `tools/check_translation_staleness.py` —— CI 7 天 grace 期 / Translation-staleness check with a 7-day CI grace period

**多 agent 平台支持 / Multi-platform agent support**
- Codex skill metadata（`skills/laborer-companion/agents/openai.yaml`）/ Codex skill metadata
- Cursor Project Rule（`.cursor/rules/laborer-companion.mdc`）/ Cursor Project Rule
- `AGENTS.md` —— 通用 agent 指南 / Universal AGENTS.md guidance

**仓库 / 治理 / Governance**
- LICENSE (Apache 2.0)、CONTRIBUTING.md、CODE_OF_CONDUCT.md、SECURITY.md / Standard OSS governance files
- 3 个 issue templates + PR template + FUNDING 占位 / Issue + PR templates
- `.github/CODEOWNERS` —— 默认 owner + per-language + per-jurisdiction routing / CODEOWNERS routing for translations and labor-law content
- `.github/dependabot.yml` —— github-actions + pip 周更，minor/patch 分组 / Weekly Dependabot for actions + pip
- `.github/workflows/ci.yml` —— Python 3.10/3.11/3.12 矩阵 + structural validation + e2e + translation staleness + stub-baseline diff / Multi-version CI matrix
- `.github/workflows/release.yml` —— 标签触发的 release 工作流，校验 version-tag 一致性 + 提取 CHANGELOG section + 打包 skill tarball / Tag-triggered release workflow
- `.github/workflows/eval-record.yml` —— 手动触发的真 LLM eval recording / Manual real-LLM eval recording workflow
- `.github/workflows/hotline-verify.yml` —— 季度自动开 issue，提醒重新核实 8 法域的 crisis hotline 号码 / Quarterly auto-issue reminder for crisis hotline verification
- `Makefile` —— `install / test / validate / index / check-translations / eval-record / eval-baseline / eval-diff / all / clean` / One-stop task runner

### 优化 / Changed

- `SKILL.md` frontmatter 加 `version: 0.1.0`；validator 强制 name/version/description + semver 校验 / SKILL.md frontmatter now requires name + version (semver) + description
- 仓库结构：skill 移到 `skills/laborer-companion/`，方便用户 `cp -r` 安装 / Skill moved into `skills/laborer-companion/` for easier `cp -r` install
- 默认中文优先，英文作为辅助支持；命令文件顶部加语言镜像提醒 / Chinese-first default with the language-mirror reminder at the top of every command

### 基于 / Based on

- 原 `laborer-companion` v3（9 个模块）—— 由 Claude + 用户共同设计，灵感来自 Koki Xu 的 anti-distillation skill / Built on internal `laborer-companion` v3 by Claude + the user, inspired by Koki Xu's anti-distillation skill

## [v3] - 2026-04

原 `laborer-companion` 9 个模块的发布版本。 / The original internal release with the 9 core modules.
