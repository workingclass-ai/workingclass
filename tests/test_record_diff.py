"""Tests for the recording (run_evals --record) + diff (eval_diff.py) loop.

Strategy: drive run_evals.py against the two existing stub LLM scripts
(`stub_llm_pass.sh`, `stub_llm_forbidden.sh`) to produce two recordings, then
exercise eval_diff against them. Verifies:
  - JSON shape is stable
  - Schema version locked
  - Regressions are detected and exit-coded
  - --show-output produces text diffs
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNNER = REPO_ROOT / "evals" / "run_evals.py"
DIFFER = REPO_ROOT / "evals" / "eval_diff.py"
FIXTURES = Path(__file__).parent / "fixtures"
STUB_PASS = FIXTURES / "stub_llm_pass.sh"
STUB_FORBIDDEN = FIXTURES / "stub_llm_forbidden.sh"

pytestmark = pytest.mark.e2e


def _record(stub: Path, out: Path, *, filter_pattern: str = "01-decode") -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--auto",
            "--llm-command",
            str(stub),
            "--filter",
            filter_pattern,
            "--record",
            str(out),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )


def _diff(baseline: Path, current: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(DIFFER), str(baseline), str(current), *extra],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=15,
    )


# ---------------------------------------------------------------------------
# Recording shape
# ---------------------------------------------------------------------------


class TestRecordingShape:
    def test_record_writes_valid_json(self, tmp_path: Path):
        out = tmp_path / "rec.json"
        result = _record(STUB_PASS, out)
        assert result.returncode == 0, result.stderr
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["schema_version"] == 1

    def test_top_level_keys_locked(self, tmp_path: Path):
        out = tmp_path / "rec.json"
        _record(STUB_PASS, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert set(data.keys()) == {"schema_version", "meta", "results"}

    def test_meta_contains_required_fields(self, tmp_path: Path):
        out = tmp_path / "rec.json"
        _record(STUB_PASS, out)
        meta = json.loads(out.read_text(encoding="utf-8"))["meta"]
        for field in ("started_at", "ended_at", "llm_command", "case_count"):
            assert field in meta, f"meta missing {field}"
        # skill_version + skill_commit are optional (None if SKILL.md missing or git absent)
        assert "skill_version" in meta
        assert "skill_commit" in meta

    def test_result_keys_locked(self, tmp_path: Path):
        out = tmp_path / "rec.json"
        _record(STUB_PASS, out)
        results = json.loads(out.read_text(encoding="utf-8"))["results"]
        assert results, "expected at least one result"
        expected_keys = {
            "case_id", "title", "module_expected", "priority", "input_lang",
            "status", "note", "stdout", "stderr", "duration_ms", "exit_code",
            "missing_keywords", "forbidden_hits", "prompt",
        }
        assert set(results[0].keys()) == expected_keys

    def test_status_uses_full_word(self, tmp_path: Path):
        # The recording must use full words ("pass"/"partial"/"fail"/"error")
        # not single letters — this is the public schema contract for diff tools.
        out = tmp_path / "rec.json"
        _record(STUB_PASS, out)
        results = json.loads(out.read_text(encoding="utf-8"))["results"]
        for r in results:
            assert r["status"] in {"pass", "partial", "fail", "error", "skip"}

    def test_record_implies_auto(self, tmp_path: Path):
        # --record without --auto should still record (auto is implied)
        out = tmp_path / "rec.json"
        result = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--llm-command",
                str(STUB_PASS),
                "--filter",
                "01-decode",
                "--record",
                str(out),
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result.returncode == 0, result.stderr
        assert out.exists()

    def test_record_rejects_non_json_extension(self, tmp_path: Path):
        out = tmp_path / "rec.txt"
        result = subprocess.run(
            [
                sys.executable, str(RUNNER), "--auto",
                "--llm-command", str(STUB_PASS),
                "--filter", "01-decode",
                "--record", str(out),
            ],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=15,
        )
        assert result.returncode == 2
        assert ".json" in result.stderr


# ---------------------------------------------------------------------------
# eval_diff
# ---------------------------------------------------------------------------


class TestEvalDiff:
    @pytest.fixture
    def two_recordings(self, tmp_path: Path) -> tuple[Path, Path]:
        baseline = tmp_path / "baseline.json"
        current = tmp_path / "current.json"
        _record(STUB_PASS, baseline)
        _record(STUB_FORBIDDEN, current)
        return baseline, current

    def test_regression_exits_nonzero(self, two_recordings: tuple[Path, Path]):
        baseline, current = two_recordings
        result = _diff(baseline, current, "--quiet")
        assert result.returncode == 1, (
            f"expected exit 1 on regression, got {result.returncode}\n{result.stdout}"
        )

    def test_no_regression_exits_zero(self, tmp_path: Path):
        # diff a recording against itself — no regression
        out = tmp_path / "rec.json"
        _record(STUB_PASS, out)
        result = _diff(out, out, "--quiet")
        assert result.returncode == 0

    def test_report_lists_regressions(self, two_recordings: tuple[Path, Path]):
        baseline, current = two_recordings
        result = _diff(baseline, current)
        assert result.returncode == 1
        assert "Regressions" in result.stdout
        assert "P0!" in result.stdout  # case 01 is P0
        assert "解码" in result.stdout  # case title preserved

    def test_show_output_dumps_unified_diff(self, two_recordings: tuple[Path, Path]):
        baseline, current = two_recordings
        result = _diff(baseline, current, "--show-output")
        assert "---" in result.stdout  # unified diff fromfile marker
        assert "+++" in result.stdout

    def test_schema_mismatch_errors(self, tmp_path: Path):
        baseline = tmp_path / "old.json"
        baseline.write_text(
            json.dumps({"schema_version": 0, "meta": {}, "results": []}),
            encoding="utf-8",
        )
        current = tmp_path / "new.json"
        _record(STUB_PASS, current)
        result = _diff(baseline, current)
        assert result.returncode == 2
        assert "schema mismatch" in result.stderr

    def test_missing_file_errors(self, tmp_path: Path):
        result = _diff(tmp_path / "ghost.json", tmp_path / "alsoghost.json")
        assert result.returncode == 2

    def test_invalid_json_errors(self, tmp_path: Path):
        bad = tmp_path / "bad.json"
        bad.write_text("not json at all", encoding="utf-8")
        ok = tmp_path / "ok.json"
        _record(STUB_PASS, ok)
        result = _diff(bad, ok)
        assert result.returncode == 2

    def test_quiet_suppresses_stdout(self, two_recordings: tuple[Path, Path]):
        baseline, current = two_recordings
        result = _diff(baseline, current, "--quiet")
        assert result.stdout == ""


# ---------------------------------------------------------------------------
# Verdict ranking semantics
# ---------------------------------------------------------------------------


class TestDiffSemantics:
    """Unit-level checks against the diff() function directly."""

    def _import_diff(self):
        # Local import so the e2e marker doesn't keep this from collection
        sys.path.insert(0, str(REPO_ROOT / "evals"))
        try:
            import eval_diff
        finally:
            if str(REPO_ROOT / "evals") in sys.path:
                sys.path.remove(str(REPO_ROOT / "evals"))
        return eval_diff

    def test_pass_to_partial_is_regression(self, tmp_path: Path):
        ed = self._import_diff()
        b = ed.Recording(1, {}, [{"case_id": "1", "title": "t", "priority": "P0", "status": "pass"}], tmp_path / "b")
        c = ed.Recording(1, {}, [{"case_id": "1", "title": "t", "priority": "P0", "status": "partial"}], tmp_path / "c")
        changes = ed.diff(b, c)
        assert changes[0].kind == "regression"

    def test_fail_to_pass_is_fix(self, tmp_path: Path):
        ed = self._import_diff()
        b = ed.Recording(1, {}, [{"case_id": "1", "title": "t", "priority": "P0", "status": "fail"}], tmp_path / "b")
        c = ed.Recording(1, {}, [{"case_id": "1", "title": "t", "priority": "P0", "status": "pass"}], tmp_path / "c")
        changes = ed.diff(b, c)
        assert changes[0].kind == "fix"

    def test_unchanged_pass(self, tmp_path: Path):
        ed = self._import_diff()
        b = ed.Recording(1, {}, [{"case_id": "1", "title": "t", "priority": "P0", "status": "pass"}], tmp_path / "b")
        c = ed.Recording(1, {}, [{"case_id": "1", "title": "t", "priority": "P0", "status": "pass"}], tmp_path / "c")
        changes = ed.diff(b, c)
        assert changes[0].kind == "unchanged"

    def test_new_case_in_current_only(self, tmp_path: Path):
        ed = self._import_diff()
        b = ed.Recording(1, {}, [], tmp_path / "b")
        c = ed.Recording(1, {}, [{"case_id": "X", "title": "t", "priority": "P1", "status": "pass"}], tmp_path / "c")
        changes = ed.diff(b, c)
        assert changes[0].kind == "new"

    def test_removed_case_in_baseline_only(self, tmp_path: Path):
        ed = self._import_diff()
        b = ed.Recording(1, {}, [{"case_id": "X", "title": "t", "priority": "P1", "status": "pass"}], tmp_path / "b")
        c = ed.Recording(1, {}, [], tmp_path / "c")
        changes = ed.diff(b, c)
        assert changes[0].kind == "removed"
