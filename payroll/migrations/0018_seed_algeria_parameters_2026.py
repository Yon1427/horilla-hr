from datetime import date

from django.db import migrations

BRACKETS = [
    {"min": 0, "max": 20000, "rate": 0},
    {"min": 20000, "max": 40000, "rate": 23},
    {"min": 40000, "max": 80000, "rate": 27},
    {"min": 80000, "max": 160000, "rate": 30},
    {"min": 160000, "max": 320000, "rate": 33},
    {"min": 320000, "max": None, "rate": 35},
]


def seed(apps, schema_editor):
    Parameter = apps.get_model("payroll", "AlgeriaPayrollParameter")
    Parameter.objects.get_or_create(
        company_id=None,
        effective_from=date(2026, 1, 1),
        defaults={
            "snmg_monthly": 24000,
            "irg_brackets": BRACKETS,
            "source_url": "https://www.joradp.dz/",
        },
    )


def unseed(apps, schema_editor):
    Parameter = apps.get_model("payroll", "AlgeriaPayrollParameter")
    Parameter.objects.filter(
        company_id=None, effective_from=date(2026, 1, 1)
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0017_algeria_payroll_parameter"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
