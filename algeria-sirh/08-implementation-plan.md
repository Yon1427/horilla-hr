# Algerian SIRH — Implementation Plan (M0 + M1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development`
> (recommended) or `executing-plans` to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the fork safe to run payroll and add a correct, effective-dated
Algerian private-sector payroll core (SNMG, CNAS, IRG), without rewriting
Horilla's engine.

**Architecture:** Keep Horilla's component engine. Fix the eight defects that
corrupt payroll first (M0). Then add one effective-dated parameter model, one
IRG function, one `FilingStatus` engine switch, and seed CNAS as a normal
`Deduction` (the model already has `rate`, `employer_rate`, `is_pretax`,
`is_tax`). No parallel payroll engine, no new Django app in M0/M1.

**Tech Stack:** Python 3.12, Django 5.2, Horilla 2.3.0, Django `TestCase`,
existing factories (`horilla.testkit`, `payroll.tests.factories_payroll`),
Black + isort (pre-commit).

**Fork:** `https://github.com/Yon1427/horilla-hr` (created from
`horilla/horilla-hr`, branch `2.0`, commit `bba4b37`).

---

## Scope check

The Algerian product has independent subsystems. This plan covers **M0
(stabilise)** and **M1 (payroll core)** only. M2+ are separate plans, one per
subsystem, because each produces working software on its own.

| Milestone | Scope | Plan |
|---|---|---|
| **M0** | 8 payroll/attendance defects + CSV injection + leave balance race | this document |
| **M1** | DZ parameters, CNAS, IRG, payslip golden test, costisation | this document |
| M2 | Statutory declarations (DAC, DAS, G50, G29, ANEM, AT/MP, TFPC/TAPP) | separate |
| M3 | Contract types + shift/rotation engine (`07`) | separate |
| M4 | Localization, bilingual documents, holidays, e-signature, retention | separate |
| M5 | CASNOS + BTPH overlay + bank payment files | separate |
| M6 | Costisation UI, budgets, raise simulator | separate |
| M7 | ANPDP/DPO tooling, hardening, load tests | separate |

**Definition of done for this plan:** `python manage.py test` passes for the
touched apps; the 80 000 DA golden payslip produces net **60 844,00**; the
IRG boundary suite passes; `make test-smoke` is green.

---

## Repo setup

- [ ] **Step 0.1: add the fork remote and branch**

```bash
cd /home/sidali/sirh
git remote add fork https://github.com/Yon1427/horilla-hr.git 2>/dev/null || true
git fetch origin 2.0
git switch -c algeria/m0-m1 origin/2.0
```

- [ ] **Step 0.2: baseline the test suite for the apps you touch**

```bash
python manage.py test payroll base leave horilla_views --keepdb
```

Expected: the suite passes before any change. If a test already fails, record
it in `algeria-sirh/09-baseline-failures.md` and do not fix it in this plan.

- [ ] **Step 0.3: confirm the test helpers exist**

```bash
grep -n "def make_company\|def make_employee" horilla/testkit/factories.py
grep -n "def make_active_contract\|def make_deduction\|def make_filing_status" payroll/tests/factories_payroll.py
```

Expected: all five functions found. Every test below uses them, so a scenario
cannot leak real data.

---

## File structure (files this plan creates or changes)

```
base/
  methods.py                                  # M0-1 weekly-off calendar
  tests/test_company_leave_dates.py           # NEW
leave/
  views.py                                    # M0-5/M0-6 approval atomicity
  tests/test_approval_balance_atomic.py       # NEW
horilla/
  export_safety.py                            # M0-4 safe_row helper
  tests/test_export_safety.py                 # NEW (or extend)
horilla_views/
  views.py                                    # M0-4 CSV writer
payroll/
  models/models.py                            # M0-7 Decimal payslip, M1-12 tax_engine
  models/tax_models.py                        # M1-9 AlgeriaPayrollParameter
  methods/errors.py                           # NEW: PayrollBlockedError
  methods/methods.py                          # M0-7/M0-8
  methods/tax_calc.py                         # M1-12 engine branch + as_of
  methods/dz_irg.py                           # NEW: IRG engine
  methods/bulk_generate.py                    # NEW: M0-2/M0-3 service
  methods/dz_cost.py                          # NEW: M1-15 costisation
  views/component_views.py                    # M0-2/M0-3/M0-8 view uses service
  management/commands/seed_algeria_payroll.py # NEW: M1-13
  migrations/0016_payslip_decimal_money.py
  migrations/0017_algeria_payroll_parameter.py
  migrations/0018_seed_algeria_parameters_2026.py
  migrations/0019_filingstatus_tax_engine.py
  tests/test_bulk_payslip_period.py           # NEW
  tests/test_bulk_payslip_atomic.py           # NEW
  tests/test_decimal_money.py                 # NEW
  tests/test_dz_irg.py                        # NEW
  tests/test_dz_payroll_golden.py             # NEW
  tests/test_dz_cost.py                       # NEW
algeria-sirh/
  08-implementation-plan.md                   # this file
  09-baseline-failures.md                     # only if Step 0.2 finds one
```

---

# M0 — Stabilise (do this before any Algerian feature)

## Task 1: Weekly-off calendar must not crash and must agree with attendance

Why: `get_company_leave_dates` runs `int("")` for the UI's “All” choice and
indexes a 4-row February with week 4. It used Sunday-first weeks while
`is_company_leave` used Monday-first; the Algerian week starts Sunday (weekend
is Friday–Saturday), so Sunday-first is the convention both must use. One
config 500s payroll and attendance.

**Files:**
- Modify: `base/methods.py:1592-1618` (`is_company_leave`), `base/methods.py:1668-1705` (`get_company_leave_dates`)
- Test: `base/tests/test_company_leave_dates.py` (create)

- [ ] **Step 1: Write the failing test**

```python
from datetime import date

from django.test import TestCase

from base.methods import get_company_leave_dates, is_company_leave
from base.models import CompanyLeaves


class CompanyLeaveDatesTest(TestCase):
    def test_empty_week_means_every_week(self):
        CompanyLeaves.objects.create(based_on_week="", based_on_week_day="0")
        self.assertIn(date(2026, 1, 5), get_company_leave_dates(2026))

    def test_fifth_week_in_a_four_row_month_does_not_raise(self):
        CompanyLeaves.objects.create(based_on_week="4", based_on_week_day="0")
        dates = get_company_leave_dates(2026)  # Feb 2026 is 4 Sunday-first rows
        self.assertIsInstance(dates, list)

    def test_payroll_and_attendance_agree_on_week_number(self):
        CompanyLeaves.objects.create(based_on_week="0", based_on_week_day="0")
        day = date(2024, 9, 2)  # first Monday, inside Sunday-first week 0
        self.assertIn(day, get_company_leave_dates(2024))
        self.assertTrue(is_company_leave(day))
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test base.tests.test_company_leave_dates -v 2
```

Expected: `ValueError: invalid literal for int()` and/or `IndexError`, and the
agreement test fails.

- [ ] **Step 3: Add one week helper and use it in both functions**

