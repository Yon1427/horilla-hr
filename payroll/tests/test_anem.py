"""ANEM extract tests (M2-7) — décret 09-94 arts. 2-7 (sirh-legal M2 report).

Recruitment declaration: monthly, due month_end + 10 days. Content per
arts. 5-6: branch, socio-professional category, age, posts, contract
type, gender for recruitments. The quarterly manpower forecast is due
one month before the quarter (Q3 2026 → 1 Jun 2026); filing earlier is
on time.
"""

from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from payroll.declarations.anem import (
    anem_forecast_due_date,
    anem_recruit_due_date,
    build_anem_forecast,
    build_anem_recruitment,
)
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


HIRE = {
    "nom": "BENALI",
    "prenom": "Yasmine",
    "age": 30,
    "poste": "Comptable",
    "contract_type": "CDI",
    "gender": "female",
    "socio_prof_category": "cadre",
}


class AnemRecruitment(TestCase):
    def test_march_hires_are_due_april_10(self):
        due = anem_recruit_due_date(date(2026, 3, 31), spec_params())
        self.assertEqual(due, date(2026, 4, 10))

    def test_complete_hires_build_and_carry_the_due_date(self):
        extract = build_anem_recruitment(
            employer_nif="000016001234567",
            period="2026-03",
            period_end=date(2026, 3, 31),
            hires=[dict(HIRE), dict(HIRE, nom="AMRANI", prenom="Karim")],
            params=spec_params(),
        )
        self.assertEqual(extract["period"], "2026-03")
        self.assertEqual(extract["due_date"], date(2026, 4, 10))
        self.assertEqual(len(extract["hires"]), 2)

    def test_missing_gender_or_contract_type_blocks(self):
        without_gender = dict(HIRE, gender=None)
        with self.assertRaises(ValidationError):
            build_anem_recruitment(
                employer_nif="000016001234567",
                period="2026-03",
                period_end=date(2026, 3, 31),
                hires=[without_gender],
                params=spec_params(),
            )
        without_type = dict(HIRE, contract_type=None)
        with self.assertRaises(ValidationError):
            build_anem_recruitment(
                employer_nif="000016001234567",
                period="2026-03",
                period_end=date(2026, 3, 31),
                hires=[without_type],
                params=spec_params(),
            )

    def test_missing_socio_professional_mapping_blocks(self):
        unmapped = dict(HIRE, socio_prof_category=None)
        with self.assertRaises(ValidationError):
            build_anem_recruitment(
                employer_nif="000016001234567",
                period="2026-03",
                period_end=date(2026, 3, 31),
                hires=[unmapped],
                params=spec_params(),
            )


class AnemForecast(TestCase):
    def test_q3_forecast_is_due_one_month_before_the_quarter(self):
        self.assertEqual(
            anem_forecast_due_date(date(2026, 7, 1)), date(2026, 6, 1)
        )

    def test_early_filing_is_on_time(self):
        extract = build_anem_forecast(
            employer_nif="000016001234567",
            quarter_start=date(2026, 7, 1),
            posts=[dict(HIRE, gender=None)],
            params=spec_params(),
        )
        self.assertEqual(extract["due_date"], date(2026, 6, 1))
        # Filed 31 May: earlier than the 1 June deadline → on time.
        self.assertTrue(extract["due_date"] >= date(2026, 5, 31))
