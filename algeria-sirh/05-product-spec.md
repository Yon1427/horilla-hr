# 05 — Algerian SIRH product specification (v0.1)

**Scope: private sector only** (loi 90-11). Public-sector statutes, concours and
public pay grids are out of scope.

Derived from `01-payroll-costisation.md`, `02-legal-declarations.md`,
`03-rh-workflow.md`, `04-localization-compliance.md`, `07-contrats-et-rotation.md`. Every rule below carries a
source tag back to those files; `UNVERIFIED` marks anything that must not ship as
a blocking rule before counsel/primary-source review.

Conventions: `[01 §x]`, `[02 §x]`, `[03 §x]`, `[04 §x]` point to the research file.
Confidence: **OFF** official, **REP** reputable secondary, **PRAC** practice,
**UNV** unverified / sources conflict.

---

## 1. Product shape

A multi-company, multi-establishment HR and payroll system for the Algerian
private sector, with
Arabic/French output, an effective-dated rules engine, and statutory declaration
extracts. One jurisdiction module (`DZ`) so a future country is a plugin, not a fork.

```
Core HR ─┬─ Contracts & documents
         ├─ Time & attendance ── Leave ── Payroll ── Costing
         ├─ Recruitment ── Onboarding ── Lifecycle ── Offboarding
         ├─ Training · Occupational health · Discipline
         ├─ Declarations (CNAS · DGI · ANEM · CACOBATPH · CASNOS)
         └─ Reporting · Admin & configuration
```

### Non-negotiable product principles

1. **Nothing legal is hard-coded.** SNMG, IRG brackets, CNAS split, TFPC/TAPP,
   leave accrual, overtime rates, notice and holidays are **effective-dated
   parameters** with a source and a version [03 design warning; 01 §10].
2. **One pay element object** with explicit flags: `cotisable_cnas`,
   `imposable_irg`, `counts_for_snmg`, `proratisable`, `cascade_order`,
   `monthly_recurring` vs `exceptional` [01 §10.1].
3. **Payroll is immutable once validated.** Corrections create a new version;
   payslip, bank file and declarations always reconcile [04 §4].
4. **Maker-checker on money.** Payroll, salary changes, bank file release and
   declarations need two people [03 §9.2].
5. **Locale is per company/establishment**, not global: UI language, document
   language, format locale, jurisdiction [04 §10.1].
6. **Every statutory figure is traceable** to a source URL and effective date;
   the admin UI shows it next to the value.

---

## 2. Domain model

### 2.1 Company / establishment
`legal_name_fr/ar`, `NIF`, `NIS`, `CNAS_employer_no`, `CASNOS_no`,
`CACOBATPH_no` (BTPH), `activity_code`, `wilaya`, `collective_agreement_id`,
`ri_deposit_date`, `payroll_calendar`, `rounding_policy`, `sector`
(general | BTPH), `locale` (see §9).

### 2.2 Employee
Identity (FR/AR names, birth, gender, nationality, photo), **NIN** (mandatory on
G29 since 2026 [01 §3.7]), **NSS/CNAS number**, address, contacts, dependants,
bank RIB/CCP, disability/pensioner flags (sensitive), hire/seniority dates,
category, position, establishment, manager, collective agreement, exit data.

### 2.3 Contract
`type` = CDI | CDD | APPRENTICESHIP | INTERIM, start/end, `cdd_motive_code`
(art. 12 [02 §1.3]), trial start/end, weekly hours, part-time/night/shift flags,
signed_at, language, documents, notice rule (CCN).

> CDI is the default and need not be written; CDD **must** state duration and
> motive, and a non-compliant CDD is reclassified as CDI (art. 14) [02 §1.1–1.3].

### 2.4 Pay element
`code`, labels FR/AR, type (fixed/variable/allowance/deduction/employer charge),
flags above, base rule, proration basis, effective dates, CCN/contract source,
journal account, cost centre rule.

### 2.5 Time
Timesheet: date, planned/worked/night/overtime hours, rest-day/holiday work,
absence type/reason, source (manual/clock/biometric/mobile), approval.

### 2.6 Payroll run and payslip
`payroll_period`, `run_id`, `batch`, per employee: base, allowances, overtime,
leave indemnity, gross, CNAS employee/employer, IRG base/withheld, net, bank
reference, payslip document id, status, version, approvals.

### 2.7 Leave
Type, accrual rule, reference period, balance, carry-over, request/approval,
justification, indemnity.

