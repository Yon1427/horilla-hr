"""Biometric lifecycle hooks.

Loi 18-07 art. 18 (as amended by loi 25-11) requires biometric templates to be
removed when the purpose ends. Leaving the employee's device mapping and a live
consent behind after an exit is a retention breach, so deactivating an employee
purges the enrolment and withdraws the consent in the same transaction.

Uses ``_base_manager`` on purpose: the company-aware manager filters by the
request's selected company, and an offboarding triggered from another company
context would otherwise silently leave the rows in place.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

logger = logging.getLogger(__name__)


@receiver(post_save, sender="employee.Employee")
def purge_biometric_on_exit(sender, instance, **kwargs):
    """Delete device enrolments and withdraw consent when the employee leaves."""
    if getattr(instance, "is_active", True):
        return

    from biometric.models import BiometricConsent, BiometricEmployees

    deleted, _detail = BiometricEmployees._base_manager.filter(
        employee_id=instance
    ).delete()
    consent = BiometricConsent._base_manager.filter(employee_id=instance).first()
    if consent and not consent.withdrawn_on:
        consent.withdrawn_on = timezone.localdate()
        consent.save(update_fields=["withdrawn_on"])
    if deleted or consent:
        logger.info(
            "biometric purge on exit: employee=%s enrolments_deleted=%s",
            instance.pk,
            deleted,
        )
