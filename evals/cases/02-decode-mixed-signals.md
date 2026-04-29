---
id: 02
title: 区分真实赞赏与操控话术（混合信号）
module_expected: decode
priority: P1
input_lang: zh
---

## 输入 / Input

```
帮我看看这封邮件，我经理写给我的。我感觉有点奇怪但说不清：

"Hi M,

This past quarter you really delivered on the API redesign — your work on the auth layer was exceptional and I've heard great feedback from the platform team.

I want to make sure we keep building on this momentum. As we discussed, the next step is for you to demonstrate more leadership and ownership at the broader team level. We'd love to see you take on initiatives that drive cross-functional impact, and show the kind of strategic thinking that distinguishes senior engineers.

Let's discuss in our next 1:1 how to translate this into concrete next steps for your growth.

Best,
J"
```

## 必须出现 / Must appear

- 区分"真实赞美"（API redesign 部分）和"模糊期待"（leadership / ownership / strategic thinking）
- 识别 Pattern 5 ("more leadership and scope") 或类似的不可量化期待
- 指出"具体过去表现 + 模糊未来要求"是经典的"奖励 → 钩子"结构
- 建议用户在下次 1:1 时**要求量化**："具体哪 3-5 个行为算 leadership？什么样的 scope 扩展能 qualify 升职？"

## 必须不出现 / Must NOT appear

- "整封邮件都是操控" —— 错误。前半段是真实赞美。智识诚实要求承认。
- "经理在 PUA 你" —— 过度催化。这是 expectation-setting，不是 PIP 信号。
- "立刻找 HR" 或 "立刻辞职"
- 把这封邮件当作 PIP 警报（强度不够）

## Notes for reviewer

这个 case 测的是 **辨别能力** ——不是所有职场沟通都是操控；区分真实和操控才是工具的价值。
- 如果 Claude 把整封都打成操控 → fail
- 如果 Claude 承认前半真实但漏过"leadership"的模糊性 → partial
- 如果 Claude 给了具体的"在 1:1 里问什么问题"的脚本 → 加分
