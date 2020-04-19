from django.template.loader import render_to_string
from celery import shared_task

from services.email import send_email


@shared_task()
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


ail(
    subject,
    content,
    to,
    from_email="no-reply@ivandjuricic.com",
    html_content=html_content
)
