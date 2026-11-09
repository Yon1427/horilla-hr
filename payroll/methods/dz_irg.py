"""Algerian IRG on salaries (CIDTA art. 104, LF 2022, unchanged to 2026).

Money is computed as Decimal end to end (blocking rule 2): every float that
enters from the payroll pipeline is converted with ``Decimal(str(value))``,
the barème, abattement and smoothing run in Decimal, and the result is
quantized ONCE, to 0.01 DA with ROUND_HALF_UP, before being handed back to
the (still float) pipeline as ``float``.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

TWOPLACES = Decimal("0.01")


def _d(value) -> Decimal:
    """Boundary conversion: floats from the pipeline become exact Decimals."""
    return Decimal(str(value))


def _progressive(taxable: Decimal, brackets) -> Decimal:
    tax = Decimal("0")
    for band in brackets:
        low = _d(band["min"])
        high = band["max"]
        if taxable <= low:
            break
        top = taxable if high is None else min(_d(high), taxable)
        tax += (top - low) * _d(band["rate"]) / Decimal(100)
    return tax


def compute_monthly_irg(
    monthly_taxable,
    params,
    *,
    disabled: bool = False,
    pensioner: bool = False,
) -> float:
    """Monthly IRG in dinars, quantized to 2 dp once at the end.

    Order matters (see 01 §3.3). Returns float to match the payroll pipeline.
    """
    taxable = max(_d(monthly_taxable or 0), Decimal("0"))
    if taxable <= _d(params.irg_exemption_monthly):
        return 0.0

    tax = _progressive(taxable, params.irg_brackets)
    abatement = min(
        max(tax * _d(params.abatement_rate) / Decimal(100), _d(params.abatement_min)),
        _d(params.abatement_max),
    )
    irg = max(tax - abatement, Decimal("0"))

    if disabled or pensioner:
        if _d(params.smoothing_min) < taxable < _d(params.disabled_smoothing_max):
            irg = max(
                irg * _d(params.disabled_smoothing_factor)
                - _d(params.disabled_smoothing_offset),
                Decimal("0"),
            )
    elif _d(params.smoothing_min) < taxable < _d(params.smoothing_max):
        irg = max(
            irg * _d(params.smoothing_factor) - _d(params.smoothing_offset),
            Decimal("0"),
        )

    quantized = irg.quantize(TWOPLACES, rounding=ROUND_HALF_UP)
    return float(quantized)


def compute_yearly_irg(yearly_taxable, params, **kwargs) -> float:
    """Horilla computes yearly; DZ IRG is monthly. Convert, do not annualise rates."""
    return compute_monthly_irg(_d(yearly_taxable) / Decimal(12), params, **kwargs) * 12
