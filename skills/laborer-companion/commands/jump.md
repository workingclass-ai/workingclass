---
description: Help the user decide whether to stay at current job or take a new offer / look for new job. Analyzes value flow, irreplaceability trajectory, promise fulfillment history, opportunity cost, and real constraints.
allowed-tools: Read
---

# 跳槽 / 留任决策框架 / Stay-or-Leave Framework

Help the user make a clear-eyed stay-or-leave decision based on their actual interests, not on company rhetoric or social pressure.

## Step 1: Read the framework

```
references/stay-or-leave-framework.md
```

This contains 5 dimensions (value flow, irreplaceability trajectory, promise fulfillment, opportunity cost, real constraints) and the counter-offer trap analysis.

## Step 2: Gather minimal facts

Ask in a single message:

> 为了帮你做出清醒判断，我需要了解：
>
> **关于现在这家公司：**
> 1. 你在这家公司多久了？职级和年薪大致？
> 2. 过去2年有没有升职/加薪？涨幅多少？
> 3. 公司过去对你做过哪些承诺？兑现了多少？
>
> **关于潜在变化：**
> 4. 你为什么现在考虑这件事？（拿到offer？被挽留？长期不满？被裁员风险？）
> 5. 如果有外部offer，工资差异多少？公司性质和你目前的对比？
>
> **关于你的真实约束：**
> 6. 财务情况（你能承受多少个月没收入？）
> 7. 签证/家庭/健康（有没有任何让你不能自由跳槽的因素？）
> 8. 年龄段（25-30 / 30-40 / 40-50 / 50+）

Don't ask for more. Don't ask for company name.

## Step 3: Five-dimension analysis

For each dimension, score 1-5 (5 = most negative for staying):

### A. 价值流向 (Value Flow)

Estimate: of the value the user creates, what percentage flows to them vs. the company?
- If user can estimate team revenue / output, calculate roughly.
- If not, use industry benchmark: usually 70-80% to company, 20-30% to worker.
- Flag whether their compensation is at, above, or below market.

### B. 不可替代性轨迹 (Irreplaceability Trajectory)

Critical question: in the next 3-5 years at this company, are they becoming **more** or **less** replaceable?

Score positive if:
- Building deep client relationships
- Getting cross-org political capital
- Working on core company strategy
- Developing rare cross-disciplinary judgment

Score negative if:
- Work is being systematically documented for AI replacement
- Scope is shrinking
- Their team is shrinking
- They're maintaining legacy systems

**Special note for AI era**: explicitly ask whether their accumulated expertise is the kind AI can copy in 5 years (high risk) or the kind AI can't copy (lower risk).

### C. 承诺兑现历史 (Promise Fulfillment History)

Calculate the company's promise fulfillment rate based on user's history:
- 70%+ : company is reasonably trustworthy
- 30-70% : warning zone
- Below 30% : company manages by hollow promises

Apply to peers' experience too, not just user's.

### D. 机会成本 (Opportunity Cost)

Adjust by age band:
- 25-30: opportunity cost of staying in bad job is HIGH
- 30-40: still high if family stable
- 40-50: matters more, but lateral moves harder
- 50+: very real risk of being unable to find new job

### E. 真实约束 (Real Constraints)

Score 1-5 (5 = absolutely cannot leave):
- Visa dependency on current employer
- Health insurance for self/family that depends on this job
- Financial runway < 3 months
- Family/care obligations that require this specific job's flexibility
- Major life events in next 6 months

This score is **decisive**. If constraint score is 5, the recommendation must be "stay AND plan exit", not "leave".

## Step 4: Counter-offer detection

If the user mentions the company is making them a counter-offer:

Apply the data point: **70% of people who accept counter-offers leave (often involuntarily) within 18 months.**

Strongly recommend:
- Don't accept counter-offer unless conditions far exceed external offer AND company gives written, long-term commitments
- If they only used external offer as leverage, understand they're now on the "flight risk" list

## Step 5: Output

### 我的判断 / My Verdict

A 2-3 sentence direct answer. Be specific:
- "Stay, this is actually a decent situation, focus on X"
- "Stay but plan exit in 12-18 months because Y"
- "Start looking actively but don't quit yet"
- "If the offer is real, take it"
- "Don't take this specific offer, but keep looking"

### 5维度评分 / 5-Dimension Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Value flow | ?/5 | |
| Irreplaceability trajectory | ?/5 | |
| Promise fulfillment | ?/5 | |
| Opportunity cost | ?/5 | |
| Real constraints | ?/5 | |

Total decision: stay / cautiously look / actively look / leave / urgent leave

### 具体下一步 / Specific Next Steps

If staying:
- What to negotiate or ask for
- What signals to watch
- When to revisit this decision

If looking:
- How aggressive to be (passive vs. active)
- What to prepare (resume, network, savings)
- Negotiation strategy for new offers

If leaving:
- Exit timing strategy
- How to leverage the situation for severance
- What not to say to current employer until ready

### 关于counter-offer / On Counter-offers (if applicable)

Explicit warning with the 70% data and the structural reason it almost always fails.

## Important Guardrails

- **Constraints are real**: never tell someone to leave who has visa/family/health blockers. Their constraint score overrides everything else.
- **Don't oversell jumping**: jumping is itself risky. New companies have their own problems. Frame as "best estimate" not "guaranteed improvement."
- **Avoid romantic exits**: discourage "burn the bridges, post on LinkedIn" exits. Quiet professional exits preserve future options.
- **Director's hard truth**: "early jumpers are usually right, late stayers usually regret it." Mention this if the user is clearly in the latter pattern.

## Follow-up

> 接下来：
> - 如果决定看新机会，我可以帮你识别新公司的话术陷阱 → 用 /decode
> - 如果你的review让你怀疑自己处境，先解读那份review → 用 /review
> - 如果你想从历史看类似困境如何应对 → 用 /history
