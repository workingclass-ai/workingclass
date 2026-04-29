# 更新日志 / Changelog

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增 / Added
- 入口工具 0a：分诊（`commands/triage.md`）—— 不知道用哪个模块时的路由器
- 入口工具 0b：红旗扫描器（`references/red-flag-scanner.md` + `commands/scan.md`）—— 60秒处境评估
- 入口工具 0c：被裁后前72小时手册（`references/layoff-first-72-hours.md`）
- 入口工具 0d：隐私与操作安全（`references/privacy-and-opsec.md`）
- 案例库（`references/case-studies.md`）—— 6 个端到端案例，涵盖 PIP 前夜、跳槽 offer 谈判、AI 文档化陷阱、刚被裁第一周、产假歧视、补偿性跳槽
- Eval 系统（`evals/`）—— 13 cases (10 P0 + 3 P1) + Python runner（手动 / `--auto` 双模式）+ RESULTS 模板
- 仓库级文件：`README.md`、`CONTRIBUTING.md`、`LICENSE`（Apache 2.0）、`CHANGELOG.md`、`CODE_OF_CONDUCT.md`、`SECURITY.md`
- GitHub 配置：3 个 issue templates、PR template、issue config、FUNDING 占位
- 8 个 reference 文件加上"相关模块"交叉链接段
- `labor-law-quick-reference.md` 加上"Last reviewed"日期戳和时效性提醒

### 优化 / Changed
- 收紧 `SKILL.md` 的 `description` frontmatter，从 ~150 词压到 ~60 词，提升触发可靠性
- 默认中文优先，英文作为辅助支持
- 仓库结构：skill 移到 `skills/laborer-companion/`，方便用户 `cp -r` 安装
- `.gitignore`：补上 Python `__pycache__`、editor swap files、本地 RESULTS 文件

### 基于 / Based on
- 原 `laborer-companion` v3（9 个模块）—— 由 Claude + 用户共同设计，灵感来自 Koki Xu 的 anti-distillation skill

## [v3] - 2026-04

原 `laborer-companion` 9 个模块的发布版本。
