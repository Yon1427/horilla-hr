# M0 delivery notes — stabilisation

Branch: `algeria/m0-m1` (fork `github.com/Yon1427/horilla-hr`)
Baseline before work: `base payroll leave horilla_views` → **1,491 tests, OK** (1 expected failure).

## Commits

| Task | Commit | What changed |
|---|---|---|
| M0-1 | `235ed7e` | Weekly-off calendar: `None`/`""` = every week, short-month guard, **Sunday-first** week index shared by payroll and attendance |
| M0-2/M0-3 | `dfe4c8b` | Bulk payslips: per-employee period, `payroll/methods/bulk_generate.py`, atomic batch, notifications on commit |
| M0-4 | `22b1dfa` | CSV formula injection: `safe_row()` applied to the quick export and the contributions export |
| M0-5/M0-6 | `6590aea` | Leave: `select_for_update` on the balance, one transaction, no `except: pass`; `no_approval()` locks and saves in one block |
| M0-8 | `0d994f5` | Unresolved attendance conflicts raise `PayrollBlockedError` instead of zeroing the month |
| M0-7 | `8474210` | `Payslip` money → `Decimal(14,2)` + migration `0016`; `money()` rounding; float reads fixed in `payslip_edit` and payslip PDF data |

## Test evidence

- M0-1: `test_company_leave_dates` + `test_holiday_form` → 16 OK; **attendance 293 OK**.
- M0-2/3: `test_bulk_payslip_period`, `test_bulk_payslip_atomic`, `test_batch_run` → 25 OK (rollback proven: 1 saved → 0 after failure).
- M0-4: `test_export_safety_row`, `test_export_scoping`, `test_report_execution` → 48 OK.
- M0-5/6: `test_approval_atomic` (including real `FOR UPDATE`) + `test_approve_balance` + `test_leave_request_idor` → 10 OK; **leave 136 OK**.
- M0-8: `test_unresolved_conflict_block` + `test_batch_run` + golden payslip → 41 OK.
- M0-7: `test_decimal_money` + golden payslip + `test_payslip_edit` → 115 OK; **payroll 1,011 tests**, only 4 test-side `Decimal - float` errors, fixed and re-run (54 OK).

## Decisions worth carrying forward

- **Week starts Sunday.** The Algerian weekend is Friday–Saturday. `month_week_index` converts the 1st's `weekday()` with `(weekday + 1) % 7`; `calendar.setfirstweekday(6)`; the “every week” column is `(based_on_week_day + 1) % 7`.
- **Money is Decimal at rest, float in the calculation engine.** `save_payslip` quantizes; read sites that do arithmetic with engine floats convert explicitly. Do not remove those `float(...)` conversions without converting the engine.
- **Conflicts block.** A monthly summary with `unresolved_conflicts > 0` must never produce a payslip; `bulk_generate` reports it per employee and continues with the rest.
- **Leave approval is locked under the company-scoped manager**, using `select_for_update(of=("self",))` to avoid PostgreSQL's nullable-outer-join error.

## Known issues (not M0 blockers)

1. Background mail threads (`leave/threading.py`) render templates after the request ends; the `default_currency` context processor then inserts `PayrollSettings` for a company that may be gone. In tests this logs an `IntegrityError` (`payroll_payrollsettings` FK) without failing. Fix by making the context processor read-only.
2. The bulk success message now reports `len(saved)`, not the requested count; skipped employees still get an error message.
3. `leave_request_creation` still uses `referer_parts[-2]` on an unvalidated referer; a malformed/missing referer can `IndexError`. Pre-existing.

## Next

M1 — Algerian payroll core, tasks M1-9..M1-16 in `08-implementation-plan.md`:
effective-dated parameters, 2026 seed, IRG engine and boundaries, `FilingStatus.tax_engine`, component seed command, 80,000 DA golden payslip, employer cost service.
