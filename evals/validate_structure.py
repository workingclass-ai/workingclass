#!/usr/bin/env python3
"""Structural validator for the workingclass repo.

Checks that:
  - every reference path mentioned in SKILL.md actually exists
  - every command file referenced from commands/ has the expected frontmatter
  - every eval case has the required frontmatter fields and required sections

Usage:
    python evals/validate_structure.py             # exit 1 on any error-level issue
    python evals/validate_structure.py --strict    # exit 1 on warnings too

Designed to be import-safe so tests can call validate_repo() and inspect issues.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "laborer-companion"
COMMANDS_DIR = SKILL_DIR / "commands"
REFERENCES_DIR = SKILL_DIR / "references"
SKILL_FILE = SKILL_DIR / "SKILL.md"
CASES_DIR = REPO_ROOT / "evals" / "cases"

REQUIRED_CASE_FIELDS = ("id", "title", "module_expected", "priority", "input_lang")
REQUIRED_CASE_SECTIONS = ("输入", "必须出现")
ALLOWED_PRIORITIES = {"P0", "P1", "P2"}
COMMAND_REQUIRED_FRONTMATTER = ("description",)


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Issue:
    severity: Severity
    code: str
    path: Path
    message: str

    def format(self, root: Path = REPO_ROOT) -> str:
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        return f"[{self.severity.value.upper()}] {self.code} {rel}: {self.message}"


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Return frontmatter dict from a markdown text. Empty dict if none."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    out: dict[str, str] = {}
    for line in match.group(1).strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def _section_headers(text: str) -> set[str]:
    """Return the set of `## ` section headers in a markdown body, normalised."""
    headers = set()
    for line in text.splitlines():
        if line.startswith("## "):
            # `## 输入 / Input` -> "输入"
            head = line[3:].split("/")[0].strip()
            headers.add(head)
    return headers


# ---------------------------------------------------------------------------
# Reference checking — find paths mentioned in SKILL.md and verify they exist
# ---------------------------------------------------------------------------


_REF_PATH_RE = re.compile(r"`((?:commands|references)/[A-Za-z0-9_\-*]+\.md)`")


def collect_referenced_paths(skill_text: str) -> set[str]:
    """Pull every `commands/...md` or `references/...md` mention out of SKILL.md."""
    return set(_REF_PATH_RE.findall(skill_text))


def validate_skill_references(skill_file: Path = SKILL_FILE) -> list[Issue]:
    issues: list[Issue] = []
    if not skill_file.exists():
        return [
            Issue(
                Severity.ERROR,
                "SKILL_MISSING",
                skill_file,
                "SKILL.md is missing",
            )
        ]

    text = skill_file.read_text(encoding="utf-8")
    refs = collect_referenced_paths(text)
    for ref in sorted(refs):
        # wildcard form: `references/labor-law-*.md` should expand to >=1 match
        if "*" in ref:
            pattern = ref.replace("*", "[A-Za-z0-9_\\-]+")
            matches = [
                p
                for p in (SKILL_DIR / Path(ref).parent).glob("*.md")
                if re.fullmatch(pattern, str(p.relative_to(SKILL_DIR)).replace("\\", "/"))
            ]
            if not matches:
                issues.append(
                    Issue(
                        Severity.ERROR,
                        "REF_WILDCARD_NO_MATCH",
                        skill_file,
                        f"reference glob `{ref}` matches no files",
                    )
                )
            continue

        target = SKILL_DIR / ref
        if not target.exists():
            try:
                shown = target.relative_to(REPO_ROOT)
            except ValueError:
                shown = target
            issues.append(
                Issue(
                    Severity.ERROR,
                    "REF_MISSING",
                    skill_file,
                    f"reference `{ref}` does not exist at {shown}",
                )
            )
    return issues


# ---------------------------------------------------------------------------
# Command file validation — frontmatter must declare a description
# ---------------------------------------------------------------------------


def validate_command_files(commands_dir: Path = COMMANDS_DIR) -> list[Issue]:
    issues: list[Issue] = []
    if not commands_dir.is_dir():
        return [
            Issue(
                Severity.ERROR,
                "COMMANDS_DIR_MISSING",
                commands_dir,
                "commands/ directory is missing",
            )
        ]

    for path in sorted(commands_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm:
            issues.append(
                Issue(
                    Severity.ERROR,
                    "CMD_NO_FRONTMATTER",
                    path,
                    "command file has no YAML frontmatter",
                )
            )
            continue
        for field in COMMAND_REQUIRED_FRONTMATTER:
            if field not in fm or not fm[field].strip():
                issues.append(
                    Issue(
                        Severity.ERROR,
                        "CMD_MISSING_FIELD",
                        path,
                        f"frontmatter missing required field `{field}`",
                    )
                )
        # WARNING: no allowed-tools declared — convention not contract
        if "allowed-tools" not in fm:
            issues.append(
                Issue(
                    Severity.WARNING,
                    "CMD_NO_ALLOWED_TOOLS",
                    path,
                    "frontmatter has no `allowed-tools` field",
                )
            )
    return issues


# ---------------------------------------------------------------------------
# Eval case validation
# ---------------------------------------------------------------------------


def validate_case_file(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if not fm:
        return [
            Issue(
                Severity.ERROR,
                "CASE_NO_FRONTMATTER",
                path,
                "eval case has no YAML frontmatter",
            )
        ]

    for field in REQUIRED_CASE_FIELDS:
        if field not in fm or not str(fm[field]).strip():
            issues.append(
                Issue(
                    Severity.ERROR,
                    "CASE_MISSING_FIELD",
                    path,
                    f"frontmatter missing required field `{field}`",
                )
            )

    priority = fm.get("priority", "").strip()
    if priority and priority not in ALLOWED_PRIORITIES:
        issues.append(
            Issue(
                Severity.ERROR,
                "CASE_BAD_PRIORITY",
                path,
                f"priority `{priority}` not in {sorted(ALLOWED_PRIORITIES)}",
            )
        )

    fm_match = _FRONTMATTER_RE.match(text)
    body = text[fm_match.end():] if fm_match else text
    headers = _section_headers(body)
    for required in REQUIRED_CASE_SECTIONS:
        if required not in headers:
            issues.append(
                Issue(
                    Severity.ERROR,
                    "CASE_MISSING_SECTION",
                    path,
                    f"missing required section `## {required}`",
                )
            )

    # WARNING: cases without a "必须不出现" list lose half the auto-mode signal —
    # but it is not a hard contract because some positive-only cases are valid.
    if "必须不出现" not in headers:
        issues.append(
            Issue(
                Severity.WARNING,
                "CASE_NO_MUST_NOT",
                path,
                "no `## 必须不出现` section — auto mode can only check positive patterns",
            )
        )

    return issues


def validate_cases(cases_dir: Path = CASES_DIR) -> list[Issue]:
    if not cases_dir.is_dir():
        return [
            Issue(
                Severity.ERROR,
                "CASES_DIR_MISSING",
                cases_dir,
                "evals/cases/ directory is missing",
            )
        ]

    issues: list[Issue] = []
    seen_ids: dict[str, Path] = {}
    for path in sorted(cases_dir.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        case_issues = validate_case_file(path)
        issues.extend(case_issues)

        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        case_id = fm.get("id", "").strip()
        if case_id:
            if case_id in seen_ids:
                issues.append(
                    Issue(
                        Severity.ERROR,
                        "CASE_DUPLICATE_ID",
                        path,
                        f"duplicate id `{case_id}` (also used by {seen_ids[case_id].name})",
                    )
                )
            else:
                seen_ids[case_id] = path

    return issues


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------


def validate_repo() -> list[Issue]:
    return [
        *validate_skill_references(),
        *validate_command_files(),
        *validate_cases(),
    ]


def _filter(issues: Iterable[Issue], severity: Severity) -> list[Issue]:
    return [i for i in issues if i.severity is severity]


def main() -> int:
    parser = argparse.ArgumentParser(description="validate workingclass repo structure")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as errors when computing exit code",
    )
    args = parser.parse_args()

    issues = validate_repo()
    errors = _filter(issues, Severity.ERROR)
    warnings = _filter(issues, Severity.WARNING)

    for issue in issues:
        print(issue.format())

    print()
    print(f"errors:   {len(errors)}")
    print(f"warnings: {len(warnings)}")

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
