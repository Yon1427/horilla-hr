"""DAS extract (M2-4): Déclaration Annuelle des Salaires et des salariés.

Annual per-employee, per-quarter nominative CNAS return (loi 83-14 art. 14;
contract from the sirh-legal M2 report). The NSS is the row key — a row
whose NSS is missing is emitted with a blocking completeness flag, never
silently dropped (an omitted line makes a hole in the career record).
BTPH is a different return, different year (1 Jul-30 Jun, CACOBATPH): the
extractor selects GENERAL only; BTPH rows are a separate M5 contract.

Money is Decimal end to end: each quarter is quantized once at 0.01
HALF_UP and the annual totals are the exact sum of the quantized
quarters, so DAS reconciles with 12 × DAC to the centime.
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

TWOPLACES = Decimal("0.01")

REGIME_GENERAL = "GENERAL"


def _d(value) -> Decimal:
    """Boundary conversion: floats from the pipeline become exact Decimals."""
    return Decimal(str(value))


def _q(value) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def build_das_row(
    nss,
    nom,
    prenom,
    monthly,
    params,
    *,
    hire_date=None,
    exit_date=None,
    birth_date=None,
    contract_type="CDI",
    nin=None,
) -> dict:
    """One DAS row from 12 monthly {gross, base} pairs in calendar order.

    `monthly` entries may also carry `time_worked` (unit per
    `params.das_time_unit`, UNV: DAYS|HOURS). Gross figures exclude
    non-cotisable elements by contract (the DAC reconciliation covers them).
    """
    if len(monthly) != 12:
        raise ValidationError(
            _("A DAS row needs exactly 12 monthly pairs, one per calendar month.")
        )

    row = {
        "nss": nss or None,
        "nom": nom,
        "prenom": prenom,
        "birth_date": birth_date,
        "hire_date": hire_date,
        "exit_date": exit_date,
        "contract_type": contract_type,
        "nin": nin,
        # F-04: a row without an NSS must be visible and flagged, never dropped.
        "blocking_completeness": not nss,
    }
    annual = {"gross": Decimal("0"), "base": Decimal("0")}
    for quarter_index in range(4):
        months = monthly[quarter_index * 3 : quarter_index * 3 + 3]
        gross = sum((_d(m["gross"]) for m in months), Decimal("0"))
        base = sum((_d(m["base"]) for m in months), Decimal("0"))
        employee = base * _d(params.cnas_employee_rate) / Decimal(100)
        employer = base * _d(params.cnas_employer_rate) / Decimal(100)
        fnpos = base * _d(params.fnpos_rate) / Decimal(100)
        time_worked = sum(
            (_d(m.get("time_worked", 0)) for m in months), Decimal("0")
        )
        q = f"q{quarter_index + 1}"
        row[f"gross_{q}"] = _q(gross)
        row[f"base_{q}"] = _q(base)
        row[f"contrib_employee_{q}"] = _q(employee)
        row[f"contrib_employer_{q}"] = _q(employer)
        row[f"fnpos_{q}"] = _q(fnpos)
        row[f"time_worked_{q}"] = time_worked
        annual["gross"] += _q(gross)
        annual["base"] += _q(base)

    row["annual_gross"] = annual["gross"]
    row["annual_base"] = annual["base"]
    row["annual_employee"] = sum(
        (row[f"contrib_employee_q{i}"] for i in range(1, 5)), Decimal("0")
    )
    row["annual_employer"] = sum(
        (row[f"contrib_employer_q{i}"] for i in range(1, 5)), Decimal("0")
    )
    row["annual_fnpos"] = sum(
        (row[f"fnpos_q{i}"] for i in range(1, 5)), Decimal("0")
    )
    row["annual_due"] = (
        row["annual_employee"] + row["annual_employer"] + row["annual_fnpos"]
    )
    return row


def build_das(rows, employer_cnas_no, employer_nif, declaration_year, params) -> dict:
    """The annual extract: rows as returned by build_das_row."""
    if not employer_cnas_no:
        raise ValidationError(_("The employer CNAS number is required."))
    if not rows:
        raise ValidationError(_("A DAS must carry at least one employee row."))

    totals = {
        "annual_gross_total": sum(
            (row["annual_gross"] for row in rows), Decimal("0")
        ),
        "annual_base_total": sum(
            (row["annual_base"] for row in rows), Decimal("0")
        ),
        "annual_due_total": sum(
            (row["annual_due"] for row in rows), Decimal("0")
        ),
    }
    return {
        "employer_cnas_no": employer_cnas_no,
        "employer_nif": employer_nif,
        "declaration_year": declaration_year,
        "regime": REGIME_GENERAL,
        "rows": rows,
        "totals": totals,
    }


def das_due_date(declaration_year, params) -> date:
    """+30 days after 31 Dec (DEC-04, C11 open: weekend shift is UNV).

    shortcut: the literal +30 days is returned; the 30-vs-31-Jan wording
    and any weekend/holiday shift stay parameters until CNAS confirms.
    """
    return date(declaration_year + 1, 1, 1) + timedelta(days=params.das_due_days - 1)
