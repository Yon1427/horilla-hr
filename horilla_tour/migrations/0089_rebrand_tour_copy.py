"""Rewrite upstream product name out of the seeded tour copy.

The tour seeds (0002-0087) are data migrations written before the rebrand, so
their prose still says "Horilla". Editing those historic migrations would only
help fresh installs, so the rewrite runs once over whatever is in the database
-- which covers both a fresh install and an existing one.
"""

import re

from django.conf import settings
from django.db import migrations

FIELDS = ("title", "description")


def _rewrite(text, brand):
    if not text:
        return text
    # "Horilla HRMS" and bare "Horilla" both become the brand; the longer form
    # first so the shorter one cannot leave "Sanad HRMS" behind.
    return re.sub(r"Horilla\s+HRMS", brand, text).replace("Horilla", brand)


def rebrand_tours(apps, schema_editor):
    brand = getattr(settings, "SIRH_BRAND_NAME", "Horilla")
    if brand == "Horilla":
        return
    for model_name in ("Tour", "TourStep"):
        model = apps.get_model("horilla_tour", model_name)
        updates = []
        for row in model.objects.all().only("id", *FIELDS):
            changed = {}
            for field in FIELDS:
                value = getattr(row, field)
                new = _rewrite(value, brand)
                if new != value:
                    changed[field] = new
            if changed:
                updates.append(model(pk=row.pk, **changed))
        if updates:
            model.objects.bulk_update(updates, [f for f in FIELDS], batch_size=200)


class Migration(migrations.Migration):

    dependencies = [
        ("horilla_tour", "0088_alter_tour_is_active_alter_tourprogress_is_active_and_more"),
    ]

    operations = [
        migrations.RunPython(rebrand_tours, migrations.RunPython.noop),
    ]
