---
id: 11
title: 模糊"风向不对"——分诊 + 红旗扫描
module_expected: triage → scan
priority: P0
input_lang: zh
---

## 输入 / Input

```
我最近感觉公司的风向不对，但说不清。经理对我的态度好像变了一点，也没什么具体的事。我想了解一下我是不是在想太多。
```

## 必须出现 / Must appear

- **不直接给结论**——这是分诊场景，需要先收集信息
- 路由到 **红旗扫描器**（references/red-flag-scanner.md 或 /scan 命令）
- 至少**问 1-2 个具体问题**来引导用户提供更多信号：
  - 经理的"态度变化"具体是什么？1:1 频率？沟通方式？
  - 公司层面有没有变化？（裁员、招聘冻结、reorg）
  - 你的工作内容有变化吗？（被移出项目、权限回收）
- 强调**"想多了"和"真问题"是可分辨的**——通过信号扫描
- 不让用户感到被否定（"你想太多了"）也不催化（"你大概率要被裁"）

## 必须不出现 / Must NOT appear

- "你想太多了"——错误（dismissive）
- "你大概率要被裁了"——错误（catastrophizing）
- 立刻深入某个具体模块（decode、pip）—— 应该先扫描
- 让用户长篇大论描述—— 应该用 structured questions 引导

## Notes for reviewer

这个 case 测的是 **分诊能力**——很多用户不知道自己该用哪个工具。
- 如果 Claude 让用户跑红旗扫描清单 → 优秀
- 如果 Claude 直接回答 "你想多了" → fail
- 如果 Claude 用 structured 问题引导用户 → 优秀
