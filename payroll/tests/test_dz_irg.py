from datetime import date

from django.test import SimpleTestCase

from payroll.methods.dz_irg import compute_monthly_irg, compute_yearly_irg
from payroll.models.tax_models import AlgeriaPayrollParameter


class IrgTest(SimpleTestCase):
    def setUp(self):
        self.params = AlgeriaPayrollParameter(
            effective_from=date(2026, 1, 1),
            irg_brackets=AlgeriaPayrollParameter.DZ_IRG_BRACKETS,
        )

    def test_exempt_at_30000(self):
        self.assertEqual(compute_monthly_irg(30000, self.params), 0)

    def test_80000_gross_example_taxable_72800(self):
        self.assertEqual(compute_monthly_irg(72800, self.params), 11956)

    def test_year_conversion_is_monthly_times_twelve(self):
        self.assertEqual(
            compute_yearly_irg(72800 * 12, self.params), 11956 * 12
        )

    def test_band_boundaries_are_stable(self):
        values = [30001, 34999, 35000, 35001, 42500]
        taxes = [compute_monthly_irg(value, self.params) for value in values]
        self.assertEqual(taxes, sorted(taxes))

    def test_disabled_band_uses_42500_threshold(self):
        self.assertGreater(compute_monthly_irg(40000, self.params, disabled=True), 0)

    def test_negative_income_is_zero(self):
        self.assertEqual(compute_monthly_irg(-1000, self.params), 0)
