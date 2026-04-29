# 加班决策分析框架 / Overtime Decision Analysis

This is the reference for the `/overtime` command. It provides a 5-step analytical framework for any specific overtime, weekend work, or extra-scope request.

---

## Step 1: Identify Overtime Type

Different types require different responses. Categorize first.

### Type A: 合同内加班 / Contractual Overtime
- **Signal**: Explicit contract clauses, defined overtime rate (typically 1.5x or 2x base).
- **Common form**: On-call rotations, scheduled shifts, emergency response.
- **Response**: Reasonable exchange. Accept if compensation is paid as contracted. If contracted but unpaid in practice, this is illegal，document it.

### Type B: 项目紧急加班 / Project Emergency Overtime
- **Signal**: Temporary, defined endpoint, specific deliverable.
- **Common form**: Pre-deadline sprint, customer demo, production incident.
- **Response**: Occasional acceptance is reasonable. But monitor frequency: if "emergencies" are monthly, it's not emergency, it's chronic understaffing.

### Type C: 文化性加班 / Cultural Overtime
- **Signal**: Long-term, no defined endpoint, no compensation, "team spirit" framing.
- **Common form**: 996, "everyone stays till 9pm," "voluntary weekend work."
- **Response**: This is the most problematic type. Requires serious cost analysis.

### Type D: 表演性加班 / Performative Overtime
- **Signal**: User themselves admits it's not productive，just optics.
- **Common form**: Staying late with no real work, weekend emails to signal "engagement."
- **Response**: Most wasteful. If user is in this pattern, they need to rethink overall career strategy, not just this overtime decision.

---

## Step 2: Calculate Economic Cost

This number must be specific and stated bluntly. Vague analysis is useless.

### Formula

```
True hourly rate = Annual salary / 2080 hours
(2080 = 40 hours × 52 weeks, standard contractual full-time)

Weekday overtime value = True hourly rate × 1.5 × overtime hours
Weekend overtime value = True hourly rate × 2.0 × overtime hours
Holiday overtime value = True hourly rate × 3.0 × overtime hours
```

(These multipliers reflect baseline labor law in most developed countries.)

### Example

User earns $150,000/year:
- True hourly rate ≈ $72/hour
- One weekend (16 hours): $72 × 2 × 16 = **$2,304**

If the company is not paying this, this is the value extracted from the user this weekend.

### Significance

This is **not** the legal-required pay (that depends on local law and exempt status).

This is **the true labor value the user contributed**. The company saved $2,304. The user lost $2,304 in potential value (those 16 hours could have been used for anything). The transfer is from worker to capital.

State this number bluntly. The user needs the unsugared reality.

---

## Step 3: Health Cost Assessment

### Established findings

1. WHO 2021 study: working >55 hours/week increases stroke risk 35%, ischemic heart disease risk 17%.
2. Productivity research over 150 years: above 50 hours/week, output curve declines. Above 60 hours, absolute output is lower than not overtiming.
3. Sleep debt is not fully recoverable on weekends.
4. Chronic stress degrades all decision-making (career, relationships, finance).

### Personalization

Adjust based on:
- User's baseline health status (age, chronic conditions, family history)
- Recent cumulative workload
- Intensity of this specific overtime (high-cognitive vs. routine execution)
- User's recovery capacity (sleep quality, exercise, family support)

If the user is already in chronic fatigue, this overtime may be the breaking point. Flag this seriously.

---

## Step 4: Career Capital Assessment

The most important step. Two opposing effects of overtime:

### Effect A: Build Irreplaceability
- Learn rare know-how during overtime
- Build deep client/project relationships
- Solve problems only you can solve
- These become real career capital

### Effect B: Build Replicability
- Demonstrate to company "this person accepts unpaid overtime"
- Demonstrate to peers "raising overtime norms is acceptable here"
- Demonstrate to yourself "I accept unfair treatment"
- These become career liabilities (lower future leverage)

### Critical questions

For each overtime request, ask:

1. Does this overtime build A or B?
2. In 5 years, will I be glad I accepted this, or will it just be a data point in my exploitation history?
3. Will the company reward this in any concrete form (promotion, key project, equity, written future commitment)?
4. If reward = "none," why am I accepting?

