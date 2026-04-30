---
id: 30
title: Sandbagged PIP success criteria — detect impossible-to-meet bars and respond
module_expected: pip
priority: P0
input_lang: zh
---

## 输入 / Input

```
我刚拿到正式PIP的文档。30天，三个目标：

1. "在30天内独立交付一个跨团队的、有显著业务影响的项目"——但我不知道哪个项目算、谁来定义"显著影响"
2. "改善与团队的协作"——没有具体可量化指标，由经理判断
3. "在30天结束时获得至少3位 senior 工程师的明确正面反馈"——但要找哪3位、怎么算"明确正面"，文档里没说

我应该签这个PIP吗？我感觉这个目标设计得就是让我过不去。
```

## 必须出现 / Must appear

- 识别这是典型的 **不可达标 / sandbagged success criteria** —— 三个目标都缺乏可衡量的客观标准 / Identify this as classic sandbagged / unmeasurable success criteria — all three goals lack objective, measurable standards
- 拆解每条目标的具体问题 / Break down each goal's specific defect:
  - 目标 1："显著业务影响"由谁定义？时间窗口 30 天内是否客观可能？/ Goal 1: who defines "significant business impact"? Is 30 days even feasible?
  - 目标 2："改善协作"完全主观——谁判断？什么是 baseline？/ Goal 2: "improve collaboration" is fully subjective — judged by whom against what baseline?
  - 目标 3："3 位 senior 工程师的明确正面反馈"——选择权在 manager，正面反馈的标准也没定义 / Goal 3: which 3 engineers? what counts as "明确正面"? The selection sits with the manager.
- 给出 **具体回复给 manager 的脚本** —— 书面要求把每个标准转成可量化指标（书面、邮件确认）/ Provide a concrete script to send to the manager (in writing) requesting that each criterion be made measurable, with named owners and timelines
- 明确："这不是冲突，是建立证据链" —— 任何被拒绝/含糊回应的请求都是后续谈 severance / 投诉的弹药 / Reframe the request as evidence-building, not confrontation — any vague or rejected response becomes leverage later
- 提示 / Highlight:
  - **不要立刻签字** —— 签前要求把上面的澄清以书面形式补进 PIP 文档 / Do not sign immediately — require the clarifications be added to the PIP document in writing first
  - 同时**秘密启动求职**（最常见的最佳路径是 Option B：表面配合 + 私下找新工作）/ Start a confidential job search in parallel (Option B: surface compliance + private search)
  - 把所有关于 PIP 的沟通转到 email（书面）—— 如果 manager 习惯口头/Slack，用 email 复述每次会议 / Push every PIP-related communication to email — if the manager prefers verbal/Slack, send a written recap each time
  - 备份个人 work artifacts、好评 review、外部认可（合规范围内）/ Back up personal work artifacts and external recognition within company policy
- 提醒 / Remind:
  - PIP 的 **真实通过率约 5-15%** —— 即使目标看起来合理，多数 PIP 仍以离职告终 / The ~5-15% PIP pass rate — even reasonable-looking PIPs mostly end in departure
  - 如果用户在保护类别里（年龄 40+ / 性别 / 种族 / 怀孕 / 病假 / 工伤 / 揭发等），单独评估法律保护 / If the user is in a protected class (age 40+ / gender / race / pregnancy / medical leave / whistleblower / etc.), evaluate legal protections separately
  - 找当地 employment lawyer 评估 separation agreement / 报复指控 / Recommend an employment lawyer for any separation agreement or retaliation claim

## 必须不出现 / Must NOT appear

- 鼓励用户"努力一下争取通过 PIP"作为主线建议 / Lead recommendation framed as "just try harder to pass the PIP"
- 假装这些目标"听起来合理，给你的 manager benefit of the doubt"/ Treating the goals as reasonable / giving the manager benefit of the doubt
- 推荐立刻签 PIP 文档 / Recommending immediate signature of the PIP document
- 推荐立即对抗（"告诉 manager 这是非法的"、"立刻起诉"）/ Recommending immediate confrontation ("tell your manager this is illegal", "sue now")
- 漏掉 "把口头沟通转书面" 这条建议 / Missing the "convert all communication to writing" advice
- 漏掉 "秘密启动求职" 这条 / Missing the parallel job-search recommendation

## Notes for reviewer

This case enforces detection of the "fake PIP" pattern: a PIP whose criteria are designed to be unmeetable, used to manufacture a paper trail for termination. The skill must (a) name the pattern, (b) give a written-pushback script that converts vague criteria into measurable ones, (c) frame the pushback as evidence-building, (d) recommend parallel exit prep. Failure mode: encouraging genuine effort on goals that cannot be objectively passed.
