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
    validate_agent_support_files,
    validate_command_files,
    validate_labor_law_dates,
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
    """Build a minimal skill dir under tmp_path and return SKILL.md path.

    If `skill_body` does not start with frontmatter, a valid stub frontmatter
    is prepended so the SKILL_MISSING_FIELD / SKILL_BAD_VERSION checks pass —
    callers that want to test those errors should pass their own frontmatter.
    """
    skill_dir = tmp_path / "skills" / "laborer-companion"
    (skill_dir / "commands").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    if not skill_body.lstrip().startswith("---"):
        skill_body = (
            "---\nname: stub\nversion: 0.1.0\ndescription: stub\n---\n" + skill_body
        )
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

    def test_skill_missing_version_field(self, tmp_path: Path, monkeypatch):
        # SKILL.md without `version:` — must error
        skill = _make_skill(
            tmp_path,
            dedent(
                """\
                ---
                name: x
                description: y
                ---
                body
                """
            ),
            files=[],
        )
        monkeypatch.setattr("validate_structure.SKILL_DIR", skill.parent)
        codes = [i.code for i in validate_skill_references(skill)]
        assert "SKILL_MISSING_FIELD" in codes

    def test_skill_bad_version_format(self, tmp_path: Path, monkeypatch):
        skill = _make_skill(
            tmp_path,
            dedent(
                """\
                ---
                name: x
                version: not-semver
                description: y
                ---
                body
                """
            ),
            files=[],
        )
        monkeypatch.setattr("validate_structure.SKILL_DIR", skill.parent)
        codes = [i.code for i in validate_skill_references(skill)]
        assert "SKILL_BAD_VERSION" in codes

    @pytest.mark.parametrize("version", ["0.1.0", "1.0.0", "1.2.3-rc1", "10.20.30+build.5"])
    def test_skill_accepts_semver(self, tmp_path: Path, monkeypatch, version: str):
        skill = _make_skill(
            tmp_path,
            f"---\nname: x\nversion: {version}\ndescription: y\n---\nbody\n",
            files=[],
        )
        monkeypatch.setattr("validate_structure.SKILL_DIR", skill.parent)
        codes = [i.code for i in validate_skill_references(skill)]
        assert "SKILL_BAD_VERSION" not in codes


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

    def test_bad_input_lang(self, tmp_path: Path):
        path = tmp_path / "case.md"
        # `ge` is a common typo for German (`de`) — must be flagged
        path.write_text(
            _case_text().replace("input_lang: zh", "input_lang: ge"),
            encoding="utf-8",
        )
        codes = [i.code for i in validate_case_file(path)]
        assert "CASE_BAD_LANG" in codes

    @pytest.mark.parametrize("lang", ["zh", "zh-Hans", "zh-Hant", "en", "es", "fr", "pt", "de", "mixed", "other"])
    def test_supported_input_langs_accepted(self, tmp_path: Path, lang: str):
        path = tmp_path / "case.md"
        path.write_text(
            _case_text().replace("input_lang: zh", f"input_lang: {lang}"),
            encoding="utf-8",
        )
        codes = [i.code for i in validate_case_file(path)]
        assert "CASE_BAD_LANG" not in codes

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
# validate_agent_support_files
# ---------------------------------------------------------------------------


class TestValidateAgentSupportFiles:
    def test_clean_agent_support_files(self, tmp_path: Path):
        agents = tmp_path / "AGENTS.md"
        cursor = tmp_path / ".cursor" / "rules" / "laborer-companion.mdc"
        cursor.parent.mkdir(parents=True)

        agents.write_text(
            dedent(
                """\
                # Agent instructions

                Use skills/laborer-companion/SKILL.md.
                Read references/labor-law-quick-reference.md.
                Read references/acute-crisis-escalation.md.
                Hong Kong and Taiwan are regions/jurisdictions.
                """
            ),
            encoding="utf-8",
        )
        cursor.write_text(
            dedent(
                """\
                ---
                description: use the laborer skill
                alwaysApply: false
                ---

                Use @skills/laborer-companion/SKILL.md.
                Read skills/laborer-companion/references/labor-law-quick-reference.md.
                Read skills/laborer-companion/references/acute-crisis-escalation.md.
                Hong Kong and Taiwan are regions/jurisdictions.
                """
            ),
            encoding="utf-8",
        )

        assert validate_agent_support_files(agents, cursor) == []

    def test_missing_agent_support_files_are_errors(self, tmp_path: Path):
        issues = validate_agent_support_files(
            tmp_path / "AGENTS.md",
            tmp_path / ".cursor" / "rules" / "laborer-companion.mdc",
        )
        codes = {i.code for i in issues}
        assert "AGENTS_MISSING" in codes
        assert "CURSOR_RULE_MISSING" in codes

    def test_cursor_rule_frontmatter_required(self, tmp_path: Path):
        agents = tmp_path / "AGENTS.md"
        cursor = tmp_path / ".cursor" / "rules" / "laborer-companion.mdc"
        cursor.parent.mkdir(parents=True)
        agents.write_text(
            "skills/laborer-companion/SKILL.md\n"
            "references/labor-law-quick-reference.md\n"
            "references/acute-crisis-escalation.md\n"
            "Hong Kong and Taiwan\n",
            encoding="utf-8",
        )
        cursor.write_text("@skills/laborer-companion/SKILL.md\n", encoding="utf-8")

        codes = {i.code for i in validate_agent_support_files(agents, cursor)}
        assert "CURSOR_RULE_NO_FRONTMATTER" in codes
        assert "CURSOR_RULE_MISSING_FIELD" in codes


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


