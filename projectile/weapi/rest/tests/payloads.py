import tempfile

from django.contrib.auth import get_user_model

from accountio.choices import (
    OrganizationStatus,
    OrganizationUserRole,
    OrganizationUserStatus,
)

from catalogio.choices import (
    ProductCollectionKind,
    ProductCollectionVisibility,
    ProductDiscountKind,
    ProductDiscountStatus,
    ProductDiscountVariant,
    ProductStatus,
    ServiceStatus,
)

from common.choices import Currency

from collabio.choices import ProjectStatus, ProjectVisibility, ProjectParticipantStatus

from contentio.choices import CustomerServiceStatus

from docx import Document

from openpyxl import Workbook

from fileroomio.choices import FileExtension, FileKind, FileStatus, FileVisibility

from gruppio.choices import GroupStatus, MemberRole, MemberStatus

from mediaroomio.choices import MediaImageConnectorKind, MediaImageKind

from newsdeskio.choices import NewsdeskPostKind, NewsdeskPostStatus

from PIL import Image

from tagio.choices import TagCategory, TagStatus


def user(email=None):
    if email == None:
        email = "user@example.com"
    return get_user_model().objects.create_user(email, "pass1232word")


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


def create_organization():
    """Create and return an organization"""
    payload = {
        "name": "Acme Corp",
        "display_name": "Acme",
        "status": OrganizationStatus.ACTIVE,
        "registration_no": "24434",
        "country": "se",
        "kind": "UNKNOWN",
    }
    return payload


def create_organization_two():
    """Create and return an organization"""
    payload = {
        "name": "Cyberdyne Systems",
        "display_name": "Cyberdyne",
        "status": OrganizationStatus.ACTIVE,
        "registration_no": "244434",
        "country": "se",
        "kind": "UNKNOWN",
    }
    return payload


def create_organization_user(organization_id, user):
    """Create and return an organization user"""
    payload = {
        "organization": organization_id,
        "user": user.id,
        "role": OrganizationUserRole.STAFF,
        "status": OrganizationUserStatus.ACTIVE,
    }
    return payload


def product_payload():
    payload = {
        "title": "Tesla Model-3",
        "status": ProductStatus.PUBLISHED,
    }
    return payload


def product_payload_with_brand(brand_uid):
    payload = {
        "title": "Tesla Model-3",
        "status": ProductStatus.PUBLISHED,
        "brand_uid": brand_uid,
    }
    return payload


def product_payload_with_brand(brand):
    payload = {
        "title": "Tesla Model-3",
        "status": ProductStatus.PUBLISHED,
        "brand": brand,
    }
    return payload


def user_payload(user):
    payload = {
        "email": user.email,
        "password": "pass12346word",
        "first_name": "New",
        "last_name": "User",
        "role": OrganizationUserRole.STAFF,
        "status": OrganizationStatus.ACTIVE,
        "password": "new1234password",
    }
    return payload


def collection_payload():
    payload = {
        "title": "Office Equipments",
        "kind": ProductCollectionKind.COLLECTION,
        "visibility": ProductCollectionVisibility.PUBLIC,
    }
    return payload


def partners_payload():
    payload = {
        "name": "partner organization",
        "display_name": "codeiopart",
        "status": OrganizationStatus.ACTIVE,
        "registration_no": "244ds434",
        "country": "ae",
        "kind": "UNKNOWN",
        "email": "abdcdd@gmail.com",
    }
    return payload


# Second payload with same data as partners_payload
def partners_payload_two():
    payload = {
        "name": "partner organization",
        "display_name": "codeiopart",
        "status": OrganizationStatus.ACTIVE,
        "registration_no": "244ds434",
        "country": "ae",
        "kind": "UNKNOWN",
        "email": "abdcde@gmail.com",
    }
    return payload


def product_brand_payload():
    """Create and returns a productBrand"""

    return {
        "title": "PoorMan",
    }


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


def project_payload():
    """payloads for creating project"""
    return {
        "title": "Office Furniture",
        "status": ProjectStatus.ACTIVE,
        "visibility": ProjectVisibility.PUBLIC,
    }


def project_participants_payload(user_uid):
    return {
        "user_uid": user_uid,
        "role": "Polisher",
        "status": ProjectParticipantStatus.ACCEPTED,
    }


def group_payload():
    return {
        "name": "Tech Giants",
        "description": "Groups tech giants organization",
        "status": GroupStatus.ACTIVE,
    }


def group_payload_one():
    return {
        "name": "Tech Giants",
        "description": "Groups tech giants organization",
        "status": GroupStatus.ACTIVE,
        "first_name": "Elon",
        "last_name": "Musk",
        "email": "musk@example.com",
        "password": "pass123word",
    }


def group_payload_two():
    return {
        "name": "Microsoft",
        "description": "Microsoft tech giants organization",
        "status": GroupStatus.ACTIVE,
        "first_name": "Bill",
        "last_name": "Gates",
        "email": "gates@example.com",
        "password": "pass123word",
    }


def member_payload(user):
    payload = {
        "user": user,
        "role": MemberRole.ADMIN,
        "status": MemberStatus.USER_ACCEPTED,
    }
    return payload


def media_image_payload(image):
    return {
        "image": image,        
        "caption": "BMW",
        "copyright": "Bmw",
        "priority": 1,
        "kind": MediaImageKind.IMAGE
    }


