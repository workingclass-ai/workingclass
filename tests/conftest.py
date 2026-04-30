"""Shared pytest fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = REPO_ROOT / "evals"
CASES_DIR = EVAL_DIR / "cases"
SKILL_DIR = REPO_ROOT / "skills" / "laborer-companion"

# Make evals/ importable without installing the package — mirrors pythonpath in
# pyproject.toml so static analysers (pyright) and ad-hoc runs both resolve it.
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def eval_dir() -> Path:
    return EVAL_DIR


@pytest.fixture(scope="session")
def cases_dir() -> Path:
    return CASES_DIR


@pytest.fixture(scope="session")
def skill_dir() -> Path:
    return SKILL_DIR


@pytest.fixture
def write_case(tmp_path: Path):
    """Factory: write a fake case markdown file to tmp_path/cases and return its path."""

    cases = tmp_path / "cases"
    cases.mkdir(exist_ok=True)

    def _write(filename: str, content: str) -> Path:
        path = cases / filename
        path.write_text(content, encoding="utf-8")
        return path

    return _write
