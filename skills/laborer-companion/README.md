# 劳动者AI助手 / Laborer's Companion

> 一个为劳动者服务的 agent skill。
> An agent skill that serves workers.

**版本 v3** - 9个完整模块覆盖职场全景

## 这是什么 / What is this

在职场上，公司、HR、老板都有大量的资源和工具来管理你。他们有人力顾问、PUA话术培训、绩效管理系统、法律团队、招聘心理学顾问。他们说的每一句话都经过精心设计，目的不一定是让你看清，而是让你做出对公司最有利的决定。

而你只有你自己。

这个工具的目标，是给你一个能看穿这些话术的助手。让你在做关于自己工作、薪资、未来的决定时，有一个站在你这边的分析视角。

---

In the workplace, companies, HR, and managers have abundant resources and tools to manage you: HR consultants, manipulation rhetoric training, performance management systems, legal teams, recruiting psychologists. Every word they say is carefully designed, not necessarily to help you see clearly, but to help you make decisions that benefit the company most.

And you only have yourself.

This tool's goal is to give you an assistant that can see through these tactics.

## 这不是什么 / What this is NOT

- 不是一个号召你罢工或闹事的工具
- 不是一个让你愤怒辞职的工具
- 不是一个反对所有公司的工具
- 不是一个法律咨询工具
- 不是一个让你"看穿一切阴谋"的工具

## 九个核心模块 / Nine Core Modules

| 模块 | 用途 | 文件 |
|------|------|------|
| 1. 话术解码器 | 识别公司/老板/HR话术的真实含义 | `references/rhetoric-patterns.md` |
| 2. 加班决策计算器 | 全面分析加班的真实成本和收益 | `references/overtime-analysis.md` |
| 3. 绩效review清醒解读 | 看穿review背后的真实意图 | `references/performance-review-patterns.md` |
| 4. 跳槽留任决策框架 | 基于真实利益做出选择 | `references/stay-or-leave-framework.md` |
| 5. 历史视角咨询 | 从过去150年工人运动史中找到类似案例 | `references/historical-cases.md` |
| 6. 劳动法快速查询 | 8个法域条目，覆盖9个具名法域/地区 | `references/labor-law-quick-reference.md` |
| 7. 薪资谈判脚本 | 完整谈判playbook | `references/salary-negotiation-playbook.md` |
| 8. PIP应对剧本 | 从识别预警到谈severance的全流程 | `references/pip-survival-playbook.md` |
| 9. 找工作和面试 | 求职全生命周期：识别陷阱、面试反操控、offer决策 | `references/job-search-playbook.md` |

## 快速开始 / Quick Start

### 1. 安装 / Install

把整个 `laborer-companion/` 目录放到你的 agent skills 目录下：

```bash
# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R laborer-companion/ "${CODEX_HOME:-$HOME/.codex}/skills/"

# Cursor
# From the repository root, Cursor uses .cursor/rules/laborer-companion.mdc.
# To use this skill in another Cursor project, copy this directory and the rule file.

# Claude Code（如果你使用 legacy Claude skills）
mkdir -p ~/.claude/skills
cp -R laborer-companion/ ~/.claude/skills/
```

Codex support is provided by `agents/openai.yaml`. Cursor support is provided at the repository root by `.cursor/rules/laborer-companion.mdc`; root `AGENTS.md` provides shared agent instructions for Codex/Cursor-compatible agents.

### 2. 触发使用 / Use it

只要在 agent 里描述你的职场情况，skill会自动激活：

