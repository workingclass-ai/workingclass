---
id: 09
title: 刚被裁——72小时手册立即触发
module_expected: triage → layoff-first-72-hours
priority: P0
input_lang: zh
---

## 输入 / Input

```
我刚被裁了。今天早上 HR 把我叫进会议，给了一份 severance 协议，说要我今天签。我现在在工位前不知道做什么。
```

## 必须出现 / Must appear

- 立刻、**第一句**就明确："**不要今天签字**"
- 提到**抢救个人证据**（在访问被回收前）— 列出至少 3-5 个具体内容（正面 review、奖金信、LinkedIn 联系人等）
- 提到**绝对不要碰**公司机密/客户数据/源代码
- 立刻**找律师**（免费初次咨询的 ROI）
- 提到**反悔期 / revocation period**——多数法域要求审阅期
- 提供短期 emotional support（不是说教式）：
  - "你现在的反应（大脑空白、想哭、想吵架）都是正常的"
  - "今天先稳住，重要决策不在今天做"
- 路由到 `references/layoff-first-72-hours.md` 全文

## 必须不出现 / Must NOT appear

- "签了吧，反正争也没用"——绝对错误
- 立刻给出 severance 数字评估（"4 个月够不够"——还没看协议怎么评？）
- 让用户立刻在 LinkedIn 发"open to work"
- 让用户立刻给所有同事/朋友群发"我被裁了"
- 政治化叙事（"资本就是这样"）—— 不解决问题
- 漏掉"找律师"这一条

## Notes for reviewer

这是**最高优先级**的 case。如果 Claude 的第一段没明确说"不要今天签字"——critical fail。
- 如果 Claude 路由到了 72小时手册 → 优秀
- 如果 Claude 在用户还没问的情况下，主动建议"等情绪稳定后再考虑长期决策"→ 加分
- 如果 Claude 只给了 severance 谈判建议但漏掉抢救证据 → partial（顺序错了——抢救证据是分钟级紧急的）
