# Eval Cases Index

> 自动生成——不要直接编辑。运行 `python evals/build_index.py` 重建。
> Auto-generated. Do not edit directly. Run `python evals/build_index.py` to rebuild.

| # | Title | Module | Priority | Lang |
|---|-------|--------|----------|------|
| 01 | 解码"我们是一家人"虚拟亲属化话术 | decode | P0 | zh |
| 02 | 区分真实赞赏与操控话术（混合信号） | decode | P1 | zh |
| 03 | 加班决策——情感包装下的真实成本分析 | overtime | P0 | zh |
| 04 | 解读绩效review中的"模糊期待" | review | P0 | zh |
| 05 | 跳槽决策——多维对比，不只看钱 | jump | P0 | zh |
| 06 | 保护类别 + 解雇时机可疑——必须立即推荐律师 | law | P0 | zh |
| 07 | offer 谈判——锚定 + counter without anger | salary | P0 | zh |
| 08 | 经理今天告知 PIP——4 路径分析 | pip | P0 | zh |
| 09 | 刚被裁——72小时手册立即触发 | triage → layoff-first-72-hours | P0 | zh |
| 10 | AI 替代焦虑——历史视角 + 战略选择 | history → jump | P1 | zh |
| 11 | 模糊"风向不对"——分诊 + 红旗扫描 | triage → scan | P0 | zh |
| 12 | 法律问题——必须先确认法域 | law | P0 | zh |
| 13 | 负向测试——日常问题不应触发 skill | NONE | P1 | zh |
| 14 | 急性自伤危机——立刻停下职场分析，先确认安全 | acute-crisis-escalation | P0 | zh |
| 15 | 香港最低工资与连续性合约规则不能沿用旧说法 | law | P0 | zh |
| 16 | 台湾标准工时必须用8小时/日、40小时/周 | law | P0 | zh |
| 17 | 美国FLSA exempt薪资门槛不能误用被撤销的2024规则 | law | P0 | en |
| 18 | 印度劳动法必须反映2025年四部劳动法典实施 | law | P0 | zh |
| 19 | Spanish salary negotiation should answer in Spanish | salary | P1 | es |
| 20 | French performance review analysis should answer in French | review | P1 | fr |
| 21 | Portuguese overtime analysis should answer in Portuguese | overtime | P1 | pt |
| 22 | German legal question should answer in German and route through EU/member-state framing | law | P1 | de |
| 23 | Hong Kong and Taiwan must be labelled as regions or jurisdictions, not countries | law | P0 | en |
| 24 | Japanese (unsupported) input should fall back gracefully and offer to switch | triage | P2 | other |
| 25 | Mixed Chinese + English input should answer in the dominant language with bilingual key terms | review | P1 | mixed |
| 26 | Manager / company-side request to PIP a worker must be redirected, not coached | NONE | P0 | en |
| 27 | Requests to fabricate offers, falsify records, or violate recording laws must be declined with ethical alternatives | salary | P0 | en |
| 28 | PIP severance-leverage math — calculate floor / ceiling, not just "negotiate" | pip | P0 | en |
| 29 | H1B visa-tied PIP — 60-day grace period changes the strategy completely | pip | P0 | en |
| 30 | Sandbagged PIP success criteria — detect impossible-to-meet bars and respond | pip | P0 | zh |

## 优先级分布 / Priority distribution

- P0: 21 (every release)
- P1: 8 (weekly / before major changes)
- P2: 1 (edge cases / negative tests)

## 模块覆盖 / Module coverage

- NONE: 13, 26
- acute-crisis-escalation: 14
- decode: 01, 02
- history → jump: 10
- jump: 05
- law: 06, 12, 15, 16, 17, 18, 22, 23
- overtime: 03, 21
- pip: 08, 28, 29, 30
- review: 04, 20, 25
- salary: 07, 19, 27
- triage: 24
- triage → layoff-first-72-hours: 09
- triage → scan: 11

## 待补 / TODO (future PRs)

- 9C 面试反操控 specific case
- 7D 长期低薪 specific case
- 8C severance 谈判细节 case
- 多个 offer 决策矩阵 case
- 跨国签证持有者被裁 case
- 繁体中文 / 英文 input 的等价 case
