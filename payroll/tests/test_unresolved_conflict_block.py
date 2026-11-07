from datetime import date

from django.test import TestCase

from horilla.testkit import make_company, make_employee
from payroll.methods.errors import PayrollBlockedError
from payroll.methods.methods import compute_salary_on_period


class UnresolvedConflictTest(TestCase):
    def test_unresolved_conflict_raises(self):
        company = make_company()
        employee = make_employee(company=company, email="conflict@test.dz")
        with self.assertRaises(PayrollBlockedError):
            compute_salary_on_period(
                employee,
                date(2024, 1, 1),
                date(2024, 1, 31),
                month_summary={"unresolved_conflicts": 1},
            )

    def test_no_conflict_does_not_raise(self):
        company = make_company()
        employee = make_employee(company=company, email="noconflict@test.dz")
        # Must not raise the block when the summary has no conflict.
        compute_salary_on_period(
            employee,
            date(2024, 1, 1),
            date(2024, 1, 31),
            month_summary={"unresolved_conflicts": 0},
        )
