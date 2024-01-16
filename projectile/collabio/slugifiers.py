# Slug Generators
def get_project_slug(instance):
    uid_partial = str(instance.uid).split("-")[0]
    return f"{instance.title}-{instance.country}-{uid_partial}"


def get_organization_slug(instance):
    return f"{instance.organization.slug}"
