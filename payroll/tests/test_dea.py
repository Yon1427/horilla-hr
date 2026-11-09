"""DEA extract tests (M2-2) — golden fixture from the sirh-legal report.

Hire 2026-02-02 → due 2026-02-12 (D+10, hire day D0); first affiliation
carries nss=null and nin=null; overdue from D+11.
"""

from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from horilla.testkit import make_company, make_employee
from payroll.declarations.dea import build_dea, dea_due_date, dea_is_overdue
from payroll.models.models import Contract
from payroll.models.tax_models import AlgeriaPayrollParameter
from payroll.tests.factories_payroll import make_active_contract


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


class DeaReferenceCase(TestCase):
    def setUp(self):
        self.company = make_company("DEA Co")
        self.employee = make_employee(company=self.company, email="dea@test.dz")
        self.employee.employee_first_name = "Yasmine"
        self.employee.employee_last_name = "BENALI"
        self.employee.dob = date(1995, 3, 14)
        self.employee.save()
        # make_employee's own contract would compete for "active".
        Contract.objects.filter(employee_id=self.employee).delete()
        self.contract = make_active_contract(self.employee, wage=80000)
        self.contract.contract_start_date = date(2026, 2, 2)
        self.contract.save()

    def test_reference_case_matches_the_fixture(self):
        extract = build_dea(
            self.employee,
            self.contract,
            employer_cnas_no="16-1234567",
            employer_nif="000016001234567",
            params=spec_params(),
        )
        self.assertEqual(extract["hire_date"], date(2026, 2, 2))
        self.assertEqual(extract["due_date"], date(2026, 2, 12))
        self.assertEqual(extract["nom"], "BENALI")
        self.assertEqual(extract["prenom"], "Yasmine")
        self.assertEqual(extract["date_naissance"], date(1995, 3, 14))
        self.assertIsNone(extract["nss"])
        self.assertIsNone(extract["nin"])
        self.assertEqual(extract["salaire_embauche_brut"], Decimal("80000"))
        self.assertEqual(extract["cnas_base_initiale"], Decimal("80000"))

    def test_overdue_starts_the_day_after_the_due_date(self):
        params = spec_params()
        self.assertEqual(dea_due_date(date(2026, 2, 2), params), date(2026, 2, 12))
        self.assertFalse(dea_is_overdue(date(2026, 2, 2), date(2026, 2, 12), params))
        self.assertTrue(dea_is_overdue(date(2026, 2, 2), date(2026, 2, 13), params))

    def test_missing_cnas_number_is_refused(self):
        with self.assertRaises(ValidationError):
            build_dea(self.employee, self.contract, employer_cnas_no="")

    def test_nin_becomes_mandatory_only_via_the_parameter(self):
        params = spec_params(dea_nin_required=True)
        with self.assertRaises(ValidationError):
            build_dea(self.employee, self.contract, "16-1234567", params=params)
        extract = build_dea(
            self.employee,
            self.contract,
            "16-1234567",
            nin="199503140012345678",
            params=params,
        )
        self.assertEqual(extract["nin"], "199503140012345678")
