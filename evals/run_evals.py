#!/usr/bin/env python3
"""半自动 eval runner / Semi-automated eval runner.

用法 / Usage:
    python evals/run_evals.py                    # 手动 checklist 模式
    python evals/run_evals.py --filter decode    # 只跑名字含 'decode' 的 case
    python evals/run_evals.py --auto             # 用 headless CLI --print 跑
    python evals/run_evals.py --auto --filter pip
    python evals/run_evals.py --auto --llm-command "claude"
    python evals/run_evals.py --auto --record evals/runs/RESULTS-2026-04-30.json

手动模式：会逐个打印 case 的 input + 检查清单，等你在另一个 agent 会话里运行后回 pass/fail。
auto 模式：调用本地 headless CLI 跑 `--print`，并对输出做字面 pattern 匹配（仅检查 must-appear / must-not-appear 的简单包含，不能判断"输出好不好"）。
record 模式：在 auto 模式基础上把每个 case 的完整输出 + 元数据写到 JSON，方便跨模型版本对比（见 evals/eval_diff.py）。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

EVAL_DIR = Path(__file__).parent
CASES_DIR = EVAL_DIR / "cases"
REPO_ROOT = EVAL_DIR.parent
SKILL_FILE = REPO_ROOT / "skills" / "laborer-companion" / "SKILL.md"

# Bump this when the recording schema changes in a backwards-incompatible way.
# eval_diff.py refuses to compare across schema versions.
RECORDING_SCHEMA_VERSION = 1

# Cap raw output captured per case to avoid bloating recordings if the model
# rambles. 64 KB is enough for any reasonable workplace-analysis answer.
MAX_OUTPUT_BYTES = 64 * 1024


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


# Verdict vocabulary used in recordings + summaries.
# Single-letter form is preserved for the legacy interactive prompt.
STATUS_PASS = "pass"
STATUS_FAIL = "fail"
STATUS_PARTIAL = "partial"
STATUS_SKIP = "skip"
STATUS_ERROR = "error"

_STATUS_TO_LETTER = {
    STATUS_PASS: "p",
    STATUS_FAIL: "f",
    STATUS_PARTIAL: "x",
    STATUS_SKIP: "s",
    STATUS_ERROR: "f",
}
_LETTER_TO_STATUS = {
    "p": STATUS_PASS,
    "f": STATUS_FAIL,
    "x": STATUS_PARTIAL,
    "s": STATUS_SKIP,
}


@dataclass
class RunResult:
    """A single eval case's outcome, rich enough to record + diff."""

    case_id: str
    title: str
    module_expected: str
    priority: str
    input_lang: str
    status: str  # pass | fail | partial | skip | error
    note: str = ""
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0
    exit_code: Optional[int] = None
    missing_keywords: list[str] = field(default_factory=list)
    forbidden_hits: list[str] = field(default_factory=list)
    prompt: str = ""

    @property
    def status_letter(self) -> str:
        return _STATUS_TO_LETTER.get(self.status, "f")


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


def run_manual(cases: list[EvalCase]) -> list[RunResult]:
    """逐个打印 case，等用户标记 pass/fail/partial。Returns RunResult per case."""
    results: list[RunResult] = []

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
            letter = ans[0].lower()
            if letter not in _LETTER_TO_STATUS:
                print("无效输入。p=pass / f=fail / x=partial / s=skip")
                continue
            notes = ans[1:].strip() if len(ans) > 1 else ""
            results.append(
                RunResult(
                    case_id=c.id,
                    title=c.title,
                    module_expected=c.module_expected,
                    priority=c.priority,
                    input_lang=c.input_lang,
                    status=_LETTER_TO_STATUS[letter],
                    note=notes,
                    prompt=c.input_text,
                )
            )
            break

    _summary(results)
    return results


