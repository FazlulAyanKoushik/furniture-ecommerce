from django.urls import reverse


def group_list_url():
    return reverse("group.list")


def group_detail_url(slug):
    return reverse("group.detail", args=[slug])


def group_member_list_url(slug):
    return reverse("members.list", args=[slug])


def group_member_detail_url(slug, member_uid):
    return reverse("members.detail", args=[slug, member_uid])


def group_admin_list_url(slug):
    return reverse("admins.list", args=[slug])
