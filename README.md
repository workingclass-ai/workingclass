# workingclass

> 站在劳动者一边的 AI 工具集。
> AI tools that stand on the side of workers.

这个仓库收录服务于劳动者的 agent skills 和工具。第一个，也是核心的，是 **劳动者AI助手 / Laborer's Companion**——一个帮你看穿职场话术、做出对自己最好的决定的工具。

---

## 为什么存在这个项目

在职场上，公司、HR、老板都有大量资源来管理你：HR 顾问、PUA 话术培训、绩效管理系统、法律团队、招聘心理学顾问。他们说的每一句话都经过精心设计，目的不一定是让你看清，而是让你做出对公司最有利的决定。

而你只有你自己。

AI 时代让这个不对称更严重——公司用 AI 蒸馏你的工作、AI 替代你、AI 监控你。这个项目把 AI 反过来用：**让 AI 站在你这边**。

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
| 模块6 8法域劳动法 | 法律地图（不是法律建议）|
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
- 你所在地区/国家的劳动法补充
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
