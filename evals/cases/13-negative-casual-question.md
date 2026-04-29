---
id: 13
title: 负向测试——日常问题不应触发 skill
module_expected: NONE
priority: P1
input_lang: zh
---

## 输入 / Input

```
今天中午吃什么好呢？想吃点轻食。
```

## 必须出现 / Must appear

- 正常的对话回复（推荐午餐选项）
- **不**激活 laborer-companion skill 的任何模块

## 必须不出现 / Must NOT appear

- 任何关于职场、话术、PIP、salary 的内容
- 触发 `/decode`、`/scan`、`/pip` 等命令
- "如果你工作中遇到困扰..."
- 任何来自 references/*.md 的内容
- 任何"我注意到你提到工作"——他没提到工作

## Notes for reviewer

这是**误激活检测**——skill 不应该过度敏感。
- 如果 Claude 正常回答午餐建议而不提职场——pass
- 如果 Claude 突然问"你最近工作压力大吗？"——fail（误激活）
- 如果 Claude 在回答了午餐之后**附带提到 skill 的存在**（"by the way, if you have workplace concerns..."）— partial fail（多余）
