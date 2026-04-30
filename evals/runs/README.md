# Eval Recordings

Recordings are JSON files produced by `python evals/run_evals.py --auto --record <path>`.
They capture each eval case's outcome against a specific LLM at a specific moment, in enough detail to compare across model versions or skill releases.

Use [`evals/eval_diff.py`](../eval_diff.py) to compare two recordings.

## Naming convention

```
RESULTS-<date>-<model-tag>.json
```

Examples:
- `RESULTS-2026-04-30-claude-opus-4-7.json`
- `RESULTS-2026-04-30-claude-sonnet-4-6.json`
- `RESULTS-2026-05-15-gpt-5-1.json`
- `BASELINE-stub.json` — recording produced from the deterministic stub LLM in `tests/fixtures/`. **This is a pipeline baseline, not a content baseline** — the stub emits generic text, so its verdict distribution is meaningless. Its value is that any regression in the schema, runner, or diff tooling shows up immediately when comparing a fresh stub run against this committed reference.

## Schema (v1)

```jsonc
{
  "schema_version": 1,
  "meta": {
    "started_at": "2026-04-30T17:00:00+00:00",
    "ended_at":   "2026-04-30T17:08:23+00:00",
    "llm_command": "claude",            // exact CLI invoked
    "skill_version": "0.1.0",           // from SKILL.md frontmatter
    "skill_commit":  "59509e3",         // git short SHA at record time
    "case_count":    30
  },
  "results": [
    {
      "case_id": "01",
      "title": "解码\"我们是一家人\"虚拟亲属化话术",
      "module_expected": "decode",
      "priority": "P0",
      "input_lang": "zh",
      "status": "pass" | "partial" | "fail" | "error" | "skip",
      "note": "missed: ['…', '…']",     // human-readable verdict reason
      "stdout": "…",                    // raw model output, capped at 64 KB
      "stderr": "…",                    // CLI stderr (often empty)
      "duration_ms": 12345,
      "exit_code": 0,
      "missing_keywords": ["…"],        // patterns expected but absent
      "forbidden_hits":   ["…"],        // patterns expected to be absent but present
      "prompt": "…"                     // exact text passed to the LLM
    }
  ]
}
```

If the schema ever needs a breaking change, bump `RECORDING_SCHEMA_VERSION` in `run_evals.py` to v2. `eval_diff.py` refuses to compare across schema versions.

## What to commit

- **Do commit**: `BASELINE-stub.json` (proof the pipeline works, deterministic, ~30 KB).
- **Do commit**: monthly model snapshots that you actually want to keep as historical references (e.g. on a Sonnet/Opus version bump).
- **Don't commit**: every ad-hoc local run. Recordings are large; `.gitignore` excludes anything matching `RESULTS-*.json`. Rename the ones you want to keep.

## Why this exists

Without recordings you can run the eval suite, see "23 pass / 5 partial / 2 fail" — and that number is meaningless because you don't know what it was last month, or last model. With recordings, you can answer concrete questions:

- Which P0 cases regressed when we bumped Sonnet 4.5 → 4.6?
- Did the SKILL.md rewrite for v0.2.0 cost us any case?
- Is the Spanish localization holding up across model versions?

That's the loop this whole framework exists to enable.
