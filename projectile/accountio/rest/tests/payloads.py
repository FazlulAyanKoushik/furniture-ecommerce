from django.contrib.auth import get_user_model

from accountio.choices import (
    OrganizationStatus,
    OrganizationUserRole,
    OrganizationUserStatus,
)

from fileroomio.choices import (
    FileExtension,
    FileKind,
    FileStatus,
    FileVisibility,
)

from catalogio.choices import ProductStatus

from collabio.choices import (
    ProjectStatus,
    ProjectVisibility,
)

from mediaroomio.choices import MediaImageKind

from newsdeskio.choices import (
    NewsdeskPostKind,
    NewsdeskPostStatus,
)


def user(email=None):
    if email == None:
        email = "user@example.com"
    return get_user_model().objects.create_user(email, "pass1232word")


def create_organization():
    """Creates and returns an organization"""
    payload = {
        "name": "Pran RFL",
        "display_name": "PRAN",
        "status": OrganizationStatus.ACTIVE,
        "registration_no": "24434",
        "country": "se",
        "kind": "UNKNOWN",
    }
    return payload


def create_product(organization):
    """Creates and returns a product"""
    payload = {
        "title": "iphone",
        "status": ProductStatus.PUBLISHED,
        "organization": organization,
    }
    return payload


def create_organization_user(organization_id, user):
    """Create organization user payload (staff)"""
    payload = {
        "organization": organization_id,
        "user": user.id,
        "role": OrganizationUserRole.STAFF,
        "status": OrganizationUserStatus.ACTIVE,
    }
    return payload


def create_organization_partner_payload():
    payload = {
        "name": "Acme Corp",
        "display_name": "Acme",
        "status": OrganizationStatus.ACTIVE,
        "registration_no": "9876542",
        "country": "se",
        "kind": "UNKNOWN",
    }
    return payload


def organization_onboard_payload():
    payload = {
        "email": "musk@example.com",
        "password": "pass123word",
        "phone": "0168766000",
        "first_name": "Elon",
        "last_name": "Musk",
        "organization_name": "Tesla",
        "organization_no": "12151",
        "country": "BD",
    }
    return payload


def organization_onboard_payload_two():
    payload = {
        "email": "bertal@example.com",
        "password": "Pass321word",
        "phone": "0177766110",
        "first_name": "Art",
        "last_name": "Tin",
        "organization_name": "Height",
        "organization_no": "57903",
        "country": "UK",
    }
    return payload


def user_payload(user):
    payload = {
        "email": user.email,
        "first_name": "New",
        "last_name": "User",
        "role": OrganizationUserRole.STAFF,
        "status": OrganizationStatus.ACTIVE,
        "password": "Password1234",
    }
    return payload


def organization_staff_payload(user):
    """Create organization user payload (staff)"""
    payload = {
        "user_uid": user,
        "role": OrganizationUserRole.STAFF,
        "status": OrganizationUserStatus.ACTIVE,
    }
    return payload


def organization_user_list_payload():
    payload = {
        "email": "dip@example.com",
        "first_name": "Test",
        "last_name": "Create",
        "role": OrganizationUserRole.STAFF,
        "status": OrganizationUserStatus.ACTIVE,
    }
    return payload


def news_payload():
    """Payload for creating news"""
    payload = {
        "title": "Black Friday",
        "kind": NewsdeskPostKind.EVENT,
        "status": NewsdeskPostStatus.PUBLISHED,
    }
    return payload


def product_image_payload():
    payload = {
        "width": 20,
        "height": 20,
        "caption": "Tesla Model-3",
        "copyright": "Tesla",
        "priority": 1,
    }
    return payload


def product_payload():
    payload = {
        "title": "Tesla Model-3",
        "status": ProductStatus.PUBLISHED,
    }
    return payload


def project_payload():
    return {
        "title": "Office Furniture",
        "status": ProjectStatus.ACTIVE,
        "visibility": ProjectVisibility.PUBLIC,
    }


def file_item_payload(image_file):
    return {
        "fileitem": image_file,
        "kind": FileKind.IMAGE,
        "extension": FileExtension.IMAGE,
        "visibility": FileVisibility.PUBLIC,
        "status": FileStatus.PUBLISHED,
    }


def organization_invitation_paylaod():
    return {"message": "Test Message"}


def organization_showroom_list_payload(image):
    return {
        "image": image,
        "title": "Test Title",
        "caption": "BMW",
        "copyright": "Bmw",
        "priority": 1,
    }
