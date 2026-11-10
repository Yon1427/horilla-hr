"""G50 extract tests (M2-5) — golden fixture from the sirh-legal M2 report.

G50 is the monthly IRG withholding return + payment, totals only (the
per-employee detail is an internal annex; G29 is the annual nominative
return). Window: 1st-20th of M+1. Golden February 2026, one 80 000 DA
employee: taxable base 72 800, withheld 11 956, payment 11 956.
"""

from datetime import date
from decimal import Decimal

from django.test import TestCase

from payroll.declarations.g50 import build_g50, g50_window
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


class G50Golden(TestCase):
    def test_reference_month_matches_the_fixture(self):
        g50 = build_g50(
            company_nif="000016001234567",
            fiscal_period="2026-02",
            lines=[("B-001", "BENALI", "Yasmine", 72800, 11956)],
            params=spec_params(),
        )
        self.assertEqual(
            g50["irg_salaries_taxable_base_total"], Decimal("72800.00")
        )
        self.assertEqual(
            g50["irg_salaries_withheld_total"], Decimal("11956.00")
        )
        self.assertEqual(g50["payment_amount"], Decimal("11956.00"))
        self.assertEqual(len(g50["per_employee_detail"]), 1)

    def test_withheld_total_is_the_sum_of_the_detail_lines(self):
        lines = [
            ("B-001", "A", "One", 72800, 11956),
            ("B-002", "B", "Two", 30000, 0),
            ("B-003", "C", "Three", 35000, 897.33),
        ]
        g50 = build_g50(
            company_nif="000016001234567",
            fiscal_period="2026-02",
            lines=lines,
            params=spec_params(),
        )
        self.assertEqual(
            g50["irg_salaries_withheld_total"],
            Decimal("11956.00") + Decimal("0.00") + Decimal("897.33"),
        )
        self.assertEqual(
            g50["irg_salaries_taxable_base_total"],
            Decimal("72800.00") + Decimal("30000.00") + Decimal("35000.00"),
        )

    def test_neant_month_still_files(self):
        # No withholding in the month: the G50 files with zero totals (PAY-21).
        g50 = build_g50(
            company_nif="000016001234567",
            fiscal_period="2026-02",
            lines=[],
            params=spec_params(),
        )
        self.assertEqual(g50["irg_salaries_withheld_total"], Decimal("0.00"))
        self.assertEqual(g50["payment_amount"], Decimal("0.00"))
        self.assertTrue(g50["neant"])

    def test_ten_percent_bonus_slice_stays_separate(self):
        g50 = build_g50(
            company_nif="000016001234567",
            fiscal_period="2026-02",
            lines=[("B-001", "BENALI", "Yasmine", 72800, 11956)],
            bonus_10_base=10000,
            bonus_10_irg=1000,
            params=spec_params(),
        )
        # The 10 % flat slice never merges into the barème totals.
        self.assertEqual(
            g50["irg_salaries_taxable_base_total"], Decimal("72800.00")
        )
        self.assertEqual(g50["irg_10pct_total"], Decimal("1000.00"))
        self.assertEqual(
            g50["payment_amount"], Decimal("11956.00") + Decimal("1000.00")
        )

    def test_window_is_the_first_to_the_twentieth_of_the_next_month(self):
        start, end = g50_window("2026-02", spec_params())
        self.assertEqual(start, date(2026, 3, 1))
        self.assertEqual(end, date(2026, 3, 20))
