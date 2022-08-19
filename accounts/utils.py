from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import User, Doctor, Patient


def send_email(subject: str, content: str, users: any):
    """
    Send email to a list of users.

    :param subject: The subject of the email.
    :param content: The content of the email.
    :param users: A User, Doctor, Patient, or list of Users.
    """
    if isinstance(users, User) or isinstance(users, Doctor) or isinstance(users, Patient):
        users = [users.email,]
    elif isinstance(users, list):
        users = [user.email for user in users]
    msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, users)
    msg.attach_alternative(content, "text/html")
    msg.content_subtype = "html"
    msg.send(fail_silently=False)
