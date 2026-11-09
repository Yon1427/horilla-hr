"""Golden Algerian payslip: 80 000 DA gross -> 60 844 net (01 section 7.2).

Wires M1-12 (dz_irg engine switch) + M1-13 (CNAS seed shape) end to end:
CNAS 9 % pretax of gross, IRG on the remainder through FilingStatus dz_irg.
Do not change 60 844 unless the source in 01 section 7.2 changes.
"""

from datetime import date
from unittest.mock import patch

from django.test import TestCase

from horilla.testkit import make_company, make_employee
from payroll.methods.payroll_run import payroll_calculation
from payroll.models.models import Contract, Deduction, FilingStatus
from payroll.tests.factories_payroll import make_active_contract

PERIOD_START = date(2026, 1, 1)
PERIOD_END = date(2026, 1, 31)
WORKING_DAYS = 22
PER_DAY = 80000.0 / WORKING_DAYS

EMPTY_LEAVES = {
    "paid_leave": 0,
    "unpaid_leaves": 0,
    "partial_pay_days": 0,
    "total_leaves": 0,
    "paid_leave_dates": [],
    "unpaid_leave_dates": [],
    "custom_leave_dates": [],
    "custom_leave_breakdown": [],
    "leave_dates": [],
}


class DzGoldenPayslip(TestCase):
    def test_80000_gross_matches_the_reference_case(self):
        company = make_company("DZ Golden Co")
        employee = make_employee(company=company, email="dz@test.dz")
        # make_employee's own contract (if any) would compete for "active".
        Contract.objects.filter(employee_id=employee).delete()
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

        with patch(
            "payroll.methods.methods.months_between_range",
            return_value=[
                {"working_days_on_period": WORKING_DAYS, "per_day_amount": PER_DAY}
            ],
        ), patch(
            "payroll.methods.methods.get_daily_salary",
            return_value={"day_wage": PER_DAY},
        ), patch(
            "payroll.methods.methods.get_leaves", return_value=EMPTY_LEAVES
        ):
            data = payroll_calculation(employee, PERIOD_START, PERIOD_END)

        self.assertIsNotNone(data, "engine returned no payslip data")
        self.assertEqual(data["gross_pay"], 80000.0)
        self.assertEqual(data["total_deductions"], 7200.0 + 11956.0)
        self.assertEqual(data["net_pay"], 60844.0)
