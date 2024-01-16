def get_customer_service_slug(instance):
    return f"{instance.name}"


def get_faq_media_path_prefix(instance, filename):
    return f"faqs/{instance.slug}/{filename}"


def get_faq_slug(instance):
    return f"{instance.category}-{instance.title}"


def get_organization_media_path_prefix(instance, filename):
    return f"organizations/{instance.slug}/{filename}"
