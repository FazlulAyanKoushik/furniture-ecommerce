def get_ad_organization_slug(instance):
    return f"{instance.organization.name}"


def get_ad_product_slug(instance):
    return f"{instance.product.title}-{instance.organization.name}"


def get_ad_project_slug(instance):
    return f"{instance.project.title}-{instance.organization.name}"
