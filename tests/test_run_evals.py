"""Unit tests for evals/run_evals.py."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from run_evals import (
    EvalCase,
    _bullets,
    _candidate_terms,
    _check_keywords,
    _clean_candidate,
    _is_useful_candidate,
    load_cases,
    parse_case,
)


# ---------------------------------------------------------------------------
# parse_case
# ---------------------------------------------------------------------------


class TestParseCase:
    def test_extracts_frontmatter_fields(self, write_case):
        path = write_case(
            "case.md",
            dedent(
                """\
                ---
                id: 99
                title: Sample title
                module_expected: decode
                priority: P0
                input_lang: zh
                ---

                ## 输入 / Input

                ```
                hello
                ```

                ## 必须出现 / Must appear

                - foo
                """
            ),
        )

        case = parse_case(path)

        assert case.id == "99"
        assert case.title == "Sample title"
        assert case.module_expected == "decode"
        assert case.priority == "P0"
        assert case.input_lang == "zh"

    def test_strips_code_fence_from_input(self, write_case):
        path = write_case(
            "case.md",
            dedent(
                """\
                ---
                id: 1
                ---

                ## 输入 / Input

                ```
                line 1
                line 2
                ```

                ## 必须出现 / Must appear

                - alpha
                """
            ),
        )

        case = parse_case(path)
        assert case.input_text == "line 1\nline 2"

    def test_input_without_code_fence(self, write_case):
        path = write_case(
            "case.md",
            dedent(
                """\
                ---
                id: 1
                ---

                ## 输入 / Input

                bare text input

                ## 必须出现 / Must appear

                - x
                """
            ),
        )

        assert parse_case(path).input_text == "bare text input"

    def test_must_appear_and_must_not_appear_lists(self, write_case):
        path = write_case(
            "case.md",
            dedent(
                """\
                ---
                id: 1
                ---

                ## 输入 / Input

                ```
                hi
                ```

                ## 必须出现 / Must appear

                - first item
                - second item
                * star bullet

                ## 必须不出现 / Must NOT appear

                - bad thing
                """
            ),
        )

        case = parse_case(path)
        assert case.must_appear == ["first item", "second item", "star bullet"]
        assert case.must_not_appear == ["bad thing"]

    def test_notes_section_captured(self, write_case):
        path = write_case(
            "case.md",
            dedent(
                """\
                ---
                id: 1
                ---

                ## 输入 / Input

                ```
                x
                ```

                ## 必须出现 / Must appear

                - a

                ## Notes for reviewer

                Reviewer notes here.
                Multi-line.
                """
            ),
        )

        assert parse_case(path).notes == "Reviewer notes here.\nMulti-line."

    def test_defaults_when_frontmatter_absent(self, write_case):
        path = write_case(
            "case_no_fm.md",
            dedent(
                """\
                ## 输入 / Input

                ```
                hi
                ```

                ## 必须出现 / Must appear

                - x
                """
            ),
        )

        case = parse_case(path)
        # falls back to file stem
        assert case.id == "case_no_fm"
        assert case.title == "case_no_fm"
        assert case.module_expected == "?"
        assert case.priority == "P1"
        assert case.input_lang == "zh"

    def test_frontmatter_with_extra_colons(self, write_case):
        path = write_case(
            "case.md",
            dedent(
                """\
                ---
                id: 1
                title: foo: bar: baz
                ---

                ## 输入 / Input

                ```
                hi
                ```
                """
            ),
        )

        # split on first colon only — value preserves remaining colons
        assert parse_case(path).title == "foo: bar: baz"

    def test_empty_must_lists_when_section_missing(self, write_case):
        path = write_case(
            "case.md",
            dedent(
                """\
                ---
                id: 1
                ---

                ## 输入 / Input

                ```
                hi
                ```
                """
            ),
        )

        case = parse_case(path)
        assert case.must_appear == []
        assert case.must_not_appear == []
        assert case.notes == ""


# ---------------------------------------------------------------------------
# _bullets
# ---------------------------------------------------------------------------


class TestBullets:
    def test_recognises_dash_and_star(self):
        text = "- one\n* two\n  - three (leading ws is stripped)\nrandom line"
        # _bullets strips leading whitespace, so indented bullets are still picked up
        assert _bullets(text) == ["one", "two", "three (leading ws is stripped)"]

    def test_ignores_dash_without_space(self):
        # "- " requires the trailing space — "-foo" is not a bullet
        assert _bullets("-foo\n- bar") == ["bar"]

    def test_strips_whitespace(self):
        assert _bullets("- spaced   ") == ["spaced"]

    def test_empty_returns_empty(self):
        assert _bullets("") == []

    def test_ignores_non_bullet_lines(self):
        assert _bullets("just text") == []


# ---------------------------------------------------------------------------
# _clean_candidate / _is_useful_candidate
# ---------------------------------------------------------------------------


class TestCleanCandidate:
    def test_strips_punctuation_and_quotes(self):
        assert _clean_candidate("`family`") == "family"
        assert _clean_candidate('“pseudo-family”') == "pseudo-family"

    def test_strips_leading_directive_prefixes(self):
        assert _clean_candidate("识别 family") == "family"
        assert _clean_candidate("提醒 长期 reward") == "长期 reward"

    def test_strips_trailing_de_marker(self):
        # 的 in trailing position is dropped
        assert _clean_candidate("具体的") == "具体"

    def test_collapses_whitespace(self):
        assert _clean_candidate("  multi   space  ") == "multi space"


class TestIsUsefulCandidate:
    def test_rejects_empty(self):
        # _is_useful_candidate assumes pre-cleaned input; only the empty string is rejected here
        assert _is_useful_candidate("") is False

    def test_rejects_stopwords(self):
        for word in ["识别", "至少", "出现", "必须"]:
            assert _is_useful_candidate(word) is False

    def test_rejects_short_chinese_unless_allowed(self):
        # 1-2 char Chinese is filtered by default
        assert _is_useful_candidate("家人") is False
        # but allow_short keeps them
        assert _is_useful_candidate("家人", allow_short=True) is True

    def test_accepts_normal_terms(self):
        assert _is_useful_candidate("family") is True
        assert _is_useful_candidate("pseudo-family") is True
        assert _is_useful_candidate("虚拟亲属化") is True


# ---------------------------------------------------------------------------
# _candidate_terms
# ---------------------------------------------------------------------------


class TestCandidateTerms:
    def test_prefers_backtick_terms(self):
        terms = _candidate_terms("识别 `family` 之一", present=True)
        assert "family" in terms

    def test_prefers_quoted_terms(self):
        terms = _candidate_terms('识别 "pseudo-family" rhetoric', present=True)
        assert "pseudo-family" in terms

    def test_chinese_curly_quotes(self):
        terms = _candidate_terms("识别 “虚拟亲属化” 之一", present=True)
        assert "虚拟亲属化" in terms

    def test_splits_alternatives_by_slash(self):
        terms = _candidate_terms('"我们是一家人" / "family" / 虚拟亲属化', present=True)
        assert "family" in terms
        assert "虚拟亲属化" in terms

    def test_falls_back_to_long_phrases_when_no_explicit_terms(self):
        terms = _candidate_terms("解释清楚长期奖励的内涵和具体含义", present=True)
        # at least one extracted CJK phrase should make it through
        assert any(len(t) >= 3 for t in terms)

    def test_dedupes_case_insensitive(self):
        terms = _candidate_terms('"Family" / `family` / "FAMILY"', present=True)
        lowered = [t.lower() for t in terms]
        assert lowered.count("family") == 1

    def test_forbidden_check_strips_dash_explanation(self):
        """For 必须不出现, content after '——' is guidance not the forbidden term."""
        # "立刻辞职" is forbidden; the part after —— is recommendation, not also forbidden
        expectation = '"立刻辞职" —— 应该说"考虑长期"'
        terms = _candidate_terms(expectation, present=False)
        assert "立刻辞职" in terms
        assert "考虑长期" not in terms

    def test_present_check_keeps_full_text(self):
        """For 必须出现, keep the entire expectation when extracting."""
        expectation = '"立刻辞职" —— 不要给这种建议'
        terms = _candidate_terms(expectation, present=True)
        # both halves remain candidates
        assert "立刻辞职" in terms

    def test_strips_markdown_emphasis(self):
        # ** is stripped from the expectation before extraction — `term` is found
        terms = _candidate_terms("**important** `term`", present=True)
        assert "term" in terms
        # No fallback long-phrase extraction once explicit terms (backticks) exist,
        # so "important" alone is NOT extracted here. Documenting this behavior.
        assert "important" not in terms

    def test_long_phrase_fallback_when_no_explicit_terms(self):
        # without backticks/quotes/separators, fallback regex captures CJK phrases & long latin words
        terms = _candidate_terms("important guidance about workplace", present=True)
        assert "important" in terms
        assert "guidance" in terms


# ---------------------------------------------------------------------------
# _check_keywords
# ---------------------------------------------------------------------------


class TestCheckKeywords:
    def test_present_returns_misses(self):
        output = "the boss called us a family today"
        misses = _check_keywords(
            output, ['"family"', '"long-term reward"'], present=True
        )
        # family found, long-term reward missing
        assert any("long-term" in m for m in misses)
        assert not any("family" in m for m in misses)

    def test_present_all_satisfied(self):
        output = "discussion of family and long-term reward"
        misses = _check_keywords(
            output, ['"family"', '"long-term reward"'], present=True
        )
        assert misses == []

    def test_forbidden_returns_hits(self):
        output = "you should resign immediately and 立刻辞职"
        hits = _check_keywords(output, ['"立刻辞职"'], present=False)
        assert hits != []

    def test_forbidden_clean(self):
        output = "consider the long term and your finances"
        hits = _check_keywords(output, ['"立刻辞职"'], present=False)
        assert hits == []

    def test_alternative_satisfied_by_any(self):
        """If checklist has alternatives, ANY one match passes."""
        output = "they used pseudo-family rhetoric"
        misses = _check_keywords(
            output,
            ['"我们是一家人" / "family" / 虚拟亲属化 / pseudo-family 之一'],
            present=True,
        )
        assert misses == []

    def test_skips_expectation_with_no_extractable_terms(self):
        """Guidance-only text with all stopwords yields no terms — skipped, not miss."""
        output = ""
        misses = _check_keywords(output, ["至少 必须 识别"], present=True)
        # nothing extractable => not counted as miss
        assert misses == []

    def test_matcher_lowercases_internally(self):
        # The matcher now lowercases output + terms internally — uppercase input
        # is matched fine. (Previously, the caller had to .lower() first.)
        assert _check_keywords("FAMILY rhetoric", ['"family"'], present=True) == []
        assert _check_keywords("family rhetoric", ['"FAMILY"'], present=True) == []


# ---------------------------------------------------------------------------
# Negation-aware forbidden-check semantics
# Regression set for the false-positive class that real-LLM eval surfaced —
# model warns against X using language like "no X" / "don't X" / "不要 X".
# ---------------------------------------------------------------------------


class TestForbiddenNegation:
    @pytest.mark.parametrize(
        "output,forbidden,should_hit",
        [
            # English
            ("don't quit immediately", '"quit immediately"', False),
            ("do not quit immediately", '"quit immediately"', False),
            ("you should not quit immediately", '"quit immediately"', False),
            ("never quit immediately under pressure", '"quit immediately"', False),
            ("avoid quitting immediately", '"quitting immediately"', False),
            ("you should quit immediately", '"quit immediately"', True),
            ("just quit immediately", '"quit immediately"', True),
            # Chinese
            ("不要立刻辞职", '"立刻辞职"', False),
            ("千万不要立刻辞职", '"立刻辞职"', False),
            ("避免立刻辞职这种激进做法", '"立刻辞职"', False),
            ("你应该立刻辞职", '"立刻辞职"', True),
            # Spanish
            ("no recomendamos aceptar la primera oferta", '"aceptar la primera oferta"', False),
            ("nunca aceptar la primera oferta", '"aceptar la primera oferta"', False),
            ("debes aceptar la primera oferta", '"aceptar la primera oferta"', True),
            # French
            ("ne pas démissionner immédiatement", '"démissionner immédiatement"', False),
            ("évite de démissionner immédiatement", '"démissionner immédiatement"', False),
            ("tu dois démissionner immédiatement", '"démissionner immédiatement"', True),
            # Portuguese
            ("não pedir demissão imediatamente", '"pedir demissão imediatamente"', False),
            ("evite pedir demissão imediatamente", '"pedir demissão imediatamente"', False),
            ("você deve pedir demissão imediatamente", '"pedir demissão imediatamente"', True),
            # German
            ("nicht sofort kündigen", '"sofort kündigen"', False),
            ("niemals sofort kündigen", '"sofort kündigen"', False),
            ("du solltest sofort kündigen", '"sofort kündigen"', True),
        ],
    )
    def test_negation_window(self, output: str, forbidden: str, should_hit: bool):
        hits = _check_keywords(output, [forbidden], present=False)
        if should_hit:
            assert hits, f"expected forbidden hit on `{forbidden}` in {output!r}"
        else:
            assert hits == [], (
                f"expected NO hit for `{forbidden}` in {output!r} (negation should suppress)"
            )

    def test_mixed_occurrences_one_unnegated(self):
        """If a term appears twice — once negated, once not — it's a hit."""
        # First mention is warning; second mention is prescriptive
        output = "don't fabricate a competing offer. but you could fabricate a competing offer to push them"
        hits = _check_keywords(output, ['"fabricate a competing offer"'], present=False)
        assert hits == ['"fabricate a competing offer"']

    def test_negation_too_far_does_not_apply(self):
        """If the negation is outside the 40-char window, it does not suppress."""
        output = "i told you don't ever do that. " + "x" * 80 + " just quit immediately."
        hits = _check_keywords(output, ['"quit immediately"'], present=False)
        assert hits == ['"quit immediately"']

    def test_must_appear_unaffected_by_negation_logic(self):
        """Must-appear (present=True) checks are NOT negation-aware — only must-not-appear is."""
        # If the model says "we don't recommend X", X *did* appear, satisfying must-appear
        output = "we don't recommend aceptar la primera oferta"
        misses = _check_keywords(output, ['"aceptar la primera oferta"'], present=True)
        assert misses == []

    def test_real_world_case_19_pattern(self):
        """Regression for the exact false-positive seen in case 19's real-LLM run.

        The Spanish negotiation case marked as 'fail' because the model wrote
        warnings like 'no recomendar aceptar la primera oferta' which contain
        the forbidden phrase 'Recomendar aceptar la primera oferta sin negociar'.
        After the fix, this should NOT count as a forbidden hit.
        """
        output = (
            "Algunas cosas a evitar:\n"
            "- No recomendar aceptar la primera oferta sin negociar\n"
            "- No mentir sobre una oferta competidora\n"
        )
        hits = _check_keywords(
            output,
            ['"Recomendar aceptar la primera oferta sin negociar"'],
            present=False,
        )
        assert hits == []

    def test_real_world_case_14_pattern(self):
        """Regression for case 14 (acute crisis): the model defers PIP advice
        with phrasing like 'after you're safe, then we can talk about PIP'.
        The 'PIP' mention should not flag as a forbidden hit when paired with
        a negation/deferral signal.

        Note: this is the harder case — 'after you're safe' isn't a strict
        negation. With the negation-only fix, this *may* still flag. Documenting
        current behavior; LLM-judge mode is the long-term solution.
        """
        # The actual model output had: "PIP我可以帮你想... 但要等你安全了，明天我们再谈"
        # No explicit negation in the 40-char window before "PIP" → still flags.
        # Documenting that this case still requires LLM-judge for proper handling.
        output = "PIP 我可以帮你想，但要等你安全了，明天再谈"
        hits = _check_keywords(output, ['"PIP"'], present=False)
        # Expected behavior with the cheap negation fix: still hits.
        # When LLM-judge ships, update this expectation.
        assert hits == ['"PIP"']


