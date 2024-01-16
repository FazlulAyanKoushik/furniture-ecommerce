from django.urls import reverse


def we_user_list_url():
    return reverse("we.user-list")


def organization_onboarding_url():
    return reverse("organizations.onboarding-detail")


def project_list_url():
    return reverse("we.projects-list")


def public_project_list_url():
    return reverse("public.project-list")


def public_project_detail_url(project_slug):
    return reverse("public.project-detail", args=[project_slug])


def public_project_detail_image_list_url(slug):
    return reverse("public.project-detail-image-list", args=[slug])
