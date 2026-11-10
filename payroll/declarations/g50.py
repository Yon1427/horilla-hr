"""G50 extract (M2-5): monthly IRG withholding return + payment.

Totals-only return (CIDTA arts. 73-75, 129): taxable base total and IRG
withheld total for the month, plus a separate 10 %-flat slice for
non-monthly bonuses that never merges into the barème totals. The
per-employee detail is an internal annex — G29 is the annual nominative
return. Filed 1st-20th of M+1. A month with no withholding still files
with zero totals (PAY-21 « néant »).

Money is Decimal; totals are the exact sum of the quantized lines.
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

TWOPLACES = Decimal("0.01")


def _d(value) -> Decimal:
    """Boundary conversion: floats from the pipeline become exact Decimals."""
    return Decimal(str(value))


def _q(value) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def build_g50(
    company_nif,
    fiscal_period,
    lines,
    params,
    *,
    tax_office="",
    bonus_10_base=0,
    bonus_10_irg=0,
) -> dict:
    """The monthly payroll slice of the G50.

    `lines` are (matricule, nom, prenom, taxable, irg) tuples from the
    month's CLOSED payroll runs; the return itself files only the totals.
    """
    if not company_nif:
        raise ValidationError(_("The company NIF is required."))

    detail = [
        {
            "matricule": matricule,
            "nom": nom,
            "prenom": prenom,
            "taxable": _q(_d(taxable)),
            "irg": _q(_d(irg)),
        }
        for matricule, nom, prenom, taxable, irg in lines
    ]
    base_total = sum((line["taxable"] for line in detail), Decimal("0"))
    withheld_total = sum((line["irg"] for line in detail), Decimal("0"))
    bonus_10_base_dec = _q(_d(bonus_10_base))
    bonus_10_irg_dec = _q(_d(bonus_10_irg))

    return {
        "company_nif": company_nif,
        "tax_office": tax_office,
        "fiscal_period": fiscal_period,
        "irg_salaries_taxable_base_total": base_total,
        "irg_salaries_withheld_total": withheld_total,
        "irg_10pct_base_total": bonus_10_base_dec,
        "irg_10pct_total": bonus_10_irg_dec,
        "payment_amount": withheld_total + bonus_10_irg_dec,
        "neant": withheld_total == 0 and bonus_10_irg_dec == 0,
        # Internal pre-fill annex, never filed as the G50 itself.
        "per_employee_detail": detail,
    }


def g50_window(fiscal_period: str, params) -> tuple[date, date]:
    """Filing window 1st..g50_due_day of the month following the period.

    `fiscal_period` is "YYYY-MM" (e.g. "2026-02" → 2026-03-01..2026-03-20).
    """
    year, month = (int(part) for part in fiscal_period.split("-"))
    first = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    last = first + timedelta(days=params.g50_due_day - 1)
    return first, last
