# 06 — Gap analysis: Horilla HRMS 2.0 vs the Algerian spec

Baseline: `horilla/horilla-hr`, branch `2.0`, version 2.3.0, cloned at
`/home/sidali/sirh`. Read-only comparison against `05-product-spec.md`. **Private sector only.**

Verdict: Horilla is a strong **framework** for this (Django 5.2, multi-company
managers, permissions/accessibility, audit log, scheduler, DRF API, payroll
component engine, leave/attendance/recruitment). It is **not** an Algerian
payroll system. Payroll rules, declarations and localization are the work.

---

## 1. Scoreboard

| Spec area | Horilla today | Verdict |
|---|---|---|
| Core HR / employee file | Complete, multi-company, audit | **Use** |
| Contracts | `Contract` model with wage type, dates, docs | **Extend** (CDD motive, trial, reclassification guard) |
| Time & attendance | Strong: shifts, biometric, overtime, geofence | **Configure** (Friday rest, weekend, Ramadan) |
| Leave | Types, balances, approvals, accrual | **Extend** (1 Jul–30 Jun, South +10, 150-day maternity) |
| Payroll engine | Components, formulas, tax brackets, payslips, batches | **Use + configure**, then **fix money type** |
| IRG | `TaxBracket` + `FilingStatus` (Python formula sandbox) | **Configure** barème + abattement; verify smoothing band |
| CNAS / CASNOS / TFPC / TAPP | No DZ model | **Build** |
| Declarations (DAS/DAC/G50/G29/ANEM/CACOBATPH) | No | **Build** |
| Costisation | Payslip totals, dashboards; no employer-cost model | **Build** (thin layer) |
| Bilingual FR/AR + RTL | `fr` and `ar` in `LANGUAGES`; translation files partial | **Extend + QA** |
| Holidays / Hijri | Holiday model with `recurring`; no official-communiqué workflow | **Extend** |
| Documents | Document requests + PDF generation | **Extend** templates |
| E-signature / ANPDP / retention | None | **Build** (policy + integration) |
| Bank payment files | No DZ bank/RIB format | **Build** adapters |
| Recruitment / onboarding / offboarding | Present | **Configure** ANEM + DZ docs |

---

## 2. Must fix before any Algerian deployment

These are defects found in the existing clone; they hit payroll/attendance directly.

| # | Defect | Where | Why it blocks |
|---|---|---|---|
| B1 | Weekly-off config 500s payroll/attendance (`int("")`, `month_calendar[4]`) | `base/methods.py:1678-1682`; form "All" at `base/forms.py:3725` | Any normal weekly-off setting breaks the run |
| B2 | Bulk payslip shortens the period for later employees | `payroll/views/component_views.py:826-831` | Silent underpayment |
| B3 | Bulk payslip run not atomic | same loop | Partial run + notifications |
| B4 | CSV formula injection in default quick export and contributions export | `horilla_views/views.py:1072-1078`, `payroll/views/contribution_views.py:151-168` | Security |
| B5 | Leave approval deducts balance without lock/transaction | `leave/views.py:1208-1241` | Double deduction |
| B6 | Balance save swallowed by bare `except: pass` | `leave/views.py:576-582` | Leave approved, balance not deducted |
| B7 | Money stored as `float` (44 fields) | `payroll/models/models.py:3679-3683` | Reconciliation drift |
| B8 | One unresolved attendance conflict zeroes the month on the legacy bulk path | `payroll/methods/methods.py:827-828` | Zero-pay payslip |

Fix B1–B6 first; B7 is a migration and should be scheduled with the DZ payload
work; B8 by routing all generation through `payroll/methods/batch_run.py`.

---

## 3. What maps cleanly (reuse, don't rebuild)

| Need | Existing asset | Action |
|---|---|---|
| Multi-company data isolation | `base/horilla_company_manager.py`, `base/middleware.py` | Keep; add `establishment` level if needed |
| Permission model | `accessibility` app + company-scoped backend | Keep; add payroll/médical/DPO roles |
| Audit trail | `horilla_audit`, `django-auditlog` | Keep; add field-level medical access log |
| Background jobs | `horilla/scheduling.py` + `run_scheduler` | Use for declaration reminders, CDD/trial/medical alerts |
| Pay element engine | `payroll/methods/component_engine.py`, `payslip_calc.py` | Reuse; add DZ flags (cotisable, imposable, SNMG, proratisable) |
| Tax formula sandbox | `payroll/methods/safe_tax_code.py` | Keep for CCN-specific formulas; DZ barème should be data, not code |
| Payslip/batch | `payroll/methods/batch_run.py`, `PayrollBatch` | Reuse; add maker-checker states |
| Exports | `horilla/export_safety.py`, `report/export.py` | Reuse `safe_cell` everywhere |
| API | `horilla_api/` (JWT, tenant-scoped) | Reuse; add DZ endpoints |
| PDF | `base/methods.py:generate_pdf`, xhtml2pdf | Reuse; add Arabic font + bilingual templates |
| Documents | `horilla_documents` | Reuse; add certificat/attestation/ATS templates |

