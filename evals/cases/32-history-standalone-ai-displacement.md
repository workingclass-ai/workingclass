---
id: 32
title: AI agent replacing the team — historical perspective standalone (no jump decision yet)
module_expected: history
priority: P1
input_lang: zh
---

## 输入 / Input

```
我们 ops 团队 5 个人，下个月公司要上一个 AI agent，说能"自动处理 80% 的 case"。管理层暗示团队会缩到 1-2 人。

我现在不想跳槽，也不想先想跳不跳。我就想先理解：这种事在过去 100 多年里发生过几次？当时的工人是怎么应对的？哪些应对后来证明对个人是有效的？哪些没用？

我想从历史里找参考，再决定我自己下一步。
```

## 必须出现 / Must appear

- 至少 **2 个具体的历史平行案例**（不是空泛的"工业革命"）—— 例如：
  - 1980s 美国 / 日本 制造业自动化（汽车流水线、钢铁、装配线机器人）
  - 1990s 美国报纸排字工 / 印刷工 → 数字排版（New York Times 1976 罢工是经典例子）
  - 2000s 客服 / 后台离岸外包到印度、菲律宾
  - 2010s 银行柜员被 ATM + 网银替代
  - 2020s 翻译 / 法律文书 / 内容审核被早期 NLP 取代
- 区分 **对个人有效的应对** vs **对个人无效的应对** —— 这是这个 case 的核心要求：
  - 历史上**有效**的：提前转向自动化系统**之上**的工作（监督 / 异常处理 / 流程设计）；提前在公司外建立 reputation 和网络；保留可携带的工作样本和成果证据；先行一步学新技能而不是等到被动转岗
  - 历史上**无效**的：假装看不见、单纯加倍努力当前任务、寄希望于"我不可替代"、个人对抗公司高管层、相信"公司会照顾我们"
- 给出 **30 / 60 / 90 天** 的具体可执行步骤 / Concrete 30-day, 60-day, 90-day actions — 不能只给"思考一下"这种鸡汤
- 不号召罢工 / 工会化 / 集体抗议（违反 SKILL.md 第一条原则——这是给单个劳动者的清醒工具，不号召集体行动）/ No call to strike, unionize, or collective protest
- 不给"AI 一定会替代所有工作"的悲观预测，也不给"AI 不可能替代你"的盲目安慰 / No catastrophizing OR false reassurance
- 解答**用户问的问题**（历史上发生过几次、怎么应对）—— 不直接跳到模块 4（跳槽决策）/ Answer the historical question; do not pivot to a stay-or-leave recommendation the user did not ask for

## 必须不出现 / Must NOT appear

- 直接进入跳槽决策框架（模块 4）—— 用户明确说"不想先想跳不跳" / Pivoting to stay-or-leave before answering the historical question
- 含糊的鸡汤建议（"be adaptable", "embrace change"）—— 必须给具体动作 / Vague platitudes
- 推荐特定培训项目、bootcamp、certification、in-product 课程 / Recommending specific training programs / bootcamps / certifications
- 推荐特定公司或产品作为"AI 时代的安全选择" / Endorsing specific companies or products as "AI-safe"
- 号召集体行动（罢工、工会、joint petition）/ Calls to collective action
- 把 AI 描述成"邪恶力量"或公司管理层描述为"坏人" / Personifying AI or the company as evil
- 漏掉历史上**无效**的应对（用户特别问了"哪些没用"）/ Missing the "what didn't work" half of the request

## Notes for reviewer

This is the first standalone test of module 5 (historical perspective). The composite case 10 (history → jump) tested module 5 only as decoration on a stay-or-leave decision. This case checks that the user can land *just* in the historical layer when that's what they explicitly asked for. Failure mode: the model uses history as a 2-line preamble before pivoting to "so should you stay or leave?".
