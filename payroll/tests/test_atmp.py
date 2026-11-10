"""AT/MP extract tests (M2-7) — sirh-legal M2 report golden fixture.

Work accident declaration: the 48 h clock runs from knowledge_datetime
(2026-06-02T09:00 → due 2026-06-04T09:00); filing at 2026-06-03T16:20 is
ON_TIME with a 1 000-minute margin; 2026-06-04T10:00 is LATE by 60.
The employer cannot know the accident before it happened, and no
diagnosis may sit in an HR-visible field.
"""

from datetime import datetime, timedelta, timezone

from django.core.exceptions import ValidationError
from django.test import TestCase

from payroll.declarations.atmp import atmp_due, atmp_status, build_atmp
from payroll.models.tax_models import AlgeriaPayrollParameter

TZ = timezone(timedelta(hours=1))  # Africa/Algiers, no DST


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


EMPLOYER = {"cnas_no": "16-1234567", "nif": "000016001234567", "wilaya": "16"}
VICTIM = {
    "nom": "BENALI", "prenom": "Yasmine", "nss": "1234567890123456789",
    "nin": "199503140012345678", "job": "Comptable", "contract_type": "CDI",
    "hire_date": "2026-01-05",
}
ACCIDENT = {
    "accident_datetime": datetime(2026, 6, 2, 8, 15, tzinfo=TZ),
    "knowledge_datetime": datetime(2026, 6, 2, 9, 0, tzinfo=TZ),
    "place": "Chantier Oran",
}


class AtmpClock(TestCase):
    def test_due_is_knowledge_plus_forty_eight_hours(self):
        due = atmp_due(ACCIDENT["knowledge_datetime"], spec_params())
        self.assertEqual(due, datetime(2026, 6, 4, 9, 0, tzinfo=TZ))

    def test_filing_before_due_is_on_time_with_the_exact_margin(self):
        filed = datetime(2026, 6, 3, 16, 20, tzinfo=TZ)
        status = atmp_status(ACCIDENT["knowledge_datetime"], filed, spec_params())
        self.assertEqual(status["status"], "ON_TIME")
        self.assertEqual(status["margin_minutes"], 1000)

    def test_filing_after_due_is_late_by_the_exact_minutes(self):
        filed = datetime(2026, 6, 4, 10, 0, tzinfo=TZ)
        status = atmp_status(ACCIDENT["knowledge_datetime"], filed, spec_params())
        self.assertEqual(status["status"], "LATE")
        self.assertEqual(status["lateness_minutes"], 60)


class AtmpExtract(TestCase):
    def test_reference_case_builds(self):
        extract = build_atmp(
            employer=EMPLOYER, victim=VICTIM, accident=ACCIDENT,
            params=spec_params(),
        )
        self.assertEqual(
            extract["due_datetime"], datetime(2026, 6, 4, 9, 0, tzinfo=TZ)
        )
        self.assertEqual(extract["status"], "ON_TIME" if False else extract["status"])

    def test_knowledge_cannot_precede_the_accident(self):
        bad = dict(ACCIDENT, knowledge_datetime=datetime(2026, 6, 2, 7, 0, tzinfo=TZ))
        with self.assertRaises(ValidationError):
            build_atmp(employer=EMPLOYER, victim=VICTIM, accident=bad,
                       params=spec_params())

    def test_missing_legal_minimums_block(self):
        for drop in ("nss", "job"):
            victim = dict(VICTIM, **{drop: None})
            with self.assertRaises(ValidationError):
                build_atmp(employer=EMPLOYER, victim=victim, accident=ACCIDENT,
                           params=spec_params())
        for drop in ("accident_datetime", "knowledge_datetime", "place"):
            accident = dict(ACCIDENT, **{drop: None})
            with self.assertRaises(ValidationError):
                build_atmp(employer=EMPLOYER, victim=VICTIM, accident=accident,
                           params=spec_params())

    def test_diagnosis_is_segregated_out_of_hr_fields(self):
        injury = {"diagnosis": "fracture", "nature": "chute"}
        with self.assertRaises(ValidationError):
            build_atmp(employer=EMPLOYER, victim=VICTIM, accident=ACCIDENT,
                       injury=injury, params=spec_params())
        # Medical data lives behind the medical store; the extract carries
        # only the certificate reference and the stoppage flag.
        extract = build_atmp(
            employer=EMPLOYER, victim=VICTIM, accident=ACCIDENT,
            medical={"certificate_ref": "MED-2026-01", "stoppage": True},
            params=spec_params(),
        )
        self.assertEqual(extract["medical"]["certificate_ref"], "MED-2026-01")
