#!/usr/bin/env python3
"""Memory-isolated eval runner using the Anthropic SDK directly.

Why this exists
---------------
`run_evals.py --auto` shells out to `claude --print "<prompt>"`. That subprocess
inherits the user's environment and Claude Code auto-loads memory files
(`~/.claude/CLAUDE.md`, `<cwd>/CLAUDE.md`, etc.) on startup. If a contributor's
memory file contains private context (people's names, email addresses, employer
relationships), the model uses that context to "personalize" responses to vague
case prompts, and the recording captures the personalized output.

This module bypasses Claude Code entirely. It loads `SKILL.md` from the repo,
uses it as the system prompt, sends each case input as a single user message,
and records the response. There is no subprocess, no shell environment leak,
no auto-loaded memory.

How verdict computation works
-----------------------------
Identical to `run_auto`'s output classification: same `_check_keywords` matcher,
same RunResult shape, same recording schema. The runner is interchangeable.

Cost & cache
------------
The system prompt (SKILL.md content) is the same across every case in a single
run. We mark it with `cache_control: ephemeral` so the prompt is cached after
the first call. Across 33 cases this drops effective input cost by ~90%.

Public API
----------
- `build_system_prompt(skill_dir)` — pure function, no API calls
- `call_model(client, system, user_text, model)` — single round-trip
- `run_one_case(client, case, system, model)` → RunResult
- `run_api_mode(cases, model, *, client=None)` → list[RunResult]
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Protocol

from run_evals import (
    EvalCase,
    MAX_OUTPUT_BYTES,
    RunResult,
    STATUS_ERROR,
    STATUS_FAIL,
    STATUS_PARTIAL,
    STATUS_PASS,
    _check_keywords,
    _summary,
    _truncate,
)

# Default skill directory; tests may override.
SKILL_DIR_DEFAULT = Path(__file__).resolve().parent.parent / "skills" / "laborer-companion"

# Default model. CLAUDE.md says: "Opus 4.7: 'claude-opus-4-7'".
DEFAULT_MODEL = "claude-opus-4-7"

# Per-call output cap. Generous; matches MAX_OUTPUT_BYTES on the recording side.
DEFAULT_MAX_TOKENS = 4096

# How long before we give up on a single API call.
DEFAULT_TIMEOUT_S = 180


# ---------------------------------------------------------------------------
# Type stubs so the module type-checks without anthropic installed
# ---------------------------------------------------------------------------


class _AnthropicMessageResponse(Protocol):
    """Minimal protocol for the response shape we use. Lets tests inject fakes
    without depending on anthropic at type-check time."""

    @property
    def content(self) -> list[Any]: ...


class _AnthropicClientProtocol(Protocol):
    """Minimal protocol for the client shape we use."""

    @property
    def messages(self) -> Any: ...


if TYPE_CHECKING:
    AnthropicClient = _AnthropicClientProtocol
else:
    AnthropicClient = Any


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)


def build_system_prompt(skill_dir: Path = SKILL_DIR_DEFAULT) -> str:
    """Read SKILL.md and return its body (frontmatter stripped) as the system prompt.

    We intentionally do NOT include `references/*.md` or `commands/*.md` content
    in the system prompt. Two reasons:
      1. The system prompt is cached — keeping it stable per-skill-version is
         what makes the cache valuable.
      2. SKILL.md is the canonical entry point. Cases that exercise specific
         playbooks indirectly test whether SKILL.md routes the model correctly.

    The returned string never contains anything from the user's home directory
    or local memory files. It is bounded by what's committed in this repo.
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"{skill_md} not found — cannot build system prompt")

    text = skill_md.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    body = text[match.end():] if match else text
    return body.strip()


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------


def call_model(
    client: AnthropicClient,
    system: str,
    user_text: str,
    model: str = DEFAULT_MODEL,
    *,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    timeout: float = DEFAULT_TIMEOUT_S,
) -> str:
    """Make a single Anthropic message call. Returns the text body of the response.

    The system prompt is sent as a single content block with `cache_control:
    {"type": "ephemeral"}` so subsequent calls in the same run reuse the cache.
    """
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        timeout=timeout,
        system=[
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_text}],
    )
    # response.content is a list of content blocks; take the first text block.
    # The SDK returns objects with `.type` and `.text`; tests may pass dicts.
    for block in response.content:
        if isinstance(block, dict):
            if block.get("type") == "text":
                return block.get("text", "")
        elif getattr(block, "type", None) == "text":
            return getattr(block, "text", "")
    return ""


