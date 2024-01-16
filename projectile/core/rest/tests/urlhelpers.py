from django.urls import reverse


def me_detail_url():
    return reverse("me-detail")

def me_password_url():
    return reverse("me-password")

def me_status_url():
    return reverse("me-status")


def me_user_email_list_url():
    return reverse("me-email-list")


def me_user_email_list_detail(uid):
    return reverse("me-email-detail", args=[uid])


def user_detail_url(slug):
    return reverse("user-detail", args=[slug])


def me_organization_list_url():
    return reverse("me-organization-list")


def me_organization_select_url(uid):
    """Creates a url to get user organizations"""
    return reverse("me-organization-set_default", args=[uid])


def phone_list_url():
    return reverse("me-phone-list")


def phone_detail_url(uid):
    return reverse("me-phone-detail", args=[uid])
