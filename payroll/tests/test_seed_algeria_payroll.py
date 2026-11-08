from django.core.management import call_command
from django.test import TestCase

from payroll.models.models import Allowance, Deduction, FilingStatus


class SeedTest(TestCase):
    def test_seed_is_idempotent(self):
        call_command("seed_algeria_payroll")
        call_command("seed_algeria_payroll")
        self.assertEqual(
            FilingStatus.objects.filter(filing_status="Algérie IRG 2026").count(), 1
        )
        self.assertEqual(
            Deduction.objects.filter(title="CNAS Salariale 9%").count(), 1
        )

    def test_cnas_component_has_employee_and_employer_rates(self):
        call_command("seed_algeria_payroll")
        cnas = Deduction.objects.get(title="CNAS Salariale 9%")
        self.assertEqual(cnas.rate, 9)
        self.assertEqual(cnas.employer_rate, 25.5)
        self.assertTrue(cnas.is_pretax)
        self.assertFalse(cnas.is_tax)