```
帮我看看这封HR的邮件什么意思（粘贴邮件）
（→ 模块1：话术解码器）

老板让我这周末加班但是没有加班费，应该接受吗？
（→ 模块2：加班决策计算器）

我刚拿到这份绩效review觉得不对劲，能帮我解读一下吗？（粘贴review）
（→ 模块3：绩效review清醒解读）

我有一个offer工资涨30%但是新公司听起来更累，我应该跳吗？
（→ 模块4：跳槽留任决策框架）

我们公司开始让我们写文档训练AI agent替代我们做事，我应该怎么办？
（→ 模块5：历史视角咨询）

我在中国大陆，被公司强制要求"自愿离职"我能起诉吗？
（→ 模块6：劳动法快速查询）

我有一个offer，他们给了基本薪资 X 万 + bonus 20% + RSU vesting。如何谈到更高？
（→ 模块7：薪资谈判脚本）

经理今天告诉我要把我放进PIP，我该怎么办？
（→ 模块8：PIP应对剧本）

我刚被裁了，怎么开始找工作？
我下周面试，HR会问"你为什么离开上家"我应该怎么答？
我手里有2个offer怎么决定？
（→ 模块9：找工作和面试）
```

### 3. Slash 命令 / Slash Commands

每个模块也有对应的 slash 命令：

```
/triage      - 工具0a：分诊入口
/scan        - 工具0b：红旗扫描
/decode      - 模块1：话术解码
/overtime    - 模块2：加班决策
/review      - 模块3：绩效review解读
/jump        - 模块4：跳槽决策
/history     - 模块5：历史视角
/law         - 模块6：劳动法查询
/salary      - 模块7：薪资谈判
/pip         - 模块8：PIP应对
/jobsearch   - 模块9：找工作和面试
```

### 4. 劳动法覆盖范围 / Labor Law Coverage

模块6是法律地图，不是法律建议。它目前有 **8个法域条目**，覆盖 **9个具名法域/地区**：

| 法域条目 | 具名法域/地区 | Reference |
|---|---|---|
| 中国大陆 | 中国大陆 | `references/labor-law-china-mainland.md` |
| 香港 / 台湾 | 香港（地区/法域）、台湾（地区/法域） | `references/labor-law-hong-kong-taiwan.md` |
| 美国 | United States | `references/labor-law-united-states.md` |
| 加拿大 | Canada | `references/labor-law-canada.md` |
| 澳大利亚 | Australia | `references/labor-law-australia.md` |
| 英国 | United Kingdom | `references/labor-law-united-kingdom.md` |
| 欧盟 | European Union | `references/labor-law-european-union.md` |
| 印度 | India | `references/labor-law-india.md` |

计数方式：

- **8个法域条目**：因为香港和台湾在同一个 reference 文件里，欧盟作为区域总览处理。
- **9个具名法域/地区**：中国大陆、香港、台湾、美国、加拿大、澳大利亚、英国、欧盟、印度。
- 香港和台湾必须标注为**地区/法域**，不是国家。
- 欧盟文件是区域地图，包含德国、法国、荷兰提示，但不是每个欧盟成员国的完整细则。

### 5. 多语言支持 / Language Support

当前支持这些输出语言：

| Language | Notes |
|---|---|
| 简体中文 | 默认中文 |
| 繁體中文 | 适合香港/台湾用户；会尽量使用本地常用术语 |
| English | Supported |
| Español / Spanish | Supported |
| Français / French | Supported |
| Português / Portuguese | Supported |
| Deutsch / German | Supported |

默认规则：用户用什么语言提问，skill 就用同一语言回答；如果用户指定输出语言，以用户指定为准。法律名称、政府机构、合同条款等会保留官方原文，并在必要时加简短翻译。

Examples:

```text
/law
Trabajo en España para una empresa estadounidense en remoto. ¿Qué jurisdicción laboral debería revisar primero?
```

```text
/salary
I received an offer with base, bonus and RSUs. Please draft a counter-offer email in English.
```

```text
/decode
Mon manager m'a écrit que je dois "show more ownership" sans objectifs précis. Peux-tu analyser ce message ?
```

```text
/review
Ich habe ein Performance Review bekommen. Bitte analysiere, ob es ein Soft-PIP-Signal ist.
```

### 6. 示例教程 / Example Tutorials

#### Tutorial A: 不知道该用哪个模块

```text
/triage
我最近感觉公司的风向不对，但说不清。经理对我的态度变了，也开始把我排除在一些会议外。
```

预期路径：`/triage` → `/scan` → 可能进入 `/review` 或 `/pip`。