### 2.8 Medical visit
`type` = pre-employment | periodic | return-to-work | reassignment | spontaneous,
due/done, `fit_status` + restrictions only (never diagnosis), next due.
Occupational health data is held by the physician; HR sees fitness only [02 §7.9].

### 2.9 Declaration
`type`, period, due date, status, amount, receipt ref, evidence, rejection reason.

### 2.10 CASNOS entity (non-salaried)
Activity, registration, declared annual income, base (min 12×SNMG, max 240×SNMG),
15 % contribution, payment schedule. A person can be salaried (CNAS) **and**
CASNOS at the same time [01 §5.1].

---

## 3. Rule catalogue

Each rule is an object: `id`, `inputs`, `output`, `effective_from`, `source`,
`confidence`, `edge_cases`, `tests`.

### 3.1 Payroll — PAY

| ID | Rule | Notes / confidence |
|---|---|---|
| PAY-01 | **SNMG floor** = 24 000 DA/month (138,46 DA/h) from 1 Jan 2026 | `décret 26-01` [01 §0] OFF; version the value |
| PAY-02 | **CNAS base** = cotisable elements; floor SNMG; **no ceiling** | excl. family benefits, expense reimbursements, exceptional indemnities, qualifying residence allowance [01 §4.2] OFF |
| PAY-03 | **CNAS split** = 9 % employee + 25 % employer + 0,5 % FNPOS = **34,5 %** | no ceiling; older "26/9" is a double count [01 §4.1, 02 §7.3] OFF |
| PAY-04 | **BTPH overlay** = +12,21 % CACOBATPH congés payés +0,375 % employer chômage-intempéries; employer load ≈ 38,085 %; no leave provision | [01 §4.3] OFF |
| PAY-05 | **IRG taxable base** = gross taxable − employee CNAS 9 % − pension withholding | order matters [01 §3.3] OFF |
| PAY-06 | **IRG exemption** ≤ 30 000 DA/month taxable | [01 §3.2] OFF |
| PAY-07 | **IRG barème** 0 / 23 / 27 / 30 / 33 / 35 % on monthly slices 0–20k, 20k–40k, 40k–80k, 80k–160k, 160k–320k, >320k | CIDTA art. 104, LF 2022, unchanged 2026 [01 §3.2] OFF |
| PAY-08 | **40 % abattement on the tax**, floor 1 000 / cap 1 500 DA/month | [01 §3.4] OFF |
| PAY-09 | **Smoothing band** 30 000–35 000 DA: `IRG = IRG×(137/51) − 27 925/8`, floor 0 | **boundary at 35 000 is UNV**; implement the official DGI lookup and test 30 000 / 30 001 / 34 999 / 35 000 / 35 001 [01 §3.9] |
| PAY-10 | **Disabled/pensioner band** up to 42 500 DA: `IRG = IRG×(93/61) − 81 213/41`, replaces the normal band | [01 §3.3] OFF |
| PAY-11 | **No family quotient, no per-child IRG reduction**; dependants recorded but tax-neutral | [01 §3.5] OFF |
| PAY-12 | **Non-monthly bonus / arrears** → **10 % flat**, separate payment, no abattement | monthly recurring bonus stays in the barème [01 §3.6] OFF |
| PAY-13 | **Exempt items** (mission, zone, family allowances, AT/MP benefits, unemployment, dismissal indemnity, residence ≤70 % of base) | [01 §3.6] OFF |
| PAY-14 | **Overtime**: +50 % minimum; **cap 20 % of legal duration = 8 h/week**; exceptions require representatives + inspector notification | [01 §2.4, 02 §2.5] OFF |
| PAY-15 | **Night window** 21:00–05:00; night premium per CCN | [02 §2.3] OFF |
| PAY-16 | **Daily amplitude** 12 h; minimum 5 working days/week; 40 h/week | [02 §2.1] OFF (12 h article number UNV) |
| PAY-17 | **Ramadan hours** = company/CCN policy, default no change for private sector | [02 §2.7] PRAC/UNV |
| PAY-18 | **Proration** for hire/exit/part-time/unpaid absence; basis configurable (30 days / working days / 173,33 h) | [01 §10.4] PRAC |
| PAY-19 | **Rounding** chosen per company (2 dp or nearest dinar) and applied consistently | no legal rule [01 §10.3] PRAC |
| PAY-20 | **Advance/loan repayment cap** = company policy; no statutory cap located | [01 §10.4] UNV |
| PAY-21 | **Payslip** must itemise every element by name and amount (art. 86); IRG line or "néant" wording | [01 §8, 02 §8] OFF |