```python
# base/methods.py, above is_company_leave
def month_week_index(value):
    """0-based week of the month, Sunday-first (Algerian weekend is Fri-Sat)."""
    sunday_based_weekday = (value.replace(day=1).weekday() + 1) % 7
    return (value.day + sunday_based_weekday - 1) // 7
```

```python
# is_company_leave
date_week_no = month_week_index(input_date)
company_leave = CompanyLeaves.objects.filter(
    Q(based_on_week__in=[None, ""], based_on_week_day=date_week_day)
    | Q(based_on_week=date_week_no, based_on_week_day=date_week_day)
).first()
```

```python
# get_company_leave_dates
for company_leave in company_leaves:
    based_on_week = company_leave.based_on_week
    based_on_week_day = company_leave.based_on_week_day
    for month in range(1, 13):
        calendar.setfirstweekday(6)  # Sunday-first, same as month_week_index
        month_calendar = calendar.monthcalendar(year, month)
        if based_on_week not in (None, ""):
            week_no = int(based_on_week)
            weeks = month_calendar[week_no] if week_no < len(month_calendar) else []
            for day in [d for d in weeks if d != 0]:
                leave_date = datetime.strptime(
                    f"{year}-{month:02}-{day:02}", "%Y-%m-%d"
                ).date()
                if (
                    leave_date.weekday() == int(based_on_week_day)
                    and leave_date not in company_leave_dates
                ):
                    company_leave_dates.append(leave_date)
        else:
            # Sunday-first rows: Monday (0) sits in column 1, Sunday (6) in 0.
            day_column = (int(based_on_week_day) + 1) % 7
            for week in month_calendar:
                if week[day_column] != 0:
                    leave_date = datetime.strptime(
                        f"{year}-{month:02}-{week[day_column]:02}",
                        "%Y-%m-%d",
                    ).date()
                    if leave_date not in company_leave_dates:
                        company_leave_dates.append(leave_date)
```

- [ ] **Step 4: Run the test again**

```bash
python manage.py test base.tests.test_company_leave_dates base.tests.test_holiday_form -v 2
```

Expected: PASS. Existing holiday tests still pass.

- [ ] **Step 5: Commit**

```bash
git add base/methods.py base/tests/test_company_leave_dates.py
git commit -m "fix(base): weekly-off calendar handles All/Fifth Week and agrees with attendance"
```

---

## Task 2: Bulk payslip must not shorten later employees' period

Why: `start_date` is reassigned inside the loop, so the first late joiner
underpays everyone after them.

**Files:**
- Create: `payroll/methods/bulk_generate.py`
- Modify: `payroll/views/component_views.py:826-875` (loop)
- Test: `payroll/tests/test_bulk_payslip_period.py`

- [ ] **Step 1: Write the failing test**

```python
from datetime import date

from django.test import SimpleTestCase

from payroll.methods.bulk_generate import employee_period_start


class EmployeePeriodStartTest(SimpleTestCase):
    def test_later_contract_start_clamps_only_that_employee(self):
        class Contract:
            contract_start_date = date(2024, 1, 15)

        self.assertEqual(
            employee_period_start(date(2024, 1, 1), Contract()),
            date(2024, 1, 15),
        )

    def test_earlier_contract_keeps_requested_start(self):
        class Contract:
            contract_start_date = date(2023, 12, 1)

        self.assertEqual(
            employee_period_start(date(2024, 1, 1), Contract()),
            date(2024, 1, 1),
        )

    def test_missing_contract_returns_requested_start(self):
        self.assertEqual(
            employee_period_start(date(2024, 1, 1), None), date(2024, 1, 1)
        )
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_bulk_payslip_period -v 2
```

Expected: `ModuleNotFoundError: payroll.methods.bulk_generate`.

- [ ] **Step 3: Create the service with the correct per-employee start**

```python
"""Bulk payslip generation, extracted from the view so it can be tested."""

from __future__ import annotations

import datetime

from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext as _

from payroll.methods.errors import PayrollBlockedError
from payroll.methods.payroll_run import payroll_calculation
from payroll.methods.methods import payslip_fields, save_payslip
from payroll.methods.tax_calc import TaxComputationError
from payroll.models.models import Contract


def employee_period_start(requested_start: datetime.date, contract) -> datetime.date:
    """The start date this employee is actually paid from."""
    if contract and requested_start < contract.contract_start_date:
        return contract.contract_start_date
    return requested_start


@transaction.atomic
def generate_bulk_payslips(
    *, request, employees, start_date, end_date, group_name, summary_by_employee
) -> list:
    """Generate payslips for a batch, all-or-nothing. Returns the saved rows."""
    saved = []
    for employee in employees:
        contract = Contract.objects.filter(
            employee_id=employee, contract_status="active"
        ).first()
        employee_start = employee_period_start(start_date, contract)
        if end_date < employee_start:
            messages.error(request, _(f"{employee}'s contract has not started yet."))
            continue
        try:
            payslip = payroll_calculation(
                employee,
                employee_start,
                end_date,
                month_summary=summary_by_employee.get(employee.pk, {}),
            )
        except (TaxComputationError, PayrollBlockedError) as exc:
            messages.error(request, str(exc))
            continue
        instance = save_payslip(
            **payslip_fields(payslip, employee, status="draft", group_name=group_name)
        )
        saved.append(instance)
        transaction.on_commit(
            lambda employee=employee, instance=instance: _notify(request, employee, instance)
        )
    return saved


def _notify(request, employee, instance):
    from django.urls import reverse
    from django.utils.translation import gettext_noop
    from notifications.signals import notify

    notify.send(
        request.user.employee_get,
        recipient=employee.employee_user_id,
        verb=gettext_noop("Payslip has been generated for you."),
        redirect=reverse("view-created-payslip", kwargs={"payslip_id": instance.id}),
        icon="close",
    )
```

- [ ] **Step 4: Make the view call the service**

Replace the loop body in `generate_payslip` with:

```python
from payroll.methods.bulk_generate import generate_bulk_payslips

generate_bulk_payslips(
    request=request,
    employees=employees,
    start_date=start_date,
    end_date=end_date,
    group_name=group_name,
    summary_by_employee=att_summary,
)
messages.success(
    request, _("%(emp_count)s payslip saved as draft") % {"emp_count": emp_count}
)
return redirect(
    f"/payroll/view-payslip/?group_by=group_name&active_group={group_name}"
)
```

- [ ] **Step 5: Run and commit**

```bash
python manage.py test payroll.tests.test_bulk_payslip_period payroll.tests.test_batch_run -v 2
git add payroll/methods/bulk_generate.py payroll/views/component_views.py payroll/tests/test_bulk_payslip_period.py
git commit -m "fix(payroll): per-employee period in bulk generation"
```

Expected: PASS.

---

## Task 3: Bulk run is atomic (no half batch, no premature notifications)

Why: a failure halfway leaves committed payslips and sent notifications.

**Files:**
- Modify: `payroll/methods/bulk_generate.py` (already `@transaction.atomic`; notifications now `on_commit`)
- Test: `payroll/tests/test_bulk_payslip_atomic.py`

