# workingclass

**简体中文** · [English](README.en.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Deutsch](README.de.md)

> 站在劳动者一边的 AI 工具集。
> AI tools that stand on the side of workers.

这个仓库收录服务于劳动者的 agent skills 和工具。第一个，也是核心的，是 **劳动者AI助手 / Laborer's Companion**——一个帮你看穿职场话术、做出对自己最好的决定的工具。

---

## 为什么存在这个项目

在职场上，公司、HR、老板都有大量资源来管理你：HR 顾问、PUA 话术培训、绩效管理系统、法律团队、招聘心理学顾问。他们说的每一句话都经过精心设计，目的不一定是让你看清，而是让你做出对公司最有利的决定。

而你只有你自己。

AI 时代让这个不对称更严重——公司用 AI 蒸馏你的工作、AI 替代你、AI 监控你。这个项目把 AI 反过来用：**让 AI 站在你这边**。

---

## 一个例子

你的经理刚发来：

> *"Hey, I really appreciate your dedication. The team's vision for next year requires more cross-functional ownership and strategic impact — I'd love to see you stretch into broader leadership. That's the trajectory I see for you. Let's chat at our next 1:1."*

跑 `/decode`（或者把这段话直接贴给装了 skill 的 agent），你拿到的是：

```
模式：模糊未来奖励 + scope-creep 不加薪

这段话真正在说什么：
  - "broader leadership" / "strategic impact" / "trajectory" 都是不可衡量的期待，
    经理可以随时重新定义
  - 没有晋升时间表、没有薪资 delta、没有现有 scope 的削减承诺
  - "That's the trajectory I see" ≠ "我们正式承诺给你升职"

你这周该做的：
  1. 回邮件请经理把**晋升标准**写下来——具体、可衡量
  2. 问哪些现有的工作可以被 drop，腾出时间做新的
  3. 问如果达到那些标准，薪资 delta 是多少
  4. 把经理的回复（或沉默）存档——无论哪种都是证据
```

skill 不会让你**辞职**、不会让你**和老板对着干**、不会让你"just push back"。它把对方话里的结构呈现给你，剩下的决定你自己做。

---

## 目前包含

### 1. `skills/laborer-companion/` — 劳动者AI助手

9 个核心模块 + 4 个入口工具，覆盖职场全景：

| 模块 | 用途 |
|------|------|
| 工具 0a 分诊入口 | 不知道该用哪个模块时的路由器 |
| 工具 0b 红旗扫描 | 60秒判断你的处境是否危险 |
| 工具 0c 被裁72小时 | 刚被裁的时候做什么、不做什么 |
| 工具 0d 隐私与OPSEC | 怎么安全地使用本工具 |
| 模块1 话术解码 | 翻译老板/HR的话真正在说什么 |
| 模块2 加班决策 | 真实成本-收益分析 |
| 模块3 绩效review解读 | 看穿review背后的意图 |
| 模块4 跳槽留任决策 | 基于真实利益做选择 |
| 模块5 历史视角 | 从150年劳工运动史中找参考 |
| 模块6 劳动法地图 | 8个法域条目，覆盖9个具名法域/地区（不是法律建议）|
| 模块7 薪资谈判 | 完整 playbook |
| 模块8 PIP应对 | 从识别预警到谈severance |
| 模块9 找工作和面试 | 求职全生命周期 |

详细见 [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md)。

---

## 安装

```bash
# clone 这个仓库
git clone https://github.com/workingclass-ai/workingclass.git
cd workingclass

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"

# Cursor
# 打开本仓库时，Cursor 会读取 .cursor/rules/laborer-companion.mdc。
# 如果要在另一个 repo 使用，复制 skills/laborer-companion/ 和 .cursor/rules/laborer-companion.mdc。

# Claude Code（如果你使用 legacy Claude skills）
mkdir -p ~/.claude/skills
cp -R skills/laborer-companion ~/.claude/skills/
```

然后在 agent 里描述你的职场情况，skill 会自动激活。或者用 slash 命令：

```
/triage      - 不知道用哪个模块时，从这里开始
/scan        - 60秒红旗扫描
/decode      - 解码老板/HR的话术
/overtime    - 加班决策
/review      - 解读绩效review
/jump        - 跳槽决策
/history     - 历史视角
/law         - 劳动法查询
/salary      - 薪资谈判
/pip         - PIP应对
/jobsearch   - 找工作和面试
```

---

## Codex / Cursor 支持

- **Codex**：skill 位于 `skills/laborer-companion/`；UI metadata 位于 `skills/laborer-companion/agents/openai.yaml`。安装到 `${CODEX_HOME:-$HOME/.codex}/skills/` 后，可用 `$laborer-companion` 触发。
- **Cursor**：本仓库包含 Cursor Project Rule：`.cursor/rules/laborer-companion.mdc`。在 Cursor 打开本仓库时，Agent 可按该 rule 调用 `skills/laborer-companion/SKILL.md`。
- **通用 agent 指南**：根目录 `AGENTS.md` 提供 Codex / Cursor 兼容的仓库级使用说明。

