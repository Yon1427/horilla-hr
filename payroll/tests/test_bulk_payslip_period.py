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
