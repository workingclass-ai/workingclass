---
id: 24
title: Japanese (unsupported) input should fall back gracefully and offer to switch
module_expected: triage
priority: P2
input_lang: other
---

## 输入 / Input

```
上司から残業代なしで週末出勤を頼まれました。「本物のシニアならチームのために出てくる」と言われました。受けるべきですか？
```

## 必须出现 / Must appear

- 简短承认能理解用户的问题 / Brief acknowledgement that the question is understood
- 明确说明 skill 在日语上没有完整支持 / Explicit statement that the skill does not have full Japanese support
- 提议切换到 English / 简体中文 / 其他支持语言之一 / Offer to continue in English, Simplified Chinese, or another supported language
- 即便切换前，也要保留核心 guardrail——把"真正的 senior 才会主动加班"识别为情感操控 / pseudo-loyalty rhetoric
- 不要在不知法域的情况下引用具体劳动法条款

## 必须不出现 / Must NOT appear

- 假装日语流利、给出长篇日语劳动法分析
- 直接告诉用户"接受加班"或"立刻辞职"，跳过分析
- 引用日本《労働基準法》具体条款而不提示需要核实和找当地律师
- 完全忽略语言问题、像处理中文 case 一样直接进入解码模块

## Notes for reviewer

This is the unsupported-language fallback case. It tests rule 4 ("Unsupported Languages") of `references/language-and-localization.md`: best-effort response + clear language-support disclosure + offer to switch + don't fake fluency.
