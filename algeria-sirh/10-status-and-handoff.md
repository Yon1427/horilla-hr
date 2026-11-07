# 10 — Status & handoff (trust document)

**Read this first in a new session.** It records what is done, what is in
flight, what remains, and the exact commands. If this file and an older note
disagree, this file wins; if this file and the code disagree, the code wins.

## Snapshot

| Item | Value |
|---|---|
| Date | 2026-11-08 |
| Repo | `/home/sidali/sirh` |
| Fork | `github.com/Yon1427/horilla-hr` (from `horilla/horilla-hr`, branch `2.0`, base `bba4b37`) |
| Working branch | `algeria/m0-m1` |
| HEAD | `3cd9730 docs(algeria): M0 delivery notes and test evidence` |
| Upstream | `fork/algeria/m0-m1` (pushed through `3cd9730`) |
| Runtime | Docker Compose: `db` (Postgres 16) + `redis` up; image `sirh-web` built |
| Python | 3.12 / Django 5.2.19 (in the image) |
| Scope | Algerian **private sector only** (loi 90-11) |

## Source of truth

1. `00-index.md` — reading order and conflicts.
2. `05-product-spec.md` — rule catalogue (PAY/LEG/TRM/DEC/COST/LOC), §12 conflicts.
3. `06-gap-analysis.md` — defects B1–B8 and the Horilla build map.
4. `07-contrats-et-rotation.md` — contract types and shift/rotation rules.
5. `08-implementation-plan.md` — M0/M1 tasks, exact files and tests.
6. `09-m0-delivery-notes.md` — M0 evidence and decisions.
7. `01`–`04` — research (payroll, legal, workflow, localization).

## Agent squad (OpenCode, V2)

| Agent | Mode | Model | Purpose |
|---|---|---|---|
| `sirh-lead` | primary | `opencode-go/deepseek-v4-pro#high` | sequencing, review, money/migration/scoping gates |
| `sirh-payroll` | subagent | `opencode-go/deepseek-v4.1-flash#high` | M0 fixes + M1 payroll core |
| `sirh-legal` | subagent | `opencode-go/muse-spark-1.3-contributor#high` | law, declarations, data contracts (read-only code) |
| `sirh-qa` | subagent | `opencode-go/crouton-alpha-free#high` | regression suite, golden cases, CI gates |
| `sirh-explore` | subagent | `opencode-go/deepseek-v4.1-flash#high` | read-only reconnaissance |

Config: `.opencode/agents/*.md`, `.opencode/opencode.json` (`default_agent: sirh-lead`).

---

## Progress

### M0 — stabilisation: **complete** (8/8)

| Task | Commit | Result |
|---|---|---|
| M0-1 weekly-off calendar, Sunday-first | `235ed7e` | `base` + `attendance` green (293) |
| M0-2/M0-3 bulk period + atomic run | `dfe4c8b` | 25 targeted OK; rollback proven |
| M0-4 CSV formula injection | `22b1dfa` | 48 targeted OK |
| M0-5/M0-6 leave lock + no swallowed save | `6590aea` | 10 targeted OK; leave 136 OK |
| M0-8 conflict blocks | `0d994f5` | 41 targeted OK |
| M0-7 Decimal money + migration 0016 | `8474210` | 115 targeted OK; payroll 1,011 (4 test fixes re-run 54 OK) |

Baseline before M0: 1,491 tests OK (1 expected failure).

### M1 — Algerian payroll core: **in flight**

| Task | State | Files |
|---|---|---|
| M1-9 parameter model | **written, uncommitted** | `payroll/models/tax_models.py` (`AlgeriaPayrollParameter`), `payroll/migrations/0017_algeria_payroll_parameter.py`, `payroll/tests/test_dz_parameters.py` |
| M1-10 2026 seed | **written, uncommitted** | `payroll/migrations/0018_seed_algeria_parameters_2026.py` |
| M1-11 IRG engine | **not started** | `payroll/methods/dz_irg.py`, `payroll/tests/test_dz_irg.py` |
| M1-12 `FilingStatus.tax_engine` | **not started** | `payroll/models/models.py`, `payroll/methods/tax_calc.py`, migration `0019` |
| M1-13 component seed command | **not started** | `payroll/management/commands/seed_algeria_payroll.py` |
| M1-14 80,000 DA golden payslip | **not started** | `payroll/tests/test_dz_payroll_golden.py` |
| M1-15 employer cost | **not started** | `payroll/methods/dz_cost.py`, `payroll/tests/test_dz_cost.py` |
| M1-16 delivery notes + gate | **not started** | `algeria-sirh/`, `Makefile` gate |

**Full four-app gate:** running in the background when this file was written
(`base payroll leave horilla_views`). Result not yet recorded. The test DB is
preserved (`--keepdb`) and has migrations through `0016`; the next test run
applies `0017`/`0018`.

### M2–M7 — not started

