import datetime

from django.conf import settings
from django.test import TestCase, Client
from django.utils import timezone

from custom_auth.models import AuthUser
from custom_auth.tests.factories import EmailTokenFactory


class TestPasswordResetView(TestCase):

    def setUp(self):
        self.c = Client()

    def test_success(self):
        token = EmailTokenFactory()
        data = {
            "token": str(token.id),
            'password1': "BrandNewPassword",
            "password2": "BrandNewPassword"
        }
        response = self.c.post(
            "/api/v1/reset-password/",
            data=data
        )
        self.assertEqual(response.status_code, 204)
        token.user.refresh_from_db()
        self.assertTrue(
            token.user.check_password(
                "BrandNewPassword"
            )
        )

    def test_fail_password_missmatch(self):
        token = EmailTokenFactory()
        data = {
            "token": str(token.id),
            'password1': "BrandNewPassword",
            "password2": "MissmatchPassword"
        }
        response = self.c.post(
            "/api/v1/reset-password/",
            data=data
        )
        self.assertEqual(response.status_code, 400)
        token.user.refresh_from_db()
        self.assertFalse(
            token.user.check_password(
                "BrandNewPassword"
            )
        )

    def test_fail_token_expired(self):
        token = EmailTokenFactory()
        token.created_at = timezone.now() - datetime.timedelta(days=settings.TOKEN_VALID_DAYS + 1)
        token.save()
        data = {
            "token": str(token.id),
            'password1': "BrandNewPassword",
            "password2": "BrandNewPassword"
        }
        response = self.c.post(
            "/api/v1/reset-password/",
            data=data
        )
        self.assertEqual(response.status_code, 404)
        token.user.refresh_from_db()
        self.assertFalse(
            token.user.check_password(
                "BrandNewPassword"
            )
        )
