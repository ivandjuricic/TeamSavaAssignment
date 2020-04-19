from django.core.mail import EmailMultiAlternatives


def send_email(subject, content, to, from_email=None, content_subtype="html", *args, **kwargs):
    """
    Utility function for sending emails
    """
    msg = EmailMultiAlternatives(subject, content, from_email, to)
    msg.attach_alternative(kwargs['html_content'], "text/html")
    return msg.send()
