from django.shortcuts import get_object_or_404

from rest_framework import generics, serializers

from accountio.rest.permissions import IsSameUser

from catalogio.rest.permissions import IsOrganizationStaff
from gruppio.choices import GroupStatus
from gruppio.models import Group, Member

from fileroomio.models import FileItem

from mediaroomio.models import MediaImage

from ..permissions import IsGroupOrganizationStaff

from ..serializers.groups import (
    PrivateGroupFileListSerializer,
    PrivateGroupFileDetailSerializer,
    PrivateGroupListSerializer,
    PrivateGroupDetailSerializer,
    PrivateGroupImageListSerializer,
    PrivateGroupImageDetailSerializer,
    PrivateMemberListSerializer,
    PrivateMemberDetailSerializer,
)


class PrivateGroupList(generics.ListCreateAPIView):
    queryset = Group.objects.get_public_groups()
    serializer_class = PrivateGroupListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)


class PrivateGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.get_public_groups()
    serializer_class = PrivateGroupDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "uid": self.kwargs.get("uid", None),
        }
        return get_object_or_404(Group, **kwargs)

    def perform_destroy(self, instance):
        instance.status = GroupStatus.REMOVED
        instance.save()


class PrivateMemberList(generics.ListCreateAPIView):
    queryset = Member.objects.get_status_accepted()
    serializer_class = PrivateMemberListSerializer
    permission_classes = [IsGroupOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("group_uid", None)
        return self.queryset.filter(group__uid=uid)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["group_uid"] = self.kwargs.get("group_uid", None)
        return context


class PrivateMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.get_status_accepted()
    serializer_class = PrivateMemberDetailSerializer
    permission_classes = [IsSameUser]

    def get_object(self):
        kwargs = {
            "group__uid": self.kwargs.get("group_uid", None),
            "uid": self.kwargs.get("uid", None),
        }
        return get_object_or_404(Member, **kwargs)


class PrivateGroupFileList(generics.ListCreateAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateGroupFileListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        group = get_object_or_404(Group.objects.filter(), **kwargs)
        fileitem_ids = group.fileitemconnector_set.filter().values_list(
            "fileitem_id", flat=True
        )
        return self.queryset.filter(id__in=fileitem_ids)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateGroupFileDetail(generics.RetrieveDestroyAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateGroupFileDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("group_uid", None)}
        return get_object_or_404(FileItem, **kwargs)


class PrivateGroupImageList(generics.ListCreateAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = PrivateGroupImageListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        group_image = get_object_or_404(Group.objects.filter(), uid=uid)
        image_ids = group_image.mediaimageconnector_set.filter().values_list(
            "image_id", flat=True
        )
        return self.queryset.filter(id__in=image_ids)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateGroupImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = PrivateGroupImageDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("group_uid", None)}
        return get_object_or_404(MediaImage, **kwargs)
