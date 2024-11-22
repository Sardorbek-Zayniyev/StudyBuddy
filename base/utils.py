from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import timedelta

from .models import User


def send_notification(email_subject, email_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(email_template, context)
    if isinstance(context["to_email"], str):
        to_email = []
        to_email.append(context["to_email"])
    else:
        to_email = context["to_email"]
    email = EmailMessage(email_subject, message, from_email, to=to_email)
    email.content_subtype = "html"

    email.send()


def send_verification_email(request, user, mail_subject, email_template):
    """
    Send a verification email to the user.
    """
    current_site = get_current_site(request)
    context = {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    }
    message = render_to_string(email_template, context)
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.content_subtype = "html"
    email.send()


def create_user_and_send_verification_email(request, form, email_template):
    """
    Create a user with the given role and send a verification email.
    """
    username = form.cleaned_data["username"].capitalize()
    email = form.cleaned_data["email"]
    password = form.cleaned_data["password"]
    user = User.objects.create_user(username=username, email=email, password=password)
    user.activation_sent_at = timezone.now()
    user.save()
    mail_subject = "Please activate your account"
    send_verification_email(request, user, mail_subject, email_template)
    return user


def activate_user(uidb64, token):

    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
    if not user:
        return None  # User does not exist

    if not default_token_generator.check_token(user, token):
        return None  # Invalid token

    time_difference = timezone.now() - user.activation_sent_at
    if time_difference >= timedelta(minutes=5):
        return None  # Activation link expired

    user.is_active = True
    user.save()
    return user
