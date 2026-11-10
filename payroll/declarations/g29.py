"""G29 extract (M2-6): annual per-beneficiary IRG return.

CIDTA art. 75-2/75-3: one row per beneficiary paid in the year, with
identity (NIN mandatory since LF 2026 art. 8), job, address, family
situation, and the money columns — gross, IRG base, IRG withheld, net —
all SUMS of monthly payroll values, never recomputed through an
annualised barème (monthly withholding is definitive; G29 is
informational). Rows with zero IRG carry the « néant » mention (PAY-21).
Filed by 30 April N+1.

Money is Decimal; each monthly pair is validated for internal consistency
(gross − CNAS = taxable, gross − CNAS − IRG = net, ±0.01 DA) and the
annual row is the exact sum of the quantized months.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

TWOPLACES = Decimal("0.01")
TOLERANCE = TWOPLACES


def _d(value) -> Decimal:
    """Boundary conversion: floats from the pipeline become exact Decimals."""
    return Decimal(str(value))


def _q(value) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def build_g29_row(
    nin,
    nom,
    prenom,
    monthly,
    params,
    *,
    emploi="",
    adresse="",
    situation_famille=None,
    nb_charges=0,
) -> dict:
    """One G29 row from 12 monthly {gross, cnas_sal, taxable, irg, net}
    dicts in calendar order, as recorded by the validated payroll runs."""
    if params.g29_nin_mandatory and not nin:
        raise ValidationError(
            _("The NIN is mandatory on the G29 (LF 2026 art. 8).")
        )
    if len(monthly) != 12:
        raise ValidationError(
            _("A G29 row needs exactly 12 monthly records.")
        )

    annual = {key: Decimal("0") for key in (
        "gross", "cnas_sal", "taxable", "irg", "net")}
    for month in monthly:
        gross = _d(month["gross"])
        cnas_sal = _d(month["cnas_sal"])
        taxable = _d(month["taxable"])
        irg = _d(month["irg"])
        net = _d(month["net"])
        if abs(gross - cnas_sal - taxable) > TOLERANCE:
            raise ValidationError(
                _("Inconsistent month: gross − CNAS ≠ taxable.")
            )
        if abs(gross - cnas_sal - irg - net) > TOLERANCE:
            raise ValidationError(
                _("Inconsistent month: gross − CNAS − IRG ≠ net.")
            )
        annual["gross"] += gross
        annual["cnas_sal"] += cnas_sal
        annual["taxable"] += taxable
        annual["irg"] += irg
        annual["net"] += net

    return {
        "nin": nin or None,
        "nom": nom,
        "prenom": prenom,
        "emploi": emploi,
        "adresse": adresse,
        "situation_famille": situation_famille,
        "nb_charges": nb_charges,
        "gross_annuel": _q(annual["gross"]),
        "cnas_salariale_annuelle": _q(annual["cnas_sal"]),
        "base_irg_annuelle": _q(annual["taxable"]),
        "irg_annuel": _q(annual["irg"]),
        "net_annuel": _q(annual["net"]),
        "neant_mention": annual["irg"] == 0,
    }


def build_g29(rows, employer_nif, employer_cnas_no, fiscal_year, params) -> dict:
    """The annual return: rows as returned by build_g29_row."""
    if not employer_nif:
        raise ValidationError(_("The employer NIF is required."))
    if not rows:
        raise ValidationError(_("A G29 must carry at least one beneficiary row."))

    totals = {
        "gross_total": sum((row["gross_annuel"] for row in rows), Decimal("0")),
        "irg_total": sum((row["irg_annuel"] for row in rows), Decimal("0")),
        "net_total": sum((row["net_annuel"] for row in rows), Decimal("0")),
    }
    return {
        "employer_nif": employer_nif,
        "employer_cnas_no": employer_cnas_no,
        "fiscal_year": fiscal_year,
        "rows": rows,
        "totals": totals,
    }


def g29_due_date(fiscal_year: int, params) -> date:
    """30 April of the year following the fiscal year (DEC-06 OFF)."""
    return date(fiscal_year + 1, 4, params.g29_due_day)