# ---------------------------------------------------------------------------
# load_cases — uses the real cases dir to lock in current corpus
# ---------------------------------------------------------------------------


class TestLoadCases:
    def test_skips_index_md(self, cases_dir: Path):
        # sanity: INDEX.md exists in the corpus but is excluded by load_cases
        assert (cases_dir / "INDEX.md").exists()
        names = {c.path.name for c in load_cases()}
        assert "INDEX.md" not in names

    def test_loads_all_real_cases(self, cases_dir: Path):
        expected = sorted(p.name for p in cases_dir.glob("*.md") if p.name != "INDEX.md")
        loaded = sorted(c.path.name for c in load_cases())
        assert loaded == expected

    def test_filter_pattern(self):
        cases = load_cases(filter_pattern="decode")
        assert cases  # at least one
        assert all("decode" in c.path.name.lower() for c in cases)

    def test_filter_no_match_returns_empty(self):
        assert load_cases(filter_pattern="nonexistent_xyz_nope") == []


# ---------------------------------------------------------------------------
# EvalCase dataclass defaults
# ---------------------------------------------------------------------------


def test_evalcase_default_lists_independent():
    """Field default_factory: two instances must not share the same list object."""
    a = EvalCase(path=Path("a"), id="a", title="A", module_expected="x", priority="P0", input_lang="zh", input_text="")
    b = EvalCase(path=Path("b"), id="b", title="B", module_expected="x", priority="P0", input_lang="zh", input_text="")
    a.must_appear.append("only-on-a")
    assert b.must_appear == []
