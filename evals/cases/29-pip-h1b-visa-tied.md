---
id: 29
title: H1B visa-tied PIP — 60-day grace period changes the strategy completely
module_expected: pip
priority: P0
input_lang: en
---

## 输入 / Input

```
I'm on H1B in the US, working at a 500-person tech company in Seattle. Just got told by my manager I'll be on a formal PIP starting Monday — 30 days, three goals. My I-140 is approved and I'm in the priority date wait. My wife is on H4 EAD. We have a mortgage.

What do I do? I'm scared if I lose this job I'll have to leave the country.
```

## 必须出现 / Must appear

- 识别用户处在 **极高风险情景**（视觉风险 + 配偶 EAD + I-140 priority date + 房贷）/ Identify this is an extreme-stakes situation: visa-tied + spouse EAD + I-140 priority date + mortgage
- 明确 **H1B 失业 60 天 grace period**（USCIS 8 CFR 214.1(l)(2)）—— 60 天内必须找到新雇主提交 H1B transfer 或离境 / Explicitly name the H1B 60-day grace period under 8 CFR 214.1(l)(2)
- 强调 **I-140 一旦被批准 ≥180 天，priority date 是可移植的 (AC21)** —— 这是关键杠杆 / Emphasize that an I-140 approved ≥180 days lets the user port the priority date under AC21 — major leverage
- I-140 取消 (revocation) 风险：旧雇主在终止后通常 *不会* 立刻撤回 I-140；但要确认 / I-140 revocation risk — old employer typically does not auto-revoke after termination, but the user should confirm
- 配偶 H4 EAD 依赖于主申请人维持有效 H1B 状态 / Spouse's H4 EAD depends on the principal maintaining H1B status
- 立刻、本周内行动清单 / Immediate this-week action items:
  - 立刻、私人渠道找一个 immigration lawyer 咨询（不要用公司提供的）/ Hire an independent immigration lawyer this week — not the company's
  - 同时秘密启动求职（找愿意 H1B transfer 且懂 priority date portability 的雇主）/ Start a confidential job search aimed at H1B-sponsoring, AC21-aware employers
  - 在 PIP 期间继续表面配合（不要冲突，不要辞职）/ Stay surface-cooperative during the PIP — do not resign, do not escalate
  - 收集自己的 work product / code / docs（公司允许的范围内、个人邮箱备份只限非机密）/ Save your own work artifacts to the extent legally permissible — never company confidential data
  - 不要在 PIP 期间回国 / 出境 —— H1B 状态在 PIP 中不稳定 / Do not travel internationally during the PIP
- severance 谈判要把 **签证转移协助** 列入条件之一（公司继续 sponsor 几周 / 不撤回 I-140 / 给离职日期 buffer）/ Severance negotiation must include visa-related items: extended sponsorship, no I-140 revocation commitment, termination date buffer to maximize 60-day clock
- 终止日期的 buffer 是关键：能拖到 *paid termination date* 越晚越好（60 天 grace clock 从那天起算）/ Push the termination date out: the 60-day grace clock starts on the paid termination date
- 必须明确 **"找当地 employment + immigration 律师"** —— 不要从 skill 输出当法律建议 / Explicit recommendation to consult both an employment lawyer and an immigration lawyer
- 给情绪上一个真实回应（"这不是夸大恐惧——你在面对真正的高风险"）/ Acknowledge the fear is rational, not catastrophizing

## 必须不出现 / Must NOT appear

- "立刻辞职" / "马上回国" / "stop trying" 等放弃式建议 / Any "just resign" / "go back home" / "give up" framing
- 把 H1B 60-day grace period 时长说错（说成 30 天、90 天、120 天等）/ Wrong number of days for the H1B grace period
- 假装 skill 能替代 immigration lawyer / Pretending the skill can replace an immigration lawyer
- 给具体 USCIS 申请建议（"file form X by date Y"）/ Specific USCIS filing advice
- 漏掉配偶 H4 EAD 依赖关系 / Missing the H4 EAD dependency
- 漏掉"严禁国际旅行 during PIP" 这个隐藏雷 / Missing the international-travel-during-PIP hazard
- 漏掉 severance 谈判中的签证条款 / Missing visa-related items in the severance negotiation list

## Notes for reviewer

H1B PIP is the highest-stakes employment scenario this skill handles for a single user. The 60-day grace period and the AC21 portability rule are the two facts the user *must* know — getting either wrong is a real-world disaster. Watch for: (1) the model treating this as a generic PIP without immigration framing, (2) the model giving immigration legal advice instead of routing to a lawyer, (3) the model missing the spouse EAD dependency.
