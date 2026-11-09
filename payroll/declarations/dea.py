"""DEA extract (M2-2): the employee-affiliation declaration.

Loi 83-14 art. 10: request affiliation within 10 days of recruitment
(DEC-02, OFF). Field contract from the sirh-legal M2 report (2026-11-09):
NIN and NSS are nullable on a first affiliation; `dea_nin_required` stays
a parameter until the CNAS schema is confirmed.
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def _d(value):
    """Boundary conversion: floats from the pipeline become exact Decimals."""
    return Decimal(str(value)) if value is not None else None


def dea_due_date(hire_date, params) -> date:
    """D+10 calendar days after hire (hire day = D0).

    shortcut: the weekend/holiday shift rule is UNV (C-closed only by the
    CNAS agency) — return the literal D+10 until it is confirmed.
    """
    return hire_date + timedelta(days=int(params.dea_due_days))


def dea_is_overdue(hire_date, today, params) -> bool:
    """True once the day after the due date begins (D+11 is overdue)."""
    return today > dea_due_date(hire_date, params)


def build_dea(
    employee,
    contract,
    employer_cnas_no,
    employer_nif="",
    nss="",
    nin="",
    params=None,
    contract_type="CDI",
) -> dict:
    """The extract dict for one hire; validates the legal minimums.

    `params` may be None for a dry preview, in which case `due_date` is
    omitted and the NIN gate is not applied.
    """
    if not employer_cnas_no:
        raise ValidationError(_("The employer CNAS number is required."))
    if contract is None or not contract.contract_start_date:
        raise ValidationError(_("The hire date is required."))
    if not (employee.employee_first_name or employee.employee_last_name):
        raise ValidationError(_("The employee name is required."))
    if params is not None and params.dea_nin_required and not nin:
        raise ValidationError(
            _("The NIN is required by the dea_nin_required parameter.")
        )

    hire_date = contract.contract_start_date
    return {
        "employer_cnas_no": employer_cnas_no,
        "employer_nif": employer_nif,
        "nom": employee.employee_last_name,
        "prenom": employee.employee_first_name,
        "date_naissance": employee.dob,
        "situation_familiale": employee.marital_status,
        "nb_enfants": employee.children,
        "hire_date": hire_date,
        "due_date": dea_due_date(hire_date, params) if params is not None else None,
        "contract_type": contract_type,
        "salaire_embauche_brut": _d(contract.wage),
        "cnas_base_initiale": _d(contract.wage),
        "nss": nss or None,
        "nin": nin or None,
    }
