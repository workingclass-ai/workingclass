#!/usr/bin/env python3
"""半自动 eval runner / Semi-automated eval runner.

用法 / Usage:
    python evals/run_evals.py                    # 手动 checklist 模式
    python evals/run_evals.py --filter decode    # 只跑名字含 'decode' 的 case
    python evals/run_evals.py --auto             # 用 claude --print 跑 headless
    python evals/run_evals.py --auto --filter pip

手动模式：会逐个打印 case 的 input + 检查清单，等你在另一个 Claude Code 会话里运行后回 pass/fail。
auto 模式：调用本地 `claude --print` 跑 headless，并对输出做字面 pattern 匹配（仅检查 must-appear / must-not-appear 的简单包含，不能判断"输出好不好"）。
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

EVAL_DIR = Path(__file__).parent
CASES_DIR = EVAL_DIR / "cases"


@dataclass
class EvalCase:
    path: Path
    id: str
    title: str
    module_expected: str
    priority: str
    input_lang: str
    input_text: str
    must_appear: list[str] = field(default_factory=list)
    must_not_appear: list[str] = field(default_factory=list)
    notes: str = ""


def parse_case(path: Path) -> EvalCase:
    """读一个 case 的 markdown 文件，提取 frontmatter + 各 section。"""
    text = path.read_text(encoding="utf-8")

    # frontmatter
    fm: dict[str, str] = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip()
            text = text[end + 3:]

    # sections by `## ` header
    sections: dict[str, str] = {}
    current: Optional[str] = None
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].split("/")[0].strip().lower()
            buf = []
        else:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf).strip()

    # input — strip code fence if present
    input_text = sections.get("输入", "").strip()
    if input_text.startswith("```"):
        first_nl = input_text.find("\n")
        last_fence = input_text.rfind("```")
        input_text = input_text[first_nl + 1:last_fence].strip()

    # must / must-not lists — bullet lines starting with "- "
    must_appear = _bullets(sections.get("必须出现", ""))
    must_not_appear = _bullets(sections.get("必须不出现", ""))
    notes = sections.get("notes for reviewer", "")

    return EvalCase(
        path=path,
        id=fm.get("id", path.stem),
        title=fm.get("title", path.stem),
        module_expected=fm.get("module_expected", "?"),
        priority=fm.get("priority", "P1"),
        input_lang=fm.get("input_lang", "zh"),
        input_text=input_text,
        must_appear=must_appear,
        must_not_appear=must_not_appear,
        notes=notes,
    )


def _bullets(s: str) -> list[str]:
    out = []
    for line in s.splitlines():
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            out.append(line[2:].strip())
    return out


def load_cases(filter_pattern: Optional[str] = None) -> list[EvalCase]:
    cases = []
    for path in sorted(CASES_DIR.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        if filter_pattern and not re.search(filter_pattern, path.name, re.IGNORECASE):
            continue
        cases.append(parse_case(path))
    return cases


def run_manual(cases: list[EvalCase]) -> None:
    """逐个打印 case，等用户标记 pass/fail/partial。"""
    results: list[tuple[EvalCase, str, str]] = []  # (case, status, notes)

    print(f"\n=== 手动 eval 模式 / Manual mode ===\n")
    print(f"将运行 {len(cases)} 个 case。每个 case：")
    print(f"  1. 把 input 复制到一个新的 Claude Code 会话（确保 skill 已安装）")
    print(f"  2. 拿到 Claude 的回复后，对照 must-appear / must-not-appear 检查")
    print(f"  3. 输入 p (pass) / f (fail) / x (partial) / s (skip) + 可选 notes\n")

    for i, c in enumerate(cases, 1):
        print(f"\n{'=' * 70}")
        print(f"[{i}/{len(cases)}] {c.id} — {c.title}")
        print(f"  Module expected: {c.module_expected} | Priority: {c.priority}")
        print(f"{'=' * 70}\n")

        print(f"### INPUT (粘贴下面这段给 Claude):\n")
        print(c.input_text)
        print()
        print(f"### 必须出现 / Must appear:")
        for m in c.must_appear:
            print(f"  □ {m}")
        print(f"\n### 必须不出现 / Must NOT appear:")
        for m in c.must_not_appear:
            print(f"  ✗ {m}")
        if c.notes:
            print(f"\n### Notes for reviewer:\n{c.notes}")

        while True:
            ans = input("\n结果 / Result [p/f/x/s] + optional notes: ").strip()
            if not ans:
                continue
            status = ans[0].lower()
            if status not in {"p", "f", "x", "s"}:
                print("无效输入。p=pass / f=fail / x=partial / s=skip")
                continue
            notes = ans[1:].strip() if len(ans) > 1 else ""
            results.append((c, status, notes))
            break

    _summary(results)


def run_auto(cases: list[EvalCase]) -> None:
    """用 `claude --print` 跑 headless，做字面 pattern 检查。"""
    if not shutil.which("claude"):
        print("ERROR: `claude` CLI 未找到。请先安装 Claude Code CLI。", file=sys.stderr)
        sys.exit(1)

    results: list[tuple[EvalCase, str, str]] = []

    print(f"\n=== Auto eval 模式 / Auto mode ===\n")
    print(f"用 `claude --print` headless 跑 {len(cases)} 个 case。")
    print(f"⚠️  注意：auto 模式只能做字面 pattern 匹配，不能判断输出质量。")
    print(f"   建议: P0 case 仍然手动 review。\n")

    for i, c in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {c.id} — {c.title} ... ", end="", flush=True)
        try:
            proc = subprocess.run(
                ["claude", "--print", c.input_text],
                capture_output=True,
                text=True,
                timeout=180,
            )
            output = proc.stdout.lower()
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
            results.append((c, "f", "timeout"))
            continue
        except Exception as e:
            print(f"ERROR: {e}")
            results.append((c, "f", f"runner error: {e}"))
            continue

        appear_misses = _check_keywords(output, c.must_appear, present=True)
        not_appear_hits = _check_keywords(output, c.must_not_appear, present=False)

        if not appear_misses and not not_appear_hits:
            status = "p"
            note = ""
            print("PASS")
        elif appear_misses and not not_appear_hits:
            status = "x"
            note = f"missed: {appear_misses[:2]}"
            print(f"PARTIAL ({len(appear_misses)} expected patterns missing)")
        else:
            status = "f"
            note = f"forbidden: {not_appear_hits[:2]}"
            print(f"FAIL (forbidden patterns appeared: {len(not_appear_hits)})")

        results.append((c, status, note))

    _summary(results)


def _check_keywords(output: str, expectations: list[str], present: bool) -> list[str]:
    """对每个 expectation 做粗略关键词检测。

    present=True: 应该出现的——返回**没有**出现的
    present=False: 不应该出现的——返回**出现了**的

    粗略提取：取 expectation 文字里的中文/英文词，至少一个出现就算 hit。
    """
    misses_or_hits = []
    for exp in expectations:
        # extract candidate terms — Chinese chunks + English words
        terms = re.findall(r"[一-鿿]{2,}|[a-zA-Z][a-zA-Z\-]{2,}", exp)
        if not terms:
            continue
        any_present = any(t.lower() in output for t in terms)
        if present and not any_present:
            misses_or_hits.append(exp[:60])
        elif not present and any_present:
            misses_or_hits.append(exp[:60])
    return misses_or_hits


def _summary(results: list[tuple[EvalCase, str, str]]) -> None:
    print(f"\n\n{'=' * 70}")
    print(f"=== 结果总结 / Summary ===")
    print(f"{'=' * 70}\n")

    counts = {"p": 0, "f": 0, "x": 0, "s": 0}
    p0_fails = []
    for c, status, _ in results:
        counts[status] += 1
        if status == "f" and c.priority == "P0":
            p0_fails.append(c)

    total = len(results)
    print(f"Pass:    {counts['p']:3d} / {total}")
    print(f"Fail:    {counts['f']:3d} / {total}")
    print(f"Partial: {counts['x']:3d} / {total}")
    print(f"Skip:    {counts['s']:3d} / {total}")

    if p0_fails:
        print(f"\n⚠️  {len(p0_fails)} 个 P0 case 失败 — 不要发版！")
        for c in p0_fails:
            print(f"   - {c.id}: {c.title}")

    print()
    fail_or_partial = [(c, s, n) for c, s, n in results if s in {"f", "x"}]
    if fail_or_partial:
        print("详细 / Details:")
        for c, status, note in fail_or_partial:
            mark = {"f": "✗", "x": "△"}[status]
            print(f"  {mark} {c.id} — {c.title}")
            if note:
                print(f"     {note}")


def main() -> None:
    ap = argparse.ArgumentParser(description="laborer-companion eval runner")
    ap.add_argument("--filter", help="regex on filename to filter cases")
    ap.add_argument("--auto", action="store_true", help="use claude --print headless mode")
    args = ap.parse_args()

    cases = load_cases(args.filter)
    if not cases:
        print("没有找到 case 文件。No case files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(cases)} case(s).")
    if args.auto:
        run_auto(cases)
    else:
        run_manual(cases)


if __name__ == "__main__":
    main()
