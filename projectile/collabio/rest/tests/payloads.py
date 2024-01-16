from django.contrib.auth import get_user_model

from accountio.choices import OrganizationStatus, OrganizationUserRole
from collabio.choices import ProjectStatus, ProjectVisibility


def user(email=None):
    if email == None:
        email = "user@example.com"
    return get_user_model().objects.create_user(email, "pass1232word")


def organization_onboard_payload():
    return {
        "email": "musk@example.com",
        "password": "pass123word",
        "phone": "0168766000",
        "first_name": "Elon",
        "last_name": "Musk",
        "organization_name": "Tesla",
        "organization_no": "12151",
        "country": "BD",
    }


def user_payload(user):
    return {
        "user_uid": user,
        "role": OrganizationUserRole.STAFF,
        "status": OrganizationStatus.ACTIVE,
    }


def project_payload():
    return {
        "title": "Office Furniture",
        "status": ProjectStatus.ACTIVE,
        "visibility": ProjectVisibility.GLOBAL,
    }