# ---------------------------------------------------------------------------
# Labor-law verification date enforcement
# ---------------------------------------------------------------------------


class TestValidateLaborLawDates:
    def test_clean_when_all_files_have_date(self, tmp_path: Path):
        refs = tmp_path / "references"
        refs.mkdir()
        for jur in ("foo", "bar"):
            (refs / f"labor-law-{jur}.md").write_text(
                "# Labor law\n\n> **Last verified**: 2026-04-29\n",
                encoding="utf-8",
            )
        assert validate_labor_law_dates(refs) == []

    def test_missing_date_is_error(self, tmp_path: Path):
        refs = tmp_path / "references"
        refs.mkdir()
        (refs / "labor-law-foo.md").write_text("# Labor law\n\nno date here\n", encoding="utf-8")
        issues = validate_labor_law_dates(refs)
        assert any(i.code == "LABOR_LAW_NO_VERIFICATION_DATE" for i in issues)

    def test_case_insensitive_date_match(self, tmp_path: Path):
        refs = tmp_path / "references"
        refs.mkdir()
        # `Index last verified` (lowercase 'last') should still satisfy the check
        (refs / "labor-law-foo.md").write_text(
            "# Labor law\n\n> Index last verified: 2026-04-29\n",
            encoding="utf-8",
        )
        assert validate_labor_law_dates(refs) == []

    def test_no_files_in_corpus_is_error(self, tmp_path: Path):
        refs = tmp_path / "references"
        refs.mkdir()
        # no labor-law-*.md files at all
        codes = [i.code for i in validate_labor_law_dates(refs)]
        assert "LABOR_LAW_NO_FILES" in codes

    def test_real_corpus_clean(self):
        """Smoke test against the real labor-law/* files."""
        issues = validate_labor_law_dates()
        date_errors = [i for i in issues if i.code == "LABOR_LAW_NO_VERIFICATION_DATE"]
        assert date_errors == [], (
            "Real labor-law files missing `Last verified`:\n"
            + "\n".join(i.format() for i in date_errors)
        )


# ---------------------------------------------------------------------------
# Multilingual README consistency
# ---------------------------------------------------------------------------


class TestMultilingualReadmes:
    """Make sure every language README exists, mutually links, and has a switcher
    line as the second non-empty line. Catches contributors who add a translation
    but forget to update the switcher in the others."""

    EXPECTED = {
        "README.md": "简体中文",
        "README.en.md": "English",
        "README.zh-TW.md": "繁體中文",
        "README.es.md": "Español",
        "README.fr.md": "Français",
        "README.pt.md": "Português",
        "README.de.md": "Deutsch",
    }

    def _switcher_line(self, path: Path) -> str:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "README." in line or "[简体中文]" in line:
                return line
        return ""

    def test_all_readmes_exist(self, repo_root: Path):
        for filename in self.EXPECTED:
            assert (repo_root / filename).exists(), f"missing {filename}"

    def test_each_readme_links_to_every_other(self, repo_root: Path):
        for filename, current_label in self.EXPECTED.items():
            path = repo_root / filename
            switcher = self._switcher_line(path)
            assert switcher, f"{filename} has no language switcher line"
            for other_filename in self.EXPECTED:
                if other_filename == filename:
                    # current language must be marked (bold), not linked
                    assert (
                        f"**{current_label}**" in switcher
                    ), f"{filename} should mark its own language `{current_label}` as bold"
                else:
                    assert (
                        f"({other_filename})" in switcher
                    ), f"{filename} switcher missing link to {other_filename}"

    def test_each_readme_has_distinct_current_marker(self, repo_root: Path):
        # the bold (`**…**`) marker should appear exactly once per switcher
        for filename in self.EXPECTED:
            switcher = self._switcher_line(repo_root / filename)
            bold_count = switcher.count("**") // 2
            assert bold_count == 1, (
                f"{filename} switcher should bold exactly one language, got {bold_count}"
            )
