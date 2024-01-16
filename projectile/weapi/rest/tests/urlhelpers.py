from django.urls import reverse


def we_user_list_url():
    return reverse("we.user-list")


def we_product_list_url():
    return reverse("we.product-list")


def we_product_detail_url(product_slug):
    return reverse("we.product-detail", args=[product_slug])


def we_detail_url(user_uid):
    """Create and return we user detail url"""
    return reverse("we.user-detail", args=[user_uid])


def organization_onboarding_url():
    return reverse("organizations.onboarding-detail")


def organization_url():
    return reverse("organizations.organization-list")


def user_organization_product_url():
    return reverse("loggedin.user.organization-product")


def user_organization_product_detail_url(uid):
    return reverse("loggedin.user.organization.product-detail", args=[uid])


def organization_user_url(slug):
    return reverse("organizations.organizationuser-list", args=[slug])


def collection_url():
    return reverse("collection.collection-list")


def collection_detail_url(collection_uid):
    return reverse("collection.collection-detail", args=[collection_uid])


def user_organization_product_brand_url():
    return reverse("loggedin.user.organization-product-brand")


def user_organization_product_brand_detail_url(uid):
    return reverse("loggedin.user.organization.product-brand-detail", args=[uid])


def we_partners_list_url():
    return reverse("we.partners-list")


def we_partners_detail_url(uid):
    return reverse("we.partners-detail", args=[uid])


def we_partners_bulk_create_url():
    return reverse("we.partners-file")


def set_default_organization_url(organization__uid):
    return reverse("me-organization-set_default", args=[organization__uid])


def me_organization_list_url():
    return reverse("me-organization-list")


def news_list_url():
    return reverse("we.news-list")


def news_detail_url(post_uid):
    return reverse("we.news-detail", args=[post_uid])


def we_product_image_list_url(uid):
    return reverse("we.product_image-list", args=[uid])


def we_product_image_detail_url(product_uid, image_uid):
    return reverse("we.product_image-detail", args=[product_uid, image_uid])


def we_product_set_cover_image_url(product_uid, image_uid):
    return reverse("we.product_cover_image-detail", args=[product_uid, image_uid])


def project_list_url():
    return reverse("we.projects-list")


def project_detail_url(project_uid):
    return reverse("we.projects-detail", args=[project_uid])


def participants_list_url(project_uid):
    return reverse("we.participants-list", args=[project_uid])


def participants_detail_url(project__uid, participants_uid):
    return reverse("we.participants-detail", args=[project__uid, participants_uid])


def we_url():
    return reverse("we.we-detail")


def group_list_url():
    return reverse("we.group-list")


def group_detail_url(group_uid):
    return reverse("we.group-detail", args=[group_uid])


def member_list_url(group_uid):
    return reverse("we.group.member-list", args=[group_uid])


def member_detail_url(group_uid, member_uid):
    return reverse("we.group.member-detail", args=[group_uid, member_uid])


def image_list_url():
    return reverse("we.image-list")


def image_detail_url(uid):
    return reverse("we.image-detail", args=[uid])


def add_product_to_collection_url(collection_uid):
    return reverse("collection.products", args=[collection_uid])


def we_file_list_url():
    return reverse("we.files-list")


def we_file_detail_url(uid):
    return reverse("we.file-detail", args=[uid])


def we_project_image_list_url(project_uid):
    return reverse("we.project_image-list", args=[project_uid])


def we_news_post_image_list_url(newspost_uid):
    return reverse("we.news_image-list", args=[newspost_uid])


def we_news_post_image_detail_url(newspost_uid, uid):
    return reverse("we.news_image-detail", args=[newspost_uid, uid])


def we_group_image_list_url(uid):
    return reverse("we.group_image-list", args=[uid])


def we_group_image_detail_url(uid, group_uid):
    return reverse("we.group_image-detail", args=[uid, group_uid])


def we_invite_list_url():
    return reverse("we.invites-list")


def we_invite_detail_url(token):
    return reverse("we.invites-accept", args=[token])


def product_file_list_url(product_uid):
    return reverse("we.product_file-list", args=[product_uid])


def product_file_detail_url(product_uid, file_uid):
    return reverse("we.product_file-detail", args=[product_uid, file_uid])


def project_file_list_url(product_uid):
    return reverse("we.project_file-list", args=[product_uid])


def project_file_detail_url(project_uid, file_uid):
    return reverse("we.project_file-detail", args=[project_uid, file_uid])


def news_post_file_list_url(newspost_uid):
    return reverse("we.newspost_file-list", args=[newspost_uid])


def news_post_file_detail_url(newspost_uid, file_uid):
    return reverse("we.newspost_file-detail", args=[newspost_uid, file_uid])


def project_image_detail_url(project_uid, image_uid):
    return reverse("we.project_image-detail", args=[project_uid, image_uid])


def we_project_set_cover_image_url(project_uid, image_uid):
    return reverse("we.project_cover_image-detail", args=[project_uid, image_uid])


def group_file_list_url(group_uid):
    return reverse("we.group_file-list", args=[group_uid])


def group_file_detail_url(group_uid, file_uid):
    return reverse("we.group_file-detail", args=[group_uid, file_uid])


def tag_url_list():
    return reverse("we.tags-list")


def tag_url_detail(tag_uid):
    return reverse("we.tag-detail", args=[tag_uid])


def product_tag_update_url(product_uid, tag_uid):
    return reverse("we.product_tag-detail", args=[product_uid, tag_uid])


def we_services_list_url():
    return reverse("we.service-list")


def services_detail_url(uid):
    return reverse("we.service-detail", args=[uid])


def get_showroom_list_url():
    return reverse("we.showroom-list")


def partner_user_list_url(uid):
    return reverse("we.partner-user-list", args=[uid])


def get_showroom_detail_url(uid):
    return reverse("we.showroom-detail", args=[uid])


def we_set_showroom_cover_image_url(showroom_uid, image_uid):
    return reverse("we.showroom-cover-image-change", args=[showroom_uid, image_uid])


def we_showroom_image_list_url(uid):
    return reverse("we.showroom-image-list", args=[uid])


def customer_service_list_url():
    return reverse("we.customer-service-list")


def customer_service_detail_url(uid):
    return reverse("we.customer-service-detail", args=[uid])


def we_partners_discount_url(uid):
    return reverse("we.partners-detail-discount-list", args=[uid])


def we_partner_discount_list_url():
    return reverse("we.partners-discount-list")


def we_send_added_user_set_password_mail_url(token):
    return reverse("we.invited-user-set-password", args=[token])
