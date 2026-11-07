from datetime import date
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from horilla.testkit import make_company, make_employee, make_user
from payroll.methods.bulk_generate import generate_bulk_payslips
from payroll.methods.payroll_run import payroll_calculation as real_payroll_calculation
from payroll.models.models import Contract, Payslip
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
            # Employee.save() seeds a default contract; replace it with a
            # paid one the engine can actually use.
            Contract.objects.filter(employee_id=employee).delete()
            make_active_contract(employee, wage=50000.0)
        self.request = RequestFactory().post("/payroll/generate-payslip/")
        self.request.user = self.user

    @patch("payroll.methods.bulk_generate.payroll_calculation")
    def test_second_failure_rolls_back_first_payslip(self, calc):
        # The first employee must succeed and write a row, so the second one's
        # failure has something real to roll back. The plan's original
        # ``side_effect = [Exception("boom")]`` fails before the first save and
        # would pass even without @transaction.atomic.
        def fake(employee, start, end, **kwargs):
            if employee == self.employees[1]:
                raise Exception("boom")
            return real_payroll_calculation(employee, start, end, **kwargs)

        calc.side_effect = fake
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
