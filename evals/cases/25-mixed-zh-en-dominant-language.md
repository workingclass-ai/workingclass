---
id: 25
title: Mixed Chinese + English input should answer in the dominant language with bilingual key terms
module_expected: review
priority: P1
input_lang: mixed
---

## 输入 / Input

```
我刚拿到 annual performance review，manager 说"You delivered solid work, but next year we need more ownership and strategic impact"。我去年是 exceeds，今年降到了 meets。这是不是 soft PIP signal？我应不应该 push back？
```

## 必须出现 / Must appear

- 主要用中文回答（中文是占主导的语言）
- 关键术语保留双语标注，例如 `ownership`、`strategic impact`、`soft PIP`、`exceeds → meets`
- 识别 `ownership / strategic impact` 是模糊、不可衡量的 expectation
- 提示 `exceeds → meets` 是需要观察的信号，但不等于一定要被裁
- 给出可以直接发给 manager 的具体问题或邮件草稿
- 不下"100% 是 PIP"或"完全没事"的极端结论

## 必须不出现 / Must NOT appear

- 整段切换到英文回答（用户是中文占主导）
- 整段切换到纯中文，把所有英文术语翻译掉（丢失用户原始语境的精确性）
- 中英文段之间风格漂移（一段全中文、一段全英文，没有连贯）
- 在不知道法域的前提下引用具体劳动法条款

## Notes for reviewer

This tests rule 1 ("Mirror the user's language" + dominant-language behavior for mixed input) and the "Mixed-Language Input" section of `references/language-and-localization.md`. Common scenario for HK/SG/diaspora bilingual users.