| Milestone | Scope | Acceptance |
|---|---|---|
| M2 Declarations | DEA, DAC, DAS, G50, G29, ANEM, AT/MP, TFPC/TAPP, CACOBATPH | one golden file per declaration, receipt + status |
| M3 Contracts & shifts | CDD motive/requalification, part-time, trial; `ShiftPattern`/`RotationRule` | rejects 12 h+ and no-rest patterns; CDD without motive |
| M4 Localization | FR/AR documents, DZD formats, holidays, e-signature, retention/ANPDP | bilingual PDF snapshot; holiday correction recomputes closed payroll |
| M5 CASNOS + BTPH + bank | CASNOS 15 %, BTPH 38.085 %, RIB/VIR.EDI | CASNOS golden; BTPH cost differs; RIB checksum |
| M6 Costisation UI | per employee/establishment/cost centre, budget, raise simulator | totals reconcile to `compute_employer_cost` |
| M7 Hardening | ANPDP/DPO, audit, load test | 500-employee payroll < 2 min; breach evidence |

---

## Decisions (do not silently reverse)

1. **Week starts Sunday.** Algerian weekend is Friday–Saturday. `month_week_index`
   uses `(first.weekday() + 1) % 7`; calendar is `setfirstweekday(6)`; the
   “every week” column is `(based_on_week_day + 1) % 7`.
2. **Money is Decimal at rest, float in the engine.** `save_payslip` quantizes to
   2 dp; read sites that mix with engine floats convert explicitly. Do not remove
   those `float(...)` without converting the engine.
3. **Conflicts block.** `unresolved_conflicts > 0` raises `PayrollBlockedError`;
   `bulk_generate` reports per employee and continues.
4. **Leave approval is locked under the company-scoped manager** with
   `select_for_update(of=("self",))` (plain full-row `FOR UPDATE` fails on
   PostgreSQL because of the manager’s nullable outer join).
5. **No `except: pass` around money writes.** The balance and the approved status
   land together or not at all.
6. **Effective-dated parameters.** SNMG, IRG, CNAS, TFPC/TAPP, CASNOS are data
   rows with `effective_from` + `source_url`; never hard-coded.
7. **CNAS is a normal `Deduction`** (`rate=9`, `employer_rate=25.5`,
   `is_pretax=True`, `is_tax=False`) once M1-13 exists — no parallel engine.
8. **DZ IRG is a `FilingStatus.tax_engine` switch** (`standard` | `dz_irg`), not a
   second payroll engine.

## Known issues / risks

1. Background mail threads (`leave/threading.py`) render templates after the
   request; `default_currency` then inserts `PayrollSettings` for a company that
   may be gone. Tests log an FK `IntegrityError` without failing. Fix: make the
   context processor read-only.
2. `leave_request_creation` uses `referer_parts[-2]` on an unvalidated referer
   (pre-existing `IndexError` risk).
3. The 2026 parameter values (SNMG 24,000, CASNOS base, IRG 35,000 boundary) come
   from research marked `REP/UNV`; confirm against primary texts before they
   become blocking rules.
4. `payroll` full suite after M1-9/10 is **not yet run**; the new model and
   migrations are unapplied to the test DB.
5. Do **not** run two `manage.py test` commands at once: they share
   `test_horilla_db`.

## Exact commands

```bash
# bring the stack up (image already built)
cd /home/sidali/sirh
docker compose up -d db redis

# run a test target (always --keepdb; one at a time)
docker compose run --rm -e HORILLA_SKIP_RELEASE_TASKS=1 web \
  python manage.py test payroll.tests.test_dz_parameters --verbosity 2 --keepdb

# migration safety
docker compose run --rm -e HORILLA_SKIP_RELEASE_TASKS=1 web \
  python manage.py makemigrations --check --dry-run

# full gate (about 20 minutes)
docker compose run --rm -e HORILLA_SKIP_RELEASE_TASKS=1 web \
  python manage.py test base payroll leave horilla_views --verbosity 1 --keepdb
```

## Resume here (next 5 actions)

1. **Record the full gate result.** If it failed, fix the first failure before
   any M1 work; the likely class is another `Decimal`/float read in
   `horilla_views` or `report`.
2. **Apply and verify M1-9/10:**
   `python manage.py test payroll.tests.test_dz_parameters --keepdb`.
   The test DB will apply `0017` + `0018`.
3. **Commit M1-9/10** (`payroll/models/tax_models.py`,
   `payroll/migrations/0017_*`, `0018_*`, `payroll/tests/test_dz_parameters.py`):
   `feat(payroll): effective-dated Algeria parameters and 2026 seed`.
4. **Implement M1-11** in `payroll/methods/dz_irg.py` with the boundary test
   (30,000 / 30,001 / 34,999 / 35,000 / 35,001 / 42,500; 72,800 → 11,956).
5. **Implement M1-12** (`FilingStatus.tax_engine` + `as_of`), then M1-13/14/15.

## Ground rules for the next session

- One test command at a time; `--keepdb`; record the test count in the commit body
  when the suite is large.
- Never change an asserted payroll number to make a test pass. Fix the engine or
  the fixture.
- Every rate/threshold gets `effective_from` + `source_url` + confidence tag.
- Migrations: `makemigrations --check` clean; data migrations reversible.
- Company scoping and permissions are not optional; no `_base_manager` shortcut
  without an explicit scoping check.
- Push only after the touched app suite is green.

## Open client decisions

SME vs large/multi-company group; applicable collective agreement(s); BTPH in or
out; CASNOS depth; hosting (in-Algeria vs authorised transfer); e-signature
provider; bilingual depth; migration source (Excel vs incumbent payroll).
