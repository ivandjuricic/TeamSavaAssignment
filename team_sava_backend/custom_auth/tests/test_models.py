from unittest.mock import patch
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from custom_auth.tests.factories import AuthUserFactory, EmailTokenFactory


class TestAuthUse(TestCase):

    def setUp(self):
        self.user = AuthUserFactory()

    def test_user_factory(self):
        """
        smoke test if the factory and tests have been setup
        """
        self.assertIsInstance(self.user, get_user_model())

    @patch('custom_auth.models.send_password_reset_email.delay')
    def send_password_reset_email(self, sending_task):
        # patch the task to preserve unit test boundaries
        sending_task.return_value = None
        self.user.send_password_reset_email()
        sending_task.assert_called_once()


class TestEmailToken(TestCase):

    def setUp(self):
        self.token = EmailTokenFactory()

    def test_build_token_url(self):
        self.assertEqual(
            self.token.build_token_url(),
            "{}/reset-password/{}".format(settings.DOMAIN, self.token.id)
        )