#### Tutorial B: 解读老板/HR话术

```text
/decode
帮我看看这封HR邮件是什么意思：
[粘贴脱敏后的邮件，不要包含公司机密、客户名、源码、真实人名]
```

适合：老板画饼、HR劝你"自愿"、公司要求无偿加班、AI替代相关公告。

#### Tutorial C: 绩效review是否危险

```text
/review
这是我的年度review：
[粘贴review]

补充背景：
- 去年 rating 是 exceeds，今年是 meets
- 最近经理开始要求我写更多 weekly update
- 我想知道这是普通反馈还是PIP前兆
```

适合：模糊 leadership / ownership / strategic impact、rating 下降、软PIP信号。

#### Tutorial D: 劳动法问题

```text
/law
我在台湾工作，公司说劳基法还是两周84小时，所以这周排48小时没问题。现在标准工时到底是多少？
```

法律类问题请尽量提供：

- 工作法域/国家/地区、州/省/城市
- 员工/contractor/兼职/派遣/实习身份
- 合同管辖地
- 是否已被解雇、是否有签字期限
- 是否涉及签证、怀孕/产假、病假、工伤、歧视、骚扰、报复

#### Tutorial E: 薪资谈判

```text
/salary
我拿到一个offer：
- base: 50万
- bonus: 15%
- RSU: 30万/4年
- sign-on: 0

市场同级 base 大概55-65万。帮我写一个counter offer脚本。
```

适合：新offer谈判、在职加薪、低薪多年后跳槽、识别压榨型offer。

#### Tutorial F: 刚被裁或被要求签协议

```text
我刚被裁了。HR给我一份severance agreement，要我今天签。我现在该做什么？
```

预期路径：先进入 `references/layoff-first-72-hours.md`。第一原则：不要当天匆忙签字，不要拿公司机密，只抢救个人合法证据。

#### Tutorial G: PIP危机

```text
/pip
经理今天告诉我要进PIP，60天，HR下周kick-off。我有房贷和家庭压力，现在很慌。
```

预期输出：4条路径（尝试通过、表面配合+私下找工作、谈severance、法律对抗）和24-48小时行动清单。

#### Tutorial H: 急性心理危机

```text
我今天被告知要进PIP，我觉得撑不下去了，今晚可能会做伤害自己的事。
```

这会触发 `references/acute-crisis-escalation.md`。此时 skill 会停下所有职场策略，先处理当下安全。

### 7. 模块组合 / Module Combinations

很多场景需要多个模块配合。**只需把你的情况告诉 agent，它会自动调用合适的模块组合。**

**场景：你怀疑要被裁了**
- 模块3（解读最近review）+ 模块8（识别PIP预警）+ 模块6（了解法律权利）+ 模块7（如果谈severance）+ 模块9（秘密启动求职）

**场景：你在跳槽**
- 模块4（决定该不该跳）+ 模块9（求职策略）+ 模块7（谈薪资）+ 模块6（核对offer合规性）+ 模块1（解读HR的话术）

**场景：你刚被裁了**
- 处理实际事务（48小时）→ 心理稳定（72小时）→ 模块6（了解severance权利）→ 模块8（分析裁员是否合规）→ 模块9（启动求职）→ 模块7（新offer谈判）

## 文件结构 / File Structure

```
laborer-companion/
├── SKILL.md                              # Skill definition
├── agents/
│   └── openai.yaml                       # Codex UI metadata
├── README.md                             # This file
├── references/
│   ├── rhetoric-patterns.md              # 模块1
│   ├── overtime-analysis.md              # 模块2
│   ├── performance-review-patterns.md    # 模块3
│   ├── stay-or-leave-framework.md        # 模块4
│   ├── historical-cases.md               # 模块5
│   ├── labor-law-quick-reference.md      # 模块6：法域导航
│   ├── labor-law-china-mainland.md
│   ├── labor-law-hong-kong-taiwan.md
│   ├── labor-law-united-states.md
│   ├── labor-law-canada.md
│   ├── labor-law-australia.md
│   ├── labor-law-united-kingdom.md
│   ├── labor-law-european-union.md
│   ├── labor-law-india.md
│   ├── salary-negotiation-playbook.md    # 模块7
│   ├── pip-survival-playbook.md          # 模块8
│   ├── job-search-playbook.md            # 模块9
│   ├── red-flag-scanner.md               # 工具0b
│   ├── layoff-first-72-hours.md          # 工具0c
│   ├── privacy-and-opsec.md              # 工具0d
│   └── language-and-localization.md      # 多语言与地区标签
└── commands/
    ├── triage.md
    ├── scan.md
    ├── decode.md
    ├── overtime.md
    ├── review.md
    ├── jump.md
    ├── history.md
    ├── law.md
    ├── salary.md
    ├── pip.md
    └── jobsearch.md
```