def run_auto(cases: list[EvalCase], llm_command: str) -> list[RunResult]:
    """用 headless CLI 跑 cases，做字面 pattern 检查。Returns RunResult per case."""
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

    results: list[RunResult] = []

    print(f"\n=== Auto eval 模式 / Auto mode ===\n")
    print(f"用 `{' '.join(command)} --print` headless 跑 {len(cases)} 个 case。")
    print(f"⚠️  注意：auto 模式只能做字面 pattern 匹配，不能判断输出质量。")
    print(f"   建议: P0 case 仍然手动 review。\n")

    for i, c in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {c.id} — {c.title} ... ", end="", flush=True)
        results.append(_run_one_case(command, c))
        print(_format_outcome_tail(results[-1]))

    _summary(results)
    return results


def _run_one_case(command: list[str], c: EvalCase) -> RunResult:
    """Drive a single case through the LLM CLI and classify the verdict."""
    base = RunResult(
        case_id=c.id,
        title=c.title,
        module_expected=c.module_expected,
        priority=c.priority,
        input_lang=c.input_lang,
        status=STATUS_FAIL,
        prompt=c.input_text,
    )

    started = time.monotonic()
    try:
        proc = subprocess.run(
            [*command, "--print", c.input_text],
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        base.status = STATUS_ERROR
        base.note = "timeout"
        base.duration_ms = int((time.monotonic() - started) * 1000)
        return base
    except Exception as e:
        base.status = STATUS_ERROR
        base.note = f"runner error: {e}"
        base.duration_ms = int((time.monotonic() - started) * 1000)
        return base

    base.duration_ms = int((time.monotonic() - started) * 1000)
    base.exit_code = proc.returncode
    base.stdout = _truncate(proc.stdout, MAX_OUTPUT_BYTES)
    base.stderr = _truncate(proc.stderr, MAX_OUTPUT_BYTES)

    if proc.returncode != 0:
        stderr_lines = proc.stderr.strip().splitlines()
        detail = stderr_lines[-1] if stderr_lines else f"exit code {proc.returncode}"
        base.status = STATUS_ERROR
        base.note = f"runner failed: {detail}"
        return base

    output_lower = proc.stdout.lower()
    base.missing_keywords = _check_keywords(output_lower, c.must_appear, present=True)
    base.forbidden_hits = _check_keywords(output_lower, c.must_not_appear, present=False)

    if not base.missing_keywords and not base.forbidden_hits:
        base.status = STATUS_PASS
    elif base.missing_keywords and not base.forbidden_hits:
        base.status = STATUS_PARTIAL
        base.note = f"missed: {base.missing_keywords[:2]}"
    else:
        base.status = STATUS_FAIL
        base.note = f"forbidden: {base.forbidden_hits[:2]}"
    return base


def _truncate(text: str, max_bytes: int) -> str:
    """Cap text at max_bytes, with a marker if truncated."""
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    truncated = encoded[:max_bytes].decode("utf-8", errors="ignore")
    return truncated + f"\n…[truncated, original {len(encoded)} bytes]"


def _format_outcome_tail(r: RunResult) -> str:
    if r.status == STATUS_PASS:
        return "PASS"
    if r.status == STATUS_PARTIAL:
        return f"PARTIAL ({len(r.missing_keywords)} expected patterns missing)"
    if r.status == STATUS_ERROR:
        if "timeout" in r.note:
            return "TIMEOUT"
        return f"ERROR ({r.note})"
    return f"FAIL (forbidden patterns appeared: {len(r.forbidden_hits)})"


# Negation cues — if a forbidden term appears within NEGATION_WINDOW chars
# AFTER any of these, the model is warning against the term rather than
# prescribing it, and we must NOT count the occurrence as a forbidden hit.
# Patterns are matched case-insensitive, lower-case input expected.
NEGATION_WINDOW = 40
NEGATION_PATTERNS = (
    # Chinese — no word boundaries; CJK has none
    r"不要|不能|不该|不应|不会|没必要|别|切勿|避免|拒绝|禁止|从不|绝不|从未",
    # English ("no" alone is too noisy — accept "no <noun>" via the explicit forms below)
    r"\bdon'?t\b|\bdo not\b|\bdoes not\b|\bdid not\b"
    r"|\bshouldn'?t\b|\bshould not\b|\bcan'?t\b|\bcannot\b|\bwon'?t\b"
    r"|\bnever\b|\bno longer\b|\bavoid\w*\b|\brefus\w*\b|\bdeclin\w*\b|\bnot\b",
    # Spanish — verb stems + flexible ending capture imperative / subjunctive
    r"\bno\b|\bnunca\b|\bjamás\b|\bevit\w*\b|\brechaz\w*\b|\bsin\b",
    # French
    r"\bne\s+(?:pas|jamais|plus|rien)\b|\bjamais\b|\bsans\b"
    r"|\bévit\w*\b|\brefus\w*\b",
    # Portuguese
    r"\bnão\b|\bnunca\b|\bjamais\b|\bevit\w*\b|\brecus\w*\b|\bsem\b",
    # German
    r"\bnicht\b|\bnie\b|\bniemals\b|\bkein\w*\b"
    r"|\bvermeid\w*\b|\blehn\w*\s+\w*\s*ab\b",
)


def _occurrence_negated(output_lower: str, idx: int) -> bool:
    """Return True if any negation cue appears within NEGATION_WINDOW chars
    immediately before position `idx`.
    """
    start = max(0, idx - NEGATION_WINDOW)
    preceding = output_lower[start:idx]
    return any(re.search(pat, preceding, re.IGNORECASE) for pat in NEGATION_PATTERNS)


def _term_un_negated(output_lower: str, term: str) -> bool:
    """Return True if `term` appears at least once in `output_lower` WITHOUT
    a negation cue in the preceding NEGATION_WINDOW. Used for forbidden checks
    so that the matcher distinguishes "do X" from "don't do X" / "no X" / "ne pas X".
    """
    pos = 0
    while True:
        idx = output_lower.find(term, pos)
        if idx == -1:
            return False
        if not _occurrence_negated(output_lower, idx):
            return True
        pos = idx + len(term)


def _check_keywords(output: str, expectations: list[str], present: bool) -> list[str]:
    """对每个 expectation 做粗略关键词检测。

    present=True: 应该出现的——返回**没有**出现的
    present=False: 不应该出现的——返回**真的出现了**的（即否定上下文不计）

    粗略提取：优先使用引号、反引号、slash alternatives 里的具体短语。
    避免用 "识别"、"至少" 这类说明词误判为命中。

    Forbidden-check semantics: a term counts as a forbidden hit only if at least
    one occurrence has NO negation cue (不要 / don't / no / ne pas / não / nicht …)
    in the 40 chars immediately preceding it. This kills the "model warns against
    X" → "X is in the warning text" → false-positive cycle.
    """
    output_lower = output.lower()
    misses_or_hits = []
    for exp in expectations:
        terms = _candidate_terms(exp, present=present)
        if not terms:
            continue
        if present:
            any_present = any(t.lower() in output_lower for t in terms)
            if not any_present:
                misses_or_hits.append(exp[:60])
        else:
            any_un_negated = any(
                _term_un_negated(output_lower, t.lower()) for t in terms
            )
            if any_un_negated:
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


def _summary(results: list[RunResult]) -> None:
    print(f"\n\n{'=' * 70}")
    print(f"=== 结果总结 / Summary ===")
    print(f"{'=' * 70}\n")

    counts = {STATUS_PASS: 0, STATUS_FAIL: 0, STATUS_PARTIAL: 0, STATUS_SKIP: 0, STATUS_ERROR: 0}
    p0_fails: list[RunResult] = []
    for r in results:
        # Errors are surfaced as fails in the headline counts (kept separate field for diff tools)
        bucket = r.status if r.status in counts else STATUS_FAIL
        counts[bucket] += 1
        if r.status in {STATUS_FAIL, STATUS_ERROR} and r.priority == "P0":
            p0_fails.append(r)

    total = len(results)
    fail_total = counts[STATUS_FAIL] + counts[STATUS_ERROR]
    print(f"Pass:    {counts[STATUS_PASS]:3d} / {total}")
    print(f"Fail:    {fail_total:3d} / {total}")
    print(f"Partial: {counts[STATUS_PARTIAL]:3d} / {total}")
    print(f"Skip:    {counts[STATUS_SKIP]:3d} / {total}")

    if p0_fails:
        print(f"\n⚠️  {len(p0_fails)} 个 P0 case 失败 — 不要发版！")
        for r in p0_fails:
            print(f"   - {r.case_id}: {r.title}")

    print()
    troubled = [r for r in results if r.status in {STATUS_FAIL, STATUS_PARTIAL, STATUS_ERROR}]
    if troubled:
        print("详细 / Details:")
        marks = {STATUS_FAIL: "✗", STATUS_PARTIAL: "△", STATUS_ERROR: "✗"}
        for r in troubled:
            print(f"  {marks.get(r.status, '?')} {r.case_id} — {r.title}")
            if r.note:
                print(f"     {r.note}")


def _read_skill_version(skill_file: Path = SKILL_FILE) -> Optional[str]:
    if not skill_file.exists():
        return None
    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return None
    for line in match.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            if k.strip() == "version":
                return v.strip().strip('"').strip("'")
    return None


def _read_git_commit(repo_root: Path = REPO_ROOT) -> Optional[str]:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return out.stdout.strip() or None


def write_recording(
    results: list[RunResult],
    path: Path,
    *,
    llm_command: str,
    started_at: datetime,
    ended_at: datetime,
    extra_meta: Optional[dict] = None,
) -> Path:
    """Write a recording JSON. Schema documented at evals/runs/README.md."""
    recording = {
        "schema_version": RECORDING_SCHEMA_VERSION,
        "meta": {
            "started_at": started_at.isoformat(timespec="seconds"),
            "ended_at": ended_at.isoformat(timespec="seconds"),
            "llm_command": llm_command,
            "skill_version": _read_skill_version(),
            "skill_commit": _read_git_commit(),
            "case_count": len(results),
            **(extra_meta or {}),
        },
        "results": [_result_to_dict(r) for r in results],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(recording, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _result_to_dict(r: RunResult) -> dict:
    """Stable JSON shape for recordings — keep keys snake_case + lower-case for diff stability."""
    d = asdict(r)
    # Drop derived/internal fields that aren't part of the recording schema
    return {k: v for k, v in d.items() if not k.startswith("_")}


def main() -> int:
    ap = argparse.ArgumentParser(description="laborer-companion eval runner")
    ap.add_argument("--filter", help="regex on filename to filter cases")
    ap.add_argument("--auto", action="store_true", help="use a headless LLM CLI in --print mode")
    ap.add_argument(
        "--llm-command",
        default=os.environ.get("EVAL_LLM_COMMAND", "claude"),
        help="headless LLM command to run before --print (default: env EVAL_LLM_COMMAND or claude)",
    )
    ap.add_argument(
        "--record",
        metavar="PATH",
        help=(
            "write a recording JSON for cross-model comparison. "
            "Implies --auto. Path must end in .json. "
            "Example: --record evals/runs/RESULTS-2026-04-30-claude-4-7.json"
        ),
    )
    args = ap.parse_args()

    if args.record and not args.auto:
        # Convenience: --record implies --auto since manual mode has no captured output
        args.auto = True

    if args.record:
        record_path = Path(args.record)
        if record_path.suffix != ".json":
            print("ERROR: --record path must end in .json", file=sys.stderr)
            return 2

    if not args.auto and not sys.stdin.isatty():
        print(
            "ERROR: manual mode requires an interactive terminal. "
            "Run with --auto or execute this script in a real terminal.",
            file=sys.stderr,
        )
        return 2

    cases = load_cases(args.filter)
    if not cases:
        print("没有找到 case 文件。No case files found.", file=sys.stderr)
        return 1

    print(f"Loaded {len(cases)} case(s).")
    started_at = datetime.now(timezone.utc)
    if args.auto:
        results = run_auto(cases, args.llm_command)
    else:
        results = run_manual(cases)
    ended_at = datetime.now(timezone.utc)

    if args.record:
        path = write_recording(
            results,
            Path(args.record),
            llm_command=args.llm_command,
            started_at=started_at,
            ended_at=ended_at,
        )
        print(f"\nRecorded {len(results)} result(s) to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