- [ ] **Step 1: Write the failing test**

```python
from datetime import date
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from horilla.testkit import make_company, make_employee, make_user
from payroll.methods.bulk_generate import generate_bulk_payslips
from payroll.models.models import Payslip
from payroll.tests.factories_payroll import make_active_contract


class BulkAtomicTest(TestCase):
    def setUp(self):
        self.company = make_company()
        self.user = make_user("hr1")
        self.employees = [
            make_employee(company=self.company, email=f"e{i}@test.dz")
            for i in range(2)
        ]
        for employee in self.employees:
            make_active_contract(employee, wage=50000.0)
        self.request = RequestFactory().post("/payroll/generate-payslip/")
        self.request.user = self.user

    @patch("payroll.methods.bulk_generate.payroll_calculation")
    def test_second_failure_rolls_back_first_payslip(self, calc):
        calc.side_effect = [Exception("boom")]
        with self.assertRaises(Exception):
            generate_bulk_payslips(
                request=self.request,
                employees=self.employees,
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 31),
                group_name="Jan",
                summary_by_employee={},
            )
        self.assertEqual(Payslip.objects.count(), 0)
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_bulk_payslip_atomic -v 2
```

Expected: FAIL if `@transaction.atomic` is missing (one row remains). With Task 2
applied it should pass; keep the test as the regression guard.

- [ ] **Step 3: Ensure the decorator and `on_commit` are in place**

The service from Task 2 already has `@transaction.atomic` and
`transaction.on_commit(...)`. If the first employee's calculation raises a
non-tax exception, it propagates and the transaction rolls back. Tax and
blocked errors are caught per employee and *do not* roll back the batch —
that is intentional: one bad employee must not stop the rest.

- [ ] **Step 4: Run again**

```bash
python manage.py test payroll.tests.test_bulk_payslip_atomic payroll.tests.test_bulk_payslip_period -v 2
```

- [ ] **Step 5: Commit**

```bash
git add payroll/tests/test_bulk_payslip_atomic.py
git commit -m "test(payroll): bulk run rolls back on unexpected failure"
```

---

## Task 4: Neutralise formulas in every CSV export

Why: XLSX uses `safe_cell`; the default quick-export CSV and the contributions
CSV do not.

**Files:**
- Modify: `horilla/export_safety.py`
- Modify: `horilla_views/views.py:1072-1078`
- Modify: `payroll/views/contribution_views.py:151-168`
- Test: `base/tests/test_export_safety_row.py` (create)

- [ ] **Step 1: Write the failing test**

```python
from django.test import SimpleTestCase

from horilla.export_safety import safe_row


class SafeRowTest(SimpleTestCase):
    def test_every_string_cell_is_neutralised(self):
        self.assertEqual(
            safe_row(["=HYPERLINK(\"http://x\")", 2, "ok", None, "-5"]),
            ["'=HYPERLINK(\"http://x\")", 2, "ok", "", "'-5"],
        )
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test base.tests.test_export_safety_row -v 2
```

Expected: `ImportError: cannot import name 'safe_row'`.

- [ ] **Step 3: Add the helper and use it**

```python
# horilla/export_safety.py, after safe_cell
def safe_row(row) -> list:
    """Guard every cell of one CSV/XLSX row."""
    return [safe_cell(value) for value in row]
```

```python
# horilla_views/views.py — CSV branch
from horilla.export_safety import safe_cell, safe_row

writer.writerow(safe_row([company_name]))
writer.writerow(safe_row([file_name]))
writer.writerow(safe_row([date_range]))
writer.writerow([])
writer.writerow(safe_row(headers))
writer.writerows(safe_row(row) for row in final_rows)
```

```python
# payroll/views/contribution_views.py
from horilla.export_safety import safe_row

writer.writerow(safe_row([... the existing header list ...]))
...
writer.writerow(
    safe_row([
        row["title"],
        line["employee"].badge_id or "",
        str(line["employee"]),
        line["start_date"],
        line["end_date"],
        line["status"],
        line["employee_amount"],
        line["employer_amount"],
        line["total"],
    ])
)
```

- [ ] **Step 4: Run the tests**

```bash
python manage.py test base.tests.test_export_safety_row horilla_views.tests payroll.tests.test_payroll_export -v 2
```

Expected: PASS. (Adjust the last label if `test_payroll_export` does not exist;
the command should list no failures.)

- [ ] **Step 5: Commit**

```bash
git add horilla/export_safety.py horilla_views/views.py payroll/views/contribution_views.py base/tests/test_export_safety_row.py
git commit -m "fix(exports): neutralise formulas in all CSV writers"
```

---

## Task 5: Leave approval locks the balance and is one transaction

Why: two approvals can both pass the balance check; the cancellation path
already locks, so the same balance has two different protections.

**Files:**
- Modify: `leave/views.py:1176-1245` (`leave_request_approve`)
- Test: `leave/tests/test_approval_balance_atomic.py` (create)

- [ ] **Step 1: Write the failing test (Postgres-only assertion)**

```python
from datetime import date

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext, skipIf

from horilla.testkit import make_company, make_employee

# SQLite ignores SELECT ... FOR UPDATE, so this assertion is only meaningful on
# PostgreSQL. The Docker/CI database is PostgreSQL.
@skipIf(connection.vendor == "sqlite", "select_for_update is a no-op on SQLite")
class ApprovalLocksBalanceTest(TestCase):
    def test_approval_selects_the_balance_for_update(self):
        # Build the smallest real leave request via the existing leave factories.
        from leave.tests.factories import make_leave_request  # adjust if named differently

        request = make_leave_request()
        client = self.client
        client.force_login(request.employee_id.employee_user_id)
        with CaptureQueriesContext(connection) as queries:
            client.post(f"/leave/request-approve/{request.id}/")
        self.assertTrue(
            any("FOR UPDATE" in q["sql"] for q in queries.captured_queries),
            "leave approval must lock AvailableLeave",
        )
```

If `leave/tests/factories.py` does not exist, build the objects with
`make_company`/`make_employee` + `LeaveType` + `AvailableLeave` + `LeaveRequest`
in the test `setUp`, following `leave/tests/test_leave_balance.py`.

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test leave.tests.test_approval_balance_atomic -v 2
```

Expected: FAIL (no `FOR UPDATE`).

- [ ] **Step 3: Wrap the decision in `atomic` and lock the row**

```python
# leave/views.py, inside leave_request_approve, replacing the read+write block
from django.db import transaction

with transaction.atomic():
    available_leave = (
        AvailableLeave._base_manager.select_for_update()
        .get(leave_type_id=leave_type_id, employee_id=employee_id)
    )
    total_available_leave = (
        available_leave.available_days + available_leave.carryforward_days
    )
    if leave_request.status != "approved":
        if total_available_leave >= leave_request.requested_days:
            ...  # existing decrement logic, unchanged
            leave_request.save()
            available_leave.save()
