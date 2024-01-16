from common.email import send_email

from weapi.rest.tests import urlhelpers as we_urlhelpers

subjects = {
    "se": "Kom igång med ditt konto på Supplers",
    "en": "Get started with your account on Supplers",
}

domains = {
    "127.0.0.1:3000": "http://127.0.0.1:3000",
    "api.supplers.com": "https://www.supplers.com",
    "testapi.supplers.com": "https://staging.supplers.com",
}


def send_organization_user_invite(profile=None, domain=None, message=None):
    """Send invite email to user to join organization"""
    if profile is None:
        return
    if domain is None:
        domain = "127.0.0.1:3000"

    domain = domains.get(domain, "http://127.0.0.1:3000")
    country = profile.organization.country
    context = {
        "profile": profile,
        "link": f"{domain}/invites/{profile.token}",
        "message": message,
    }
    print("ctx:", context)
    country = country.lower() if country in subjects.keys() else "en"
    subject = subjects[country]
    template = f"email/invites/organization_user_invite_en.html"
    to_email = profile.user.email
    send_email(context, template, to_email, subject)


def send_added_user_set_password_mail(user=None, domain=None, message=None):
    """Send email to user"""
    if user is None:
        return

    domain = domains.get(domain, "http://127.0.0.1:3000")
    context = {
        "profile": user,
        "link": f"{domain}{we_urlhelpers.we_send_added_user_set_password_mail_url(user.token)}",
        "message": message,
    }
    subject = f"Set your new password of SUPPLERS account"
    template = f"email/added_user_set_password.html"
    to_email = user.user.email
    send_email(context, template, to_email, subject)


def send_organization_onboarding_email(user, domain=None):
    message = "Thank you for connecting with supplers."
    if user is None:
        return
    if domain is None:
        domain = "127.0.0.1:3000"

    domain = domains.get(domain, "http://127.0.0.1:3000")
    route = f"verify/associated-emails?token={user.token}"
    context = {
        "name": user.user.get_name(),
        "link": f"{domain}/{route}",
        "message": message,
    }
    template = f"email/organization_onboarding.html"
    email = user.user.email
    subject = message
    send_email(context, template, email, subject)
