"""Declaration registry tests (M2-1, spec 02 §7 / 05 §1.4).

Maker-checker: the person who prepares a declaration cannot file it.
The extract payloads themselves arrive with M2-2..M2-8; the registry owns
the row, the status machine and the receipt.
"""

from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from horilla.testkit import make_company, make_employee
from payroll.models.declarations import (
    Declaration,
    DeclarationStatus,
    DeclarationType,
)


class DeclarationRegistryTest(TestCase):
    def setUp(self):
        self.company = make_company("Declarations Co")
        self.maker = make_employee(company=self.company, email="maker@test.dz")
        self.checker = make_employee(company=self.company, email="checker@test.dz")

    def _declaration(self, maker):
        declaration = Declaration(
            declaration_type=DeclarationType.DAC,
            company_id=self.company,
            period_start=date(2026, 1, 1),
            period_end=date(2026, 1, 31),
        )
        declaration.save()
        # HorillaModel.save() overwrites created_by from the request user
        # (None in tests); simulate the request flow via a queryset update.
        Declaration.objects.filter(pk=declaration.pk).update(
            created_by=maker.employee_user_id
        )
        declaration.refresh_from_db()
        return declaration

    def test_maker_checker_gate_refuses_self_filing(self):
        declaration = self._declaration(self.maker)
        with self.assertRaises(ValidationError):
            declaration.file(self.maker)

    def test_checker_files_and_the_status_machine_runs(self):
        declaration = self._declaration(self.maker)
        declaration.file(self.checker)
        self.assertEqual(declaration.status, DeclarationStatus.FILED)
        self.assertEqual(declaration.filed_by, self.checker)
        self.assertIsNotNone(declaration.filed_at)

        declaration.receive("RC-2026-001", self.checker)
        self.assertEqual(declaration.status, DeclarationStatus.RECEIVED)
        self.assertEqual(declaration.receipt_reference, "RC-2026-001")

        declaration.mark_paid(self.checker)
        self.assertEqual(declaration.status, DeclarationStatus.PAID)

    def test_transitions_are_not_skippable(self):
        declaration = self._declaration(self.maker)
        with self.assertRaises(ValidationError):
            declaration.receive("RC-1", self.checker)  # draft -> received
        with self.assertRaises(ValidationError):
            declaration.mark_paid(self.checker)  # draft -> paid

    def test_filed_declaration_cannot_be_filed_again(self):
        declaration = self._declaration(self.maker)
        declaration.file(self.checker)
        with self.assertRaises(ValidationError):
            declaration.file(self.checker)
