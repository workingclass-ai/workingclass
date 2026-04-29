# 劳动法快速查询 / Labor Law Quick Reference

> **Index last verified**: 2026-04-29
>
> This is a legal map, not legal advice. Always confirm current law through official sources and a qualified local employment/labour lawyer before acting.

## How to use

1. Identify the user's **work jurisdiction**: country/region, state/province, city when relevant, and whether they are employee/contractor/worker.
2. Read only the matching jurisdiction file below.
3. If the user is remote, cross-border, on a visa/work permit, union-covered, or facing dismissal/discrimination/harassment, recommend local legal advice early.
4. For current legal thresholds, deadlines, minimum wages, or statutory formulas, prefer official sources linked in the jurisdiction file.

## Jurisdiction Files

| Jurisdiction | Read this file | Use when user says |
|---|---|---|
| 中国大陆 | `references/labor-law-china-mainland.md` | 中国大陆、内地、北京、上海、深圳、996、劳动仲裁 |
| 香港 / 台湾 | `references/labor-law-hong-kong-taiwan.md` | 香港、Hong Kong、台湾、Taiwan、劳基法、Employment Ordinance |
| United States | `references/labor-law-united-states.md` | US, USA, California, New York, H1B, at-will, FLSA, EEOC |
| Canada | `references/labor-law-canada.md` | Canada, Ontario, BC, Alberta, Quebec, severance, common law notice |
| Australia | `references/labor-law-australia.md` | Australia, Fair Work, award, unfair dismissal, redundancy |
| United Kingdom | `references/labor-law-united-kingdom.md` | UK, England, Scotland, Wales, Northern Ireland, ACAS, tribunal |
| European Union | `references/labor-law-european-union.md` | EU, Germany, France, Netherlands, works council, AI Act |
| India | `references/labor-law-india.md` | India, labour codes, IT services, forced resignation, bond |

## Universal First Questions

Ask these before giving legal-specific guidance:

- Where do you physically work, and what jurisdiction governs your employment contract?
- Are you an employee, contractor, intern, fixed-term worker, casual worker, or agency worker?
- What is the issue: overtime, dismissal, severance, discrimination, harassment, non-compete, wage arrears, leave, visa/work permit, or AI/monitoring?
- Is there a deadline: signing a severance agreement, tribunal/agency filing period, visa grace period, or final working day?
- Is there a protected-status angle: pregnancy/parental leave, disability, age, race, sex/gender, union activity, whistleblowing, medical leave, harassment complaint?

## When To Stop And Escalate

Strongly recommend a local employment/labour lawyer or official advice channel when:

- The user has been dismissed, forced to resign, or given a severance/settlement agreement.
- The user alleges discrimination, sexual harassment, retaliation, whistleblowing, pregnancy/parental leave retaliation, disability accommodation failure, or union retaliation.
- The user is on a visa/work permit and termination affects immigration status.
- The user is asked to sign a waiver, release, restrictive covenant, non-compete, repayment clause, or confidentiality clause they do not understand.
- There is significant money at stake, wage theft, unpaid bonus/commission/equity, or stock option forfeiture.
- The user works cross-border or remotely across jurisdictions.

## Output Shape

When answering a legal question, use:

```markdown
## 你在 [法域] 的法律地图 / Legal Map

### 先确认
[jurisdiction, worker classification, deadlines, visa/union/protected-status flags]

### 纸面规则
[plain-language rule with statute/source name]

### 现实执行
[what usually happens in practice and where enforcement is weak/strong]

### 现在该做
[3-5 evidence-preserving, low-risk steps]

### 该问律师/官方机构的问题
[specific questions]

### 权威来源
[official source links from the jurisdiction file]
```

## Important Limits

- Do not say "this is legal/illegal" without the jurisdiction and enough facts.
- Do not invent current thresholds or filing deadlines. If not in the jurisdiction file, tell the user to verify through official sources.
- Do not advise the user to sue or not sue. Explain options and questions to ask a lawyer.
- Do not let legal analysis override safety: if the user is in acute mental-health crisis, use `references/acute-crisis-escalation.md` first.
