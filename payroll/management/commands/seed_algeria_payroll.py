from django.core.management.base import BaseCommand

from payroll.models.models import Allowance, Deduction, FilingStatus


class Command(BaseCommand):
    help = "Create the Algerian payroll components (idempotent)."

    def handle(self, *args, **options):
        filing, _ = FilingStatus.objects.get_or_create(
            filing_status="Algérie IRG 2026",
            defaults=dict(
                based_on="taxable_gross_pay",
                use_py=False,
                tax_engine="dz_irg",
            ),
        )
        Deduction.objects.get_or_create(
            title="CNAS Salariale 9%",
            defaults=dict(
                is_fixed=False,
                based_on="gross_pay",
                rate=9,
                employer_rate=25.5,
                is_pretax=True,
                is_tax=False,
                include_active_employees=True,
            ),
        )
        Allowance.objects.get_or_create(
            title="Prime de transport",
            defaults=dict(is_fixed=True, amount=0, is_taxable=False),
        )
        Allowance.objects.get_or_create(
            title="Panier",
            defaults=dict(is_fixed=True, amount=0, is_taxable=False),
        )
        self.stdout.write(self.style.SUCCESS("Algeria payroll components ready."))
