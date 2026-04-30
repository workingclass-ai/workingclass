#!/usr/bin/env python3
"""Compare two recording JSONs produced by run_evals.py --record.

Usage:
    python evals/eval_diff.py BASELINE.json CURRENT.json
    python evals/eval_diff.py BASELINE.json CURRENT.json --show-output
    python evals/eval_diff.py BASELINE.json CURRENT.json --quiet  # exit code only

Exit codes:
    0  no verdict regressions (no pass→fail/partial, no partial→fail)
    1  one or more verdicts regressed
    2  schema mismatch / file error

Verdicts compared:
    pass > partial > fail/error  (higher = better)

A "regression" = a case whose verdict went from a higher tier to a lower one.
A "fix" = the opposite. New cases (in CURRENT only) and removed cases (in BASELINE only) are listed but do not count as regressions.

Output text differs case-by-case is non-deterministic for non-deterministic
LLMs, so by default this tool only compares the verdict layer. Pass
--show-output to also dump a unified diff of stdout for cases whose verdict
changed (use this when you've already identified a flip and want to see why).
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Verdict ranking — higher number = better outcome.
VERDICT_RANK = {
    "pass": 3,
    "partial": 2,
    "fail": 1,
    "error": 0,
    "skip": -1,  # skipped cases don't trigger regression detection
}


@dataclass(frozen=True)
class Recording:
    schema_version: int
    meta: dict
    results: list[dict]
    path: Path


def load_recording(path: Path) -> Recording:
    if not path.exists():
        print(f"ERROR: {path} does not exist", file=sys.stderr)
        sys.exit(2)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: {path} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    if "schema_version" not in data:
        print(f"ERROR: {path} has no schema_version field", file=sys.stderr)
        sys.exit(2)
    return Recording(
        schema_version=data["schema_version"],
        meta=data.get("meta", {}),
        results=data.get("results", []),
        path=path,
    )


def _by_id(results: list[dict]) -> dict[str, dict]:
    return {r["case_id"]: r for r in results}


@dataclass(frozen=True)
class CaseChange:
    case_id: str
    title: str
    priority: str
    baseline_status: Optional[str]
    current_status: Optional[str]

    @property
    def kind(self) -> str:
        if self.baseline_status is None:
            return "new"
        if self.current_status is None:
            return "removed"
        b = VERDICT_RANK.get(self.baseline_status, 0)
        c = VERDICT_RANK.get(self.current_status, 0)
        if c < b:
            return "regression"
        if c > b:
            return "fix"
        return "unchanged"


def diff(baseline: Recording, current: Recording) -> list[CaseChange]:
    if baseline.schema_version != current.schema_version:
        print(
            f"ERROR: schema mismatch — baseline v{baseline.schema_version}, "
            f"current v{current.schema_version}",
            file=sys.stderr,
        )
        sys.exit(2)

    b_by = _by_id(baseline.results)
    c_by = _by_id(current.results)
    all_ids = sorted(set(b_by) | set(c_by), key=lambda s: (len(s), s))

    changes: list[CaseChange] = []
    for cid in all_ids:
        b = b_by.get(cid)
        c = c_by.get(cid)
        title = (c or b or {}).get("title", "")
        priority = (c or b or {}).get("priority", "?")
        changes.append(
            CaseChange(
                case_id=cid,
                title=title,
                priority=priority,
                baseline_status=b["status"] if b else None,
                current_status=c["status"] if c else None,
            )
        )
    return changes


def render(
    changes: list[CaseChange],
    baseline: Recording,
    current: Recording,
    *,
    show_output: bool = False,
) -> str:
    lines: list[str] = []
    lines.append(f"baseline: {baseline.path.name}  ({baseline.meta.get('skill_version', '?')} @ {baseline.meta.get('skill_commit', '?')})")
    lines.append(f"current:  {current.path.name}  ({current.meta.get('skill_version', '?')} @ {current.meta.get('skill_commit', '?')})")
    lines.append("")

    regressions = [c for c in changes if c.kind == "regression"]
    fixes = [c for c in changes if c.kind == "fix"]
    new = [c for c in changes if c.kind == "new"]
    removed = [c for c in changes if c.kind == "removed"]
    unchanged = [c for c in changes if c.kind == "unchanged"]

    lines.append(f"Regressions: {len(regressions):3d}   Fixes: {len(fixes):3d}   "
                 f"New: {len(new):3d}   Removed: {len(removed):3d}   Unchanged: {len(unchanged):3d}")
    lines.append("")

    if regressions:
        lines.append("✗ Regressions (verdict got worse):")
        for c in regressions:
            tag = "P0!" if c.priority == "P0" else c.priority
            lines.append(
                f"  {tag:<3} {c.case_id:<3} {c.baseline_status:>7} → {c.current_status:<7}  {c.title}"
            )
        lines.append("")

    if fixes:
        lines.append("✓ Fixes (verdict got better):")
        for c in fixes:
            lines.append(
                f"      {c.case_id:<3} {c.baseline_status:>7} → {c.current_status:<7}  {c.title}"
            )
        lines.append("")

    if new:
        lines.append("+ New cases (in current only):")
        for c in new:
            lines.append(f"      {c.case_id:<3} {c.current_status:<7}  {c.title}")
        lines.append("")

    if removed:
        lines.append("- Removed cases (in baseline only):")
        for c in removed:
            lines.append(f"      {c.case_id:<3} {c.baseline_status:<7}  {c.title}")
        lines.append("")

    if show_output:
        b_by = _by_id(baseline.results)
        c_by = _by_id(current.results)
        flipped = [c for c in changes if c.kind in {"regression", "fix"}]
        for c in flipped:
            lines.append("─" * 70)
            lines.append(f"### {c.case_id} — {c.title}  ({c.baseline_status} → {c.current_status})")
            lines.append("")
            b_out = b_by.get(c.case_id, {}).get("stdout", "")
            c_out = c_by.get(c.case_id, {}).get("stdout", "")
            udiff = difflib.unified_diff(
                b_out.splitlines(keepends=False),
                c_out.splitlines(keepends=False),
                fromfile="baseline",
                tofile="current",
                n=2,
                lineterm="",
            )
            lines.extend(udiff)
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("baseline", type=Path, help="path to baseline RESULTS.json")
    ap.add_argument("current", type=Path, help="path to current RESULTS.json")
    ap.add_argument("--show-output", action="store_true",
                    help="dump a per-case stdout unified diff for cases whose verdict changed")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress the report; useful in CI when only exit code matters")
    args = ap.parse_args()

    baseline = load_recording(args.baseline)
    current = load_recording(args.current)
    changes = diff(baseline, current)

    if not args.quiet:
        print(render(changes, baseline, current, show_output=args.show_output))

    regressions = [c for c in changes if c.kind == "regression"]
    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
