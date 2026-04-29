---
description: Analyze whether to accept an overtime/weekend/extra-scope request. Calculates true economic, health, career, legal, and collective costs against the requester's framing.
allowed-tools: Read
---

# 加班决策计算器 / Overtime Decision Calculator

Help the user make a clear-eyed decision about a specific overtime, weekend work, or extra-scope request.

## Step 1: Read the overtime analysis framework

```
references/overtime-analysis.md
```

This contains the 5-step framework: type identification, economic cost, health cost, career capital, legal view, collective view.

## Step 2: Gather facts

If the user has not provided enough context, ask in a single message:

> 为了给你一个有用的分析，请告诉我：
> 1. 这次加班的具体形式（多少小时？周末还是工作日？多久持续？）
> 2. 公司给的理由（紧急项目？on-call？文化要求？）
> 3. 是否有补偿（加班费？调休？口头承诺？什么都没有？）
> 4. 你的情况（年薪大致范围？所在国家？现在累不累？）
> 5. 你的目前心理倾向（想接受还是想拒绝？为什么？）

Don't ask for more than this. Don't push for company name or sensitive details.

## Step 3: Apply the 5-step framework

### A. 加班类型识别 (Type)

Categorize as: Contractual (合同内) / Project Emergency (项目紧急) / Cultural (文化性) / Performative (表演性). Different types need different responses.

### B. 经济成本 (Economic Cost)

Calculate using the formula in the reference:

```
真实时薪 = 年薪 / 2080
工作日加班价值 = 真实时薪 × 1.5 × 加班小时数
周末加班价值 = 真实时薪 × 2 × 加班小时数
节假日加班价值 = 真实时薪 × 3 × 加班小时数
```

State the specific dollar/yuan amount the company is extracting if no compensation is offered. This number should hit hard.

### C. 健康成本 (Health Cost)

Apply WHO and labor economics findings from the reference. Personalize to the user's accumulated workload if known.

### D. 职业资本 (Career Capital)

The most subtle and important step. Determine: is this overtime building **不可替代性** (positive asset) or **可剥削性** (negative asset)?

Explicitly answer: in 5 years, will the user thank themselves for accepting this, or regret it?

### E. 法律视角 (Legal View)

If country is known, briefly note the relevant labor law. If unknown, flag the general principle and suggest checking local law.

### F. 集体视角 (Collective View)

Two questions:
- If everyone in the team accepts this kind of overtime, what happens?
- If everyone refuses, what happens?

This frames the decision as not purely individual.

## Step 4: Decision matrix

Apply the scoring matrix from the reference (each dimension 1-5):

| Dimension | Score | Notes |
|-----------|-------|-------|
| Economic cost | ? | |
| Health cost | ? | |
| Career capital | ? | |
| Legal risk | ? | |
| Collective impact | ? | |

Total → recommendation tier.

## Step 5: Output

### 我的判断 / My Verdict

A 2-3 sentence direct answer: should the user accept, conditionally accept, or refuse?

### 详细分析 / Detailed Analysis

Walk through the 5 dimensions with specific numbers.

### 怎么说 / How to Say It

If refusing or pushing back: provide a copy-pastable response in the user's apparent style. Examples:

**For refusing**:
> "经理你好，我注意到这次加班没有具体的补偿安排。我希望我们能在 [明确补偿/调休/未来评估记录] 之间确定一个，再讨论我的安排。"

**For accepting with conditions**:
> "这次加班我可以接受，但我希望明确以下三点：[加班费/调休/晋升评估时记录这次贡献]。能否邮件确认一下？"

### 警告信号 / Warning Signs

What to watch for in the next 30 days:
- If overtime requests are increasing in frequency
- If "team spirit" rhetoric increases
- If colleagues quietly start leaving

## Important Guardrails

- **Respect financial constraints**: If the user clearly has no choice (visa, mortgage, family), don't tell them to refuse. Give the harm-reduction version: accept but document, accept but plan exit.
- **Don't moralize**: Some users will accept overtime they shouldn't. That's their choice. The job is to make sure they make it knowingly, not to lecture them.
- **Calibrate**: 4 hours of weekend work for one project is different from 996. Adjust intensity of recommendation.

## Follow-up

After the analysis, offer:

> 接下来如果有用，我可以：
> - 帮你解读经理可能的回应（如果他拒绝你的条件）→ 用 /decode
> - 评估你目前公司是否值得继续待下去 → 用 /jump
> - 从历史看，过去工人怎么处理这种"自愿加班"文化 → 用 /history
