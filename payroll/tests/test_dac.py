"""DAC extract tests (M2-3) — golden fixture from the sirh-legal report.

DAC = Déclaration d'Assiette des Cotisations: per-employee assiettes and
cotisations (9 % employee, 25 % employer, 0,5 % FNPOS). The totals carry
NOTHING but s×A: no leave provision, no TFPC/TAPP, no IRG, no non-cotisable
allowances. Golden: G = 80 000, A = 80 000 → 7 200 / 20 000 / 400,
total à payer 27 600.
"""

from decimal import Decimal

from django.test import TestCase

from payroll.declarations.dac import build_dac
from payroll.models.tax_models import AlgeriaPayrollParameter


def spec_params(**overrides):
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


class DacGolden(TestCase):
    def test_reference_case_matches_the_fixture(self):
        dac = build_dac(
            lines=[("B-001", "BENALI", "Yasmine", 80000, 80000, None)],
            employer_cnas_no="16-1234567",
            period="2026-02",
            params=spec_params(),
        )
        line = dac["lines"][0]
        self.assertEqual(line["gross_G"], Decimal("80000.00"))
        self.assertEqual(line["assiette_A"], Decimal("80000.00"))
        self.assertEqual(line["cot_sal"], Decimal("7200.00"))
        self.assertEqual(line["cot_pat"], Decimal("20000.00"))
        self.assertEqual(line["fnpos"], Decimal("400.00"))
        self.assertEqual(line["total_line"], Decimal("27600.00"))
        self.assertEqual(dac["totals"]["total_a_payer"], Decimal("27600.00"))
        self.assertEqual(dac["totals"]["cot_sal_total"], Decimal("7200.00"))
        self.assertEqual(dac["totals"]["cot_pat_total"], Decimal("20000.00"))
        self.assertEqual(dac["totals"]["fnpos_total"], Decimal("400.00"))

    def test_non_cotisable_allowances_stay_out_of_the_totals(self):
        # G = 85 000 with 5 000 transport; the cotisations run on A = 80 000.
        dac = build_dac(
            lines=[("B-001", "BENALI", "Yasmine", 85000, 80000, None)],
            employer_cnas_no="16-1234567",
            period="2026-02",
            params=spec_params(),
        )
        line = dac["lines"][0]
        self.assertEqual(line["gross_G"], Decimal("85000.00"))
        self.assertEqual(line["total_line"], Decimal("27600.00"))
        self.assertEqual(dac["totals"]["total_a_payer"], Decimal("27600.00"))

    def test_multi_line_totals_equal_the_header_to_the_centime(self):
        lines = [
            ("B-001", "A", "One", 33333.33, 33333.33, None),
            ("B-002", "B", "Two", 16666.67, 16666.67, None),
            ("B-003", "C", "Three", 50000.00, 50000.00, None),
        ]
        dac = build_dac(
            lines=lines, employer_cnas_no="16-1234567", period="2026-02",
            params=spec_params(),
        )
        expected_total = sum(
            (line["cot_sal"] + line["cot_pat"] + line["fnpos"])
            for line in dac["lines"]
        )
        self.assertEqual(dac["totals"]["total_a_payer"], expected_total)
        # s × ΣA: (0.255 + 0.09) × 100 000.00 = 34 500.00
        self.assertEqual(dac["totals"]["total_a_payer"], Decimal("34500.00"))