```

Do the same for `leave_request_bulk_approve` (`leave/views.py:1349`).

- [ ] **Step 4: Run the test on PostgreSQL and SQLite**

```bash
python manage.py test leave.tests.test_approval_balance_atomic leave.tests -v 2
```

Expected: PASS on Postgres; skipped on SQLite.

- [ ] **Step 5: Commit**

```bash
git add leave/views.py leave/tests/test_approval_balance_atomic.py
git commit -m "fix(leave): lock balance and approve inside one transaction"
```

---

## Task 6: A failed balance save must not leave the leave approved

Why: `try: available_leave.save() except: pass` swallows the failure after the
leave is already saved as approved.

**Files:**
- Modify: `leave/views.py:576-582`
- Test: `leave/tests/test_approval_balance_atomic.py` (extend)

- [ ] **Step 1: Write the failing test**

```python
from unittest.mock import patch

from django.test import TestCase

from leave.models import AvailableLeave, LeaveRequest


class BalanceFailureRollsBackTest(TestCase):
    def test_leave_not_approved_when_balance_save_fails(self):
        # setUp: create the leave request with require_approval="no"
        ...
        with patch.object(AvailableLeave, "save", side_effect=Exception("db")):
            self.client.post(self.approve_url)
        self.assertNotEqual(
            LeaveRequest.objects.get(pk=self.leave.pk).status, "approved"
        )
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test leave.tests.test_approval_balance_atomic -v 2
```

Expected: FAIL (status is `approved`).

- [ ] **Step 3: Remove the bare except and make both saves atomic**

```python
# leave/views.py — replace
try:
    available_leave.save()
except:
    pass

# with
available_leave.save()
```

and wrap the `leave_request.save()` + `available_leave.save()` pair in
`with transaction.atomic():` (the same block as Task 5 where possible).

- [ ] **Step 4: Run again**

```bash
python manage.py test leave.tests.test_approval_balance_atomic leave.tests -v 2
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add leave/views.py leave/tests/test_approval_balance_atomic.py
git commit -m "fix(leave): roll back approval when the balance cannot be saved"
```

---

## Task 7: Store payslip money as Decimal

Why: float money drifts when totals are summed across hundreds of payslips.

**Files:**
- Modify: `payroll/models/models.py:3679-3683` (`Payslip` fields)
- Modify: `payroll/methods/methods.py:1109-1150` (`save_payslip`)
- Create: `payroll/migrations/0016_payslip_decimal_money.py` (generated)
- Test: `payroll/tests/test_decimal_money.py`

- [ ] **Step 1: Write the failing test**

```python
from decimal import Decimal

from django.test import TestCase

from payroll.models.models import Payslip


class PayslipMoneyTypeTest(TestCase):
    def test_payslip_money_columns_are_decimal(self):
        for name in ("contract_wage", "basic_pay", "gross_pay", "deduction", "net_pay"):
            field = Payslip._meta.get_field(name)
            self.assertEqual(field.get_internal_type(), "DecimalField", name)
            self.assertEqual(field.decimal_places, 2)

    def test_three_cents_sum_exactly(self):
        self.assertEqual(
            sum([Decimal("0.10"), Decimal("0.20"), Decimal("0.30")]),
            Decimal("0.60"),
        )
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_decimal_money -v 2
```

Expected: FAIL (`FloatField`).

- [ ] **Step 3: Change the fields and the save helper**

```python
# payroll/models/models.py — Payslip
contract_wage = models.DecimalField(max_digits=14, decimal_places=2, null=True, default=0)
basic_pay = models.DecimalField(max_digits=14, decimal_places=2, null=True, default=0)
gross_pay = models.DecimalField(max_digits=14, decimal_places=2, null=True, default=0)
deduction = models.DecimalField(max_digits=14, decimal_places=2, null=True, default=0)
net_pay = models.DecimalField(max_digits=14, decimal_places=2, null=True, default=0)
```

```python
# payroll/methods/methods.py — top of file
from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal("0.01")

def money(value) -> Decimal:
    return Decimal(str(value or 0)).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
```

In `save_payslip`, replace the five `round(...)` calls:

```python
instance.basic_pay = money(kwargs["basic_pay"])
instance.contract_wage = money(kwargs["contract_wage"])
instance.gross_pay = money(kwargs["gross_pay"])
instance.deduction = min(money(kwargs["deduction"]), money(kwargs["gross_pay"]))
instance.net_pay = max(Decimal("0.00"), money(kwargs["net_pay"]))
```

- [ ] **Step 4: Generate the migration and run the tests**

```bash
python manage.py makemigrations payroll --name payslip_decimal_money
python manage.py test payroll.tests.test_decimal_money payroll.tests.test_payroll_calculation_golden -v 2
```

Expected: PASS. Inspect the migration: it must only alter the five columns.

- [ ] **Step 5: Commit**

```bash
git add payroll/models/models.py payroll/methods/methods.py payroll/migrations/0016_payslip_decimal_money.py payroll/tests/test_decimal_money.py
git commit -m "fix(payroll): store payslip money as Decimal"
```

---

## Task 8: Unresolved attendance conflicts must block, not zero the month

Why: one unresolved conflict sets `unpaid_days = total_days`, producing a
zero-pay payslip on the legacy bulk path.

**Files:**
- Create: `payroll/methods/errors.py`
- Modify: `payroll/methods/methods.py:827-828, 885-886`
- Modify: `payroll/methods/bulk_generate.py` (catch it)
- Test: `payroll/tests/test_unresolved_conflict_block.py`

- [ ] **Step 1: Write the failing test**

```python
from django.test import TestCase

from payroll.methods.errors import PayrollBlockedError
from payroll.methods.methods import compute_salary_on_period
from payroll.tests.factories_payroll import make_active_contract
from horilla.testkit import make_company, make_employee


class UnresolvedConflictTest(TestCase):
    def test_unresolved_conflict_raises(self):
        company = make_company()
        employee = make_employee(company=company, email="c@test.dz")
        make_active_contract(employee, wage=60000.0)
        with self.assertRaises(PayrollBlockedError):
            compute_salary_on_period(
                employee,
                __import__("datetime").date(2024, 1, 1),
                __import__("datetime").date(2024, 1, 31),
                month_summary={"unresolved_conflicts": 1},
            )
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_unresolved_conflict_block -v 2
```

Expected: `ModuleNotFoundError: payroll.methods.errors`.

- [ ] **Step 3: Add the error and raise it**

```python
# payroll/methods/errors.py
class PayrollBlockedError(Exception):
    """Payslip cannot be generated until a data problem is resolved."""
```

```python
# payroll/methods/methods.py — both branches
if month_summary.get("unresolved_conflicts", 0):
    raise PayrollBlockedError(
        "Unresolved attendance conflicts for this period. "
        "Resolve them before generating the payslip."
    )
