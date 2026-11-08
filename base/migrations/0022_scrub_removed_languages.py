"""Scrub removed UI languages from per-company language settings.

Keeps only en/fr/ar (settings.LANGUAGES after the fr-ar-en trim). Rows that
end up empty mean "all settings languages", per CompanyLanguageSetting docs.
"""

from django.db import migrations

REMOVED = {
    "de",
    "es",
    "it",
    "pt-br",
    "zh-hans",
    "zh-hant",
    "tr",
    "uk",
    "ro",
    "ru",
    "id",
}


def scrub_removed_languages(apps, schema_editor):
    CompanyLanguageSetting = apps.get_model("base", "CompanyLanguageSetting")
    for row in CompanyLanguageSetting.objects.all():
        codes = row.enabled_languages or []
        kept = [
            c for c in codes if c.lower().replace("_", "-") not in REMOVED
        ]
        if kept != codes:
            row.enabled_languages = kept
            row.save(update_fields=["enabled_languages"])


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0021_penaltyaccounts_additional_info_and_more"),
    ]

    operations = [
        migrations.RunPython(scrub_removed_languages, migrations.RunPython.noop),
    ]