### 3.2 Leave and working time — LEG

| ID | Rule | Notes |
|---|---|---|
| LEG-01 | Annual leave **2,5 days/month**, cap **30 calendar days/work year** | art. 41 [02 §3.1] OFF |
| LEG-02 | Reference period **1 July → 30 June**; new hire from hire date | art. 40 [02 §3.1] OFF |
| LEG-03 | First month: >15 working days counts as a full month | art. 44 [02 §3.1] OFF |
| LEG-04 | Equivalences: 24 working days / 4 weeks = 1 month; 180 h seasonal/part-time | art. 43 OFF |
| LEG-05 | **South wilayas +10 days** minimum per year | art. 42 OFF |
| LEG-06 | Leave indemnity = **1/12 of reference-year remuneration** | art. 52 OFF |
| LEG-07 | Carry-over and exit payout: **not statutory** → configurable | [02 §3.1] UNV |
| LEG-08 | Sick leave: CNAS pays 50 % first 15 days, 100 % from day 16 / hospitalisation / long-term; declaration within 2 working days | [02 §3.2] REP |
| LEG-09 | **Maternity 150 consecutive days at 100 %** (loi 25-08), start ≤42 days before due date; extensions 50 then up to 165 days for medical cases | art. 29 [02 §3.3] OFF |
| LEG-10 | Paternity = 3 paid exceptional days (birth), no separate paternity leave | art. 54 OFF |
| LEG-11 | Exceptional leave 3 paid days: marriage, birth, child marriage, death (ascendant/descendant/1st-degree collateral/spouse), circumcision | art. 54 OFF |
| LEG-12 | Hajj once per career; duration not specified → configurable | UNV |
| LEG-13 | Staff delegate credit 10 h/month | arts. 106–107 OFF |
| LEG-14 | Return-to-work medical visit after AT/MP, maternity, ≥21 days sick, repeated absences | décret 93-120 [02 §7.9] OFF |
| LEG-15 | Periodic medical visit 12 months; 6 months for reinforced categories | OFF |

> **Maternity conflict to resolve before build:** `01 §2.4` and `01 §10.3` still
> say 98 days; `02 §3.3` documents **150 days** under loi 25-08 (July 2025) and
> `03` uses 150. **Use 150 days** and delete the 98-day text. Flagged **CONFLICT**.

### 3.3 Termination — TRM

| ID | Rule | Notes |
|---|---|---|
| TRM-01 | Termination modes are the exhaustive art. 66 list; **no rupture conventionnelle** | [02 §1.2, §5.1] OFF |
| TRM-02 | During trial: terminate any time, no notice, no indemnity | art. 20 OFF |
| TRM-03 | Notice duration = **CCN only**, no statutory number → store per CCN/contract | [02 §5.2] UNV |
| TRM-04 | **No general statutory dismissal indemnity** (art. 72 repealed 1994) → per CCN/RI | [01 §7.1, 02 §5] OFF/PRAC |
| TRM-05 | Economic dismissal: +3 months' average salary (CNAC) plus CCN provisions | décret 94-09 [01 §6.3] REP |
| TRM-06 | Exit documents: certificat de travail (art. 67), attestation de salaire, final settlement, CNAS cessation | [02 §5.6] OFF |
| TRM-07 | CDD expiry alert J-60/J-30/J-7; any renewal chain raises reclassification risk | [02 §10.3] PRAC |

### 3.4 Declarations — DEC

| ID | Declaration | Trigger | Deadline | Confidence |
|---|---|---|---|---|
| DEC-01 | CNAS employer affiliation | first hire | **D+10** | OFF |
| DEC-02 | CNAS employee affiliation (DEA) | each hire | **D+10** | OFF |
| DEC-03 | CNAS **DAC** | period end | **+30 days** (monthly if ≥10 employees, quarterly if <10); loi says 15 days — portal enforces 30 | OFF + **UNV conflict** |
| DEC-04 | CNAS **DAS** | 31 Dec | **+30 days** (≈30 Jan) | OFF |
| DEC-05 | DGI **G50** (IRG + other) | month end | **1st–20th** of following month | OFF |
| DEC-06 | DGI **G29** annual salaries | year end | **30 April** N+1; NIN mandatory 2026 | OFF |
| DEC-07 | DGI **G1** personal income | year end | **30 June** | OFF |
| DEC-08 | **ANEM** recruitment | month end | **+10 days** | OFF |
| DEC-09 | **ANEM** manpower forecast | quarter | **1 month before** quarter | OFF |
| DEC-10 | Workplace accident | knowledge | **+48 h** | OFF |
| DEC-11 | TFPC + TAPP | half-year | **20 July** / **20 January**; zero declaration mandatory | OFF |
| DEC-12 | CACOBATPH DAS (BTPH) | year 1 Jul–30 Jun | **31 July** | OFF |
| DEC-13 | CASNOS income declaration / payment | annual | 31 Jan / 30 Jun (agriculture 1 Oct) | REP |
| DEC-14 | Règlement intérieur deposit | adoption | **+8 days** | OFF |