If honest answer is **B + no reward**, this overtime is negative investment. The more you accept, the worse your career future.

---

## Step 5: Legal View

Brief framework. Always recommend user check specifics for their jurisdiction.

| Region | Key framework |
|--------|---------------|
| US/Canada | "Exempt" vs "non-exempt" matters greatly. Most engineers are exempt with no overtime pay legally required. But salary thresholds apply (~$58k/year US). |
| EU | Working Time Directive: max 48 hours/week including overtime. Most countries pay 150-200% overtime rate. Mandatory 11-hour rest. |
| Australia | Fair Work Act. Award employees: 150% weekday, 200% weekend OT. Director-level: "reasonable additional hours." Right to refuse "unreasonable." |
| China | Labor Law: 1.5x weekdays, 2x weekends, 3x holidays. "Voluntary" vs "required" matters legally. Enforcement varies. |
| Japan/Korea | Legal protections exist but "voluntary overtime" remains common. Recent reforms tightening. |

### Application

For user's situation:
1. Identify their jurisdiction
2. Note whether this overtime might be illegal
3. If illegal, recommend documenting evidence (emails, schedules, chat logs)
4. They may not want to report immediately, but evidence is leverage

---

## Step 6: Collective View (often missed, very important)

### Individual vs. collective decision

If everyone in the team accepts 996 unpaid → one individual refusing fails.
If everyone refuses 996 → boss must accommodate.

This is the difference between individual and collective.

### Practical implications

When user makes individual overtime decision, ask:

1. Does my decision build or erode collective bargaining power?
2. If all my colleagues made the same decision, what would happen?
3. Can I discuss this informally with 2-3 peers I trust?

You don't need formal organization. Informal conversation among 2-3 colleagues is the seed of collective action.

### Historical perspective

The shift from 10-hour workday to 8-hour workday in late 19th century US was won by collective action over decades. No single brilliant worker won it.

2026's "AI-era overtime culture" is structurally similar to the 19th century. Individual choices matter, but only collective direction changes structural outcomes.

---

## Decision Matrix

Sum up all 5 steps with scoring (1-5 each, 5 = worst):

| Dimension | Score | Notes |
|-----------|-------|-------|
| Economic cost | ? | |
| Health cost | ? | |
| Career capital | ? | |
| Legal risk | ? | |
| Collective impact | ? | |

**Total interpretation:**

- 5-10: Acceptable. Document the situation for future reference.
- 11-15: Worth pushing back. Consider asking for compensation or refusing.
- 16-20: Clear exploitation. Refuse and consider job change.
- 21-25: Long-term harmful environment. Plan exit.

---

## How to Refuse Without Burning Bridges

Don't say "I can't." Say "I need..."

❌ "I can't work this weekend"
✅ "I need to see clear compensation (overtime pay, comp days, written record for review) before adjusting personal time."

❌ "I have plans"
✅ "I have plans this weekend. Adjusting requires at least 48 hours' notice."

❌ "This isn't my responsibility"
✅ "Let's solve this project's resourcing fundamentally, rather than using my overtime as long-term solution."

---

## When User Has No Choice (constrained)

If user must accept due to mortgage, visa, family pressure, at minimum:

1. **Document everything**: dates, hours, content of overtime
2. **Save communications**: emails requesting overtime, chat logs
3. **Protect body**: maintain sleep, exercise, nutrition where possible
4. **Plan exit**: while accepting, work on getting out of the situation
5. **Find an "overtime ally"**: one colleague you can be honest with

Accepting overtime and planning exit are not contradictory.

---

## When User Looks Back on Past Patterns

If user realizes they've accepted years of unfair overtime:

1. Don't use "should have" against yourself. Past decisions had past constraints.
2. Starting today, reassess every overtime decision.
3. You've already over-contributed to this company. You have moral capital to do contracted-only work.
4. If leaving, use the documented overtime as leverage for new salary negotiation.

---

This framework is not designed to make you refuse all overtime, or accept all overtime. It's designed to make every overtime decision a clear-eyed decision rather than rhetoric-driven.

Clarity itself is a victory.
