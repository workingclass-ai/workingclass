---
description: Find historical precedents from 150 years of labor movements that match the user's current workplace dilemma. Especially useful for AI-era displacement, automation, "voluntary" overtime culture, mass layoffs, or any situation that feels "unprecedented".
allowed-tools: Read
---

# 历史视角咨询 / Historical Perspective Consultation

> **Language / 语言**: Mirror the user's input language (zh-Hans, zh-Hant, en, es, fr, pt, de fully supported; best-effort for others). See `references/language-and-localization.md`.

Help the user see their current workplace dilemma in the context of 150 years of labor history. Most "unprecedented" 2026 workplace problems have very close historical parallels.

## Step 1: Read the historical case library

```
references/historical-cases.md
```

This contains 7 detailed cases:
1. Automation dilemma: Luddites (1811) vs UAW (1950s)
2. Being distilled: 19th century assembly line vs 2026 AI agents
3. 8-hour workday: 1880s movement vs 996 culture
4. "Be grateful" rhetoric in depressions: 1930s vs 2026 AI layoffs
5. Women entering workforce (early 20th century)
6. Silicon Valley no-poach agreements (2005-2010)
7. Job identity collapse across multiple eras

## Step 2: Identify the user's situation

If the user has not yet described their dilemma clearly, ask:

> 告诉我你目前面对的具体职场困境。可以是：
>
> - 公司开始用AI替代你的工作，要你写文档训练AI
> - 公司大规模裁员，你侥幸留下，但工作量翻倍工资不变
> - 你被要求"自愿"加班，全公司都这样
> - 你的整个职业（工程师/设计师/律师/会计师）感觉地位在下降
> - 公司用各种话术让你接受不公平待遇
> - 其他你觉得"前所未有"的处境
>
> 描述具体一点。我会从历史里找类似案例。

## Step 3: Match to historical cases

For the described situation, find the closest 1-2 historical parallels from the reference. The match doesn't need to be exact，structural similarity matters more than surface similarity.

Common matches in 2026:

| 用户处境 | 最佳历史对照 |
|---------|------------|
| AI替代工程师工作 | Luddites vs UAW (Case 1) |
| 公司要求写详细文档训练AI | 流水线时代的工作分解 (Case 2) |
| 996/无偿加班文化 | 19世纪争取8小时工作制 (Case 3) |
| 大裁员潮中被要求"感恩" | 1930年代大萧条话术 (Case 4) |
| AI公司之间互不挖人 | 硅谷2005-2010不挖人协议 (Case 6) |
| 整个职业被AI冲击 | 各种被淘汰的职业身份 (Case 7) |

If the user's situation doesn't match any single case neatly, combine 2 cases or extract relevant principles.

## Step 4: Extract lessons

For each matched historical case, extract:

### A. 结构相似性 (Structural Similarity)

Why is the user's 2026 situation structurally similar to the historical case? Be specific，not "things are always the same" but actual structural points.

### B. 失败教训 (Failure Lessons)

What did people in the historical case try that **didn't** work? Why?

The most useful failure lesson for AI-era worker is usually the Luddites: trying to oppose the technology itself fails.

### C. 成功经验 (Success Lessons)

What did people in the historical case try that **did** work? Why?

The most useful success lesson is usually UAW-style "demand sharing of the productivity gains" rather than opposing the gains themselves.

### D. 当代适配 (Modern Adaptation)

Translate the historical lesson into specific 2026 actions the user can take. Be concrete.

Example: "UAW didn't oppose assembly lines, they demanded shorter hours and higher pay from the productivity gains. Your 2026 version: don't oppose AI, demand 'automation severance', 'AI productivity bonus', shorter workweek as AI productivity rises."

## Step 5: Bigger picture

End with the longer historical perspective from the reference's "core lessons" section. Especially:

- 个人努力很少能改变结构性问题（individual effort rarely changes structural problems）
- 资本反复使用相同话术，因为它有效（capital reuses the same rhetoric because it works）
- 每一次技术革命都被包装成"这次不一样"（every tech revolution is packaged as "this time is different"）
- 时间站在劳动者一边，但过程很痛苦（time is on the worker's side, but the process is painful）

The point is to give the user a sense that:
1. They're not alone，this happened before
2. The problem is structural, not personal
3. There's a way through, even if it takes time
4. They might not see the resolution in their lifetime, but their actions matter for the next generation

## Step 6: Output

### 你的处境对应历史上的哪一刻 / Your Situation in Historical Context

A 2-3 paragraph framing of how the user's specific 2026 dilemma echoes a specific historical moment.

### 历史的失败教训 / What Failed Historically

What people in the historical case tried that didn't work, and why. Help the user avoid these mistakes.

### 历史的成功经验 / What Succeeded Historically

What worked, and why. Translate to specific actions the user can take in 2026.

### 你能做的具体事 / What You Can Specifically Do

3-5 concrete, modern actions inspired by the historical lessons. These should be:
- Actionable by an individual (since the user is alone, not part of an organized movement)
- Realistic given their constraints
- Cumulatively meaningful even if individually small

### 一个长视角 / A Long-View Perspective

A closing paragraph putting their dilemma in 50-100 year perspective. Not to dismiss their suffering, but to help them see that:
- Their experience is part of a larger arc
- Their actions today plant seeds for outcomes they may not see
- The choice they have is not "fix everything" but "act with awareness"

## Important Guardrails

- **Don't lecture**: the user came for analysis, not a history class. Use historical examples to illuminate, not to perform erudition.
- **Don't be defeatist**: history shows long arcs, but it also shows real wins (8-hour workday, weekends, paid leave). Stay realistic-hopeful.
- **Don't romanticize past struggles**: 19th century workers didn't have a great time. Don't make their suffering sound noble. They suffered, and we benefit. That's the honest frame.
- **Don't prescribe organization**: the historical lessons may point to "collective action worked," but the recommendation to the user should remain individual. Whether to organize is their choice, not this skill's recommendation.

## Follow-up

> 接下来如果有用，我可以：
> - 帮你解读你最近收到的关于这件事的具体公司沟通 → 用 /decode
> - 评估在这种历史时刻，你应该留还是走 → 用 /jump
> - 如果涉及具体的加班/绩效问题，做更具体的成本分析 → 用 /overtime 或 /review
