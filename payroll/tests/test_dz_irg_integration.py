from datetime import date

from django.test import TestCase

from payroll.methods.dz_irg import compute_monthly_irg
from payroll.methods.tax_calc import compute_yearly_tax
from payroll.models.tax_models import AlgeriaPayrollParameter
from payroll.tests.factories_payroll import make_filing_status


def spec_params(**overrides):
    """In-memory parameter row with the model defaults (01 §3.3, S2 OFF)."""
    values = dict(
        snmg_monthly=24000,
        irg_brackets=AlgeriaPayrollParameter.DZ_IRG_BRACKETS,
        irg_exemption_monthly=30000,
        abatement_rate=40,
        abatement_min=1000,
        abatement_max=1500,
        smoothing_min=30000,
        smoothing_max=35000,
        smoothing_factor=137 / 51,
        smoothing_offset=27925 / 8,
        disabled_smoothing_max=42500,
        disabled_smoothing_factor=93 / 61,
        disabled_smoothing_offset=81213 / 41,
    )
    values.update(overrides)
    return AlgeriaPayrollParameter(**values)


class IntegrationTest(TestCase):
    def test_dz_engine_returns_monthly_irg_times_twelve(self):
        filing = make_filing_status("Algérie IRG", tax_engine="dz_irg")
        tax, breakdown = compute_yearly_tax(
            filing, 72800 * 12, as_of=date(2026, 1, 31)
        )
        self.assertEqual(tax, 11956 * 12)
        self.assertEqual(breakdown["mode"], "dz_irg")


class EngineBoundaryTest(TestCase):
    """Exact figures from 01 §3.3; a centime of drift must fail, not round away."""

    def test_golden_monthly_irg_at_72800(self):
        # 72 800: tax 13 456, abattement capped at 1 500 -> 11 956 (01 §7.2).
        self.assertEqual(compute_monthly_irg(72800, spec_params()), 11956.0)

    def test_exemption_and_smoothing_lower_edge(self):
        params = spec_params()
        self.assertEqual(compute_monthly_irg(30000, params), 0.0)
        # 30 000,01 enters the 23 % band and the smoothing zone:
        # tax 2 300,0023 - 1 000 abattement = 1 300,0023
        #   × (137/51) - (27 925/8) = 1,5358... -> 1.54
        self.assertEqual(compute_monthly_irg(30000.01, params), 1.54)

    def test_smoothing_upper_edge_excluded(self):
        # Exactly 35 000: no smoothing; tax 3 450 - 1 380 abattement = 2 070.
        self.assertEqual(compute_monthly_irg(35000, spec_params()), 2070.0)

    def test_disabled_smoothing_replaces_ordinary(self):
        # 40 000 disabled: tax 4 600 - 1 500 = 3 100, then (93/61) & (81 213/41).
        self.assertEqual(
            compute_monthly_irg(40000, spec_params(), disabled=True), 2745.42
        )