### 3.5 Costisation — COST

```
monthly_cost = G + s·A + t·G + p·G + r
s = 0.255 general | 0.38085 BTPH
t = 0 .. 0.02   (TFPC 1% + TAPP 1%, net of eligible spend)
p = 0.0833 general | 0 BTPH (CACOBATPH pays leave)
r = CCN provisions (13th month, notice, indemnities) — company-specific
cost_per_paid_hour   = monthly_cost / 173.33
cost_per_productive_hour = annual_cost / ~1828  (after leave + 14 public holidays)
raise_factor = 1 + 0.255 + t + p  ≈ 1.358 general
```

Worked reference case (illustrative, 80 000 DA gross, non-BTPH, no training
spend): net **60 844**, employer cost **108 666,67/month**, **626,99/paid hour**,
**1 304 000/year**, a 1 000 DA raise costs **1 358,33/month** [01 §7.2].

Costing must expose: per employee, per establishment, per cost centre, per
month/annual, budget vs actual, headcount, overtime cost, raise campaign simulator.

### 3.6 Localization — LOC

| ID | Rule |
|---|---|
| LOC-01 | Currency **DZD**; display `1 234 567,89 DA` (fr) / `1.234.567,89 د.ج` (ar); store `DECIMAL(15,2)` |
| LOC-02 | Machine formats (CSV/API/bank): UTF-8, `.` decimal, no separators, ISO dates |
| LOC-03 | Dates `dd/mm/yyyy`; storage ISO; timezone **Africa/Algiers** UTC+1, no DST |
| LOC-04 | Hijri display only; **never compute** whether a religious day is a holiday |
| LOC-05 | Holidays: fixed list + officially proclaimed religious dates, admin-confirmed with communiqué reference, versioned per year |
| LOC-06 | Document language per company; bilingual PDFs state the prevailing language |
| LOC-07 | E-signature: only **qualified** = handwritten equivalent (loi 26-02); simple click = evidence only; wet fallback |
| LOC-08 | Data protection: loi 18-07/25-11; ANPDP declaration/authorisation; biometrics need prior authorisation; breach notification **5 days** |
| LOC-09 | Retention: payroll/accounting **10 years**; contracts life + 10; biometrics deleted at exit |
| LOC-10 | Bank: RIB modulo-97 validation, CCP support, per-bank VIR.EDI/CSV adapter |

---

## 4. State machines

**Employee:** `PREBOARDING → ACTIVE_PROBATION → ACTIVE_CONFIRMED → SUSPENDED → NOTICE → TERMINATED → ARCHIVED`
- Never auto-confirm silently at trial end; require a decision, then alert.
- Dismissal to NOTICE requires a completed procedure checklist.

**CDD:** `DRAFT → ACTIVE → EXPIRING(60) → RENEWAL_PENDING | CONVERSION_PENDING | EXPIRED → ARCHIVED`
- Block ACTIVE without motive + end date; flag renewal chains.

**Payroll run:** `DRAFT → CALCULATED → REVIEW → APPROVED → PAID → CLOSED`
- Recalc from REVIEW; corrections after APPROVED create a new version.

**Declaration:** `DRAFT → VALIDATED → SUBMITTED → ACCEPTED | REJECTED → PAID → ARCHIVED`
- SUBMITTED requires receipt + evidence; REJECTED reopens with reason, original kept.

**Leave:** `DRAFT → PENDING_MANAGER → PENDING_HR → APPROVED | REJECTED → CANCELLATION_REQUESTED → CANCELLED`
- Lock the balance row and wrap in a transaction at every state change.

**Medical visit:** `DUE → SCHEDULED → DONE → FIT | FIT_WITH_RESTRICTION | UNFIT → NEXT_DUE_SET`.

