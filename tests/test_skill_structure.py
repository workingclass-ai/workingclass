"""Structural validator tests.

Two layers:
  1. Unit tests against synthetic repos in tmp_path — exercises every issue code.
  2. Smoke tests against the real corpus — fails CI if a contributor checks in
     a broken skill / case / reference.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from validate_structure import (
    Severity,
    collect_referenced_paths,
    parse_frontmatter,
    validate_case_file,
    validate_cases,
    validate_command_files,
    validate_repo,
    validate_skill_references,
)

pytestmark = pytest.mark.structure


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------


class TestParseFrontmatter:
    def test_basic(self):
        text = "---\nfoo: bar\nbaz: qux\n---\nbody"
        assert parse_frontmatter(text) == {"foo": "bar", "baz": "qux"}

    def test_no_frontmatter_returns_empty(self):
        assert parse_frontmatter("just body text") == {}

    def test_empty_string(self):
        assert parse_frontmatter("") == {}

    def test_value_with_colon_preserved(self):
        text = "---\ntitle: hello: world: again\n---\n"
        assert parse_frontmatter(text)["title"] == "hello: world: again"

    def test_skips_lines_without_colon(self):
        text = "---\ngood: yes\nbadline\n---\n"
        assert parse_frontmatter(text) == {"good": "yes"}


# ---------------------------------------------------------------------------
# collect_referenced_paths
# ---------------------------------------------------------------------------


class TestCollectReferencedPaths:
    def test_finds_command_and_reference_paths(self):
        text = "see `commands/triage.md` and `references/red-flag-scanner.md`"
        assert collect_referenced_paths(text) == {
            "commands/triage.md",
            "references/red-flag-scanner.md",
        }

    def test_handles_wildcard_path(self):
        text = "see `references/labor-law-*.md`"
        assert "references/labor-law-*.md" in collect_referenced_paths(text)

    def test_ignores_non_skill_paths(self):
        text = "see `tests/foo.md` or `random.md`"
        assert collect_referenced_paths(text) == set()


# ---------------------------------------------------------------------------
# validate_skill_references — synthetic skill dir
# ---------------------------------------------------------------------------


def _make_skill(tmp_path: Path, skill_body: str, files: list[str] | None = None) -> Path:
    """Build a minimal skill dir under tmp_path and return SKILL.md path."""
    skill_dir = tmp_path / "skills" / "laborer-companion"
    (skill_dir / "commands").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_body, encoding="utf-8")
    for rel in files or []:
        path = skill_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\ndescription: stub\n---\nbody\n", encoding="utf-8")
    return skill_file


class TestValidateSkillReferences:
    def test_clean_repo_no_issues(self, tmp_path: Path, monkeypatch):
        skill = _make_skill(
            tmp_path,
            "see `commands/triage.md` and `references/foo.md`",
            files=["commands/triage.md", "references/foo.md"],
        )
        monkeypatch.setattr("validate_structure.SKILL_DIR", skill.parent)
        issues = validate_skill_references(skill)
        assert issues == []

    def test_missing_reference_is_error(self, tmp_path: Path, monkeypatch):
        skill = _make_skill(
            tmp_path,
            "see `references/missing.md`",
            files=[],
        )
        monkeypatch.setattr("validate_structure.SKILL_DIR", skill.parent)
        issues = validate_skill_references(skill)
        assert len(issues) == 1
        assert issues[0].severity is Severity.ERROR
        assert issues[0].code == "REF_MISSING"

    def test_wildcard_with_match_is_ok(self, tmp_path: Path, monkeypatch):
        skill = _make_skill(
            tmp_path,
            "see `references/labor-law-*.md`",
            files=["references/labor-law-australia.md"],
        )
        monkeypatch.setattr("validate_structure.SKILL_DIR", skill.parent)
        issues = validate_skill_references(skill)
        assert issues == []

    def test_wildcard_with_no_match_is_error(self, tmp_path: Path, monkeypatch):
        skill = _make_skill(
            tmp_path,
            "see `references/labor-law-*.md`",
            files=[],
        )
        monkeypatch.setattr("validate_structure.SKILL_DIR", skill.parent)
        issues = validate_skill_references(skill)
        assert len(issues) == 1
        assert issues[0].code == "REF_WILDCARD_NO_MATCH"

    def test_missing_skill_file(self, tmp_path: Path):
        nonexistent = tmp_path / "skills" / "ghost" / "SKILL.md"
        issues = validate_skill_references(nonexistent)
        assert issues and issues[0].code == "SKILL_MISSING"


# ---------------------------------------------------------------------------
# validate_command_files
# ---------------------------------------------------------------------------


def _write_cmd(commands_dir: Path, name: str, body: str) -> Path:
    commands_dir.mkdir(parents=True, exist_ok=True)
    p = commands_dir / name
    p.write_text(body, encoding="utf-8")
    return p


class TestValidateCommandFiles:
    def test_clean_command_no_issues(self, tmp_path: Path):
        cmds = tmp_path / "commands"
        _write_cmd(
            cmds,
            "triage.md",
            dedent(
                """\
                ---
                description: triage the user
                allowed-tools: Read
                ---

                body
                """
            ),
        )
        assert validate_command_files(cmds) == []

    def test_missing_frontmatter_is_error(self, tmp_path: Path):
        cmds = tmp_path / "commands"
        _write_cmd(cmds, "x.md", "no frontmatter here\n")
        issues = validate_command_files(cmds)
        codes = [i.code for i in issues]
        assert "CMD_NO_FRONTMATTER" in codes

    def test_missing_description_is_error(self, tmp_path: Path):
        cmds = tmp_path / "commands"
        _write_cmd(
            cmds,
            "x.md",
            dedent(
                """\
                ---
                allowed-tools: Read
                ---

                body
                """
            ),
        )
        issues = validate_command_files(cmds)
        codes = [i.code for i in issues]
        assert "CMD_MISSING_FIELD" in codes

    def test_missing_allowed_tools_is_warning(self, tmp_path: Path):
        cmds = tmp_path / "commands"
        _write_cmd(
            cmds,
            "x.md",
            dedent(
                """\
                ---
                description: hi
                ---

                body
                """
            ),
        )
        issues = validate_command_files(cmds)
        warns = [i for i in issues if i.severity is Severity.WARNING]
        assert any(i.code == "CMD_NO_ALLOWED_TOOLS" for i in warns)
        # and no errors
        assert all(i.severity is Severity.WARNING for i in issues)

    def test_missing_dir_is_error(self, tmp_path: Path):
        ghost = tmp_path / "ghost"
        issues = validate_command_files(ghost)
        assert issues and issues[0].code == "COMMANDS_DIR_MISSING"


# ---------------------------------------------------------------------------
# validate_case_file
# ---------------------------------------------------------------------------


def _case_text(
    *,
    fm_extra: str = "",
    sections: tuple[str, ...] = ("输入", "必须出现", "必须不出现"),
) -> str:
    fm = dedent(
        """\
        ---
        id: 99
        title: t
        module_expected: decode
        priority: P0
        input_lang: zh
        """
    ).rstrip()
    if fm_extra:
        fm += "\n" + fm_extra
    fm += "\n---\n\n"
    body_parts = []
    for sec in sections:
        body_parts.append(f"## {sec} / English\n\n- thing\n")
    return fm + "\n".join(body_parts)


class TestValidateCaseFile:
    def test_clean_case_no_errors(self, tmp_path: Path):
        path = tmp_path / "case.md"
        path.write_text(_case_text(), encoding="utf-8")
        issues = [i for i in validate_case_file(path) if i.severity is Severity.ERROR]
        assert issues == []

    def test_missing_required_field(self, tmp_path: Path):
        path = tmp_path / "case.md"
        path.write_text(
            dedent(
                """\
                ---
                id: 1
                title: x
                ---

                ## 输入

                - hi

                ## 必须出现

                - x
                """
            ),
            encoding="utf-8",
        )
        codes = [i.code for i in validate_case_file(path)]
        assert "CASE_MISSING_FIELD" in codes

    def test_bad_priority(self, tmp_path: Path):
        path = tmp_path / "case.md"
        path.write_text(
            _case_text().replace("priority: P0", "priority: P9"),
            encoding="utf-8",
        )
        codes = [i.code for i in validate_case_file(path)]
        assert "CASE_BAD_PRIORITY" in codes

    def test_missing_section(self, tmp_path: Path):
        path = tmp_path / "case.md"
        path.write_text(
            _case_text(sections=("输入",)),  # no 必须出现
            encoding="utf-8",
        )
        codes = [i.code for i in validate_case_file(path)]
        assert "CASE_MISSING_SECTION" in codes

    def test_no_must_not_section_is_warning(self, tmp_path: Path):
        path = tmp_path / "case.md"
        # has 输入 + 必须出现 but no 必须不出现
        path.write_text(_case_text(sections=("输入", "必须出现")), encoding="utf-8")
        issues = validate_case_file(path)
        warns = [i for i in issues if i.severity is Severity.WARNING]
        assert any(i.code == "CASE_NO_MUST_NOT" for i in warns)

    def test_no_frontmatter(self, tmp_path: Path):
        path = tmp_path / "case.md"
        path.write_text("just body\n", encoding="utf-8")
        codes = [i.code for i in validate_case_file(path)]
        assert "CASE_NO_FRONTMATTER" in codes


# ---------------------------------------------------------------------------
# validate_cases — duplicate detection
# ---------------------------------------------------------------------------


class TestValidateCases:
    def test_duplicate_id_is_error(self, tmp_path: Path):
        cases = tmp_path / "cases"
        cases.mkdir()
        for name in ("a.md", "b.md"):
            (cases / name).write_text(_case_text(), encoding="utf-8")
        issues = validate_cases(cases)
        codes = [i.code for i in issues]
        assert "CASE_DUPLICATE_ID" in codes

    def test_index_md_skipped(self, tmp_path: Path):
        cases = tmp_path / "cases"
        cases.mkdir()
        (cases / "INDEX.md").write_text("not a real case", encoding="utf-8")
        # only file is INDEX.md → no errors
        issues = [i for i in validate_cases(cases) if i.severity is Severity.ERROR]
        assert issues == []


# ---------------------------------------------------------------------------
# Smoke tests against the real corpus — these are the gate that protects main
# ---------------------------------------------------------------------------


class TestRealCorpus:
    def test_real_repo_has_no_errors(self):
        issues = validate_repo()
        errors = [i for i in issues if i.severity is Severity.ERROR]
        assert errors == [], "\n".join(i.format() for i in errors)

    def test_every_case_has_unique_id(self):
        from run_evals import load_cases

        ids = [c.id for c in load_cases()]
        assert len(ids) == len(set(ids)), f"duplicate case ids: {ids}"
