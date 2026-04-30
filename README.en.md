# workingclass

[简体中文](README.md) · **English** · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Deutsch](README.de.md)

> AI tools that stand on the side of workers.

This repository hosts agent skills and tools that serve workers. The first and central one is **Laborer's Companion / 劳动者AI助手** — a tool that helps you see through workplace rhetoric and make the decisions that are actually best for you.

---

## Why this project exists

At work, the company, HR, and your boss have huge resources to manage you: HR consultants, manipulation playbooks, performance management systems, legal teams, recruiting psychologists. Every sentence they say is carefully designed — not necessarily to help you see clearly, but to make you take the action that benefits the company most.

You only have yourself.

The AI era makes this asymmetry worse — companies use AI to distill your work, replace you, monitor you. This project flips AI around: **AI on your side**.

---

## What's currently included

### 1. `skills/laborer-companion/` — Laborer's Companion

9 core modules + 4 entry tools, covering the full workplace landscape:

| Module | Purpose |
|--------|---------|
| Tool 0a · Triage | Routes you when you don't know which module to use |
| Tool 0b · Red-Flag Scan | A 60-second check on whether your situation is dangerous |
| Tool 0c · First 72 Hours After Layoff | What to do — and not do — the moment you're laid off |
| Tool 0d · Privacy & OPSEC | How to use this tool safely |
| Module 1 · Rhetoric Decoder | Translate what your boss/HR is *actually* saying |
| Module 2 · Overtime Decision | Real cost-benefit analysis |
| Module 3 · Performance Review Decoder | See through the intent behind a review |
| Module 4 · Stay-or-Leave | Decide based on your real interests |
| Module 5 · Historical Perspective | Find references in 150 years of labor history |
| Module 6 · Labor Law Map | 8 jurisdiction entries covering 9 named jurisdictions/regions (not legal advice) |
| Module 7 · Salary Negotiation | Full playbook |
| Module 8 · PIP Survival | From early warning to severance negotiation |
| Module 9 · Job Search & Interview | Full lifecycle |

Details: [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md).

---

## Install

```bash
# clone the repo
git clone https://github.com/workingclass-ai/workingclass.git
cd workingclass

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"

# Cursor
# When this repo is opened in Cursor, Cursor reads .cursor/rules/laborer-companion.mdc.
# To use it in another repo, copy skills/laborer-companion/ and .cursor/rules/laborer-companion.mdc.

# Claude Code (legacy Claude skills)
mkdir -p ~/.claude/skills
cp -R skills/laborer-companion ~/.claude/skills/
```

Then describe your workplace situation in the agent and the skill will activate. Or use slash commands:

```
/triage      - Start here when you don't know which module fits
/scan        - 60-second red-flag scan
/decode      - Decode boss/HR rhetoric
/overtime    - Overtime decision
/review      - Read a performance review
/jump        - Stay-or-leave decision
/history     - Historical perspective
/law         - Labor law lookup
/salary      - Salary negotiation
/pip         - PIP survival
/jobsearch   - Job search & interview
```

---

## Codex / Cursor support

- **Codex**: the skill lives in `skills/laborer-companion/`; UI metadata lives in `skills/laborer-companion/agents/openai.yaml`. After installing it under `${CODEX_HOME:-$HOME/.codex}/skills/`, trigger it with `$laborer-companion`.
- **Cursor**: this repo includes a Cursor Project Rule at `.cursor/rules/laborer-companion.mdc`. When the repo is opened in Cursor, Agent can use that rule to load `skills/laborer-companion/SKILL.md`.
- **General agent guidance**: root `AGENTS.md` provides Codex / Cursor-compatible repository instructions.

To reuse the skill in another project, copy `skills/laborer-companion/`, `.cursor/rules/laborer-companion.mdc`, and `AGENTS.md`, keeping the rule paths consistent.

---

## Labor law coverage

Module 6 currently has **8 jurisdiction entries** covering **9 named jurisdictions/regions**:

| Entry | Notes |
|-------|-------|
| Mainland China | Standalone file |
| Hong Kong / Taiwan | Two regions/jurisdictions sharing one file; rules must not be mixed; never label as countries |
| United States | Federal + California/New York focus |
| Canada | Federal + provincial differences flagged |
| Australia | Fair Work / Awards / unfair dismissal |
| United Kingdom | UK employment / ACAS / tribunal |
| European Union | Regional overview with Germany/France/Netherlands notes; not a per-member-state encyclopedia |
| India | Four Labour Codes + IT-industry FAQs |

So if you count Hong Kong and Taiwan separately, it's **9 named jurisdictions/regions**; counted by reference file / jurisdiction entry it's **8**. Hong Kong and Taiwan must be labelled **regions/jurisdictions**, never countries, in this project.

---

## Language support

Currently supported:

- 简体中文 / Simplified Chinese
- 繁體中文 / Traditional Chinese
- English
- Español / Spanish
- Français / French
- Português / Portuguese
- Deutsch / German

Default rule: the skill answers in whichever supported language the user writes in. Statute names, agencies, and contract clauses are kept in the official original with a short translation when useful. For Traditional Chinese, region-appropriate terms (Hong Kong / Taiwan) are preferred.

---

## Examples & tutorials

More examples in [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md). Good places to start:

```text
/triage
My manager has been distant lately and I can't articulate why. Help me figure out which module to use.
```

```text
/law
I work part-time in Hong Kong, 17 hours a week. HR says the statutory minimum wage only covers some industries. Is that correct?
```

```text
/review
Here is my performance review: [paste redacted content]
I went from "exceeds" last year to "meets" this year. Is this a danger signal?
```

We welcome more tutorials and real cases — especially:

- Labor-law examples from different jurisdictions/regions
- PIP / layoff / severance walkthroughs
- Salary negotiation scripts
- Interview anti-manipulation examples
- Redacted HR / manager email samples
- Real-world usage examples in Spanish, French, Portuguese, or German

---

## Core principles

1. **No calls for collective action** — this is a clarity tool for individual workers.
2. **Acknowledge real constraints** — never give reckless "quit immediately" advice.
3. **Stay intellectually honest** — don't shape advice for political comfort.
4. **User privacy first** — see `skills/laborer-companion/references/privacy-and-opsec.md`.
5. **Don't impersonate a lawyer** — provide frameworks and the questions worth asking, never substitute professional legal counsel.

---

## Privacy warning ⚠️

- This skill does not upload your conversation to any third party.
- But the conversation between you and your AI provider may be logged by the platform, depending on your account and privacy settings.
- **Do not use this tool on a company device or company network.**
- **Do not paste company confidential data into the AI** — redact first.

Details: [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md).

---

## Inspiration

- Koki Xu's anti-distillation skill (April 2026)
- Karl Marx on labor value and alienation
- E.P. Thompson, *The Making of the English Working Class*
- 150 years of concrete worker-movement cases
- Contemporary labor economics and workplace sociology

This tool creates nothing new. It translates 150 years of working-class collective wisdom into a form usable in the 2026 AI era.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We especially welcome:

- New rhetoric pattern cases (to make Module 1 more complete)
- Labor-law additions for your country/region/jurisdiction
- Successful salary / severance negotiation cases
- PIP experiences (anonymized)
- Translation work on user-facing READMEs

---

## License

Apache 2.0 — see [LICENSE](LICENSE).

The only request: **keep the tool's core mission — to serve workers**.

---

## A paragraph

Seeing your situation clearly doesn't change your situation. But clarity is the precondition for change. And often, accepting reality with eyes open (including "I can't leave yet") is better than enduring with eyes closed.

At least you know what you're doing.