---

## 5. Workflows to ship

1. **Recruitment → offer**: requisition/approval, sourcing (ANEM, Emploi.dz), interviews, offer, pre-employment medical, candidate data retention [03 §1].
2. **Onboarding**: contract, CNAS DEA (D+10), employee file, registre, medical visit, payroll setup, probation tracking [03 §2].
3. **Time & attendance**: shifts, Friday rest + configurable weekend, Ramadan template, biometric import, overtime request/approval with cap alerts [03 §3].
4. **Leave**: request → manager → HR → balance update (locked); sick/maternity with CNAS forms; leave planning for the 1 July–30 June year [03 §4].
5. **Lifecycle events**: transfer, promotion, salary revision (maker-checker), discipline procedure, suspension, return-to-work [03 §5].
6. **Offboarding**: resignation/dismissal/end of CDD/retirement, clearance checklist, final settlement, certificat + attestation, CNAS cessation, asset return [03 §6].
7. **Training**: plan, sessions, evaluation, TFPC/TAPP eligible-spend tracking [03 §7].
8. **Occupational health**: visit scheduling, fitness-only visibility, return-to-work blocking [02 §7.9].
9. **Declarations**: prepare → validate → submit on portal → store receipt → reconcile → archive [02 §7, 01 §9].

---

## 6. Documents

One document engine, two templates (`fr`, `ar`), one data contract. No in-place
edit after validation; corrections create a new version.

Must generate: contrat CDI/CDD + avenant, bulletin de paie, attestation de
travail, attestation de salaire, ATS (CNAS), certificat de travail, ordre de
virement, reçu de solde de tout compte, CDD renewal/conversion, disciplinary
notices/minutes, CNAS DEA/DAC/DAS extracts, G50/G29 extracts, ANEM declarations,
AT/MP declaration, medical aptitude sheet, règlement intérieur + deposit receipt,
data-protection notices and breach notification [02 §10.4, 04 §4].

---

## 7. Permissions and audit

Roles: `PAYROLL_ADMIN`, `HR_ADMIN`, `HSE/OH`, `MANAGER`, `DPO`, `AUDITOR`,
`EMPLOYEE`. Hard rules:

- Medical: separate store, field-level encryption, HR sees fitness only.
- Biometric: consent + ANPDP authorisation + alternative method + delete on exit.
- Payroll: maker-checker, no self-approval, immutable audit trail.
- Declarations: four-eyes, receipt stored, rejected submissions never deleted.
- Exports: log who exported what; block cross-border transfer without a reference.
- Audit: who viewed/changed which field, when, from where.

---

## 8. Reporting

Standard: headcount, turnover, absenteeism, overtime, leave balances, payroll
register, CNAS/DAS reconciliation, IRG recap, cost per employee/establishment/
cost centre, budget vs actual, raise simulator, declaration calendar and status,
CDD/trial/medical expiry, training spend vs TFPC/TAPP.

Every report: filter by company, establishment, department, period; export
XLSX/CSV/PDF with `safe_cell` on every cell (formula-injection guard).

---

## 9. Non-functional requirements

- **Performance**: 500-employee payroll calculation < 2 min; payslip PDF < 1 s
  each after calculation; list screens < 500 ms at 10k employees.
- **Correctness**: golden-test suite (§11) runs on every rules change; payroll
  cannot be approved if any control fails.
- **Security**: RBAC + object-level scoping per company/establishment; encrypted
  medical data; audit log append-only; rate-limited login; CSRF on every
  state-changing endpoint.
- **Availability**: payroll run resumable; declarations idempotent; no
  double-submit.
- **Data residency**: in-Algeria hosting by default; offshore requires ANPDP
  authorisation reference on the company record.
- **Localization QA**: every screen and PDF tested in both languages and RTL.

---

## 10. Delivery phases

**MVP (must have to pay one company)**
Core HR + contracts, time/leave basics, payroll engine (PAY-01…PAY-14, PAY-21),
CNAS/IRG calculation, payslip PDF, bank file, cost report, declaration calendar,
audit log, role separation.

**v1 (compliance-complete)**
All declarations + extracts, documents engine, medical visits, CDD/trial alerts,
multi-establishment, BTPH overlay, CASNOS module, bilingual documents, e-signature
integration, leave reference period and South rule.

**v2 (scale)**
Recruitment, onboarding/offboarding, training + TFPC/TAPP tracking, budgeting and
raise simulator, integrations (CNAS/DGI/banks/biometric), ANPDP/DPO tooling,