```

Delete the `unpaid_days = total_days` lines.

- [ ] **Step 4: Run again**

```bash
python manage.py test payroll.tests.test_unresolved_conflict_block payroll.tests.test_batch_run -v 2
```

Expected: PASS. `bulk_generate` already catches `PayrollBlockedError` (Task 2).

- [ ] **Step 5: Commit**

```bash
git add payroll/methods/errors.py payroll/methods/methods.py payroll/tests/test_unresolved_conflict_block.py
git commit -m "fix(payroll): block on unresolved attendance conflicts instead of zeroing pay"
```

---

# M1 — Algerian payroll core

## Task 9: Effective-dated Algeria parameter model

**Files:**
- Modify: `payroll/models/tax_models.py` (append the model)
- Create: `payroll/migrations/0017_algeria_payroll_parameter.py` (generated)
- Test: `payroll/tests/test_dz_parameters.py`

- [ ] **Step 1: Write the failing test**

```python
from datetime import date

from django.test import TestCase

from horilla.testkit import make_company
from payroll.models.tax_models import AlgeriaPayrollParameter


class ParameterResolutionTest(TestCase):
    def test_latest_effective_row_wins(self):
        company = make_company()
        AlgeriaPayrollParameter.objects.create(
            company_id=company, effective_from=date(2025, 1, 1), snmg_monthly=20000
        )
        AlgeriaPayrollParameter.objects.create(
            company_id=company, effective_from=date(2026, 1, 1), snmg_monthly=24000
        )
        self.assertEqual(
            AlgeriaPayrollParameter.for_company(company, date(2026, 6, 30)).snmg_monthly,
            24000,
        )
        self.assertEqual(
            AlgeriaPayrollParameter.for_company(company, date(2025, 6, 30)).snmg_monthly,
            20000,
        )

    def test_falls_back_to_the_global_row(self):
        company = make_company()
        AlgeriaPayrollParameter.objects.create(
            company_id=None, effective_from=date(2026, 1, 1), snmg_monthly=24000
        )
        self.assertEqual(
            AlgeriaPayrollParameter.for_company(company, date(2026, 6, 30)).snmg_monthly,
            24000,
        )
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_dz_parameters -v 2
```

Expected: `ImportError: cannot import name 'AlgeriaPayrollParameter'`.

- [ ] **Step 3: Add the model**

```python
# payroll/models/tax_models.py — append
class AlgeriaPayrollParameter(HorillaModel):
    """Algerian private-sector payroll rules, effective-dated per company.

    Every figure must carry a source. A new finance law creates a new row; it
    never edits an old one, because historical payslips must keep computing.
    """

    DZ_IRG_BRACKETS = [
        {"min": 0, "max": 20000, "rate": 0},
        {"min": 20000, "max": 40000, "rate": 23},
        {"min": 40000, "max": 80000, "rate": 27},
        {"min": 80000, "max": 160000, "rate": 30},
        {"min": 160000, "max": 320000, "rate": 33},
        {"min": 320000, "max": None, "rate": 35},
    ]

    company_id = models.ForeignKey(Company, null=True, on_delete=models.PROTECT)
    effective_from = models.DateField()
    snmg_monthly = models.FloatField(default=24000)
    irg_brackets = models.JSONField(default=list)
    irg_exemption_monthly = models.FloatField(default=30000)
    abatement_rate = models.FloatField(default=40)
    abatement_min = models.FloatField(default=1000)
    abatement_max = models.FloatField(default=1500)
    smoothing_min = models.FloatField(default=30000)
    smoothing_max = models.FloatField(default=35000)
    smoothing_factor = models.FloatField(default=137 / 51)
    smoothing_offset = models.FloatField(default=27925 / 8)
    disabled_smoothing_max = models.FloatField(default=42500)
    disabled_smoothing_factor = models.FloatField(default=93 / 61)
    disabled_smoothing_offset = models.FloatField(default=81213 / 41)
    exceptional_bonus_rate = models.FloatField(default=10)
    cnas_employee_rate = models.FloatField(default=9)
    cnas_employer_rate = models.FloatField(default=25)
    fnpos_rate = models.FloatField(default=0.5)
    tfpc_rate = models.FloatField(default=1)
    tapp_rate = models.FloatField(default=1)
    source_url = models.URLField(blank=True)
    objects = HorillaCompanyManager("company_id")

    class Meta:
        ordering = ["-effective_from"]
        unique_together = ("company_id", "effective_from")

    def __str__(self):
        return f"Algeria payroll {self.effective_from}"

    @classmethod
    def for_company(cls, company, as_of):
        qs = cls.objects.filter(effective_from__lte=as_of)
        company_id = getattr(company, "pk", company)
        row = qs.filter(company_id=company_id).first() if company_id else None
        return row or qs.filter(company_id__isnull=True).first()
```

- [ ] **Step 4: Generate the migration and run**

```bash
python manage.py makemigrations payroll --name algeria_payroll_parameter
python manage.py test payroll.tests.test_dz_parameters -v 2
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add payroll/models/tax_models.py payroll/migrations/0017_algeria_payroll_parameter.py payroll/tests/test_dz_parameters.py
git commit -m "feat(payroll): effective-dated Algeria payroll parameters"
```

---

## Task 10: Seed the 2026 parameter row

**Files:**
- Create: `payroll/migrations/0018_seed_algeria_parameters_2026.py`
- Test: extend `payroll/tests/test_dz_parameters.py`

- [ ] **Step 1: Write the failing test**

```python
def test_2026_global_row_is_seeded(self):
    row = AlgeriaPayrollParameter.objects.get(
        company_id__isnull=True, effective_from=date(2026, 1, 1)
    )
    self.assertEqual(row.snmg_monthly, 24000)
    self.assertEqual(row.cnas_employee_rate, 9)
    self.assertEqual(row.cnas_employer_rate, 25)
    self.assertEqual(row.fnpos_rate, 0.5)
    self.assertEqual(row.irg_brackets, AlgeriaPayrollParameter.DZ_IRG_BRACKETS)
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_dz_parameters -v 2
```

Expected: `DoesNotExist`.

- [ ] **Step 3: Write the data migration**

```python
from datetime import date

from django.db import migrations


def seed(apps, schema_editor):
    Parameter = apps.get_model("payroll", "AlgeriaPayrollParameter")
    Parameter.objects.get_or_create(
        company_id=None,
        effective_from=date(2026, 1, 1),
        defaults={
            "snmg_monthly": 24000,
            "irg_brackets": [
                {"min": 0, "max": 20000, "rate": 0},
                {"min": 20000, "max": 40000, "rate": 23},
                {"min": 40000, "max": 80000, "rate": 27},
                {"min": 80000, "max": 160000, "rate": 30},
                {"min": 160000, "max": 320000, "rate": 33},
                {"min": 320000, "max": None, "rate": 35},
            ],
            "source_url": "https://www.joradp.dz/",
        },
    )


def unseed(apps, schema_editor):
    Parameter = apps.get_model("payroll", "AlgeriaPayrollParameter")
    Parameter.objects.filter(
        company_id=None, effective_from=date(2026, 1, 1)
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("payroll", "0017_algeria_payroll_parameter")]
    operations = [migrations.RunPython(seed, unseed)]
