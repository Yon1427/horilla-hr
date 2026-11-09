"""Statutory declarations registry (M2-1, spec 02 §7 / 05 §1.4).

One row per filing; the extract payloads arrive with each declaration type
(M2-2..M2-8). Maker-checker: the person who prepares a declaration
(``created_by``) cannot file it — a second person must.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.horilla_company_manager import HorillaCompanyManager
from base.models import Company, HorillaModel
from employee.models import Employee


class DeclarationType(models.TextChoices):
    DEA = "dea", _("Employee affiliation (DEA)")
    DAC = "dac", _("Monthly contributions (DAC)")
    DAS = "das", _("Annual contributions (DAS)")
    G50 = "g50", _("Monthly IRG (G50)")
    G29 = "g29", _("Annual IRG (G29)")
    ANEM = "anem", _("ANEM declarations")
    ATMP = "atmp", _("Work accidents (AT/MP)")
    TFPC_TAPP = "tfpc_tapp", _("TFPC/TAPP")


class DeclarationStatus(models.TextChoices):
    DRAFT = "draft", _("Draft")
    FILED = "filed", _("Filed")
    RECEIVED = "received", _("Receipt received")
    PAID = "paid", _("Paid")


class Declaration(HorillaModel):
    """A statutory filing for one company and one period."""

    declaration_type = models.CharField(
        max_length=20, choices=DeclarationType.choices
    )
    company_id = models.ForeignKey(
        Company, null=True, editable=False, on_delete=models.PROTECT
    )
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=DeclarationStatus.choices,
        default=DeclarationStatus.DRAFT,
    )
    receipt_reference = models.CharField(
        max_length=100, blank=True, verbose_name=_("Receipt reference")
    )
    filed_by = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.PROTECT,
    )
    filed_at = models.DateTimeField(null=True, blank=True)

    objects = HorillaCompanyManager()

    class Meta:
        ordering = ["-period_end", "-id"]
        verbose_name = _("Declaration")
        verbose_name_plural = _("Declarations")

    def __str__(self):
        return f"{self.get_declaration_type_display()} {self.period_start} → {self.period_end}"

    def file(self, employee) -> None:
        """draft → filed, by someone other than the preparer (05 §1.4)."""
        if self.status != DeclarationStatus.DRAFT:
            raise ValidationError(
                _("Only a draft declaration can be filed.")
            )
        if (
            employee is not None
            and employee.employee_user_id_id is not None
            and self.created_by_id == employee.employee_user_id_id
        ):
            raise ValidationError(
                _(
                    "Maker-checker: the person who prepared the declaration "
                    "cannot file it."
                )
            )
        self.status = DeclarationStatus.FILED
        self.filed_by = employee
        self.filed_at = timezone.now()
        self.save()

    def receive(self, receipt_reference, employee) -> None:
        """filed → received, with the DGI/CNAS receipt reference."""
        if self.status != DeclarationStatus.FILED:
            raise ValidationError(
                _("Only a filed declaration can receive a receipt.")
            )
        self.status = DeclarationStatus.RECEIVED
        self.receipt_reference = receipt_reference
        self.save()

    def mark_paid(self, employee) -> None:
        """received → paid."""
        if self.status != DeclarationStatus.RECEIVED:
            raise ValidationError(
                _("Only a declaration with a receipt can be marked paid.")
            )
        self.status = DeclarationStatus.PAID
        self.save()
