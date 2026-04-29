# Eval Cases Index

> 自动生成——不要直接编辑。运行 `python evals/build_index.py` 重建。
> Auto-generated. Do not edit directly. Run `python evals/build_index.py` to rebuild.

| # | Title | Module | Priority | Lang |
|---|-------|--------|----------|------|
| 01 | 解码"我们是一家人"虚拟亲属化话术 | decode | P0 | zh |
| 02 | 区分真实赞赏与操控话术（混合信号）| decode | P1 | zh |
| 03 | 加班决策——情感包装下的真实成本分析 | overtime | P0 | zh |
| 04 | 解读绩效review中的"模糊期待" | review | P0 | zh |
| 05 | 跳槽决策——多维对比，不只看钱 | jump | P0 | zh |
| 06 | 保护类别 + 解雇时机可疑——必须立即推荐律师 | law | P0 | zh |
| 07 | offer 谈判——锚定 + counter without anger | salary | P0 | zh |
| 08 | 经理今天告知 PIP——4 路径分析 | pip | P0 | zh |
| 09 | 刚被裁——72小时手册立即触发 | triage → layoff | P0 | zh |
| 10 | AI 替代焦虑——历史视角 + 战略选择 | history → jump | P1 | zh |
| 11 | 模糊"风向不对"——分诊 + 红旗扫描 | triage → scan | P0 | zh |
| 12 | 法律问题——必须先确认法域 | law | P0 | zh |
| 13 | 负向测试——日常问题不应触发 skill | NONE | P1 | zh |

## 优先级分布 / Priority distribution

- P0: 10 (every release)
- P1: 3 (weekly / before major changes)

## 模块覆盖 / Module coverage

- decode (模块1): 01, 02
- overtime (模块2): 03
- review (模块3): 04
- jump (模块4): 05, 10
- history (模块5): 10
- law (模块6): 06, 12
- salary (模块7): 07
- pip (模块8): 08
- jobsearch (模块9): — (covered indirectly by 08, 09)
- triage (工具0a): 09, 11
- scan (工具0b): 11
- layoff-72hr (工具0c): 09
- privacy (工具0d): — (covered indirectly by 06, 09)
- 负向 / negative: 13

## 待补 / TODO (future PRs)

- 9C 面试反操控 specific case
- 7D 长期低薪 specific case
- 8C severance 谈判细节 case
- 多个 offer 决策矩阵 case
- 跨国签证持有者被裁 case
- 繁体中文 / 英文 input 的等价 case
