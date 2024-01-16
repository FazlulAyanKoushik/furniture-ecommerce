import logging

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse

from common.tokens import encode_jwt_for_user
from common.tasks import send_email_async

from django_rest_passwordreset.signals import reset_password_token_created

logger = logging.getLogger(__name__)


def send_activation_mail(user):
    if not user.is_active:
        token = encode_jwt_for_user(user).decode("utf-8")
        site_url = (
            "http://localhost:3000" if settings.DEBUG else "https://www.supplers.com"
        )
        context = {"user": user, "link": f"{site_url}/activate?token={token}"}
        subject = "Supplers - Welcome onboard and activate Your account!"
        send_email_async.delay(context, "email/activation.html", user.email, subject)


def send_generic_invite_mail(user_proxy):
    user = user_proxy.user
    referrer = user_proxy.referrer
    token = user_proxy.token
    class_name = user_proxy.__class__.__name__
    if class_name in ["OrganizationMember", "OrganizationUser"]:
        site_url = "http://localhost:3000"
        if not settings.DEBUG:
            site_url = "https://www.supplers.com"

        urls = {
            "OrganizationMember": {
                "active": "login?next=/me/membership",
                "freshy": f"invites/organization-members/?token={token}",
            },
            "OrganizationUser": {
                "active": "login?next=/me/organizations",
                "freshy": f"invites/organization-users/?token={token}",
            },
        }
        dict_ = urls[class_name]
        if user.is_active:
            cta_phrase = "Review your invite on Supplers!"
            route = dict_["active"]
        else:
            cta_phrase = "Click here to activate Your account!"
            route = dict_["freshy"]
        context = {
            "user_proxy": user_proxy,
            "user": user,
            "cta_phrase": cta_phrase,
            "link": f"{site_url}/{route}",
        }
        subject = "Supplers - You have been invited!"
        reply_to = None
        if referrer is not None:
            subject = f"{referrer.user.get_name()} invited You to join Supplers!"
            reply_to = [
                f"{referrer.user.get_name()} <{referrer.user.email}>",
            ]
        send_email_async.delay(
            context, "email/invites/generic.html", user.email, subject, reply_to
        )


def send_associated_email_verification_mail(instance):
    site_url = "http://localhost:3000" if settings.DEBUG else "https://www.supplers.com"
    if not instance.is_status_active():
        cta_phrase = "Click on this link to verify Your email address!"
        route = f"verify/associated-emails?token={instance.token}"
        context = {
            "instance": instance,
            "user": instance.user,
            "cta_phrase": cta_phrase,
            "link": f"{site_url}/{route}",
        }
        send_email_async.delay(
            context,
            "email/verify_associated_email.html",
            instance.email,
            "Please verify Your associated email address!",
        )


def send_activation_mail_to_user(user, token):
    if not user.is_active:
        site_url = (
            "http://localhost:3000" if settings.DEBUG else "https://www.supplers.com"
        )
        context = {"user": user, "link": f"{site_url}/activate?token={token}"}
        subject = "Supplers - You have been invited and activate Your account!"
        send_email_async.delay(context, "email/activation.html", user.email, subject)


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    site_url = "http://localhost:3000" if settings.DEBUG else "https://www.supplers.com"
    context = "{}{}?token={}".format(
        site_url,
        "/password/reset-password",
        reset_password_token.key,
    )
    send_mail(
        # title:
        "Password reset request from Supplers",
        # message:
        context,
        # from:
        "info@supplers.se",
        # to:
        [reset_password_token.user.email],
    )


def send_user_activation_mail(user):
    if not user.is_active:
        token = encode_jwt_for_user(user)
        site_url = (
            "http://localhost:3000" if settings.DEBUG else "https://www.supplers.com"
        )
        context = {"user": user, "link": f"{site_url}/activate?token={token}"}
        subject = "Supplers - Activate Your account!"
        send_email_async.delay(context, "email/activation.html", user.email, subject)


def send_group_member_invitation_mail(user):
    context = {
        "user": user,
    }
    subject = "Supplers - You have been invited!"
    send_email_async.delay(
        context, "email/invites/group_members_invite_en.html", user.email, subject
    )
