from django.template.loader import render_to_string
from celery import shared_task
from smtplib import SMTPServerDisconnected

from services.email import send_email


@shared_task(autoretry_for=(SMTPServerDisconnected,), retry_kwargs={'max_retries': 5, 'countdown': 10})
def send_password_reset_email(token_url, email, name):
    template_name = "password_reset_email.html"
    to = [email]
    context = {
        'url': token_url,
        'name': name
    }
    subject = "Password reset"
    content = "Reset password here"
    html_content = render_to_string(template_name, context=context)
    print(html_content)

    send_email(
        subject,
        content,
        to,
        from_email="no-reply@ivandjuricic.com",
        html_content=html_content
    )
