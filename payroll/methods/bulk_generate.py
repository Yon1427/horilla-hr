"""Bulk payslip generation, extracted from the view so it can be tested."""

from __future__ import annotations

import datetime

from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_noop
from notifications.signals import notify

from payroll.methods.errors import PayrollBlockedError
from payroll.methods.methods import payslip_fields, save_payslip
from payroll.methods.payroll_run import payroll_calculation
from payroll.methods.tax_calc import TaxComputationError
from payroll.models.models import Contract


def employee_period_start(requested_start: datetime.date, contract) -> datetime.date:
    """The start date this employee is actually paid from."""
    if contract and requested_start < contract.contract_start_date:
        return contract.contract_start_date
    return requested_start


@transaction.atomic
def generate_bulk_payslips(
    *, request, employees, start_date, end_date, group_name, summary_by_employee
) -> list:
    """Generate payslips for a batch, all-or-nothing. Returns the saved rows."""
    saved = []
    for employee in employees:
        contract = Contract.objects.filter(
            employee_id=employee, contract_status="active"
        ).first()
        employee_start = employee_period_start(start_date, contract)
        if end_date < employee_start:
            messages.error(request, _(f"{employee}'s contract has not started yet."))
            continue
        try:
            payslip = payroll_calculation(
                employee,
                employee_start,
                end_date,
                month_summary=summary_by_employee.get(employee.pk, {}),
            )
        except (TaxComputationError, PayrollBlockedError) as exc:
            messages.error(request, str(exc))
            continue
        instance = save_payslip(
            **payslip_fields(payslip, employee, status="draft", group_name=group_name)
        )
        saved.append(instance)
        transaction.on_commit(
            lambda employee=employee, instance=instance: _notify(
                request, employee, instance
            )
        )
    return saved


def _notify(request, employee, instance):
    notify.send(
        request.user.employee_get,
        recipient=employee.employee_user_id,
        verb=gettext_noop("Payslip has been generated for you."),
        redirect=reverse(
            "view-created-payslip", kwargs={"payslip_id": instance.id}
        ),
        icon="close",
    )