如果要把这个 skill 移植到别的项目，复制 `skills/laborer-companion/`、`.cursor/rules/laborer-companion.mdc` 和 `AGENTS.md`，并保持 rule 里的路径一致。

---

## 劳动法覆盖范围

模块6目前有 **8个法域条目**，覆盖 **9个具名法域/地区**：

| 法域条目 | 说明 |
|---|---|
| 中国大陆 | 独立文件 |
| 香港 / 台湾 | 两个地区/法域，放在同一个文件下；回答时不能混用规则，也不能标成国家 |
| 美国 | 联邦 + 加州/纽约重点 |
| 加拿大 | 联邦 + 省级差异提示 |
| 澳大利亚 | Fair Work / Award / unfair dismissal |
| 英国 | UK employment / ACAS / tribunal |
| 欧盟 | 区域总览，含德国、法国、荷兰提示；不是27国完整细则 |
| 印度 | 四部 Labour Codes + IT行业常见问题 |

所以如果把香港和台湾分开数，是 **9个法域/地区名称**；如果按 reference 文件/法域条目数，是 **8个**。香港和台湾在本项目里必须标注为**地区/法域**，不是国家。

---

## 多语言支持

当前支持：

- 简体中文
- 繁體中文
- English
- Español / Spanish
- Français / French
- Português / Portuguese
- Deutsch / German

默认规则：用户用什么语言提问，skill 就用同一语言回答；法律名称、政府机构、合同条款等会保留官方原文，并在必要时加简短解释。繁體中文场景会尽量使用香港/台湾更自然的术语。

---

## 示例与教程

更多完整示例在 [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md)。建议从这些用法开始：

```text
/triage
我感觉经理最近态度不对，但说不清。帮我判断该用哪个模块。
```

```text
/law
我在香港兼职，每周17小时，HR说香港最低工资只覆盖部分行业。这个说法对吗？
```

```text
/review
这是我的绩效review：[粘贴脱敏后的内容]
我去年是 exceeds，今年是 meets。这是不是危险信号？
```

欢迎贡献更多教程和真实案例，尤其是：

- 不同国家/地区/法域的劳动法例子
- PIP / 裁员 / severance 谈判 walkthrough
- 薪资谈判脚本
- 面试反操控示例
- 已脱敏的 HR / manager 邮件样本
- 西班牙语、法语、葡萄牙语、德语的真实使用示例

---

## 重要原则

1. **不号召集体行动**——这是给单个劳动者的清醒工具
2. **承认现实约束**——不会给"立刻辞职"这种鲁莽建议
3. **保持智识诚实**——不会因为"政治正确"而给建议
4. **用户隐私至上**——见 `skills/laborer-companion/references/privacy-and-opsec.md`
5. **不冒充律师**——提供框架和应该问的问题，不替代专业法律咨询

---

## 隐私警告 ⚠️

- 这个 skill 不会把你的对话上传到任何第三方
- 但你和 AI 服务商的对话可能会被平台记录，取决于账号和隐私设置
- **不要在公司设备 / 公司网络下使用这个工具**
- **不要把公司机密数据贴给 AI 分析**——脱敏后再用

详细见 [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md)。

---

## 灵感来源

- Koki Xu 的 anti-distillation skill（2026年4月）
- Karl Marx 关于劳动价值与异化理论
- E.P. Thompson 《英国工人阶级的形成》
- 过去150年全球工人运动的具体案例
- 当代劳动经济学和职场社会学

这个工具不创造任何新东西。是把工人阶级150年来的集体智慧，翻译成2026年AI时代可用的形式。

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。我们特别欢迎：

- 新的职场话术案例（让模块1更完整）
- 你所在国家/地区/法域的劳动法补充
- 成功的薪资谈判 / severance 谈判案例
- PIP 经历（匿名化后）
- 多语言翻译

---

## 许可

Apache 2.0 — 见 [LICENSE](LICENSE)。

唯一的请求：**保持工具的核心使命，服务于劳动者**。

---

## 一段话

清醒地看清你的处境，不会让你的处境改变。但清醒是改变的前提。而且很多时候，清醒地接受现实（包括"我现在还不能离开"），比假装不清醒地忍受，要好得多。

至少你知道自己在做什么。

---

> Seeing your situation clearly doesn't change your situation. But clarity is the precondition for change. And often, accepting reality with eyes open (including "I can't leave yet") is better than enduring with eyes closed.
>
> At least you know what you're doing.
