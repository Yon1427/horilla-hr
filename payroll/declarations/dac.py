"""DAC extract (M2-3): Déclaration d'Assiette des Cotisations.

Periodic contributions return: per-employee gross, CNAS assiette and the
three cotisations (9 % employee, 25 % employer, 0,5 % FNPOS — OFF, décret
94-187 as rewritten by 15-236). The totals carry NOTHING but s×A: leave
provision, TFPC/TAPP and IRG are not cotisations (01 §7.1 reconciliation
rule from the sirh-legal M2 report). All money is Decimal; lines are
quantized once at 0.01 HALF_UP and the header totals are the exact sum of
the quantized lines, so the centime always reconciles.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

TWOPLACES = Decimal("0.01")


def _d(value) -> Decimal:
    """Boundary conversion: floats from the pipeline become exact Decimals."""
    return Decimal(str(value))


def _q(value) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def build_dac_line(matricule, nom, prenom, gross, assiette, nss, *, params) -> dict:
    gross_dec = _d(gross)
    assiette_dec = _d(assiette)
    cot_sal = assiette_dec * _d(params.cnas_employee_rate) / Decimal(100)
    cot_pat = assiette_dec * _d(params.cnas_employer_rate) / Decimal(100)
    fnpos = assiette_dec * _d(params.fnpos_rate) / Decimal(100)
    return {
        "matricule": matricule,
        "nom": nom,
        "prenom": prenom,
        "nss": nss,
        "gross_G": _q(gross_dec),
        "assiette_A": _q(assiette_dec),
        "cot_sal": _q(cot_sal),
        "cot_pat": _q(cot_pat),
        "fnpos": _q(fnpos),
        "total_line": _q(cot_sal + cot_pat + fnpos),
    }


def build_dac(lines, employer_cnas_no, period, params) -> dict:
    """The DAC recap for one period; `lines` are (matricule, nom, prenom,
    gross, assiette, nss) tuples straight from the payroll run."""
    if not employer_cnas_no:
        raise ValidationError(_("The employer CNAS number is required."))
    if not lines:
        raise ValidationError(_("A DAC must carry at least one employee line."))

    built = [
        build_dac_line(*line, params=params) for line in lines
    ]
    totals = {
        "gross_total": sum((line["gross_G"] for line in built), Decimal("0")),
        "assiette_total": sum((line["assiette_A"] for line in built), Decimal("0")),
        "cot_sal_total": sum((line["cot_sal"] for line in built), Decimal("0")),
        "cot_pat_total": sum((line["cot_pat"] for line in built), Decimal("0")),
        "fnpos_total": sum((line["fnpos"] for line in built), Decimal("0")),
    }
    totals["total_a_payer"] = (
        totals["cot_sal_total"] + totals["cot_pat_total"] + totals["fnpos_total"]
    )
    return {
        "employer_cnas_no": employer_cnas_no,
        "period": period,
        "lines": built,
        "totals": totals,
    }
