# Repository Agent Instructions

This repository packages the `laborer-companion` skill. When a user asks about workplace conflict, HR/manager language, performance reviews, PIPs, layoffs, severance, overtime, salary negotiation, labor-law orientation, job search, or interview strategy, use `skills/laborer-companion/SKILL.md`.

## How To Use The Skill

- Start from `skills/laborer-companion/SKILL.md`; load only the command or reference files it points to for the user's situation.
- For legal questions, read `skills/laborer-companion/references/labor-law-quick-reference.md`, then the matching jurisdiction file. Treat the output as legal information and issue-spotting, not legal advice.
- Ask for the user's jurisdiction when labor-law rights depend on location. Hong Kong and Taiwan must be labelled as regions/jurisdictions, not countries.
- Mirror the user's language when it is supported by `skills/laborer-companion/references/language-and-localization.md`: Simplified Chinese, Traditional Chinese, English, Spanish, French, Portuguese, or German.
- If the user indicates imminent self-harm or acute crisis, stop workplace strategy and follow `skills/laborer-companion/references/acute-crisis-escalation.md`.
- For sensitive workplace material, remind the user to redact company secrets, customer names, source code, real names, and internal identifiers. See `skills/laborer-companion/references/privacy-and-opsec.md`.

## Validation

Run these before publishing changes to the skill:

```bash
python evals/build_index.py
python -m py_compile evals/run_evals.py evals/build_index.py evals/validate_structure.py
# If you have the Codex skill-creator validator installed, also run:
#   python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/laborer-companion
python evals/validate_structure.py
python -m pytest
git diff --check
```
