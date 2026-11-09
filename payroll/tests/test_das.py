"""DAS extract tests (M2-4) — golden fixture from the sirh-legal M2 report.

DAS = Déclaration Annuelle des Salaires et des salariés: per-employee,
per-quarter nominative CNAS return. The 80 000 DA reference employee:
quarter = 240 000 gross/base, contributions 21 600 / 60 000 / 1 200,
annual = 960 000 / 960 000 / 86 400 / 240 000 / 4 800 / 331 200.
A row without an NSS is emitted with a blocking completeness flag, never
silently dropped.
"""

from decimal import Decimal

from django.test import TestCase

from payroll.declarations.das import build_das, build_das_row
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


MONTHS_80000 = [{"gross": 80000, "base": 80000} for _ in range(12)]


class DasGolden(TestCase):
    def test_reference_year_matches_the_fixture(self):
        row = build_das_row(
            nss="123456789012",
            nom="BENALI",
            prenom="Yasmine",
            monthly=MONTHS_80000,
            params=spec_params(),
            hire_date="2026-01-01",
        )
        for q in ("q1", "q2", "q3", "q4"):
            quarter = row[f"gross_{q}"]
            self.assertEqual(quarter, Decimal("240000.00"), q)
            self.assertEqual(row[f"base_{q}"], Decimal("240000.00"), q)
            self.assertEqual(row[f"contrib_employee_{q}"], Decimal("21600.00"), q)
            self.assertEqual(row[f"contrib_employer_{q}"], Decimal("60000.00"), q)
            self.assertEqual(row[f"fnpos_{q}"], Decimal("1200.00"), q)
        self.assertEqual(row["annual_gross"], Decimal("960000.00"))
        self.assertEqual(row["annual_base"], Decimal("960000.00"))
        self.assertEqual(row["annual_employee"], Decimal("86400.00"))
        self.assertEqual(row["annual_employer"], Decimal("240000.00"))
        self.assertEqual(row["annual_fnpos"], Decimal("4800.00"))
        self.assertEqual(row["annual_due"], Decimal("331200.00"))

    def test_extract_wraps_rows_and_carries_the_regime(self):
        row = build_das_row(
            nss="123456789012", nom="BENALI", prenom="Yasmine",
            monthly=MONTHS_80000, params=spec_params(), hire_date="2026-01-01",
        )
        extract = build_das(
            rows=[row],
            employer_cnas_no="16-1234567",
            employer_nif="000016001234567",
            declaration_year=2026,
            params=spec_params(),
        )
        self.assertEqual(extract["regime"], "GENERAL")
        self.assertEqual(extract["declaration_year"], 2026)
        self.assertEqual(len(extract["rows"]), 1)
        self.assertEqual(
            extract["totals"]["annual_due_total"], Decimal("331200.00")
        )

    def test_missing_nss_is_flagged_not_dropped(self):
        row = build_das_row(
            nss=None, nom="BENALI", prenom="Yasmine",
            monthly=MONTHS_80000, params=spec_params(), hire_date="2026-01-01",
        )
        self.assertTrue(row["blocking_completeness"])
        extract = build_das(
            rows=[row], employer_cnas_no="16-1234567",
            employer_nif="000016001234567", declaration_year=2026,
            params=spec_params(),
        )
        self.assertEqual(len(extract["rows"]), 1)  # present, flagged, not dropped
        self.assertEqual(extract["rows"][0]["nss"], None)

    def test_exactly_twelve_months_are_required(self):
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            build_das_row(
                nss="123456789012", nom="X", prenom="Y",
                monthly=MONTHS_80000[:11], params=spec_params(),
                hire_date="2026-01-01",
            )
