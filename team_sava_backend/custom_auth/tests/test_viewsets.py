import uuid
import datetime
from unittest.mock import patch

from django.conf import settings
from django.test import Client, TestCase
from django.utils import timezone
from custom_auth.models import AuthUser, EmailToken
from custom_auth.tests.factories import AuthUserFactory, EmailTokenFactory
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(TestCase):
    """
    These tests that are outside of boundaries of unittesting, but can capture
    some of the generic errors we set the framework to do for us.
    """

    def setUp(self):
        self.c = Client()

    def test_get_user_success(self):
        user = AuthUserFactory()
        refresh_token = RefreshToken.for_user(user)
        response = self.c.get(
            "/api/v1/auth-user/{}/".format(user.id),
            HTTP_AUTHORIZATION="Bearer {}".format(str(refresh_token.access_token))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_user_fail_no_token(self):
        user = AuthUserFactory()
        response = self.c.get(
            "/api/v1/auth-user/{}/".format(user.id)
        )
        self.assertEqual(response.status_code, 403)

    def test_get_user_fail_wrong_token(self):
        user = AuthUserFactory()
        response = self.c.get(
            "/api/v1/auth-user/{}/".format(user.id),
            HTTP_AUTHORIZATION="Bearer aofnaopidfndi")
        self.assertEqual(response.status_code, 401)

    def test_get_user_fail_wrong_token_type(self):
        user = AuthUserFactory()
        refresh_token = RefreshToken.for_user(user)
        response = self.c.get(
            "/api/v1/auth-user/{}/".format(user.id),
            HTTP_AUTHORIZATION="Basic {}".format(str(refresh_token.access_token))
        )
        self.assertEqual(response.status_code, 403)

    def test_get_user_fail_different_profile(self):
        user1 = AuthUserFactory()
        user2 = AuthUserFactory()
        refresh_token = RefreshToken.for_user(user1)
        response = self.c.get(
            "/api/v1/auth-user/{}/".format(user2.id),
            HTTP_AUTHORIZATION="Bearer {}".format(str(refresh_token.access_token))
        )
        self.assertEqual(response.status_code, 403)

    def test_create_user_success(self):
        data = {
            "email": "test_email@testemail.com",
            "password": "TestPassword1",
            "password2": "TestPassword1",
            "first_name": "TestFirstName",
            "last_name": "TestLastName"
        }
        response = self.c.post("/api/v1/auth-user/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            1,
            AuthUser.objects.filter(
                email="test_email@testemail.com",
                first_name="TestFirstName",
                last_name="TestLastName"
            ).count()
        )

    def test_create_user_fail_missmatch(self):
        """
        Same test could be written for all validation errors,
        adding one for custom serialzizer validation
        """
        data = {
            "email": "test_email@testemail.com",
            "password": "TestPassword1",
            "password2": "MissmatchedPassword",
            "first_name": "TestFirstName",
            "last_name": "TestLastName"
        }
        response = self.c.post("/api/v1/auth-user/", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            0,
            AuthUser.objects.filter(
                email="test_email@testemail.com",
                first_name="TestFirstName",
                last_name="TestLastName"
            ).count()
        )


class TestPasswordResetTokenViewSet(TestCase):

    def setUp(self):
        self.c = Client()

    def test_create_token_succes(self):
        user = AuthUserFactory(
            email="djuricicivan@gmail.com"
        )
        # patch no to send email
        with patch("custom_auth.models.send_password_reset_email.delay") as sender:
            sender.return_value = None
            response = self.c.post(
                "/api/v1/reset-token/",
                data={"email": "djuricicivan@gmail.com"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                EmailToken.objects.count(),
                1
            )

    def test_create_token_with_inccorrect_account(self):
        # patch no to send email
        with patch("custom_auth.models.send_password_reset_email.delay") as sender:
            sender.return_value = None
            response = self.c.post(
                "/api/v1/reset-token/",
                data={"email": "fakeemail@testemail.com"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                EmailToken.objects.count(),
                0
            )

    def test_get_token_success(self):
        token = EmailTokenFactory()
        response = self.c.get(
            "/api/v1/reset-token/{}/".format(str(token.id))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_token_fail(self):
        fake_uuid = uuid.uuid4()
        response = self.c.get(
            "/api/v1/reset-token/{}/".format(fake_uuid)
        )
        self.assertEqual(response.status_code, 404)

    def test_get_fail_token_expired(self):
        expired_date = timezone.now() - datetime.timedelta(days=settings.TOKEN_VALID_DAYS + 1)
        token = EmailTokenFactory()

        token.created_at = expired_date
        token.save()

        response = self.c.get(
            "/api/v1/reset-token/{}/".format(str(token.id))
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            EmailToken.objects.filter(active=False).count(),
            1
        )

    def test_token_get_fail_not_active(self):
        token = EmailTokenFactory(active=False)
        response = self.c.get(
            "/api/v1/reset-token/{}/".format(str(token.id))
        )
        self.assertEqual(response.status_code, 404)
