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
        row = AlgeriaPayrollParameter.for_company(company, date(2026, 6, 30))
        self.assertIsNotNone(row)
        self.assertEqual(row.snmg_monthly, 24000)
        self.assertIsNone(row.company_id)
