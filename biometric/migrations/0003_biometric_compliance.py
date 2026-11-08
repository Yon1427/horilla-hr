"""Biometric compliance: ANPDP/DPIA authorisation and per-employee consent.

Loi 18-07 art. 18 (amended by loi 25-11) makes biometric templates sensitive
data. These tables hold the legal basis the employer must be able to produce:
a company-level authorisation/DPIA row and a per-employee consent with a proof
reference. Enrolment is refused without both (see
``BiometricEmployeesManager``).

Reversible: dropping the two tables loses only compliance evidence, which is
the point of a rollback; no payroll or attendance data is touched.
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_initial"),
        ("employee", "0001_initial"),
        ("biometric", "0002_alter_biometricdevices_is_active"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BiometricProcessingAuthorisation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, blank=True, verbose_name="Created At"
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "anpdp_required",
                    models.BooleanField(
                        default=True,
                        help_text=(
                            "Untick only where counsel confirms the processing falls "
                            "outside the authorisation requirement (loi 18-07 art. 12)."
                        ),
                        verbose_name="ANPDP authorisation required",
                    ),
                ),
                (
                    "anpdp_authorisation_ref",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name="ANPDP authorisation reference",
                    ),
                ),
                ("authorisation_date", models.DateField(blank=True, null=True)),
                (
                    "dpia_completed_on",
                    models.DateField(blank=True, null=True, verbose_name="DPIA completed on"),
                ),
                (
                    "retention_months",
                    models.PositiveSmallIntegerField(
                        default=12,
                        help_text=(
                            "Templates are purged after this period unless a legal "
                            "hold applies."
                        ),
                        verbose_name="Template retention (months)",
                    ),
                ),
                (
                    "alternative_method",
                    models.CharField(
                        choices=[
                            ("manual", "Manual entry by a supervisor"),
                            ("card", "Badge / access card"),
                            ("mobile", "Mobile check-in"),
                        ],
                        default="manual",
                        help_text=(
                            "Must be offered to every employee who refuses biometrics."
                        ),
                        max_length=20,
                        verbose_name="Alternative clock-in method",
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "company_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="base.company",
                        verbose_name="Company",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Biometric processing authorisation",
                "verbose_name_plural": "Biometric processing authorisations",
            },
        ),
        migrations.CreateModel(
            name="BiometricConsent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, blank=True, verbose_name="Created At"
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                ("consent_given_on", models.DateField(blank=True, null=True)),
                (
                    "consent_reference",
                    models.CharField(
                        blank=True,
                        help_text="Signed form, ticket or document reference.",
                        max_length=255,
                        verbose_name="Consent proof reference",
                    ),
                ),
                ("withdrawn_on", models.DateField(blank=True, null=True)),
                ("expires_on", models.DateField(blank=True, null=True)),
                (
                    "company_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="base.company",
                    ),
                ),
                (
                    "employee_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="biometric_consent",
                        to="employee.employee",
                        verbose_name="Employee",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Biometric consent",
                "verbose_name_plural": "Biometric consents",
            },
        ),
    ]
