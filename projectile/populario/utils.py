# Generate Slug


def get_popular_organization_slug(instance):
    name = (
        instance.organization.display_name
        if instance.organization.display_name
        else instance.organization.name
    )
    return f"{name}-{instance.organization.kind}"


def get_popular_product_slug(instance):
    name = (
        instance.product.title
        if instance.product.title
        else instance.product.display_title
    )
    return f"{name}-{instance.organization.name}"


def get_popular_project_slug(instance):
    name = instance.project.title if instance.project.title else instance.project.slug
    return f"{name}-{instance.organization.name}"