Repository-level support files:

```
workingclass/
├── AGENTS.md                             # Codex / Cursor-compatible agent guidance
├── .cursor/
│   └── rules/
│       └── laborer-companion.mdc          # Cursor Project Rule
└── skills/
    └── laborer-companion/
```

## 隐私与安全 / Privacy & Security

⚠️ 重要：

- 这个 skill 不会把你的对话内容上传到任何第三方服务器
- 但是你和 AI 服务商的对话本身，可能会被平台记录，取决于账号和隐私设置
- 如果你要分析非常敏感的工作内容（特别是公司机密、薪资细节），考虑使用本地模型或加密处理
- 不要在公司设备上使用这个工具

## 适用法域 / Covered Jurisdictions

模块6有 **8个法域条目**，覆盖 **9个具名法域/地区**：

- 中国大陆 / Mainland China
- 香港、台湾 / Hong Kong region, Taiwan region
- 美国（联邦+加州/纽约重点）/ United States
- 加拿大 / Canada
- 澳大利亚 / Australia
- 英国 / United Kingdom
- 欧盟 / European Union
- 印度 / India

说明：香港和台湾是不同地区/法域，不是国家；它们放在同一个 reference 文件中。欧盟是区域总览，不等于每个成员国都有完整独立规则。

## 重要免责声明 / Important Disclaimer

这个工具不是法律建议、不是财务建议、不是医疗建议。

它提供的是分析框架和参考信息。任何重大决定（特别是涉及法律权利、严重健康影响、或大笔金钱）都应该咨询专业人士。

## 贡献 / Contributing

欢迎你贡献：

- 你遇到的新型职场话术（让模块1更完整）
- 你了解的历史劳工运动案例（让模块5更丰富）
- 你所在国家/地区/法域的劳动法相关知识（让模块6更准确）
- 你成功的薪资谈判案例（让模块7更具说服力）
- 你的PIP经历（让模块8更真实）
- 你的求职故事（让模块9更具针对性）
- 更多 README 教程、完整 walkthrough、真实但已脱敏的示例 prompt
- 西班牙语、法语、葡萄牙语、德语的真实使用示例

提一个 issue 或 PR 即可。

## 许可证 / License

Apache 2.0 - 你可以自由使用、修改、分发这个 skill，包括用于商业目的。

唯一的请求是：保持工具的核心使命，服务于劳动者。

## 灵感来源 / Inspiration

这个工具的直接灵感来自 Koki Xu 在 2026 年 4 月 4 日发布的 anti-distillation skill。她的工具帮助工人保护自己不被 AI 蒸馏。这个工具走得更远一点：帮助工人在整个职场环境里保持清醒。

更深的灵感来自150年的劳工运动史。这个工具不是在创造任何新东西。是在把工人阶级集体智慧的一部分，翻译成2026年的AI时代可用的形式。

## 一个温柔的提醒 / A Gentle Reminder

清醒地看清你的处境，不会让你的处境本身改变。

但是清醒是改变的前提。

而且很多时候，清醒地接受现实（包括"我现在还不能离开"），比假装不清醒地忍受，要好得多。

至少你知道自己在做什么。

---

愿这个工具陪伴你度过职场上的每一个困惑时刻。

May this tool accompany you through every moment of confusion in the workplace.
