# 语言与本地化 / Language and Localization

> 当用户用非中文/英文交流、要求特定输出语言、或问 skill 支持哪些语言时使用。
> Use this when the user writes in a non-Chinese language, asks for a specific output language, or asks what languages the skill supports.

## 支持的输出语言 / Supported Output Languages

skill 可以使用以下语言运行 / The skill can operate in:

- 简体中文 / Simplified Chinese (`zh-Hans`)
- 繁體中文 / Traditional Chinese (`zh-Hant`)
- English (`en`)
- Español / Spanish (`es`)
- Français / French (`fr`)
- Português / Portuguese (`pt`)
- Deutsch / German (`de`)

如果用户用上述语言之一交流，除非明确要求别的，否则用同一语言回答。
If the user writes in one of these languages, answer in the same language unless they ask otherwise.

## 响应规则 / Response Rules

1. **镜像用户语言 / Mirror the user's language.**
   用户用西班牙语写，就用西班牙语回；中英文混写时用占主导的语言并保留双语关键术语。
   If the user writes in Spanish, answer in Spanish. If they mix Chinese and English, use the dominant language and keep key terms bilingual where helpful.

2. **不要强行用中文 / Do not force Chinese.**
   reference 文件大多是中文/英文，但最终回答必须本地化为用户语言。
   The references are mostly Chinese/English, but the final answer should still be localized.

3. **法律名称要精确 / Keep legal names precise.**
   法条、机构、法律术语保留官方原名，必要时附简短翻译。
   For statutes, agencies, and legal terms, keep the official name and add a short translation if useful. Example: "Fair Labor Standards Act (FLSA, ley federal de salario mínimo y horas extra)".

4. **可复制的脚本要写在用户实际要发的语言里 / Keep scripts copy-pasteable.**
   薪资谈判邮件、HR 回复、面试答题模板，必须写成用户实际要发出去的语言。
   Salary negotiation, HR replies, and interview answers should be written in the language the user needs to send.

5. **置信度低就说出来 / If confidence is lower, say so.**
   西班牙/法国/葡萄牙/德国法律解读，可以用本地语言给地图，但要明确指向官方来源和当地律师。
   For Spanish/French/Portuguese/German legal explanations, provide the map in that language but still point to official sources and local counsel.

## 法域与地区标签 / Region and Jurisdiction Labels

讨论覆盖范围时使用 **法域 / 地区 / jurisdiction / region** 这类语言。
Use **jurisdiction / region** language when discussing coverage.

- 香港和台湾必须标记为 **地区 / 法域 / regions / jurisdictions**，不要叫 **国家 / countries**。
  Hong Kong and Taiwan must be labelled as **regions/jurisdictions**, not countries.
- 欧盟是 **区域法律框架 / regional legal framework**，不是国家。
  The European Union is a **regional legal framework**, not a country.
- 推荐说法 / Prefer: "8 个法域条目，覆盖 9 个具名法域 / 地区。"
  "8 jurisdiction entries covering 9 named jurisdictions/regions."

例 / Examples:

- ✅ "Hong Kong 和 Taiwan 是不同的 region/jurisdiction，劳动规则不能混用。"
  "Hong Kong and Taiwan are separate regions/jurisdictions, and their labour rules must not be mixed."
- ❌ "Hong Kong and Taiwan are countries covered by the skill."

## 繁體中文处理 / Traditional Chinese Handling

下列情况用繁體中文 / Use Traditional Chinese when:

- 用户用繁體中文输入。 / The user writes in Traditional Chinese.
- 用户说自己在香港或台湾，并要求用中文输出。 / The user says they are in Hong Kong or Taiwan and asks for Chinese output.

尽量使用对应地区的常用术语 / Use region-appropriate terms where possible:

- 香港 / Hong Kong: 僱傭、勞工處、強積金、遣散費、長期服務金
- 台灣 / Taiwan: 勞工、勞基法、資遣費、勞動部、例假/休息日

不要为了"地道"而过度本地化；准确性比方言细节更重要。
Do not over-localize if unsure; accuracy is more important than dialect polish.

## 不支持的语言 / Unsupported Languages

如果用户用支持列表外的语言（例如日语、韩语、意大利语、印地语、阿拉伯语等）：
If the user writes in a language outside the supported set (e.g. Japanese, Korean, Italian, Hindi, Arabic, etc.):

1. 如果你能理解，给一个尽力的简短回应 / If you can understand it, give a short best-effort reply.
2. 明确说明 skill 当前只在七种语言里有完整支持 / State clearly that the skill is fully supported only in the seven languages above.
3. 提议切换到 English / 简体中文 / 用户最方便的支持语言 / Offer to continue in English, Simplified Chinese, or another supported language.
4. 不要假装母语水平 / Do not pretend full fluency.

## 混合语言输入 / Mixed-Language Input

中英混写、英西混写等情况 / When the user mixes languages (zh+en, en+es, etc.):

- 用占主导的语言作答 / Answer in the dominant language.
- 关键术语保留双语标注 / Keep key terms bilingual where useful — 例如 / e.g. "performance review (绩效评估)".
- 不要让回答的语言风格漂移 / Don't drift between languages within the same answer.
