from django.conf import settings
from django.test import SimpleTestCase

from horilla.branding import BOT_USERNAME


class BotUsernameTests(SimpleTestCase):
    def test_bot_username_follows_the_brand(self):
        """Schedulers and the feed look the account up by this name."""
        self.assertEqual(BOT_USERNAME, f"{settings.SIRH_BRAND_NAME} Bot")

    def test_bot_username_is_not_the_upstream_name(self):
        self.assertNotEqual(BOT_USERNAME, "Horilla Bot")
