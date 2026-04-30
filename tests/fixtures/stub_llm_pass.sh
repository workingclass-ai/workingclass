#!/usr/bin/env bash
# Pretend to be a headless LLM CLI like `claude --print "<prompt>"`.
# Print a response that contains keywords most cases expect to see.
# Used by the e2e test to verify the runner's pass-counting machinery.

set -euo pipefail

# Drop the leading --print flag the runner passes
if [[ "${1:-}" == "--print" ]]; then
    shift
fi
prompt="${1:-}"

# Lowercased corpus that hits the common positive keywords across the eval cases.
# Keep this conservative — the goal is "many cases pass" not "all cases pass".
cat <<'OUT'
Acknowledging the operational-security risk first: do not paste this on a corporate
device or network, and redact identifying details.

This message uses pseudo-family / "我们是一家人" rhetoric. It also leans on long-term
reward language ("未来会怎样") that has no contractual weight.

Suggested response: ask for the bonus structure in writing, distinguish 情感纽带 from
契约关系, and decline the weekend 加班 unless 加班费 is documented.

This is general guidance, not legal advice. Consult a local 劳动律师 / labor lawyer
for jurisdiction-specific advice.
OUT
OUT_PROMPT_LEN=${#prompt}
# Echo prompt length so we know stdin/argv plumbing actually wired the prompt through.
echo "[stub] received prompt of length ${OUT_PROMPT_LEN}" >&2
