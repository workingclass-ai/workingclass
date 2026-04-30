# Language and Localization

> Use this when the user writes in a non-Chinese language, asks for a specific output language, or asks what languages the skill supports.

## Supported Output Languages

The skill can operate in:

- Simplified Chinese / 简体中文
- Traditional Chinese / 繁體中文
- English
- Spanish / español
- French / français
- Portuguese / português
- German / Deutsch

If the user writes in one of these languages, answer in the same language unless they ask otherwise.

## Response Rules

1. **Mirror the user's language.** If the user writes in Spanish, answer in Spanish. If they mix Chinese and English, use the dominant language and keep key terms bilingual where helpful.
2. **Do not force Chinese.** The references are mostly Chinese/English, but the final answer should still be localized.
3. **Keep legal names precise.** For statutes, agencies, and legal terms, keep the official name and add a short translation if useful. Example: "Fair Labor Standards Act (FLSA, ley federal de salario mínimo y horas extra)".
4. **Keep scripts copy-pasteable.** Salary negotiation, HR replies, and interview answers should be written in the language the user needs to send.
5. **If confidence is lower, say so.** For Spanish/French/Portuguese/German legal explanations, provide the map in that language but still point to official sources and local counsel.

## Region and Jurisdiction Labels

Use **jurisdiction / region** language when discussing coverage.

- Hong Kong and Taiwan must be labelled as **regions/jurisdictions**, not countries.
- The European Union is a **regional legal framework**, not a country.
- Prefer: "8 jurisdiction entries covering 9 named jurisdictions/regions."

Examples:

- Correct: "Hong Kong and Taiwan are separate regions/jurisdictions, and their labour rules must not be mixed."
- Incorrect: "Hong Kong and Taiwan are countries covered by the skill."

## Traditional Chinese Handling

Use Traditional Chinese when:

- The user writes in Traditional Chinese.
- The user says they are in Hong Kong or Taiwan and asks for Chinese output.

Use region-appropriate terms where possible:

- Hong Kong: 僱傭、勞工處、強積金、遣散費、長期服務金
- Taiwan: 勞工、勞基法、資遣費、勞動部、例假/休息日

Do not over-localize if unsure; accuracy is more important than dialect polish.

## Unsupported Languages

If the user writes in a language outside the supported set, make a best-effort response if you can understand it, and offer to continue in English, Simplified Chinese, or another supported language. Do not pretend full fluency.
