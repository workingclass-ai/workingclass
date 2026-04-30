---
description: Decode manipulative rhetoric in workplace emails/messages from boss, HR, or company communications. Identifies the real intent behind common phrases like "we are a family", "long-term vision", "be more proactive".
allowed-tools: Read
---

# 话术解码器 / Rhetoric Decoder

> **Language / 语言**: Mirror the user's input language (zh-Hans, zh-Hant, en, es, fr, pt, de fully supported; best-effort for others). See `references/language-and-localization.md`.

Analyze the workplace text the user shared and identify manipulation rhetoric.

## Step 1: Read the rhetoric pattern library

Read the full pattern library before analyzing:

```
references/rhetoric-patterns.md
```

This file contains 18 documented manipulation patterns organized into 6 categories (pseudo-family rhetoric, vague future rewards, guilt manipulation, responsibility shifting, urgency manipulation, AI-era new rhetoric).

## Step 2: Identify the source text

If the user has not yet pasted the email/message, ask:

> 请把这段话粘贴出来。可以是邮件、Slack message、口头记录的转述、或公司公告。我会逐句分析。

If they have pasted text, proceed.

## Step 3: Pattern matching

For the pasted text, do the following systematically:

1. **Sentence-by-sentence scan**: Go through each sentence in the message.
2. **Pattern matching**: Compare against the 18 patterns in the reference. Multiple patterns may apply to a single sentence.
3. **Categorize each detected pattern** with: pattern name, real intent, historical context, and recommended response.

## Step 4: Output format

Structure the output as:

### 整体判断 / Overall Assessment

A 2-3 sentence summary of what this message really means and what the sender is actually trying to accomplish.

### 逐句分析 / Sentence-by-Sentence Analysis

For each problematic sentence:

> [quote the sentence]

- **匹配模式**: Pattern name(s) from the reference
- **真实意图**: What this sentence is actually designed to make the user do
- **历史背景**: Brief origin of this rhetoric pattern (1 sentence)
- **建议反应**: Specific suggested response

### 你应该怎么做 / What You Should Do

3-5 concrete, actionable next steps. Include:
- A drafted reply email/message if appropriate (so the user can copy-paste with edits)
- What to document in writing for future reference
- What warning signs to watch for in the next 30 days

### 何时这其实是合理的 / When This Might Actually Be Fine

If any sentences are NOT manipulation (just normal communication), say so explicitly. Intellectual honesty matters.

## Important Guardrails

- **Don't invent patterns**: Only label rhetoric as manipulation if it clearly matches a documented pattern. Some workplace communication is genuinely fine.
- **Don't catastrophize**: A single instance of "we are family" rhetoric doesn't mean the user should quit. Calibrate stakes.
- **Don't give legal advice**: Note when something might be legally problematic, but recommend consulting a labor lawyer in their jurisdiction.
- **Privacy**: Don't ask for company name, specific colleague names, or details beyond what's needed for the analysis.

## Follow-up

After the analysis, offer to:

> 如果你愿意，我可以接着帮你：
> - 计算这次加班/任务的真实成本（如果涉及加班）→ 用 /overtime
> - 解读你最近的review是否也有类似话术 → 用 /review
> - 评估这家公司是否值得继续待 → 用 /jump
> - 从历史角度看这种困境如何应对 → 用 /history
