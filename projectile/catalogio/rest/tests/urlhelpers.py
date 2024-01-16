from django.urls import reverse

PRODUCT_URL = reverse("products.product-list")


def product_list_url():
    return reverse("products.product-list")


def product_detail_url(product_slug):
    """Create and return product detail url"""
    return reverse("products.product-detail", args=[product_slug])


def productimage_list_url(organization_slug, slug):
    return reverse("products.productimage-list", args=[organization_slug, slug])


def productimage_detail_url(organization_slug, product_slug, uid):
    """Create and return product detail url"""
    return reverse(
        "products.productimage-detail",
        args=[
            organization_slug,
            product_slug,
            uid,
        ],
    )


"""product collection url"""


def product_collection_list_url():
    return reverse("products.collection-list")


def product_collection_detail_url(slug):
    return reverse("products.collection-detail", args=[slug])


def collection_product_list_url(slug):
    return reverse("products.collection-product-list", args=[slug])


def organization_onboarding_url():
    return reverse("organizations.onboarding-detail")


def me_organization_list_url():
    return reverse("me-organization-list")


def we_user_list_url():
    return reverse("we.user-list")


def product_image_list_url(slug):
    return reverse("products.product_image-list", args=[slug])


def product_image_detail_url(product_slug, uid):
    return reverse("products.product_image-detail", args=[product_slug, uid])


def global_brands_list_url():
    return reverse("brands.brand-list")