def file_item_payload(file):
    return {
        "fileitem": file,
        "name": "test drive",
        "kind": FileKind.IMAGE,
        "extension": FileExtension.IMAGE,
        "visibility": FileVisibility.PUBLIC,
        "status": FileStatus.PUBLISHED,
    }


def products_image_payload(image):
    return {
        "image": image,
        "kind": MediaImageConnectorKind.PRODUCT,
    }


def project_image_payload(image):
    return {
        "image": image,
        "kind": MediaImageConnectorKind.PROJECT,
    }


def news_post_image_payload(image):
    return {
        "image": image,
        "kind": MediaImageConnectorKind.NEWS_POST,
    }


def group_image_payload(image):
    return {
        "image": image,
        "kind": MediaImageConnectorKind.GROUP,
    }


def admin_user_payload(user):
    payload = {
        "user_uid": user.uid,
        "role": OrganizationUserRole.ADMIN,
        "status": OrganizationStatus.ACTIVE,
    }
    return payload


def new_user_payload():
    return {
        "first_name": "Elon",
        "last_name": "Mask",
        "email": "elon@tesla.com",
        "role": "ADMIN",
    }


def staff_role_payload():
    data = {
        "first_name": "Elon",
        "last_name": "Musk",
        "email": "elon@tesla.com",
        "role": "STAFF",
    }
    return data


def product_image_payload(image_file):
    return {
        "image": image_file,
        "width": 10,
        "height": 10,
        "caption": "BMW",
        "copyright": "Bmw",
        "priority": 1,
    }


def create_organization_user_payload():
    payload = {
        "email": "mus@example.com",
        "first_name": "Lon",
        "last_name": "Musk",
        "role": OrganizationUserRole.INITIATOR,
        "status": OrganizationUserStatus.INVITED,
    }
    return payload


def tag_payload():
    return {
        "category": TagCategory.WOOD,
        "name": "Schinopsis Balansae",
        "status": TagStatus.ACTIVE,
    }


def product_payload_with_tags(tags):
    return {
        "title": "Tesla Model-3",
        "status": ProductStatus.PUBLISHED,
        "tag_uids": tags,
    }


def organization_onboard_with_tags_payload(tags):
    payload = {
        "email": "musk@example.com",
        "password": "pass123word",
        "phone": "0168766000",
        "first_name": "Elon",
        "last_name": "Musk",
        "organization_name": "Tesla",
        "organization_no": "12151",
        "country": "BD",
        "status": "ACTIVE",
        "tag_uids": tags,
    }
    return payload


def add_organization_user_payload():
    return {
        "email": "han.solo@example.com",
        "first_name": "Han",
        "last_name": "Solo",
        "role": "STAFF",
        "status": "INVITED",
    }


def generate_test_image():
    """Generate a temporary image"""

    # Create a temporary image file
    image = Image.new("RGB", (10, 10))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    image.save(tmp_file)
    tmp_file.close()
    return tmp_file.name


def generate_test_doc_file():
    """Generate a temporary DOCX file with sample data"""

    # Create a new document
    doc = Document()

    # Add a paragraph to the document
    doc.add_paragraph("Hello, World!")

    # Save the document to a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=".docx", delete=False)
    doc.save(temp_file.name)

    return temp_file


def service_payload():
    return {
        "name": "Test Service",
        "description": "Test Service Description",
        "status": ServiceStatus.ACTIVE,
    }


def service_payload_two():
    return {
        "name": "Test Service2",
        "description": "Test Service Description",
        "status": ServiceStatus.ACTIVE,
    }


def customer_service_payload():
    return {
        "name": "Test Customer Service",
        "description": "This is a test customer service",
        "status": CustomerServiceStatus.ACTIVE,
    }


def generate_test_xlsx_file():
    """Generate a temporary XLSX file with sample data"""

    wb = Workbook()
    ws = wb.active

    # Write column headers
    ws.append(
        [
            "name",
            "display_name",
            "country",
            "organization_email",
            "registration_no",
            "organization_status",
            "username",
            "user_email",
            "first_name",
            "last_name",
            "status",
            "password",
        ]
    )

    # Write sample data
    ws.append(
        [
            "Mossaddak",
            "Mossaddak Corp",
            "bd",
            "mossaddak@example.com",
            "12345",
            "ACTIVE",
            "abdul_kalam",
            "mossaddak_sium@example.com",
            "Mossaddak",
            "Sium",
            "ACTIVE",
            "pass123word",
        ]
    )
    ws.append(
        [
            "Belal Ahmed",
            "Belal Corp",
            "eg",
            "belal@example.com",
            "67890",
            "ACTIVE",
            "belal_ahmed",
            "belal@example.com",
            "Belal",
            "Ahmed",
            "DRAFT",
            "pass123word",
        ]
    )
    ws.append(
        [
            "Dipu Kanu",
            "Dipu Corp",
            "uk",
            "dipu@example.com",
            "101112",
            "ACTIVE",
            "dipu_kanu",
            "dipu@example.com",
            "Dipu",
            "Kanu",
            "ACTIVE",
            "pass123word",
        ]
    )

    # Save the workbook to a temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    wb.save(temp_file.name)
    return temp_file


def create_product_discount_payload():
    return {
        "category": "Happy New Year",
        "kind": ProductDiscountKind.DISCOUNT,
        "percent": "20.00",
        "variant": ProductDiscountVariant.AMOUNT,
        "amount": "50.00",
        "currency": Currency.USD,
        "status": ProductDiscountStatus.ACTIVE,
        "start_date": "2023-07-19",
        "stop_date": "2023-08-19",
    }
