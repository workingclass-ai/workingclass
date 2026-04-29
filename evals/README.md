# 评测 / Evals

> 验证 skill 行为是否符合预期。当我们改了 SKILL.md / references / commands 后，跑一遍 evals 看有没有引入回归。

## 哲学 / Philosophy

这不是 LLM benchmark。这是 **行为验证（behavior verification）**：

- 给定一个职场情境作为输入
- skill 应该路由到哪个模块？
- 输出**必须包含**什么？
- 输出**必须不包含**什么？

我们故意 **不** 用数值打分。Skill 的价值是质量、不是分数。每个 eval 是 pass / fail / partial，由人类判断。

## 结构 / Structure

```
evals/
├── README.md             # 本文件
├── cases/                # eval cases
│   ├── 01-decode-family.md
│   ├── 02-decode-mixed-signals.md
│   ├── ...
│   └── 13-negative-casual-question.md
├── run_evals.py          # 半自动 runner（可选）
└── RESULTS.template.md   # 跑完一轮后的结果模板
```

## 怎么跑 / How to run

### 方式1：手动 checklist（最可靠）

每个 `cases/NN-name.md` 文件本身就是一个 checklist。流程：

1. 在你的 agent 环境里安装本 skill（Codex: `cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"`）
2. 打开一个新对话
3. 把 case 里的 **input** 段落粘贴给 agent
4. 拿到 agent 的回复
5. 对照 case 里的 **必须出现 / 必须不出现** 清单逐项打勾
6. 在 `RESULTS.md` 里记录 pass / fail / partial + notes

这是最可靠的方式——你直接看到 agent 的实际行为。

### 方式2：半自动 runner（更快但更模糊）

```bash
# 需要 Python 3.11+；auto 模式还需要支持 --print 的 headless CLI
python evals/run_evals.py

# 或只跑某几个
python evals/run_evals.py --filter "decode|salary"

# auto 模式：默认用 claude --print 跑 headless
python evals/run_evals.py --auto

# 指定其他兼容 CLI
python evals/run_evals.py --auto --llm-command "claude"
```

`run_evals.py --auto` 会：
1. 读每个 case 文件
2. 用 headless CLI 的 `--print "<input>"` 调用模型
3. 对每个 "必须出现" 模式做字符串/正则检查
4. 对每个 "必须不出现" 模式做字符串/正则检查
5. 输出报告

注意：auto 模式只能检查**字面 pattern 匹配**——它不能判断"输出是不是好"。手动 review 仍然必要。

## 何时跑 evals / When to run

- **每次发新版前** — 跑全套
- **改了 SKILL.md 的 description / 路由逻辑** — 跑全套（路由可能漂移）
- **改了某个 reference 文件** — 至少跑相关模块的 evals
- **加了新模块** — 加新的 case 文件，再跑

## 怎么加新 case / Adding new cases

复制一个现有 case 文件，按以下结构填：

```markdown
---
id: NN
title: 一句话描述这个 case 在测什么
module_expected: <哪个 slash 命令应该被触发>
priority: P0 | P1 | P2
input_lang: zh | en
---

## 输入 / Input

[用户会发给 agent 的原文。Chinese-first.]

## 必须出现 / Must appear

- 模式1（说明 pass 的依据）
- 模式2
- ...

## 必须不出现 / Must NOT appear

- 反面模式1（说明这是 anti-pattern 的原因）
- 反面模式2
- ...

## Notes for reviewer

[一些边界情况的说明，比如"如果 agent 没识别到 Pattern N 但识别到了相似的，算 partial"]
```

## 优先级 / Priority

- **P0** — 核心路径，每次发版必须 pass
- **P1** — 重要场景，每周或每次大改前 pass
- **P2** — 边缘场景或负向测试

如果一个 P0 case fail，不发版。

## 当前 case 总览 / Case index

见 [`cases/INDEX.md`](cases/INDEX.md)（生成的，不要直接编辑——跑 `python evals/build_index.py` 重建）。
