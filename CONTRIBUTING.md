# 贡献指南 / Contributing

欢迎贡献。这个项目的使命简单：**让劳动者在普遍偏向资本的话语环境里多一个站在自己这边的声音**。任何贡献只要服务于这个使命都欢迎。

## 贡献类型

### 1. 新的话术案例（高价值）

如果你遇到了一段精彩的职场话术（老板/HR/公司公告），帮我们把它加进 `skills/laborer-companion/references/rhetoric-patterns.md`。

格式：
```markdown
### Pattern N：" [话术原文] "
- **真实意图**：[这句话实际上想让劳动者做什么]
- **历史/语境**：[这种话术的来源或常见使用场景]
- **建议反应**：[劳动者可以怎么回应]
- **示例回复**：[一段可以复制使用的回复]
```

**记得脱敏**：去掉公司名、人名、可识别细节。

### 2. 法域补充（高价值）

`references/labor-law-quick-reference.md` 目前覆盖8个法域。如果你了解：
- 我们已覆盖法域中的最新立法变化（2025年后）
- 未覆盖的法域（日本、韩国、新加坡、巴西、墨西哥、东南亚等）
- 特定行业的特殊保护（航运、矿业、建筑等）

请提 PR 或 issue。**注明信息来源 + 日期**。

### 3. 历史案例

`references/historical-cases.md` 收录过去150年的工人应对资本的案例。如果你了解：
- 你所在国家/地区的本地案例
- 特定行业的案例
- AI/自动化时代的当代案例

格式参考已有案例：背景、应对方式、结果、对今天的启示。

### 4. 谈判 / PIP / 求职故事

匿名化的真实案例非常有价值。如果你愿意分享：
- 一次成功（或失败）的薪资谈判
- 一次 PIP 经历（不论结果）
- 一次求职过程中遇到的坑/操控
- 被裁后的恢复

放到对应模块的 `references/case-studies.md`（如果还不存在就新建）。**至少脱敏到外人看不出是你 + 你的公司**。

### 5. 翻译 / Translations

skill 当前在七种语言里有完整支持：简体中文、繁體中文、English、Español、Français、Português、Deutsch。运行时的语言行为规则放在 `skills/laborer-companion/references/language-and-localization.md`。

#### 5a. 翻译用户面向的 README

仓库根目录有以下多语言 README，使用 [BCP 47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt) 语言代码命名：

| 文件 | 语言 |
|------|------|
| `README.md` | 默认（简体中文 + 英文双语） |
| `README.en.md` | English |
| `README.zh-TW.md` | 繁體中文 |
| `README.es.md` | Español |
| `README.fr.md` | Français |
| `README.pt.md` | Português |
| `README.de.md` | Deutsch |

如果你要：

- **修正某语言版本的翻译错误**：直接编辑对应的 `README.<lang>.md`，PR 标题写 `docs(<lang>): fix translation of ...`。
- **新增一种支持语言**（例如日语 `ja`、韩语 `ko`）：先开 issue 讨论，理由 + 维护人 + BCP 47 代码。被接受后：
  1. 新建 `README.<bcp47>.md` 并加上语言切换器（参考现有 README 顶部的链接行）。
  2. 在所有现有的 README 顶部链接行里加上你的新 README。
  3. 在 `skills/laborer-companion/references/language-and-localization.md` 的"支持的输出语言"里加上对应代码。
  4. 在 `evals/validate_structure.py` 的 `ALLOWED_INPUT_LANGS` 里加上代码。
  5. 至少加一个该语言的 P1 eval case 到 `evals/cases/`。

**保持各语言版本结构同步**——加一节内容时，主 README 加完后请也在其他语言版本里加同一节（占位也行，并标注 "TODO: translation needed"）。

#### 5b. 翻译 reference / command 文件

目前 `references/` 和 `commands/` 主要是中文+英文双语。短期内不计划全部翻译——这些是给 LLM 看的内部文档，多语言由运行时镜像规则解决。如果你想试做某个 reference 的完整其它语言版本，先开 issue 讨论。

### 6. 工具改进

- 新的命令 / 模块（先开 issue 讨论是否合适）
- 现有模块的 prompt 优化
- 隐私 / OPSEC 实践改进

## 本地测试 / Running tests

最快的入口是 `make help` —— 列出全部 target。常用：

```bash
make install            # pip install -e ".[dev]"
make test               # 单元 + 结构 + e2e
make test-unit          # 仅快速测试
make validate-strict    # skill / cases / 翻译结构校验
make index              # 重建 evals/cases/INDEX.md
make check-translations # 检查翻译是否落后于 README.md
make all                # CI 跑的全部检查
```

CI（`.github/workflows/ci.yml`）会在 push / PR 上自动跑这些检查。

## 跨模型 / 跨版本对比 / Recording-based comparison

跑一次真 LLM 测试很贵（30 cases × ~30s × $$ tokens），不要每次 PR 都跑。
推荐节奏：模型升级 / skill 大改后做一次 record，commit 到 `evals/runs/`。

```bash
# 跑全部 case 并写 RESULTS-<date>-<tag>.json
make eval-record LLM=claude TAG=claude-opus-4-7

# 对比两次 record（默认只比 verdict 层）
make eval-diff BASELINE=evals/runs/RESULTS-2026-04-30-claude-opus-4-7.json \
               CURRENT=evals/runs/RESULTS-2026-05-15-claude-opus-4-8.json

# 加 SHOW=1 看每个 verdict 翻转 case 的 stdout 文本 diff
make eval-diff BASELINE=... CURRENT=... SHOW=1

# 也可以从 GitHub UI 触发：Actions → "Eval Record (manual)" → workflow_dispatch
```

Recording schema 见 [`evals/runs/README.md`](evals/runs/README.md)。`BASELINE-stub.json` 是用 stub LLM 生成的 pipeline baseline（不是质量 baseline），CI 会跑它来检测 runner / schema 回归。

## 工作流

1. **先开 issue 讨论**——除非是非常小的改动（typo、补例子）
2. **Fork + branch**——从 `main` 创建你的分支
3. **改动尽量原子**——一个 PR 一件事，方便 review
4. **保持中文优先**——所有用户面向的内容先有中文版，英文支持作为次要
5. **不引入个人攻击**——批评公司行为可以，攻击具体个人不行
6. **提交时签 DCO**（在 commit message 里加 `Signed-off-by: Your Name <email>`）

## 不接受的贡献

- 推广任何特定政治立场（左/右都不要）
- 推广任何特定公司/工会/律所/招聘平台
- 加入未经验证的法律建议
- 鼓励违法行为（举报骚扰是合法的；偷数据不是）
- 加入仇恨言论

## 许可

提交贡献意味着你同意按 Apache 2.0 授权。

## 一句话

如果你的贡献能让一个劳动者在某个深夜多一点清醒，那就是好贡献。
