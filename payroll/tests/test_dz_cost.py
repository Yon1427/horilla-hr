"""Employer costisation golden tests (01 §7.2, OFF-derived figures).

Monthly employer cost = G + s×A + t×G + G/12 + r
    G = gross, A = CNAS base (defaults to G), s = 25 % CNAS + 0,5 % FNPOS,
    t = TFPC + TAPP (1 % + 1 % with no training/apprenticeship spend),
    leave provision = G/12 (the 8,33 % display is 1/12 rounded),
    r = extra provisions (default 0, company-specific).
Totals are quantized once to 0.01 DA, ROUND_HALF_UP, in Decimal.
"""

from datetime import date
from decimal import Decimal

from django.test import TestCase

from payroll.models.tax_models import AlgeriaPayrollParameter


def spec_params(**overrides):
    """In-memory parameter row with the model defaults (01 §7.1)."""
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
        exceptional_bonus_rate=10,
        cnas_employee_rate=9,
        cnas_employer_rate=25,
        fnpos_rate=0.5,
        tfpc_rate=1,
        tapp_rate=1,
    )
    values.update(overrides)
    return AlgeriaPayrollParameter(**values)


class DzCostGolden(TestCase):
    def test_80000_gross_reference_case(self):
        from payroll.methods.dz_cost import compute_employer_cost

        cost = compute_employer_cost(spec_params(), 80000)
        self.assertEqual(cost["gross"], Decimal("80000.00"))
        self.assertEqual(cost["cnas_employer"], Decimal("20000.00"))
        self.assertEqual(cost["fnpos"], Decimal("400.00"))
        self.assertEqual(cost["tfpc"], Decimal("800.00"))
        self.assertEqual(cost["tapp"], Decimal("800.00"))
        self.assertEqual(cost["leave_provision"], Decimal("6666.67"))
        self.assertEqual(cost["total_monthly"], Decimal("108666.67"))
        self.assertEqual(cost["cost_per_paid_hour"], Decimal("626.94"))
        self.assertEqual(cost["annual"], Decimal("1304000.04"))
        # 1 000 DA raise × (1 + 0,255 + 0,02 + 1/12) = 1 358,33 (01 §7.2)
        raise_cost = (Decimal("1000") * cost["raise_factor"]).quantize(
            Decimal("0.01")
        )
        self.assertEqual(raise_cost, Decimal("1358.33"))

    def test_non_cotisable_allowances_stay_out_of_the_cnas_base(self):
        from payroll.methods.dz_cost import compute_employer_cost

        # G = 85 000 with 5 000 transport; A = 80 000.
        cost = compute_employer_cost(spec_params(), 85000, cnas_base=80000)
        self.assertEqual(cost["gross"], Decimal("85000.00"))
        self.assertEqual(cost["cnas_employer"], Decimal("20000.00"))
        self.assertEqual(cost["tfpc"], Decimal("850.00"))
        self.assertEqual(cost["leave_provision"], Decimal("7083.33"))
        self.assertEqual(cost["total_monthly"], Decimal("114183.33"))

    def test_zero_training_and_apprenticeship_spend_gives_the_ceiling_rates(self):
        from payroll.methods.dz_cost import compute_employer_cost

        params = spec_params(tfpc_rate=0, tapp_rate=0)
        cost = compute_employer_cost(params, 80000)
        self.assertEqual(cost["tfpc"], Decimal("0.00"))
        self.assertEqual(cost["tapp"], Decimal("0.00"))
        # 80000 + 20400 + 0 + 6666.67 = 107066.67
        self.assertEqual(cost["total_monthly"], Decimal("107066.67"))

    def test_extra_provisions_are_added_but_default_to_zero(self):
        from payroll.methods.dz_cost import compute_employer_cost

        base = compute_employer_cost(spec_params(), 80000)
        self.assertEqual(base["extra_provisions"], Decimal("0.00"))
        with_provisions = compute_employer_cost(
            spec_params(), 80000, extra_provisions=10000
        )
        self.assertEqual(with_provisions["extra_provisions"], Decimal("10000.00"))
        self.assertEqual(
            with_provisions["total_monthly"], Decimal("118666.67")
        )
