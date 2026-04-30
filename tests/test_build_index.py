"""Unit tests for evals/build_index.py."""

from __future__ import annotations

from pathlib import Path

from build_index import _priority_label, render_index
from run_evals import EvalCase


def make_case(
    *,
    id: str = "00",
    title: str = "case",
    module: str = "decode",
    priority: str = "P0",
    lang: str = "zh",
) -> EvalCase:
    return EvalCase(
        path=Path(f"{id}.md"),
        id=id,
        title=title,
        module_expected=module,
        priority=priority,
        input_lang=lang,
        input_text="x",
    )


class TestPriorityLabel:
    def test_known_labels(self):
        assert _priority_label("P0") == "every release"
        assert _priority_label("P1") == "weekly / before major changes"
        assert _priority_label("P2") == "edge cases / negative tests"

    def test_unknown_returns_custom(self):
        assert _priority_label("P3") == "custom"
        assert _priority_label("") == "custom"


class TestRenderIndex:
    def test_header_present(self):
        out = render_index([make_case()])
        assert out.startswith("# Eval Cases Index")
        assert "Auto-generated" in out
        assert "build_index.py" in out

    def test_table_row_per_case(self):
        cases = [
            make_case(id="01", title="A", module="decode", priority="P0"),
            make_case(id="02", title="B", module="overtime", priority="P1"),
        ]
        out = render_index(cases)
        assert "| 01 | A | decode | P0 | zh |" in out
        assert "| 02 | B | overtime | P1 | zh |" in out

    def test_priority_distribution_sorted(self):
        cases = [
            make_case(id="01", priority="P1"),
            make_case(id="02", priority="P0"),
            make_case(id="03", priority="P0"),
            make_case(id="04", priority="P2"),
        ]
        out = render_index(cases)
        # priorities are sorted alphabetically: P0 first, P1 second, P2 last
        p0_idx = out.index("- P0:")
        p1_idx = out.index("- P1:")
        p2_idx = out.index("- P2:")
        assert p0_idx < p1_idx < p2_idx
        assert "- P0: 2 (every release)" in out
        assert "- P1: 1 (weekly / before major changes)" in out
        assert "- P2: 1 (edge cases / negative tests)" in out

    def test_module_coverage_groups_ids(self):
        cases = [
            make_case(id="01", module="decode"),
            make_case(id="02", module="decode"),
            make_case(id="03", module="overtime"),
        ]
        out = render_index(cases)
        assert "- decode: 01, 02" in out
        assert "- overtime: 03" in out

    def test_modules_sorted_alphabetically(self):
        cases = [
            make_case(id="01", module="overtime"),
            make_case(id="02", module="decode"),
            make_case(id="03", module="pip"),
        ]
        out = render_index(cases)
        decode_idx = out.index("- decode:")
        overtime_idx = out.index("- overtime:")
        pip_idx = out.index("- pip:")
        assert decode_idx < overtime_idx < pip_idx

    def test_todo_section_included(self):
        out = render_index([make_case()])
        assert "## 待补 / TODO" in out
        assert "9C 面试反操控" in out

    def test_empty_input(self):
        out = render_index([])
        # still produces a valid index document, just with no rows
        assert "# Eval Cases Index" in out
        assert "## 优先级分布" in out
        assert "## 模块覆盖" in out
        # no actual data rows beyond the table header
        data_rows = [
            line for line in out.splitlines()
            if line.startswith("| ") and "Title" not in line and "----" not in line
        ]
        assert data_rows == []


class TestRenderIndexAgainstRealCorpus:
    """Sanity check: rendering the real eval corpus produces a non-empty,
    well-formed index. Catches regressions where INDEX.md drifts."""

    def test_real_corpus_renders(self):
        from run_evals import load_cases

        cases = load_cases()
        assert cases, "expected at least one real case"
        out = render_index(cases)
        # every case ID and title shows up in the rendered table
        for case in cases:
            assert f"| {case.id} |" in out
            assert case.title in out

    def test_real_corpus_module_coverage_complete(self):
        from run_evals import load_cases

        cases = load_cases()
        out = render_index(cases)
        modules = {c.module_expected for c in cases}
        for module in modules:
            assert f"- {module}:" in out