---

## 11. Golden tests (seed the suite with these)

1. **IRG boundaries**: taxable 30 000 → 0; 30 001, 34 999, 35 000, 35 001 →
   compare to the official DGI table; 42 500 disabled/pensioner boundary.
2. **CNAS**: gross 80 000 → employee 7 200, employer 20 000, FNPOS 400; total
   34,5 %; no ceiling above 320 000.
3. **Gross-to-net**: 80 000 → IRG 11 956 → net 60 844 [01 §7.2].
4. **Employer cost**: 80 000 → 108 666,67; raise 1 000 → 1 358,33.
5. **BTPH**: employer load 38,085 %, no leave provision.
6. **Leave**: hire 20 June → accrual from hire date; 2,5/month; 30-day cap;
   South +10; reference period 1 July–30 June.
7. **Overtime**: 8 h/week cap alert; +50 %; rest-day compensation.
8. **Maternity**: 150 days, 100 %, start ≤42 days before due date.
9. **CDD**: missing motive → block; expiry alerts at J-60/30/7; renewal chain
   warning.
10. **Declaration deadlines**: DEA D+10, DAC +30, DAS +30, G50 1–20, ANEM +10,
    AT/MP +48 h, TFPC/TAPP 20 Jul & 20 Jan.
11. **CSV/XLSX export**: a name starting with `=` is neutralised in every cell.
12. **Money**: no float drift when summing 500 payslips.

---

## 12. Conflicts and verification register

These must be closed before the rule ships as blocking.

| # | Conflict / gap | Files | Decision for now |
|---|---|---|---|
| C1 | Maternity **98 vs 150 days** | 01 §2.4/§10.3 vs 02 §3.3, 03 | Use **150** (loi 25-08); delete 98 |
| C2 | CNAS **employer 25 % vs 26 %** | 01 §4.1, 02 §7.3 | Use **25 % + 0,5 % FNPOS**, table-driven |
| C3 | DAC deadline **15 vs 30 days** | 01 §4.4, 02 §7.3 | Implement 30 (portal), show legal 15 |
| C4 | IRG **band join at 35 000** | 01 §3.9 | Use DGI lookup table; test boundaries |
| C5 | Notice duration | 02 §5.2 | CCN parameter, no default |
| C6 | CDD max duration / renewal cap | 02 §1.3 | No statutory cap; warn on chains |
| C7 | Weekend | 02 §2.2, 04 §3.1 | Statutory rest = Friday; weekend per establishment |
| C8 | Ramadan hours (private) | 02 §2.7 | No statutory change; policy parameter |
| C9 | 2026 religious holidays | 04 §3.2 | Only Eid al-Adha confirmed; others admin-confirmed |
| C10 | CASNOS 2026 base/rate | 01 §5.2 | REP; verify decree 26-257 |
| C11 | DAS exact day (30 vs 31 Jan) | 02 §7.4, 04 §4 | +30 days, shift rule UNV |
| C12 | TFPC/TAPP effective rate & eligible spend | 01 §6.2 | Version by finance law |
| C13 | Payslip retention (5 vs 10 years) | 01 §8.4, 04 §5.3 | 10 years |
| C14 | E-payslip delivery legal value | 04 §5.2 | Portal + timestamp; UNV |
| C15 | Public-sector rules | 03 §1.5 | Out of scope — private sector only |
| C16 | Transport/panier IRG treatment | 01 §10.4 | Parameter + written tax position |
| C17 | Overtime hourly base | 01 §10.4 | CCN parameter |
| C18 | Advance repayment cap | 01 §10.4 | Company policy |

---

## 13. Open product decisions (need the client)

1. **Target size**: private SME, or large enterprise/multi-company group. It
   changes approval thresholds, hosting and declaration volume.
2. **Collective agreement(s)** to support at launch; notice, 13th month, premiums
   and dismissal indemnity come from there.
3. **Hosting**: in-Algeria only, or offshore with ANPDP authorisation.
4. **E-signature provider**: integrate a qualified provider on the ANCE trusted
   list, or ship wet-signature fallback first.
5. **BTPH**: in scope at launch? It changes CNAS base, leave provision and DAS year.
6. **CASNOS**: full module (non-salaried) or only a flag on the employee record?
7. **Bilingual depth**: French-first UI with Arabic documents, or full Arabic UI
   at launch.
8. **Migration**: import from Excel or an incumbent payroll system; which fields
   are authoritative.
