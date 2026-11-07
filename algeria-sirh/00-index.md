# Algerian SIRH — research and product spec

Goal: a build-ready specification for an Algerian HR/payroll system (SIRH),
covering payroll and costisation (including CASNOS), labour law and statutory
declarations, HR workflow, and localization/compliance operations.

**Scope: private sector only** (loi 90-11). Public-sector statutes, concours and
public pay grids are out of scope.

Status: **research complete, spec drafted.** All findings carry a source URL and
a confidence tag; `UNVERIFIED` items must be closed with counsel/primary sources
before they become blocking rules.

## Files

| File | Contents | Lines |
|---|---|---|
| `01-payroll-costisation.md` | SNMG, gross-to-net, IRG barème, CNAS, CASNOS, TFPC/TAPP, employer cost, bulletin de paie, declarations calendar | 862 |
| `02-legal-declarations.md` | Contracts, working time, leave, termination, discipline, statutory filings, records, loi 18-07 | 852 |
| `03-rh-workflow.md` | Hire-to-retire processes, approvals, roles, data and states (Mermaid maps) | 996 |
| `04-localization-compliance.md` | FR/AR + RTL, DZD formats, 2026 holidays, documents, e-signature, hosting, bank/CNAS integrations | 617 |
| `05-product-spec.md` | **Build spec**: modules, domain model, rule catalogue (PAY/LEG/TRM/DEC/COST/LOC), state machines, workflows, documents, NFRs, phases, golden tests, conflict register | — |
| `06-gap-analysis.md` | Horilla 2.0 vs the spec: scoreboard, must-fix defects, reuse map, build list, effort shape | — |
| `07-contrats-et-rotation.md` | Contract types (CDI/CDD/part-time/apprenticeship/home/interim/aided), trial, termination; shift systems 2x8/3x8/4x8, nightly limits, rotation rules, ITP/night premiums | 409 |
| `10-status-and-handoff.md` | **Read first**: snapshot, progress, decisions, known issues, resume commands | 180 |
| `09-m0-delivery-notes.md` | M0 stabilisation: commits, test evidence, decisions and known issues | 42 |
| `08-implementation-plan.md` | M0 stabilisation + M1 Algeria payroll core, task-by-task TDD plan | 1769 |

## Headline numbers (2026)

- **SNMG**: 24 000 DA/month from 1 Jan 2026 (`décret 26-01`) — not raised in 2024–25.
- **CNAS**: 9 % employee + 25 % employer + 0,5 % FNPOS = **34,5 %**, no ceiling.
- **IRG**: 0/23/27/30/33/35 %, 40 % abattement (1 000–1 500 DA), exemption
  ≤ 30 000 DA taxable; non-monthly bonuses 10 % flat.
- **Overtime**: +50 % minimum, cap 8 h/week (20 % of legal duration).
- **Leave**: 2,5 days/month, 30-day cap, reference year 1 July–30 June, +10 days south.
- **Maternity**: **150 days** at 100 % (loi 25-08); the 98-day text in `01` is stale.
- **TAP**: abolished 1 Jan 2024. TFPC 1 % (≥20 employees) + TAPP 1 %, **half-yearly**
  (20 July / 20 January).
- **CASNOS**: 15 %, base 12×SNMG → 240×SNMG (2026 rebase).
- **Employer cost**: ≈ **135,8 %** of gross in the general case (BTPH higher).

## Conflicts to close first

See `05-product-spec.md §12`. The three that change money or a legal deadline:
1. **Maternity 98 vs 150 days** — use 150.
2. **CNAS 25 % vs 26 % employer** — use 25 % + 0,5 % FNPOS.
3. **DAC deadline 15 vs 30 days** — implement 30 (portal), keep the legal 15 visible.

## Conventions

- `OFF` official, `REP` reputable secondary, `PRAC` practice, `UNV`/`UNVERIFIED`
  no source or sources conflict.
- "Law" and "common practice" are kept separate; they diverge often in Algeria.
- Figures are 2026 unless the source states otherwise.

## Still needs the client

SME vs large group / multi-company, collective agreement(s), hosting, e-signature
provider, BTPH in or out, CASNOS depth, bilingual depth, migration source.
