"""AT/MP extract (M2-7): work accident declaration to CNAS.

The 48 h clock (DEC-10) runs from `knowledge_datetime` — when the
employer learned of the accident — never before the accident itself
(`knowledge >= accident` is enforced). Calendar-hours vs working-hours
interpretation stays UNV; the conservative calendar clock is applied.
Diagnosis never enters HR-visible fields: the extract carries only the
medical certificate reference, its date and the work-stoppage flag.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def atmp_due(knowledge_datetime: datetime, params) -> datetime:
    """knowledge + 48 h (DEC-10; calendar hours, conservative)."""
    return knowledge_datetime + timedelta(hours=params.atmp_due_hours)


def atmp_status(knowledge_datetime: datetime, filed_datetime: datetime, params) -> dict:
    """ON_TIME / LATE with the exact margin, for the declaration state."""
    due = atmp_due(knowledge_datetime, params)
    if filed_datetime <= due:
        return {
            "status": "ON_TIME",
            "margin_minutes": int((due - filed_datetime).total_seconds() // 60),
        }
    return {
        "status": "LATE",
        "lateness_minutes": int(
            (filed_datetime - due).total_seconds() // 60
        ),
    }


def build_atmp(employer, victim, accident, params, *, injury=None, medical=None) -> dict:
    """The minimal CNAS declaration payload (ATMP-02)."""
    if not employer.get("cnas_no"):
        raise ValidationError(_("AT/MP: the employer CNAS number is required."))
    for field in ("nss", "job"):
        if not victim.get(field):
            raise ValidationError(_("AT/MP: the victim %(field)s is required.") % {"field": field})
    for field in ("accident_datetime", "knowledge_datetime", "place"):
        if accident.get(field) is None:
            raise ValidationError(_("AT/MP: the accident %(field)s is required.") % {"field": field})
    if accident["knowledge_datetime"] < accident["accident_datetime"]:
        raise ValidationError(
            _("AT/MP: the employer cannot know the accident before it happened.")
        )
    if injury and injury.get("diagnosis"):
        raise ValidationError(
            _("AT/MP: diagnoses belong to the medical store, never HR fields.")
        )

    status = atmp_status(
        accident["knowledge_datetime"],
        # A not-yet-filed declaration shows its due clock only.
        accident.get("filed_datetime") or accident["knowledge_datetime"],
        params,
    )
    return {
        "employer": employer,
        "victim": victim,
        "accident": accident,
        "injury": injury or {},
        "medical": medical or {},
        "due_datetime": atmp_due(accident["knowledge_datetime"], params),
        "status": status,
    }
