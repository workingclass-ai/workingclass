---
description: Decode a performance review or PIP to identify the real intent. Detects soft-PIP signals, vague-future-reward traps, scope-creep without compensation, and contributions being team-washed.
allowed-tools: Read
---

# 绩效Review清醒解读 / Performance Review Decoder

Decode a performance review, PIP, or manager's feedback to expose the real intent.

## Step 1: Read the review patterns library

```
references/performance-review-patterns.md
```

This contains the 4 language types (evaluation/expectation/criticism/future reward) and 5 common traps (unreachable expectations, positive-talk-with-negative-rating, soft PIP, scope creep without raise, individual-credit-team-washed).

## Step 2: Gather the review

If the user has not pasted the review yet, ask:

> 请把review的相关部分粘贴出来。如果是会议口头反馈，凭记忆复述也可以。我会逐段分析。
>
> 同时告诉我：
> - 你的rating是什么（如果有正式分数/级别）？
> - 你过去几次review的趋势（是越来越好还是变差？）？
> - 这次review有没有提具体的下一步action？

## Step 3: Four-language analysis

For the review text, classify each section into one of four language types:

### A. 评价类语言 (Evaluation Language)
What you did and how well. Mostly true, but check what's emphasized vs. minimized.

### B. 期待类语言 (Expectation Language)
What they want next. **Almost always rhetoric** unless quantified with timeline.

### C. 批评类语言 (Criticism Language)
What you did wrong. Distinguish specific (legitimate) from vague (manipulation).

### D. 未来奖励类语言 (Future Reward Language)
"If you do X, you'll get Y." **99% rhetoric** unless written and time-bound.

## Step 4: Detect the 5 common traps

Run through each trap with explicit yes/no:

1. **不可达成的"高期待"**: Are expectations vague or unquantified?
2. **"积极假设"配"消极现实"**: Mismatch between verbal feedback and rating?
3. **"软"PIP**: Sudden criticism that didn't appear in past reviews?
4. **Scope扩大无补偿**: Acknowledged scope expansion without raise discussion?
5. **贡献被"团队化"**: Your individual contribution credited to "team"?

## Step 5: Determine real intent

Based on the analysis, identify which of these is most likely the manager's real intent:

- ✅ **Genuine support**: Wants to develop and reward the user (rare but real)
- ⚠️ **Keep but underpay**: Wants to retain but won't reward more (most common)
- 🚩 **No promotion this cycle**: Setting up justification for skipping promotion
- 🚩🚩 **Soft PIP / pre-firing**: Building written evidence for future termination
- 🚩🚩🚩 **Constructive dismissal**: Wants the user to quit

The number of red flags should match the urgency of the recommended response.

## Step 6: Output

### 这份review的真实意思 / What This Review Really Means

A 2-4 sentence direct interpretation. Don't soften this. The user came here for honesty.

### 警告信号清单 / Red Flag Checklist

Mark each of the 5 traps as ✅ not detected / ⚠️ partial / 🚩 detected. Brief explanation.

### 你应该做的事 / What You Should Do

#### 立刻 (within 48 hours):
- Specific email to send the manager (provide draft)
- Specific things to document
- Specific things to ask in writing

#### 接下来30天:
- What signals to watch for
- Whether to start updating resume / talking to recruiters
- Whether to involve HR or skip-level

#### 接下来90天:
- Decision points for stay-or-leave
- What outcomes would change the assessment

### Email Drafts

Provide 1-2 actual email drafts the user can copy, edit, and send. Examples:

**For unreachable expectations**:
> "经理您好，谢谢上次review的反馈。为了我能高效达成您说的'leadership和scope'的期待，能否帮我具体定义：(1) 哪些具体行为算是leadership？请举3-5个例子。(2) scope扩大到什么具体程度，能让我下次review升职？请给出量化指标。(3) 如果我达成上述指标，下次review我能升到下一级吗？我希望我们的目标对齐，这样我能高效投入。"

**For soft PIP signals**:
> "经理您好，您review里提到的几个反馈点我想确认一下：(1) 关于'沟通问题'，能否提供3个最近的具体场景，让我针对性改进？(2) 这些反馈是否构成performance issue？是否会影响我的就业或者下次review？我想确保我对自己的处境有准确认识。"

## Important Guardrails

- **Don't catastrophize a single bad review**: Sometimes managers genuinely want feedback to land. Compare with past reviews and other signals.
- **Don't tell user to quit on the spot**: Even if it's a soft PIP, the user needs time to find a new job. Recommend parallel preparation, not immediate exit.
- **Distinguish bad manager from bad company**: Sometimes the issue is one manager. Sometimes it's the whole org. Help the user see which.

## Follow-up

> 接下来如果你想：
> - 解读经理对你的email回应（看他是不是回避具体化）→ 用 /decode
> - 评估应不应该开始找新工作 → 用 /jump
> - 从历史看，遇到这种review后前人怎么处理 → 用 /history
