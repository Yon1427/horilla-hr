"""Employer costisation (01 §7).

Monthly employer cost = G + s×A + t×G + G/12 + r

    G = gross remuneration; A = CNAS base (subset of G, defaults to G);
    s = employer CNAS + FNPOS (25 % + 0,5 % outside BTPH);
    t = TFPC + TAPP (0–2 %; the full 2 % applies with no training spend);
    G/12 = paid-leave provision (the "8,33 %" in the spec is 1/12 rounded);
    r = company-specific provisions (dismissal, notice, CCN) — default 0.

IRG is not an employer cost; it is withheld from the employee. BTPH
(38,085 % incl. CACOBATPH, no leave provision) is M5 and not implemented
here. All money is Decimal; the total is quantized once, 0.01 DA,
ROUND_HALF_UP, then the derived figures (hourly, annual) follow.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal("0.01")
PAID_HOURS_MONTHLY = Decimal("173.33")


def _d(value) -> Decimal:
    """Boundary conversion: floats from the pipeline become exact Decimals."""
    return Decimal(str(value))


def compute_employer_cost(
    params,
    gross,
    cnas_base=None,
    *,
    extra_provisions=0,
) -> dict:
    """Employer cost for one month under the given effective-dated parameters.

    Returns a breakdown dict with every line quantized to 2 dp. The lines
    are summed unrounded in Decimal and the total is quantized once.
    """
    gross_dec = _d(gross)
    cnas_base_dec = gross_dec if cnas_base is None else _d(cnas_base)

    s_rate = _d(params.cnas_employer_rate) + _d(params.fnpos_rate)
    t_rate = _d(params.tfpc_rate) + _d(params.tapp_rate)

    cnas_employer = (cnas_base_dec * _d(params.cnas_employer_rate)) / Decimal(100)
    fnpos = (cnas_base_dec * _d(params.fnpos_rate)) / Decimal(100)
    tfpc = (gross_dec * _d(params.tfpc_rate)) / Decimal(100)
    tapp = (gross_dec * _d(params.tapp_rate)) / Decimal(100)
    leave_provision = gross_dec / Decimal(12)
    extra = _d(extra_provisions)

    total = (
        gross_dec + cnas_employer + fnpos + tfpc + tapp + leave_provision + extra
    )
    total = total.quantize(TWOPLACES, rounding=ROUND_HALF_UP)

    q = lambda value: value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    return {
        "gross": q(gross_dec),
        "cnas_employer": q(cnas_employer),
        "fnpos": q(fnpos),
        "tfpc": q(tfpc),
        "tapp": q(tapp),
        "leave_provision": q(leave_provision),
        "extra_provisions": q(extra),
        "total_monthly": total,
        "cost_per_paid_hour": (total / PAID_HOURS_MONTHLY).quantize(
            TWOPLACES, rounding=ROUND_HALF_UP
        ),
        "annual": (total * 12).quantize(TWOPLACES, rounding=ROUND_HALF_UP),
        # Marginal factor of a gross raise (01 §7.4): 1 + s + t + 1/12.
        "raise_factor": Decimal(1) + s_rate / Decimal(100) + t_rate / Decimal(100)
        + Decimal(1) / Decimal(12),
    }
