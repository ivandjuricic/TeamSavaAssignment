from unittest import TestCase
from unittest.mock import patch
from services.email import send_email


class TestEmailServices(TestCase):

    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_send_email(self, email_msg_send_method):
        send_email("MSG SUBJECT", "MSGCONTENT", to=[
                   "test_email@email.com"], html_content="<h1>oifanoi</h1>")
        email_msg_send_method.assert_called_once()
