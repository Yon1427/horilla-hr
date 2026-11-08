"""Product branding values that code (not templates) needs.

Kept apart from ``horilla.methods`` on purpose: that module imports the user
model, and ``base/scheduler.py`` imports this constant at module scope, so a
model import here would pull the user model into ``apps.populate()`` phase 1
and make ``INSTALLED_APPS`` ordering load-bearing.
"""

from django.conf import settings

# Name of the automation account schedulers and the activity feed attribute
# work to. Derived from the brand so a rename is one setting, and so a lookup
# cannot drift from the account ``createhorillauser`` creates.
BOT_USERNAME = f"{getattr(settings, 'SIRH_BRAND_NAME', 'Horilla')} Bot"


def get_bot_user():
    """The automation account, or None when it has not been created yet."""
    from horilla_auth.models import HorillaUser

    return HorillaUser.objects.filter(username=BOT_USERNAME).first()
