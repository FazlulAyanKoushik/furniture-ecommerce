from django.urls import reverse


def organization_group_list_url(organization_slug):
    """Create and return list url for organization group with slug"""
    return reverse("organizations.organization_groups-list", args=[organization_slug])


def organization_group_detail_url(organization_slug, slug):
    """Create and return detail url for organization group with slug"""
    return reverse(
        "organizations.organization_group-detail", args=[organization_slug, slug]
    )


# organization user url
def organization_user_list_url(user_slug):
    """Create and return a organization user url"""
    return reverse("organizations.organization_users-list", args=[user_slug])


def organizaion_user_detail_url(organization_slug, slug):
    return reverse(
        "organizations.organization_user-detail", args=[organization_slug, slug]
    )


def organization_url():
    return reverse("organizations.organizations-list")


def org_product_url(organization_slug):
    return reverse("organizations.products-list", args=[organization_slug])


def org_product_detail_url(organization_slug, slug):
    return reverse("organizations.product-detail", args=[organization_slug, slug])


def organization_product_image_list(organization_slug, product_slug):
    return reverse(
        "organizations.product_image-list", args=[organization_slug, product_slug]
    )


def set_default_organization_url(organization_uid):
    return reverse("me-organization-set_default", args=[organization_uid])


def organization_onboarding_url():
    return reverse("organizations.onboarding-detail")


def organization_news_url(organization_slug):
    return reverse("organizations.news-list", args=[organization_slug])


def organization_news_detail_url(organization_slug, post_slug):
    """generates and return url for detail news view"""
    return reverse("organizations.news-detail", args=[organization_slug, post_slug])


def we_user_list_url():
    return reverse("we.user-list")


def organization_user_url(slug):
    return reverse("organizations.organization_users-list", args=[slug])


def set_default_organization_url(organization_uid):
    return reverse("me-organization-set_default", args=[organization_uid])


def me_organization_list_url():
    return reverse("me-organization-list")


def organization_product_image_list_url(organization_slug, product_slug):
    return reverse(
        "organizations.product_images-list", args=[organization_slug, product_slug]
    )


def organization_product_image_detail_url(organization_slug, product_slug, uid):
    return reverse(
        "organizations.product_images-detail",
        args=[organization_slug, product_slug, uid],
    )


def we_product_image_list_url(slug):
    return reverse("we.product_image-list", args=[slug])


def we_detail_url():
    return reverse("we.we-detail")


def we_list_url():
    return reverse("we.user-list")


def we_product_list_url():
    return reverse("we.product-list")


def project_list_url():
    return reverse("we.projects-list")


def public_organization_project_list_url(organization_slug):
    return reverse("organizations.projects-list", args=[organization_slug])


def public_organization_project_retrieve_url(organization_slug, project_slug):
    return reverse(
        "organizations.project-detail", args=[organization_slug, project_slug]
    )

def public_organizations_by_project_url():
    """return a list of organization by projects"""
    return reverse("organizations.organization-by-project")


def organization_list_url():
    """Create and return list organization url"""
    return reverse("organizations.organizations-list")


def organization_detail_url(organization_slug):
    """Create and return detail organization url"""
    return reverse("organizations.organization-detail", args=[organization_slug])


def file_item_list_url(organization_slug):
    return reverse("organizations.file_items-list", args=[organization_slug])


def file_item_detail_url(organization_slug, uid):
    return reverse("organizations.file_item-detail", args=[organization_slug, uid])


def organization_image_list_url(organization_slug):
    return reverse("organizations.organization_image-list", args=[organization_slug])


def organization_image_detail_url(organization_slug, uid):
    return reverse(
        "organizations.organization_image-detail", args=[organization_slug, uid]
    )


def organization_invitation_create_url(slug):
    return reverse("organizations.partner-invite", args=[slug])


def organization_showroom_list_url(slug):
    return reverse("organizations.showroom-list", args=[slug])


def organization_brand_url(slug):
    return reverse("organizations.brand-list", args=[slug])
