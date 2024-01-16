import logging

logger = logging.getLogger(__name__)


def get_brand_slug(instance):
    return f"{instance.organization.slug}-{instance.title}"


def get_collection_slug(instance):
    return f"{instance.organization.slug}-{instance.title}"


def get_product_slug(instance):
    return f"{instance.organization.slug}-{instance.title}"


def get_material_slug(instance):
    return f"{instance.organization.slug}-{instance.name}"

def get_service_slug(instance):
    return f"{instance.title}"