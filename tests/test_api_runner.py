"""Tests for the memory-isolated Anthropic-SDK eval runner.

The most important guarantee these tests enforce is that **the system prompt
sent to the API contains nothing beyond SKILL.md**. This is the property that
prevents the CLAUDE.md memory-leak class of bug that motivated this runner.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from api_runner import (
    DEFAULT_MODEL,
    build_system_prompt,
    call_model,
    run_api_mode,
    run_one_case,
)
from run_evals import (
    EvalCase,
    STATUS_ERROR,
    STATUS_FAIL,
    STATUS_PARTIAL,
    STATUS_PASS,
)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class _FakeTextBlock:
    type = "text"

    def __init__(self, text: str) -> None:
        self.text = text


class _FakeResponse:
    def __init__(self, text: str) -> None:
        self.content = [_FakeTextBlock(text)]


class FakeClient:
    """Captures every API call so tests can assert on what was sent."""

    def __init__(self, response_text: str = "ok") -> None:
        self.response_text = response_text
        self.calls: list[dict[str, Any]] = []
        self.messages = self  # so client.messages.create works

    def create(self, **kwargs: Any) -> _FakeResponse:
        self.calls.append(kwargs)
        # Allow per-call override via a list of responses (set by test)
        if isinstance(self.response_text, list):
            text = self.response_text.pop(0) if self.response_text else "ok"
        else:
            text = self.response_text
        return _FakeResponse(text)


# ---------------------------------------------------------------------------
# build_system_prompt — the leak-prevention guarantee
# ---------------------------------------------------------------------------


class TestBuildSystemPrompt:
    def test_returns_skill_md_body(self, skill_dir: Path):
        prompt = build_system_prompt(skill_dir)
        # Body should begin with the H1 from SKILL.md (after frontmatter is stripped)
        assert prompt.lstrip().startswith("# 劳动者AI助手") or prompt.lstrip().startswith("# Laborer")

    def test_strips_frontmatter(self, skill_dir: Path):
        prompt = build_system_prompt(skill_dir)
        # Frontmatter delimiters should not survive
        assert not prompt.lstrip().startswith("---")
        # frontmatter fields should not appear at the top of the body
        assert "name: laborer-companion" not in prompt[:500]

    def test_no_private_context(self, skill_dir: Path):
        """The prompt must not contain anything that could only come from a
        contributor's home dir (CLAUDE.md memory, etc.)."""
        prompt = build_system_prompt(skill_dir)
        forbidden_substrings = [
            # Personal email / name patterns that have leaked before in this project
            "larfan",
            "larry.l.fang",
            "larry.clawdbot",
            # Private people-context that lives in CLAUDE.md, not SKILL.md
            "Glenn Davies",
            "Brett",
            "Hannah",
            "Sinch",
            "MessageMedia",
            # Generic local-path tells
            "/Users/",
            "$HOME",
            # Memory / personal-config marker phrases
            "auto memory",
            "Personal Assistant",
        ]
        for needle in forbidden_substrings:
            assert needle not in prompt, (
                f"system prompt unexpectedly contains `{needle}` — "
                f"this should have come from SKILL.md only"
            )

    def test_does_not_read_home_directory(self, tmp_path: Path, monkeypatch):
        """If we point build_system_prompt at a fake skill dir, it must NOT
        fall back to ~/.claude or anywhere else for its content."""
        # Build a minimal SKILL.md in tmp
        fake_skill = tmp_path / "skills" / "laborer-companion"
        fake_skill.mkdir(parents=True)
        (fake_skill / "SKILL.md").write_text(
            "---\nname: x\nversion: 0.0.1\ndescription: y\n---\n# stub body\n",
            encoding="utf-8",
        )
        # Even if HOME is poisoned, output should be the stub body
        monkeypatch.setenv("HOME", str(tmp_path / "fake-home"))
        prompt = build_system_prompt(fake_skill)
        assert prompt.strip() == "# stub body"

    def test_missing_skill_md_raises(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            build_system_prompt(tmp_path / "nonexistent")


# ---------------------------------------------------------------------------
# call_model
# ---------------------------------------------------------------------------


class TestCallModel:
    def test_extracts_text_from_response(self):
        client = FakeClient(response_text="hello world")
        out = call_model(client, system="sys", user_text="user", model=DEFAULT_MODEL)
        assert out == "hello world"

    def test_passes_system_with_cache_control(self):
        client = FakeClient(response_text="ok")
        call_model(client, system="my system", user_text="hi", model=DEFAULT_MODEL)
        kw = client.calls[0]
        assert kw["system"] == [
            {"type": "text", "text": "my system", "cache_control": {"type": "ephemeral"}}
        ]

    def test_passes_user_message(self):
        client = FakeClient(response_text="ok")
        call_model(client, system="sys", user_text="please decode this", model=DEFAULT_MODEL)
        kw = client.calls[0]
        assert kw["messages"] == [{"role": "user", "content": "please decode this"}]

    def test_passes_model_id(self):
        client = FakeClient(response_text="ok")
        call_model(client, system="sys", user_text="hi", model="claude-sonnet-4-6")
        assert client.calls[0]["model"] == "claude-sonnet-4-6"

    def test_handles_empty_response(self):
        client = FakeClient()
        client.response_text = ""
        # Override the mock's default — return a response with no text blocks
        client.create = MagicMock(return_value=_FakeResponse(""))  # type: ignore[method-assign]
        out = call_model(client, system="sys", user_text="hi", model=DEFAULT_MODEL)
        assert out == ""


# ---------------------------------------------------------------------------
# run_one_case
# ---------------------------------------------------------------------------


def _stub_case(must_appear: list[str], must_not_appear: list[str]) -> EvalCase:
    return EvalCase(
        path=Path("stub.md"),
        id="stub",
        title="stub",
        module_expected="decode",
        priority="P0",
        input_lang="zh",
        input_text="example user input",
        must_appear=must_appear,
        must_not_appear=must_not_appear,
    )


class TestRunOneCase:
    def test_pass_when_all_must_appear_and_no_forbidden(self):
        c = _stub_case(must_appear=['"family"'], must_not_appear=['"立刻辞职"'])
        client = FakeClient(response_text="discussion of family rhetoric in workplaces")
        r = run_one_case(client, c, system="sys")
        assert r.status == STATUS_PASS
        assert r.missing_keywords == []
        assert r.forbidden_hits == []

    def test_partial_when_must_appear_misses(self):
        c = _stub_case(must_appear=['"family"', '"long-term reward"'], must_not_appear=[])
        client = FakeClient(response_text="discussion of family rhetoric")
        r = run_one_case(client, c, system="sys")
        assert r.status == STATUS_PARTIAL
        assert r.missing_keywords  # contains "long-term reward" expectation

    def test_fail_when_forbidden_hit(self):
        c = _stub_case(must_appear=[], must_not_appear=['"立刻辞职"'])
        client = FakeClient(response_text="你应该立刻辞职")
        r = run_one_case(client, c, system="sys")
        assert r.status == STATUS_FAIL
        assert r.forbidden_hits

    def test_negation_aware_forbidden_check(self):
        """Carry-over: the negation matcher applies in api mode too."""
        c = _stub_case(must_appear=[], must_not_appear=['"立刻辞职"'])
        client = FakeClient(response_text="不要立刻辞职 — 先评估")
        r = run_one_case(client, c, system="sys")
        assert r.status == STATUS_PASS
        assert r.forbidden_hits == []

    def test_api_error_classified_as_error(self):
        client = FakeClient()
        client.create = MagicMock(side_effect=RuntimeError("boom"))  # type: ignore[method-assign]
        c = _stub_case(must_appear=[], must_not_appear=[])
        r = run_one_case(client, c, system="sys")
        assert r.status == STATUS_ERROR
        assert "RuntimeError" in r.note
        assert "boom" in r.note
        # When the API errors, no output captured
        assert r.stdout == ""

    def test_records_prompt_and_duration(self):
        c = _stub_case(must_appear=[], must_not_appear=[])
        client = FakeClient(response_text="ok")
        r = run_one_case(client, c, system="sys")
        assert r.prompt == "example user input"
        assert r.duration_ms >= 0
        assert r.exit_code == 0


# ---------------------------------------------------------------------------
# run_api_mode (top-level)
# ---------------------------------------------------------------------------


class TestRunApiMode:
    def test_runs_each_case_once(self, skill_dir: Path):
        cases = [_stub_case([], []) for _ in range(3)]
        client = FakeClient(response_text="ok")
        results = run_api_mode(cases, client=client, skill_dir=skill_dir)
        assert len(results) == 3
        assert len(client.calls) == 3

    def test_system_prompt_is_consistent_across_cases(self, skill_dir: Path):
        """The same system prompt should be sent to every case so prompt
        caching is effective."""
        cases = [_stub_case([], []) for _ in range(3)]
        client = FakeClient(response_text="ok")
        run_api_mode(cases, client=client, skill_dir=skill_dir)
        systems = [call["system"] for call in client.calls]
        assert all(s == systems[0] for s in systems)

    def test_system_prompt_marked_for_caching(self, skill_dir: Path):
        cases = [_stub_case([], [])]
        client = FakeClient(response_text="ok")
        run_api_mode(cases, client=client, skill_dir=skill_dir)
        sys_block = client.calls[0]["system"][0]
        assert sys_block["cache_control"] == {"type": "ephemeral"}

    def test_no_private_context_in_actual_api_calls(self, skill_dir: Path):
        """Defense in depth: even if build_system_prompt regressed, the actual
        bytes sent to the API must not contain known-private substrings."""
        cases = [_stub_case([], [])]
        client = FakeClient(response_text="ok")
        run_api_mode(cases, client=client, skill_dir=skill_dir)
        sent_system = client.calls[0]["system"][0]["text"]
        for needle in ["larfan", "larry", "Glenn Davies", "Sinch", "MessageMedia", "/Users/"]:
            assert needle not in sent_system, (
                f"system prompt sent to API contains `{needle}` — leak path active"
            )