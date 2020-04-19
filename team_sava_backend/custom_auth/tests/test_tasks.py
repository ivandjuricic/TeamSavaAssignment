from unittest.mock import patch
from django.test import TestCase
from custom_auth.tasks import send_password_reset_email


class TestAuthUse(TestCase):

    @patch('custom_auth.tasks.render_to_string')
    @patch('custom_auth.tasks.send_email')
    def test_send_password_reset_email(self, send_method, render_method):
        data = {
            "token_url": "/random_test_url",
            "email": "test_email@test_email.com",
            "name": "TestName"
        }
        send_password_reset_email(**data)
        render_method.assert_called_with(
            "password_reset_email.html",
            context={
                'url': data['token_url'],
                'name': data['name']
            }
        )
        send_method.assert_called_once()
