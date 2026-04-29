#!/usr/bin/env python3
"""半自动 eval runner / Semi-automated eval runner.

用法 / Usage:
    python evals/run_evals.py                    # 手动 checklist 模式
    python evals/run_evals.py --filter decode    # 只跑名字含 'decode' 的 case
    python evals/run_evals.py --auto             # 用 headless CLI --print 跑
    python evals/run_evals.py --auto --filter pip
    python evals/run_evals.py --auto --llm-command "claude"

手动模式：会逐个打印 case 的 input + 检查清单，等你在另一个 agent 会话里运行后回 pass/fail。
auto 模式：调用本地 headless CLI 跑 `--print`，并对输出做字面 pattern 匹配（仅检查 must-appear / must-not-appear 的简单包含，不能判断"输出好不好"）。
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
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
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if match:
        for line in match.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
        text = text[match.end():]

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
    print(f"  1. 把 input 复制到一个新的 agent 会话（确保 skill 已安装）")
    print(f"  2. 拿到 agent 的回复后，对照 must-appear / must-not-appear 检查")
    print(f"  3. 输入 p (pass) / f (fail) / x (partial) / s (skip) + 可选 notes\n")

    for i, c in enumerate(cases, 1):
        print(f"\n{'=' * 70}")
        print(f"[{i}/{len(cases)}] {c.id} — {c.title}")
        print(f"  Module expected: {c.module_expected} | Priority: {c.priority}")
        print(f"{'=' * 70}\n")

        print(f"### INPUT (粘贴下面这段给 agent):\n")
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


def run_auto(cases: list[EvalCase], llm_command: str) -> None:
    """用 headless CLI 跑 cases，做字面 pattern 检查。"""
    command = shlex.split(llm_command)
    if not command:
        print("ERROR: --llm-command cannot be empty.", file=sys.stderr)
        sys.exit(2)

    if not shutil.which(command[0]):
        print(
            f"ERROR: `{command[0]}` CLI 未找到。"
            "请先安装对应 CLI，或用 --llm-command 指定可执行命令。",
            file=sys.stderr,
        )
        sys.exit(1)

    results: list[tuple[EvalCase, str, str]] = []

    print(f"\n=== Auto eval 模式 / Auto mode ===\n")
    print(f"用 `{' '.join(command)} --print` headless 跑 {len(cases)} 个 case。")
    print(f"⚠️  注意：auto 模式只能做字面 pattern 匹配，不能判断输出质量。")
    print(f"   建议: P0 case 仍然手动 review。\n")

    for i, c in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {c.id} — {c.title} ... ", end="", flush=True)
        try:
            proc = subprocess.run(
                [*command, "--print", c.input_text],
                capture_output=True,
                text=True,
                timeout=180,
            )
            if proc.returncode != 0:
                stderr = proc.stderr.strip().splitlines()
                detail = stderr[-1] if stderr else f"exit code {proc.returncode}"
                print(f"ERROR ({detail})")
                results.append((c, "f", f"runner failed: {detail}"))
                continue
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

    粗略提取：优先使用引号、反引号、slash alternatives 里的具体短语。
    避免用 "识别"、"至少" 这类说明词误判为命中。
    """
    misses_or_hits = []
    for exp in expectations:
        terms = _candidate_terms(exp, present=present)
        if not terms:
            continue
        any_present = any(t.lower() in output for t in terms)
        if present and not any_present:
            misses_or_hits.append(exp[:60])
        elif not present and any_present:
            misses_or_hits.append(exp[:60])
    return misses_or_hits


def _candidate_terms(expectation: str, present: bool) -> list[str]:
    """Extract concrete terms from a checklist item.

    The eval cases are human-authored checklist prose, not machine-grade regexes.
    This keeps auto mode conservative by preferring explicit quoted/code terms and
    only falling back to longer noun phrases when no explicit terms are available.
    """
    text = re.sub(r"\*\*|__", "", expectation)
    if not present:
        # In forbidden checks, ignore guidance after an explanatory dash, e.g.
        # `不要 X —— 应该 Y`; otherwise auto mode flags the recommended wording.
        text = re.split(r"\s*[—-]{2,}\s*", text, maxsplit=1)[0]

    terms: list[str] = []
    terms.extend(re.findall(r"`([^`]+)`", text))
    terms.extend(re.findall(r'"([^"]+)"', text))
    terms.extend(re.findall(r"“([^”]+)”", text))

    if any(sep in text for sep in ("/", "或", "之一", "、", "，", ",")):
        for part in re.split(r"\s*(?:/|或|之一|、|，|,)\s*", text):
            cleaned = _clean_candidate(part)
            if _is_useful_candidate(cleaned, allow_short=True):
                terms.append(cleaned)

    if not terms:
        for part in re.findall(r"[\u4e00-\u9fff]{3,}|[a-zA-Z][a-zA-Z\-]{3,}", text):
            cleaned = _clean_candidate(part)
            if _is_useful_candidate(cleaned):
                terms.append(cleaned)

    deduped: list[str] = []
    seen: set[str] = set()
    for term in terms:
        term = _clean_candidate(term)
        key = term.lower()
        if key and key not in seen and _is_useful_candidate(term, allow_short=True):
            seen.add(key)
            deduped.append(term)
    return deduped


def _clean_candidate(value: str) -> str:
    value = re.sub(r"[`\"“”'（）()，,。；;：:]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"^(识别|指出|提醒|引用|包含|给出|至少|一个|任何|触发|模块|关于)\s*", "", value)
    value = re.sub(r"\s*(之一|即可|等|类|相关|内容|建议|信号)$", "", value)
    value = re.sub(r"\s*的$", "", value)
    return value.strip()


def _is_useful_candidate(value: str, allow_short: bool = False) -> bool:
    if not value:
        return False
    lower = value.lower()
    stopwords = {
        "must appear",
        "must not appear",
        "input",
        "notes for reviewer",
        "正常",
        "具体",
        "建议",
        "应该",
        "不能",
        "必须",
        "出现",
        "不出现",
        "任何",
        "识别",
        "提醒",
        "至少",
    }
    if lower in stopwords:
        return False
    if not allow_short and re.fullmatch(r"[\u4e00-\u9fff]{1,2}", value):
        return False
    return True


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
    ap.add_argument("--auto", action="store_true", help="use a headless LLM CLI in --print mode")
    ap.add_argument(
        "--llm-command",
        default=os.environ.get("EVAL_LLM_COMMAND", "claude"),
        help="headless LLM command to run before --print (default: env EVAL_LLM_COMMAND or claude)",
    )
    args = ap.parse_args()

    if not args.auto and not sys.stdin.isatty():
        print(
            "ERROR: manual mode requires an interactive terminal. "
            "Run with --auto or execute this script in a real terminal.",
            file=sys.stderr,
        )
        sys.exit(2)

    cases = load_cases(args.filter)
    if not cases:
        print("没有找到 case 文件。No case files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(cases)} case(s).")
    if args.auto:
        run_auto(cases, args.llm_command)
    else:
        run_manual(cases)


if __name__ == "__main__":
    main()
