"""Algerian IRG on salaries (CIDTA art. 104, LF 2022, unchanged to 2026)."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal("0.01")


def _progressive(taxable: float, brackets) -> float:
    tax = 0.0
    for band in brackets:
        low = float(band["min"])
        high = band["max"]
        if taxable <= low:
            break
        top = taxable if high is None else min(float(high), taxable)
        tax += (top - low) * float(band["rate"]) / 100
    return tax


def compute_monthly_irg(
    monthly_taxable: float,
    params,
    *,
    disabled: bool = False,
    pensioner: bool = False,
) -> float:
    """Monthly IRG in dinars, rounded to 2 dp. Order matters (see 01 §3.3)."""
    taxable = max(float(monthly_taxable or 0), 0.0)
    if taxable <= float(params.irg_exemption_monthly):
        return 0.0

    tax = _progressive(taxable, params.irg_brackets)
    abatement = min(
        max(tax * float(params.abatement_rate) / 100, float(params.abatement_min)),
        float(params.abatement_max),
    )
    irg = max(tax - abatement, 0.0)

    if disabled or pensioner:
        if float(params.smoothing_min) < taxable < float(params.disabled_smoothing_max):
            irg = max(
                irg * float(params.disabled_smoothing_factor)
                - float(params.disabled_smoothing_offset),
                0.0,
            )
    elif float(params.smoothing_min) < taxable < float(params.smoothing_max):
        irg = max(
            irg * float(params.smoothing_factor)
            - float(params.smoothing_offset),
            0.0,
        )

    return float(Decimal(str(irg)).quantize(TWOPLACES, rounding=ROUND_HALF_UP))


def compute_yearly_irg(yearly_taxable: float, params, **kwargs) -> float:
    """Horilla computes yearly; DZ IRG is monthly. Convert, do not annualise rates."""
    return compute_monthly_irg(float(yearly_taxable) / 12, params, **kwargs) * 12
