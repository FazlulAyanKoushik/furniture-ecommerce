from django.shortcuts import get_object_or_404

from rest_framework import generics

from gruppio.rest.serializers.groups import (
    GlobalAdminListSerializer,
    GlobalGroupListSeriailizer,
    GlobalGroupDetailSeriailizer,
    GlobalMemberListSerializer,
    GlobalMemberDetailSerializer,
)

from ...choices import GroupStatus
from ...models import Group, Member


class GlobalGroupList(generics.ListAPIView):
    queryset = Group.objects.select_related("organization").filter(
        status=GroupStatus.ACTIVE
    )
    serializer_class = GlobalGroupListSeriailizer


class GlobalGroupDetail(generics.RetrieveAPIView):
    queryset = Group.objects.get_status_active()
    serializer_class = GlobalGroupDetailSeriailizer
    lookup_field = "slug"


class GlobalMemberList(generics.ListAPIView):
    queryset = Member.objects.get_status_accepted()
    serializer_class = GlobalMemberListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug", None)
        return self.queryset.filter(group__slug=slug)


class GlobalMemberDetail(generics.RetrieveAPIView):
    queryset = Member.objects.get_status_accepted()
    serializer_class = GlobalMemberDetailSerializer

    def get_object(self):
        kwargs = {
            "group__slug": self.kwargs.get("group_slug", None),
            "uid": self.kwargs.get("uid", None),
        }
        return get_object_or_404(Member, **kwargs)


class GlobalGroupAdminList(generics.ListAPIView):
    queryset = Member.objects.get_role_admins()
    serializer_class = GlobalAdminListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug", None)
        return self.queryset.filter(group__slug=slug)
