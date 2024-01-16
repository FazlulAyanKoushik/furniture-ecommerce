import uuid


# Slug Generators
def get_organization_slug(instance):
    name = instance.display_name if instance.display_name else instance.name
    return f"{name}-{instance.country}"


# Media File Prefixes
def get_organization_media_path_prefix(instance, filename):
    return f"organizations/{instance.slug}/{filename}"


def get_organization_file_path_prefix(instance, filename):
    prefix = str(uuid.uuid4()).split("-")[:1]
    return f"organizations/{instance.slug}/{prefix}-{filename}"


def get_organization_customer_service_path_prefix(instance):
    return f"organizations/{instance.slug}"


def get_customer_service_slug(instance):
    return f"{instance.name}"