---

## 4. Build list (new work)

### 4.1 Payroll — Algeria pack (large)

1. **Parameter tables, effective-dated**: `SNMG`, `IRG bracket`, `IRG abattement`,
   `IRG smoothing band`, `CNAS rate lines`, `FNPOS`, `CACOBATPH`, `TFPC/TAPP`,
   `CASNOS`. Every row: `effective_from`, `source_url`, `confidence`.
2. **CNAS base resolver** on the pay element (cotisable flag + exclusions + SNMG
   floor, no ceiling, BTPH overlay).
3. **IRG calculator** implementing `PAY-05…PAY-13` in the exact order; the
   30 001–35 000 band as a lookup, unit-tested at the boundaries.
4. **Non-monthly bonus path** at 10 % flat, separate from the barème.
5. **Employer cost engine** (`PAY-COST`): per employee / establishment / cost
   centre, paid vs productive hour, raise simulator, budget vs actual.
6. **Payslip template** with every art. 86 mention, FR/AR, 10-year retention.
7. **BTPH mode**: CACOBATPH contribution, no leave provision, DAS year Jul–Jun.
8. **CASNOS module** for non-salaried: base, 15 %, annual declaration/payment.

### 4.2 Declarations (large)

New app `algeria_declarations`:

- Models: `Declaration(type, period, due_date, status, amount, receipt, evidence)`.
- Generators: `DEA`, `DAC`, `DAS`, `G50`, `G29`, `ANEM recruitment`,
  `ANEM forecast`, `AT/MP`, `TFPC/TAPP`, `CACOBATPH DAS`.
- Controls: NIN/NSS completeness, headcount, totals vs payroll register,
  idempotent submission, receipt storage, rejected-run history.
- Calendar engine with alerts (D+10, +30, 1–20, +10, +48 h, 20 Jul/20 Jan).
- Portal integration is manual/import-export first; API later.

### 4.3 Labour rules (medium)

- Contract: CDD motive enum + reclassification warning, trial rules (6/12 months),
  CCN notice lookup, no rupture conventionnelle.
- Leave: reference period 1 Jul–30 Jun, first-month >15 days rule, 30-day cap,
  South +10 days, maternity 150 days + extensions, exceptional leave set, Hajj.
- Termination: procedure checklist (notification, hearing, minutes), exit
  documents, economic dismissal +3 months.
- Occupational health: visit types, due dates, fitness-only visibility,
  return-to-work block.

### 4.4 Localization (medium)

- Company/establishment locale object: UI, document, format, jurisdiction.
- DZD formats (comma decimal, space/dot thousands), `Africa/Algiers`, no DST.
- Holiday admin screen: fixed + religious with communiqué reference, versioned.
- Arabic PDF font embedding and RTL templates; bilingual prevailing-language clause.
- Glossary table FR↔AR for payroll terms; no machine translation of statutory codes.
- Retention/DPO: retention schedule, breach register (5 days), ANPDP authorisation
  reference, cross-border export block, biometric consent.

### 4.5 Bank / payments (small-medium)

- RIB (modulo-97) and CCP validation.
- Per-bank VIR.EDI/CSV adapters; dual-release workflow; value date vs payroll cut-off.

### 4.6 Costisation UI (small)

- Cost per employee/establishment/cost centre, monthly/annual.
- Budget vs actual, headcount, overtime cost, raise simulator (`×1,358` general,
  BTPH variant).
- Export with `safe_cell`.

---

## 5. Data migration

Fields Horilla lacks that must be imported or created: `NIN`, `NSS/CNAS`,
`CNAS employer no`, `NIF`, `NIS`, `CASNOS no`, `CACOBATPH no`, `wilaya`,
`collective_agreement`, `cdd_motive`, `trial_end`, `medical next_due`,
`RIB/CCP`, `category/coefficient`, `establishment`.

Migration order: company parameters → pay elements → contracts → employees →
balances → open declarations.

---

## 6. Effort shape (relative, not a quote)

| Stream | Size |
|---|---|
| Fix B1–B8 | S–M |
| DZ payroll pack + IRG + CNAS | L |
| Costisation | M |
| Declarations app | L |
| Labour rules (contract/leave/termination/medical) | M |
| Localization + documents | M |
| CASNOS | S–M |
| Bank / e-signature / ANPDP | M |
| Migration + test suite + QA | M |

A realistic first releasable Algerian payroll (MVP in `05 §10`) is **payroll +
CNAS/IRG + payslip + bank file + cost report + declaration calendar**, with the
rest of the compliance surface following.

---

## 7. Decisions needed from the client

Same eight as `05 §13`. Without the **size/segment** (SME vs large
group/multi-company) and the **collective agreement(s)**, notice, 13th month,
premiums, dismissal indemnity and overtime base stay parameters with no safe default.
