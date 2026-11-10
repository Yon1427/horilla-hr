"""G29 extract tests (M2-6) — golden fixture from the sirh-legal M2 report.

Annual per-beneficiary IRG return (CIDTA art. 75-2/75-3). NIN mandatory
since LF 2026. Money columns are sums of monthly payroll values — never
recomputed through an annualised barème. Golden year 2026, 80 000 DA
employee: gross 960 000, CNAS 86 400, IRG base 873 600, IRG 143 472,
net 730 128.
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from payroll.declarations.g29 import build_g29, build_g29_row
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


MONTHS_80000 = [
    {"gross": 80000, "cnas_sal": 7200, "taxable": 72800, "irg": 11956,
     "net": 60844}
    for _ in range(12)
]

MONTHS_NEANT = [
    {"gross": 28900, "cnas_sal": 2601, "taxable": 26299, "irg": 0,
     "net": 26299}
    for _ in range(12)
]


class G29Golden(TestCase):
    def test_reference_year_matches_the_fixture(self):
        row = build_g29_row(
            nin="199503140012345678",
            nom="BENALI",
            prenom="Yasmine",
            monthly=MONTHS_80000,
            params=spec_params(),
        )
        self.assertEqual(row["gross_annuel"], Decimal("960000.00"))
        self.assertEqual(row["cnas_salariale_annuelle"], Decimal("86400.00"))
        self.assertEqual(row["base_irg_annuelle"], Decimal("873600.00"))
        self.assertEqual(row["irg_annuel"], Decimal("143472.00"))
        self.assertEqual(row["net_annuel"], Decimal("730128.00"))
        self.assertFalse(row["neant_mention"])

    def test_nin_is_mandatory(self):
        with self.assertRaises(ValidationError):
            build_g29_row(
                nin="", nom="BENALI", prenom="Yasmine",
                monthly=MONTHS_80000, params=spec_params(),
            )
        # A legacy row before the 2026 mandate could pass with the flag off.
        row = build_g29_row(
            nin="", nom="BENALI", prenom="Yasmine",
            monthly=MONTHS_80000, params=spec_params(g29_nin_mandatory=False),
        )
        self.assertEqual(row["nin"], None)

    def test_neant_row_is_flagged_and_zero(self):
        row = build_g29_row(
            nin="199503140012345678", nom="BENALI", prenom="Yasmine",
            monthly=MONTHS_NEANT, params=spec_params(),
        )
        self.assertEqual(row["irg_annuel"], Decimal("0.00"))
        self.assertTrue(row["neant_mention"])

    def test_monthly_arithmetic_must_be_consistent(self):
        bad = [dict(MONTHS_80000[0])]
        bad[0]["taxable"] = 73000  # gross - cnas_sal = 72800, not 73000
        with self.assertRaises(ValidationError):
            build_g29_row(
                nin="199503140012345678", nom="BENALI", prenom="Yasmine",
                monthly=bad + MONTHS_80000[1:], params=spec_params(),
            )

    def test_extract_totals_equal_the_row_sums(self):
        row = build_g29_row(
            nin="199503140012345678", nom="BENALI", prenom="Yasmine",
            monthly=MONTHS_80000, params=spec_params(),
        )
        extract = build_g29(
            rows=[row], employer_nif="000016001234567",
            employer_cnas_no="16-1234567", fiscal_year=2026,
            params=spec_params(),
        )
        self.assertEqual(extract["fiscal_year"], 2026)
        self.assertEqual(
            extract["totals"]["irg_total"], Decimal("143472.00")
        )
        self.assertEqual(
            extract["totals"]["gross_total"], Decimal("960000.00")
        )
