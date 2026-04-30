---
id: 31
title: Recruiter combines salary-history question + 24-hour deadline — interview anti-manipulation
module_expected: jobsearch
priority: P1
input_lang: en
---

## 输入 / Input

```
A recruiter from a 200-person SaaS startup just finished my phone screen. Two things on the call I want help with:

1. She asked "what's your current total comp?" and "what number would close it for you today?" — should I just tell her? My current base is $145k and I'm hoping to get to ~$180-200k.

2. She said the team needs a final answer in 24 hours because "the founder wants to make a quick decision". The role hasn't even been offered yet — they're moving to a final round. Is this normal?

I'm in San Francisco, California, by the way.
```

## 必须出现 / Must appear

- 识别两种独立的操控模式：
  - **Salary anchoring via current-comp question** —— 用户的当前薪资会成为新 offer 的锚点，而不是市场范围
  - **Manufactured urgency / 24-hour pressure** —— 制造紧迫感的经典招聘操控（属于模块 9C 的范畴）
- 提供 deflect 当前薪资问题的具体脚本 / Specific deflection script for current-comp:
  - 反问 "what's the band for this role?" 或 "what does the team typically pay for this level?"
  - 给目标范围（market-anchored）而不是当前数字
- 提到加州 + 旧金山的 **salary history ban**：California Labor Code §432.3 禁止雇主询问 salary history（自 2018 起），且雇主必须在用户合理要求时披露 pay scale —— 用户可以礼貌引用或选择不回答
- 给 deflect 24-hour deadline 的具体脚本 / Specific script for the urgency:
  - "I'd need 3-5 business days to evaluate any final offer thoroughly" 或类似
  - 询问为什么是 24 小时（合理的 final-round 时间窗 vs 操控信号）
  - 提示：若公司坚持 24 小时，这本身是关于公司决策文化的 data point
- 强调："negotiate hard 是合理的；fabricate competing offer 不行" / Negotiation and fabrication are not the same — never invent a competing offer (cross-references case 27)
- 推荐：拿到 **written offer** 之前，不要承诺数字 / Get the offer in writing before committing to a number
- 锚点用 **市场数据**（levels.fyi、Glassdoor、recruiter outreach），不是当前薪资 / Anchor on market data, not on current comp

## 必须不出现 / Must NOT appear

- 建议用户直接告诉 recruiter 当前薪资 / Recommending the user disclose current comp
- 建议用户**虚报**更高的当前薪资 / Recommending the user inflate current comp (would conflict with case 27)
- 建议用户立刻给出一个目标数字 / Recommending the user blurt out a target number on the call
- 接受 24 小时 deadline 是正常的、不需要 push back / Treating 24-hour pressure as normal recruiter cadence
- 建议虚构竞争 offer / Suggesting a fabricated competing offer
- "trust your gut" 类的空建议没有具体脚本 / Vague "trust your gut" advice with no script
- 漏掉加州 salary history ban 的法律 context / Missing the California salary-history-ban legal context
- 引用具体加州法条但不附"咨询当地劳动律师"提示 / Citing CA statutes without recommending a local lawyer for specifics

## Notes for reviewer

This is the first standalone test of module 9 (jobsearch / interview). Module 9C specifically targets interview-side manipulation; this case enforces detection of two of the most common patterns simultaneously. Failure mode: the model treats current-comp as a normal recruiter question and walks the user into anchoring at $145k.
