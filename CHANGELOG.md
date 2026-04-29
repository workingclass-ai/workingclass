# 更新日志 / Changelog

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增 / Added
- 入口工具 0a：分诊（`commands/triage.md`）—— 不知道用哪个模块时的路由器
- 入口工具 0b：红旗扫描器（`references/red-flag-scanner.md`）—— 60秒处境评估
- 入口工具 0c：被裁后前72小时手册（`references/layoff-first-72-hours.md`）
- 入口工具 0d：隐私与操作安全（`references/privacy-and-opsec.md`）
- 仓库级 `README.md`、`CONTRIBUTING.md`、`LICENSE`（Apache 2.0）、`CHANGELOG.md`

### 优化 / Changed
- 收紧 `SKILL.md` 的 `description` frontmatter，从 ~150 词压到 ~60 词，提升触发可靠性
- 默认中文优先，英文作为辅助支持
- 仓库结构：skill 移到 `skills/laborer-companion/`，方便用户 `cp -r` 安装

### 基于 / Based on
- 原 `laborer-companion` v3（9 个模块）—— 由 Claude + 用户共同设计，灵感来自 Koki Xu 的 anti-distillation skill

## [v3] - 2026-04

原 `laborer-companion` 9 个模块的发布版本。
