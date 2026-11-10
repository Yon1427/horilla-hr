"""ANEM extracts (M2-7): employment declarations (décret 09-94 arts. 2-7).

Two extracts: the monthly recruitment declaration (due month_end + 10
days, content per arts. 5-6: branch, socio-professional category, age,
posts, contract type, gender for recruitments) and the quarterly
manpower forecast (due one month before the quarter). Modifications of
transmitted information must be notified immediately with reasons
(art. 4) — the SIRH re-files a corrected extract rather than patching.

The socio-professional category mapping is never inferred: a hire without
it blocks the extract (ANEM-03). Gender is only ever taken from explicit
master data, never guessed.
"""

from __future__ import annotations

from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def anem_recruit_due_date(period_end: date, params) -> date:
    """Month end + 10 days (DEC-08, OFF)."""
    return period_end + timedelta(days=params.anem_recruit_due_days)


def anem_forecast_due_date(quarter_start: date) -> date:
    """One month before the quarter (DEC-09, OFF)."""
    month = quarter_start.month - 1
    year = quarter_start.year
    if month == 0:
        month, year = 12, year - 1
    return date(year, month, 1)


def _validate_hire(hire) -> None:
    if not hire.get("contract_type"):
        raise ValidationError(
            _("ANEM: the contract type is required for every hire.")
        )
    if hire.get("gender") is None:
        raise ValidationError(
            _("ANEM: the gender is required for every recruitment.")
        )
    if not hire.get("socio_prof_category"):
        raise ValidationError(
            _("ANEM: the socio-professional category must be mapped, not inferred.")
        )


def build_anem_recruitment(
    employer_nif, period, period_end, hires, params
) -> dict:
    """The monthly recruitment declaration."""
    if not employer_nif:
        raise ValidationError(_("The employer NIF is required."))
    if not hires:
        raise ValidationError(_("A recruitment declaration needs hires."))
    for hire in hires:
        _validate_hire(hire)
    return {
        "employer_nif": employer_nif,
        "period": period,
        "due_date": anem_recruit_due_date(period_end, params),
        "hires": hires,
    }


def build_anem_forecast(employer_nif, quarter_start, posts, params) -> dict:
    """The quarterly manpower forecast; posts carry no gender (future hires)."""
    if not employer_nif:
        raise ValidationError(_("The employer NIF is required."))
    if not posts:
        raise ValidationError(_("A forecast needs at least one post."))
    for post in posts:
        if not post.get("contract_type"):
            raise ValidationError(
                _("ANEM: the contract type is required for every forecast post.")
            )
        if not post.get("socio_prof_category"):
            raise ValidationError(
                _("ANEM: the socio-professional category must be mapped, not inferred.")
            )
    return {
        "employer_nif": employer_nif,
        "quarter_start": quarter_start,
        "due_date": anem_forecast_due_date(quarter_start),
        "posts": posts,
    }
