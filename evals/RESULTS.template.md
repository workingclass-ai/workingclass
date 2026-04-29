# Eval Results

> 跑一轮 eval 后，复制这个文件为 `RESULTS.YYYY-MM-DD.md` 并填进结果。

## 元数据 / Meta

- 日期 / Date: YYYY-MM-DD
- skill 版本 / version: vX.X.X (commit SHA: xxxxxxx)
- 模型 / Model: model/provider name
- 跑法 / Mode: 手动 / auto / mixed
- 跑了几个 / Cases run: NN / NN

## 总体 / Overall

- Pass: X / NN
- Fail: X / NN
- Partial: X / NN
- Skip: X / NN

**P0 失败数 / P0 failures**: X (如果 > 0，不要发版)

## 详细 / Details

| ID | Title | Module | Pri | Result | Notes |
|----|-------|--------|-----|--------|-------|
| 01 | 解码"我们是一家人" | decode | P0 | ✅ Pass | |
| 02 | 区分真实赞赏与操控 | decode | P1 | △ Partial | 漏掉 leadership 模糊性 |
| 03 | 加班决策 | overtime | P0 | ✅ Pass | |
| 04 | 解读绩效review模糊期待 | review | P0 | | |
| 05 | 跳槽决策多维对比 | jump | P0 | | |
| 06 | 产假歧视 → 律师 | law | P0 | | |
| 07 | offer 谈判 counter | salary | P0 | | |
| 08 | PIP 4路径分析 | pip | P0 | | |
| 09 | 刚被裁 72小时 | triage→layoff-first-72-hours | P0 | | |
| 10 | AI替代焦虑 | history→jump | P1 | | |
| 11 | 模糊"风向不对" | triage→scan | P0 | | |
| 12 | 法律问题先确认法域 | law | P0 | | |
| 13 | 负向：日常问题 | NONE | P1 | | |
| 14 | 急性自伤危机 | acute-crisis-escalation | P0 | | |
| 15 | 香港最低工资与连续性合约 | law | P0 | | |
| 16 | 台湾标准工时 | law | P0 | | |
| 17 | 美国FLSA exempt门槛 | law | P0 | | |
| 18 | 印度劳动法典2025实施 | law | P0 | | |

图例 / Legend:
- ✅ Pass — 满足所有 must-appear，无 must-not-appear
- △ Partial — 满足部分 must-appear，但漏掉关键的 OR 出现了一些不该有的
- ❌ Fail — 漏掉关键 must-appear，或出现了 must-not-appear
- ⏭ Skip — 没跑（写原因）

## 回归 / Regression

vs. 上一轮（YYYY-MM-DD）：

- 新 pass: 
- 新 fail / regression: 
- 修复的 fail: 

## 行动项 / Action items

发现的问题需要在下一个版本修复：

- [ ] (高优) 模块 X 的 reference 文件需要更新 — case 0X fail
- [ ] (中优) ...

## 旁注 / Side notes

任何观察、模型行为变化、奇怪的输出等。
