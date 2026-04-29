# 安全策略 / Security Policy

## 报告漏洞 / Reporting Vulnerabilities

如果你发现了：
- 这个项目的代码 / 配置中的安全问题
- skill 中可能泄露用户隐私的设计
- 可能危害用户安全的话术或建议（例如：可能让用户违法、暴露身份的指引）

**请不要在 public issue 里发**。改用：

- GitHub Security Advisory: https://github.com/workingclass-ai/workingclass/security/advisories/new
- 或私信给 maintainer

我们会在 7 天内回复，30 天内尝试修复。

## 用户隐私准则 / User Privacy Guidelines

这个项目本身**不收集任何用户数据**。所有 skill 内容都是本地运行（在用户的 Claude Code 实例上）。

但是：

1. **你和 Claude 的对话会被 Anthropic 记录**——这是 Anthropic 的隐私政策范围
2. **不要在公司设备上使用这些工具**——你的雇主可能监控
3. **不要把公司机密贴给 AI**——脱敏后再用

完整指南见 [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md)。

## 反恶意使用 / Anti-Abuse

这个工具旨在**保护劳动者**，不是用来：
- 骚扰或追踪雇主、HR、同事
- 伪造证据、操纵法律程序
- 教唆违法行为

如果你发现工具被用于上述目的，请通过 Security Advisory 报告。
