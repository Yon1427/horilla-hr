"""Rename the automation account to the current product brand.

Schedulers and the activity feed look the bot up by ``horilla.methods
.BOT_USERNAME``, which is derived from ``SIRH_BRAND_NAME``. A database seeded
before the rebrand still holds the old name, so without this every scheduled
notification silently has no sender.
"""

from django.conf import settings
from django.db import migrations

OLD_USERNAME = "Horilla Bot"


def rename_bot(apps, schema_editor):
    User = apps.get_model("horilla_auth", "HorillaUser")
    new_username = f"{getattr(settings, 'SIRH_BRAND_NAME', 'Horilla')} Bot"
    if new_username == OLD_USERNAME:
        return
    if User.objects.filter(username=new_username).exists():
        return
    User.objects.filter(username=OLD_USERNAME).update(username=new_username)


class Migration(migrations.Migration):

    dependencies = [
        ("horilla_auth", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(rename_bot, migrations.RunPython.noop),
    ]
