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
