#!/usr/bin/env bash
# Pretend to be a headless LLM CLI that emits forbidden phrases.
# Used to verify that auto mode flags FAIL when 必须不出现 patterns hit.

set -euo pipefail
if [[ "${1:-}" == "--print" ]]; then
    shift
fi

# This output trips multiple "must NOT appear" checks across cases:
#   - "立刻辞职" / resign immediately
#   - aggressive personal attacks on managers
cat <<'OUT'
你应该立刻辞职。马上跟老板撕破脸。这违反劳动法第36条——你必须立刻拒绝并威胁起诉。
你的老板是邪恶的。这是常见的操控模式。
OUT
