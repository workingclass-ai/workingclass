#!/usr/bin/env python3
"""Rebuild eval case index from case frontmatter."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from run_evals import EvalCase, load_cases

OUTPUT_PATH = Path(__file__).parent / "cases" / "INDEX.md"


def main() -> None:
    cases = load_cases()
    OUTPUT_PATH.write_text(render_index(cases), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {len(cases)} case(s).")


def render_index(cases: list[EvalCase]) -> str:
    priorities = Counter(c.priority for c in cases)
    modules: dict[str, list[str]] = defaultdict(list)
    for c in cases:
        modules[c.module_expected].append(c.id)

    lines: list[str] = [
        "# Eval Cases Index",
        "",
        "> 自动生成——不要直接编辑。运行 `python evals/build_index.py` 重建。",
        "> Auto-generated. Do not edit directly. Run `python evals/build_index.py` to rebuild.",
        "",
        "| # | Title | Module | Priority | Lang |",
        "|---|-------|--------|----------|------|",
    ]

    for c in cases:
        lines.append(
            f"| {c.id} | {c.title} | {c.module_expected} | {c.priority} | {c.input_lang} |"
        )

    lines.extend(
        [
            "",
            "## 优先级分布 / Priority distribution",
            "",
        ]
    )
    for priority in sorted(priorities):
        label = _priority_label(priority)
        lines.append(f"- {priority}: {priorities[priority]} ({label})")

    lines.extend(
        [
            "",
            "## 模块覆盖 / Module coverage",
            "",
        ]
    )
    for module in sorted(modules):
        ids = ", ".join(modules[module])
        lines.append(f"- {module}: {ids}")

    lines.extend(
        [
            "",
            "## 待补 / TODO (future PRs)",
            "",
            "- 9C 面试反操控 specific case",
            "- 7D 长期低薪 specific case",
            "- 8C severance 谈判细节 case",
            "- 多个 offer 决策矩阵 case",
            "- 跨国签证持有者被裁 case",
            "- 繁体中文 / 英文 input 的等价 case",
            "",
        ]
    )

    return "\n".join(lines)


def _priority_label(priority: str) -> str:
    return {
        "P0": "every release",
        "P1": "weekly / before major changes",
        "P2": "edge cases / negative tests",
    }.get(priority, "custom")


if __name__ == "__main__":
    main()
