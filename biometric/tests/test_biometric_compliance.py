"""Compliance gate for biometric enrolment (Loi 18-07 art. 18 / loi 25-11).

The gate is deliberately a blocker: a template stored without a legal basis is
the finding an ANPDP inspection reports. These tests pin the two independent
conditions (company authorisation, employee consent), the ANPDP "not required"
escape hatch, and the purge-on-exit obligation.
"""

from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from biometric.models import (
    BiometricConsent,
    BiometricDevices,
    BiometricEmployees,
    BiometricProcessingAuthorisation,
)
from employee.models import Employee
from horilla.testkit.factories import make_company, make_employee


class BiometricComplianceTests(TestCase):
    def setUp(self):
        self.company = make_company("Sanad Test")
        self.employee = make_employee(company=self.company, email="bio@test.dz")
        self.device = BiometricDevices.objects.create(
            name="ZKTeco 1",
            machine_type="zk",
            machine_ip="10.0.0.10",
            company_id=self.company,
        )

    def authorise(self, **overrides):
        defaults = {
            "company_id": self.company,
            "dpia_completed_on": date(2026, 1, 1),
            "anpdp_authorisation_ref": "ANPDP-2026-001",
        }
        defaults.update(overrides)
        return BiometricProcessingAuthorisation.objects.create(**defaults)

    def consent(self, **overrides):
        defaults = {
            "employee_id": self.employee,
            "company_id": self.company,
            "consent_given_on": date(2026, 1, 1),
            "consent_reference": "FORM-2026-001",
        }
        defaults.update(overrides)
        return BiometricConsent.objects.create(**defaults)

    def enrol(self):
        return BiometricEmployees.objects.create(
            user_id="1001",
            employee_id=self.employee,
            device_id=self.device,
        )

    def test_blocked_without_company_authorisation(self):
        self.consent()
        with self.assertRaises(ValidationError):
            self.enrol()

    def test_blocked_without_employee_consent(self):
        self.authorise()
        with self.assertRaises(ValidationError):
            self.enrol()

    def test_allowed_with_authorisation_and_consent(self):
        self.authorise()
        self.consent()
        row = self.enrol()
        self.assertTrue(
            BiometricEmployees._base_manager.filter(pk=row.pk).exists()
        )

    def test_withdrawn_consent_blocks_new_enrolment(self):
        self.authorise()
        self.consent(withdrawn_on=date(2026, 2, 1))
        with self.assertRaises(ValidationError):
            self.enrol()

    def test_expired_consent_blocks_new_enrolment(self):
        self.authorise()
        self.consent(expires_on=date(2025, 12, 31))
        with self.assertRaises(ValidationError):
            self.enrol()

    def test_anpdp_reference_required_by_default(self):
        self.authorise(anpdp_authorisation_ref="")
        self.consent()
        with self.assertRaises(ValidationError):
            self.enrol()

    def test_anpdp_not_required_escape_hatch(self):
        self.authorise(anpdp_required=False, anpdp_authorisation_ref="")
        self.consent()
        self.enrol()  # no raise

    def test_missing_dpia_blocks(self):
        self.authorise(dpia_completed_on=None)
        self.consent()
        with self.assertRaises(ValidationError):
            self.enrol()

    def test_bulk_create_is_gated_too(self):
        """bulk_create bypasses save(), so the manager gate must cover it."""
        self.authorise()
        with self.assertRaises(ValidationError):
            BiometricEmployees.objects.bulk_create(
                [
                    BiometricEmployees(
                        user_id="1002",
                        employee_id=self.employee,
                        device_id=self.device,
                    )
                ]
            )

    def test_exit_purges_enrolment_and_withdraws_consent(self):
        self.authorise()
        consent = self.consent()
        row = self.enrol()

        employee = Employee.objects.get(pk=self.employee.pk)
        employee.is_active = False
        employee.save()

        self.assertFalse(
            BiometricEmployees._base_manager.filter(pk=row.pk).exists()
        )
        consent.refresh_from_db()
        self.assertIsNotNone(consent.withdrawn_on)

    def test_consent_withdrawal_cannot_predate_consent(self):
        with self.assertRaises(ValidationError):
            BiometricConsent.objects.create(
                employee_id=self.employee,
                company_id=self.company,
                consent_given_on=date(2026, 3, 1),
                withdrawn_on=date(2026, 1, 1),
                consent_reference="FORM-2",
            )