# ---------------------------------------------------------------------------
# Per-case orchestration
# ---------------------------------------------------------------------------


def run_one_case(
    client: AnthropicClient,
    case: EvalCase,
    system: str,
    model: str = DEFAULT_MODEL,
) -> RunResult:
    """Drive a single case through the API and classify the verdict.

    Same scoring logic as `_run_one_case` in run_evals.py — keeps the recording
    schema interchangeable across runner modes.
    """
    base = RunResult(
        case_id=case.id,
        title=case.title,
        module_expected=case.module_expected,
        priority=case.priority,
        input_lang=case.input_lang,
        status=STATUS_FAIL,
        prompt=case.input_text,
    )

    started = time.monotonic()
    try:
        output = call_model(client, system, case.input_text, model=model)
    except Exception as e:
        base.status = STATUS_ERROR
        base.note = f"api error: {type(e).__name__}: {e}"
        base.duration_ms = int((time.monotonic() - started) * 1000)
        return base

    base.duration_ms = int((time.monotonic() - started) * 1000)
    base.exit_code = 0  # API mode has no shell exit code; 0 = "API call returned"
    base.stdout = _truncate(output, MAX_OUTPUT_BYTES)
    # Match run_auto's lowercasing convention before keyword checks
    output_lower = output.lower()
    base.missing_keywords = _check_keywords(output_lower, case.must_appear, present=True)
    base.forbidden_hits = _check_keywords(output_lower, case.must_not_appear, present=False)

    if not base.missing_keywords and not base.forbidden_hits:
        base.status = STATUS_PASS
    elif base.missing_keywords and not base.forbidden_hits:
        base.status = STATUS_PARTIAL
        base.note = f"missed: {base.missing_keywords[:2]}"
    else:
        base.status = STATUS_FAIL
        base.note = f"forbidden: {base.forbidden_hits[:2]}"
    return base


# ---------------------------------------------------------------------------
# Top-level runner
# ---------------------------------------------------------------------------


def run_api_mode(
    cases: list[EvalCase],
    model: str = DEFAULT_MODEL,
    *,
    client: Optional[AnthropicClient] = None,
    skill_dir: Path = SKILL_DIR_DEFAULT,
) -> list[RunResult]:
    """Run every case via the Anthropic API and return the results.

    `client` lets tests inject a fake. In production, leave it None and we
    construct a real `anthropic.Anthropic()` from `ANTHROPIC_API_KEY`.
    """
    if client is None:
        client = _make_real_client()

    system = build_system_prompt(skill_dir)
    print(f"\n=== API eval mode ===\n")
    print(f"Model:        {model}")
    print(f"Skill dir:    {skill_dir}")
    print(f"System prompt: {len(system)} chars (cached after first call)")
    print(f"Cases:        {len(cases)}")
    print(
        f"\n⚠️  This makes real Anthropic API calls — costs tokens. "
        f"Press Ctrl-C to abort.\n"
    )

    results: list[RunResult] = []
    for i, c in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {c.id} — {c.title} ... ", end="", flush=True)
        r = run_one_case(client, c, system, model=model)
        results.append(r)
        print(_format_outcome_tail(r))

    _summary(results)
    return results


def _make_real_client() -> AnthropicClient:
    """Construct an anthropic.Anthropic client. Imported lazily so the module
    is importable (and testable) without the SDK installed."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. "
            "Export your Anthropic key before running the api-mode eval, or "
            "pass `client=` to run_api_mode() with a fake."
        )
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError(
            "The `anthropic` SDK is not installed. "
            "Run `pip install anthropic` (or `uv sync` if using uv)."
        ) from e
    return anthropic.Anthropic()


def _format_outcome_tail(r: RunResult) -> str:
    """Match the wording of run_auto's per-case status line."""
    if r.status == STATUS_PASS:
        return "PASS"
    if r.status == STATUS_PARTIAL:
        return f"PARTIAL ({len(r.missing_keywords)} expected patterns missing)"
    if r.status == STATUS_ERROR:
        return f"ERROR ({r.note})"
    return f"FAIL (forbidden patterns appeared: {len(r.forbidden_hits)})"