```

- [ ] **Step 4: Run**

```bash
python manage.py migrate payroll
python manage.py test payroll.tests.test_dz_parameters -v 2
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add payroll/migrations/0018_seed_algeria_parameters_2026.py payroll/tests/test_dz_parameters.py
git commit -m "data(payroll): seed 2026 Algeria parameters"
```

---

## Task 11: IRG engine with boundary tests

**Files:**
- Create: `payroll/methods/dz_irg.py`
- Test: `payroll/tests/test_dz_irg.py`

- [ ] **Step 1: Write the failing test**

```python
from datetime import date

from django.test import SimpleTestCase

from payroll.methods.dz_irg import compute_monthly_irg
from payroll.models.tax_models import AlgeriaPayrollParameter


class IrgTest(SimpleTestCase):
    def setUp(self):
        self.p = AlgeriaPayrollParameter(
            effective_from=date(2026, 1, 1),
            irg_brackets=AlgeriaPayrollParameter.DZ_IRG_BRACKETS,
        )

    def test_exempt_at_30000(self):
        self.assertEqual(compute_monthly_irg(30000, self.p), 0)

    def test_80000_gross_example_taxable_72800(self):
        self.assertEqual(compute_monthly_irg(72800, self.p), 11956)

    def test_band_boundaries_are_stable(self):
        values = [30001, 34999, 35000, 35001, 42500]
        taxes = [compute_monthly_irg(v, self.p) for v in values]
        self.assertEqual(taxes, sorted(taxes))  # no negative jump

    def test_disabled_band_uses_42500_threshold(self):
        self.assertGreater(
            compute_monthly_irg(40000, self.p, disabled=True),
            0,
        )
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_dz_irg -v 2
```

Expected: `ModuleNotFoundError`.

- [ ] **Step 3: Write the engine**

```python
"""Algerian IRG on salaries (CIDTA art. 104, LF 2022, unchanged to 2026)."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


def _progressive(taxable: float, brackets) -> float:
    tax = 0.0
    for band in brackets:
        low = float(band["min"])
        high = band["max"]
        if taxable <= low:
            break
        top = taxable if high is None else min(float(high), taxable)
        tax += (top - low) * float(band["rate"]) / 100
    return tax


def compute_monthly_irg(
    monthly_taxable: float,
    params,
    *,
    disabled: bool = False,
    pensioner: bool = False,
) -> float:
    """Monthly IRG in dinars, rounded to 2 dp. Order matters (see 01 §3.3)."""
    taxable = max(float(monthly_taxable or 0), 0.0)
    if taxable <= float(params.irg_exemption_monthly):
        return 0.0

    tax = _progressive(taxable, params.irg_brackets)
    abatement = min(
        max(tax * float(params.abatement_rate) / 100, float(params.abatement_min)),
        float(params.abatement_max),
    )
    irg = max(tax - abatement, 0.0)

    if disabled or pensioner:
        if float(params.smoothing_min) < taxable < float(params.disabled_smoothing_max):
            irg = max(
                irg * float(params.disabled_smoothing_factor)
                - float(params.disabled_smoothing_offset),
                0.0,
            )
    elif float(params.smoothing_min) < taxable < float(params.smoothing_max):
        irg = max(
            irg * float(params.smoothing_factor)
            - float(params.smoothing_offset),
            0.0,
        )

    return float(Decimal(str(irg)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def compute_yearly_irg(yearly_taxable: float, params, **kwargs) -> float:
    """Horilla computes yearly; DZ IRG is monthly. Convert, do not annualise rates."""
    return compute_monthly_irg(float(yearly_taxable) / 12, params, **kwargs) * 12
```

- [ ] **Step 4: Run and fix the boundary expectation**

```bash
python manage.py test payroll.tests.test_dz_irg -v 2
```

Expected: PASS. If `test_band_boundaries_are_stable` fails, the smoothing
formula or its coefficients are wrong — do **not** "fix" the test. Check
`01 §3.3/§3.9` and the DGI table first.

- [ ] **Step 5: Commit**

```bash
git add payroll/methods/dz_irg.py payroll/tests/test_dz_irg.py
git commit -m "feat(payroll): Algerian IRG engine with boundary tests"
```

---

## Task 12: Wire the DZ engine into `FilingStatus`

**Files:**
- Modify: `payroll/models/models.py:165-260` (`FilingStatus`)
- Modify: `payroll/methods/tax_calc.py` (`compute_yearly_tax`, `calculate_taxable_amount`)
- Create: `payroll/migrations/0019_filingstatus_tax_engine.py`
- Test: `payroll/tests/test_dz_irg_integration.py`

- [x] **Step 1: Write the failing test**

```python
from datetime import date

from django.test import TestCase

from payroll.methods.tax_calc import compute_yearly_tax
from payroll.tests.factories_payroll import make_filing_status


class IntegrationTest(TestCase):
    def test_dz_engine_returns_monthly_irg_times_twelve(self):
        filing = make_filing_status("Algérie IRG", tax_engine="dz_irg")
        tax, breakdown = compute_yearly_tax(
            filing, 72800 * 12, as_of=date(2026, 1, 31)
        )
        self.assertEqual(tax, 11956 * 12)
        self.assertEqual(breakdown["mode"], "dz_irg")
```

- [x] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_dz_irg_integration -v 2
```

Expected: `TypeError: ... unexpected keyword argument 'tax_engine'`.

- [x] **Step 3: Add the field, the branch, and `as_of`**

```python
# FilingStatus
tax_engine = models.CharField(
    max_length=20,
    choices=[("standard", _("Standard slabs")) , ("dz_irg", _("Algeria IRG"))],
    default="standard",
)
```

```python
# payroll/methods/tax_calc.py
def compute_yearly_tax(filing, yearly_income, employee=None, as_of=None):
    if getattr(filing, "tax_engine", "standard") == "dz_irg":
        from payroll.methods.dz_irg import compute_monthly_irg
        from payroll.models.tax_models import AlgeriaPayrollParameter

        company = None
        if employee is not None:
            company = getattr(employee, "get_company", lambda: None)()
        params = AlgeriaPayrollParameter.for_company(company, as_of or date.today())
        if params is None:
            raise TaxComputationError(
                "No Algeria payroll parameters effective on this date."
            )
        monthly = compute_monthly_irg(
            float(yearly_income) / 12,
            params,
            disabled=bool(getattr(employee, "is_disabled", False)),
        )
        federal_tax = monthly * 12
        return federal_tax, {
            "gross_yearly_income": round(float(yearly_income), 2),
            "standard_deduction": 0.0,
            "taxable_income": round(float(yearly_income), 2),
            "tax_before_relief": round(federal_tax, 2),
            "rebate_applied": 0.0,
            "rebate_limit": None,
            "rebate_max": None,
            "cess_applied": 0.0,
            "tax": round(federal_tax, 2),
            "mode": "dz_irg",
            "slabs": [],
        }
    ...  # existing body unchanged
```

```python
# calculate_taxable_amount — pass the period end
tax, breakdown = compute_yearly_tax(
    filing, yearly_taxable, employee=employee, as_of=end_date
)
```

Add `as_of=date.today()` in `preview_yearly_tax`.

- [x] **Step 4: Generate the migration and run**

```bash
python manage.py makemigrations payroll --name filingstatus_tax_engine
python manage.py test payroll.tests.test_dz_irg_integration payroll.tests.test_dz_irg -v 2
```

Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add payroll/models/models.py payroll/methods/tax_calc.py payroll/migrations/0019_filingstatus_tax_engine.py payroll/tests/test_dz_irg_integration.py
git commit -m "feat(payroll): FilingStatus can run the Algeria IRG engine"
```

---

## Task 13: Seed CNAS, IRG and the DZ allowances

Why: CNAS 9% employee + 25% employer + 0.5% FNPOS is expressible as a normal
`Deduction` (`rate`, `employer_rate`, `is_pretax`, `is_tax`). No parallel engine.

**Files:**
- Create: `payroll/management/commands/seed_algeria_payroll.py`
- Test: `payroll/tests/test_seed_algeria_payroll.py`

- [ ] **Step 1: Write the failing test**

```python
from django.core.management import call_command
from django.test import TestCase

from payroll.models.models import Deduction, FilingStatus


class SeedTest(TestCase):
    def test_seed_is_idempotent(self):
        call_command("seed_algeria_payroll")
        call_command("seed_algeria_payroll")
        self.assertEqual(FilingStatus.objects.filter(filing_status="Algérie IRG 2026").count(), 1)
        self.assertEqual(Deduction.objects.filter(title="CNAS Salariale 9%").count(), 1)

    def test_cnas_component_has_employee_and_employer_rates(self):
        call_command("seed_algeria_payroll")
        cnas = Deduction.objects.get(title="CNAS Salariale 9%")
        self.assertEqual(cnas.rate, 9)
        self.assertEqual(cnas.employer_rate, 25.5)
        self.assertTrue(cnas.is_pretax)
        self.assertFalse(cnas.is_tax)
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_seed_algeria_payroll -v 2
```

Expected: `CommandError: Unknown command`.

- [ ] **Step 3: Write the command**

```python
from django.core.management.base import BaseCommand

from payroll.models.models import Allowance, Deduction, FilingStatus


class Command(BaseCommand):
    help = "Create the Algerian payroll components (idempotent)."

    def handle(self, *args, **options):
        filing, _ = FilingStatus.objects.get_or_create(
            filing_status="Algérie IRG 2026",
            defaults=dict(
                based_on="taxable_gross_pay",
                use_py=False,
                tax_engine="dz_irg",
            ),
        )
        Deduction.objects.get_or_create(
            title="CNAS Salariale 9%",
            defaults=dict(
                is_fixed=False,
                based_on="gross_pay",
                rate=9,
                employer_rate=25.5,
                is_pretax=True,
                is_tax=False,
                include_active_employees=True,
            ),
        )
        Allowance.objects.get_or_create(
            title="Prime de transport",
            defaults=dict(is_fixed=True, amount=0, is_taxable=False),
        )
        Allowance.objects.get_or_create(
            title="Panier",
            defaults=dict(is_fixed=True, amount=0, is_taxable=False),
        )
        self.stdout.write(self.style.SUCCESS("Algeria payroll components ready."))
```

- [ ] **Step 4: Run**

```bash
python manage.py test payroll.tests.test_seed_algeria_payroll -v 2
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add payroll/management/commands/seed_algeria_payroll.py payroll/tests/test_seed_algeria_payroll.py
git commit -m "feat(payroll): seed Algerian CNAS/IRG components"
```

---

## Task 14: End-to-end golden payslip (80 000 DA)

**Files:**
- Test: `payroll/tests/test_dz_payroll_golden.py`
- Reference: `payroll/tests/test_payroll_calculation_golden.py` (copy its patching pattern)

- [ ] **Step 1: Write the failing test**

```python
from datetime import date
from unittest.mock import patch

from django.test import TestCase

from horilla.testkit import make_company, make_employee
from payroll.methods.payroll_run import payroll_calculation
from payroll.models.models import Deduction, FilingStatus
from payroll.tests.factories_payroll import make_active_contract


class DzGoldenPayslip(TestCase):
    def test_80000_gross_matches_the_reference_case(self):
        company = make_company()
        employee = make_employee(company=company, email="dz@test.dz")
        contract = make_active_contract(employee, wage=80000.0)

        filing, _ = FilingStatus.objects.get_or_create(
            filing_status="Algérie IRG 2026",
            defaults=dict(based_on="taxable_gross_pay", tax_engine="dz_irg"),
        )
        contract.filing_status = filing
        contract.save()
        Deduction.objects.get_or_create(
            title="CNAS Salariale 9%",
            defaults=dict(
                is_fixed=False,
                based_on="gross_pay",
                rate=9,
                employer_rate=25.5,
                is_pretax=True,
                is_tax=False,
                include_active_employees=True,
            ),
        )

        with patch("payroll.methods.methods.get_working_days", return_value={
            "total_working_days": 22,
            "working_days_on": [],
            "company_leave_dates": [],
        }), patch("payroll.methods.methods.get_leaves", return_value={
            "paid_leave": 0, "unpaid_leaves": 0, "partial_pay_days": 0,
            "total_leaves": 0, "paid_leave_dates": [], "unpaid_leave_dates": [],
            "custom_leave_dates": [], "custom_leave_breakdown": [], "leave_dates": [],
        }):
            data = payroll_calculation(employee, date(2026, 1, 1), date(2026, 1, 31))

        self.assertAlmostEqual(data["gross_pay"], 80000.0, places=2)
        self.assertAlmostEqual(data["total_deductions"], 7200.0 + 11956.0, places=2)
        self.assertAlmostEqual(data["net_pay"], 60844.0, places=2)
```

- [ ] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_dz_payroll_golden -v 2
```

Expected: FAIL. Record the actual gross/IRG/net in the failure message. If gross
is not 80 000, the contract wage or the working-day patch is wrong; fix the
fixture, not the assertion.

- [ ] **Step 3: Fix the wiring, not the numbers**

- If CNAS is not deducted, confirm `include_active_employees=True` and
  `is_pretax=True`.
- If IRG is 0, confirm `contract.filing_status_id` is set and the parameter row
  for 2026 exists (`python manage.py migrate payroll`).
- If gross is prorated, confirm the contract covers the whole period and
  `deduct_leave_from_basic_pay=True`.

Do not change the expected 60 844 unless the source in `01 §7.2` changes.

- [ ] **Step 4: Run the full payroll suite**

```bash
python manage.py test payroll -v 2
```

Expected: PASS. Any other golden test that changed means pay changed; inspect
the diff before accepting.

- [ ] **Step 5: Commit**

```bash
git add payroll/tests/test_dz_payroll_golden.py
git commit -m "test(payroll): golden Algerian payslip (80k -> net 60,844)"
```

---

## Task 15: Employer cost service (costisation)

**Files:**
- Create: `payroll/methods/dz_cost.py`
- Test: `payroll/tests/test_dz_cost.py`

- [x] **Step 1: Write the failing test**

```python
from datetime import date
from decimal import Decimal

from django.test import SimpleTestCase

from payroll.methods.dz_cost import compute_employer_cost
from payroll.models.tax_models import AlgeriaPayrollParameter


class CostTest(SimpleTestCase):
    def setUp(self):
        self.p = AlgeriaPayrollParameter(
            effective_from=date(2026, 1, 1),
            snmg_monthly=24000,
            cnas_employee_rate=9,
            cnas_employer_rate=25,
            fnpos_rate=0.5,
            tfpc_rate=1,
            tapp_rate=1,
        )

    def test_reference_case(self):
        cost = compute_employer_cost(80000, self.p)
        self.assertEqual(cost.total, Decimal("108666.67"))
        self.assertEqual(cost.per_paid_hour, Decimal("626.99"))

    def test_raise_factor(self):
        self.assertEqual(
            compute_employer_cost(1000, self.p).total, Decimal("1358.33")
        )
```

- [x] **Step 2: Run it and watch it fail**

```bash
python manage.py test payroll.tests.test_dz_cost -v 2
```

Expected: `ModuleNotFoundError`.

- [x] **Step 3: Write the service**

```python
"""Algerian employer cost (see algeria-sirh/01 §7)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal("0.01")
PAID_HOURS = Decimal("173.33")


def _q(value) -> Decimal:
    return Decimal(str(value)).quantize(TWOPLACES, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class EmployerCost:
    gross: Decimal
    cnas_employer: Decimal
    fnpos: Decimal
    tfpc: Decimal
    tapp: Decimal
    leave_provision: Decimal
    total: Decimal
    per_paid_hour: Decimal


def compute_employer_cost(
    gross,
    params,
    *,
    sector: str = "general",
    training_credit: float = 0.0,
) -> EmployerCost:
    gross_d = Decimal(str(gross))
    cnas = _q(gross_d * Decimal(str(params.cnas_employer_rate)) / 100)
    fnpos = _q(gross_d * Decimal(str(params.fnpos_rate)) / 100)
    tfpc_rate = max(0.0, float(params.tfpc_rate) - float(training_credit))
    tfpc = _q(gross_d * Decimal(str(tfpc_rate)) / 100)
    tapp = _q(gross_d * Decimal(str(params.tapp_rate)) / 100)
    leave = (
        Decimal("0")
        if sector == "btph"
        else _q(gross_d * Decimal("0.0833"))
    )
    total = gross_d + cnas + fnpos + tfpc + tapp + leave
    return EmployerCost(
        gross=gross_d,
        cnas_employer=cnas,
        fnpos=fnpos,
        tfpc=tfpc,
        tapp=tapp,
        leave_provision=leave,
        total=_q(total),
        per_paid_hour=_q(total / PAID_HOURS),
    )
```

- [x] **Step 4: Run**

```bash
python manage.py test payroll.tests.test_dz_cost -v 2
```

Expected: PASS. If `626.99` fails by a cent, check the rounding order; round the
total first, then divide.

- [ ] **Step 5: Commit**

```bash
git add payroll/methods/dz_cost.py payroll/tests/test_dz_cost.py
git commit -m "feat(payroll): Algerian employer cost service"
```

---

## Task 16: Document the switch and close M0/M1

**Files:**
- Modify: `algeria-sirh/00-index.md` (status)
- Create: `algeria-sirh/10-m0-m1-delivery-notes.md`

- [ ] **Step 1: Write the delivery note**

```markdown
# M0/M1 delivery notes

- Branch: `algeria/m0-m1`
- Commands:
  - `python manage.py migrate payroll`
  - `python manage.py seed_algeria_payroll`
- What is now correct: weekly-off calendar, bulk period, atomic batch, CSV
  safety, leave balance lock, Decimal money, conflict blocking, IRG, CNAS,
  costisation.
- What is still out of scope: declarations, contract types, shifts, bilingual
  documents, CASNOS, BTPH, bank files.
```

- [ ] **Step 2: Run the full gate**

```bash
python manage.py makemigrations --check --dry-run
python manage.py test payroll base leave horilla_views
make test-smoke
```

Expected: no missing migrations, all tests pass.

- [ ] **Step 3: Commit and push**

```bash
git add algeria-sirh/00-index.md algeria-sirh/10-m0-m1-delivery-notes.md
git commit -m "docs(algeria): M0/M1 delivery notes"
git push -u fork algeria/m0-m1
```

---

## Task 17: Localization pass — pin English-asserting tests (QA gate)

**Context:** the fork serves French by default, upstream/fork tests assert
English UI strings, and `makemigrations --check` resolves lazy-translated
field metadata in the active locale (fake `horilla_documents` drift under
French). Resolution (2026-11-09): `LANGUAGE_CODE` is env-overridable, CI
runs the check AND the smoke suite with `LANGUAGE_CODE=en` (canonical
msgids for the check, English assertions for the tests), the `fr` catalogues
still compile as the translation gate, and the two golden payslip tests pin
`fr` themselves via `override_settings`.

- [x] `horilla/settings/base.py`: `LANGUAGE_CODE = env("LANGUAGE_CODE", default="fr")`
- [x] CI: `LANGUAGE_CODE: en` on the makemigrations-check and test steps
- [x] `test_payroll_calculation_golden.py` + `test_dz_payroll_golden.py`: `@override_settings(LANGUAGE_CODE="fr")`
- [ ] Re-run `make test-smoke` until the gate is green, then re-pin Railway.

## M2+ roadmap (separate plans)

| Milestone | Working software produced | Acceptance test |
|---|---|---|
| M2 Declarations | DAC, DAS, G50, G29, ANEM, AT/MP, TFPC/TAPP extracts with receipt + status | one golden file per declaration compared to a hand-checked sample |
| M3 Contracts & shifts | CDD motive + requalification guard; part-time; trial; `ShiftPattern`/`RotationRule` with 12 h / 8 h OT / rolling-rest validators | roster refuses 12 h+ and no-rest patterns; CDD without motive is rejected |
| M4 Localization | FR/AR documents, DZD formats, holiday admin with communiqué, retention + ANPDP | bilingual PDF snapshot; holiday correction recomputes a closed payroll |
| M5 CASNOS + BTPH + bank | CASNOS annual base/15 %; BTPH 38.085 %; RIB/VIR.EDI adapters | CASNOS golden case; BTPH cost differs from general; RIB checksum rejects bad keys |
| M6 Costisation UI | per employee/establishment/cost centre, budget vs actual, raise simulator | dashboard totals reconcile to `compute_employer_cost` |
| M7 Hardening | ANPDP register, DPO, breach clock, load test 500 employees | 500-employee payroll < 2 min; breach workflow produces evidence |

---

## Execution handoff

Plan complete and saved to `algeria-sirh/08-implementation-plan.md`.

Two execution options:

1. **Subagent-driven (recommended)** — one fresh subagent per task, review
   between tasks.
2. **Inline execution** — run the tasks in this session with checkpoints.

Which approach?
