from django.shortcuts import get_object_or_404

from rest_framework import generics, serializers, filters

from accountio.models import Organization

from catalogio.rest.permissions import IsOrganizationStaff

from fileroomio.choices import FileStatus
from fileroomio.models import FileItem, FileItemAccess

from ..serializers.files import (
    PrivateOrganizationFileListSerializer,
    PrivateOrganizationFileDetailSerializer,
)


class PrivateOrganizationFileList(generics.ListCreateAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateOrganizationFileListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "extension"]
    ordering_fields = ["name", "extension", "created_at"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)


class PrivateOrganizationFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateOrganizationFileDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "organization": self.request.user.get_organization(),
            "uid": self.kwargs.get("uid", None),
        }
        return get_object_or_404(FileItem.objects.filter(), **kwargs)

    def patch(self, request, *args, **kwargs):
        data = request.data
        if "access" in data:
            access = data["access"]
            # Delete old relations
            fileitem = self.get_object()
            fileitem.fileitemaccess_set.filter().delete()
            # Set new instances
            instances = []
            for item in access:
                uid = item["value"]
                fileitemaccess = FileItemAccess()
                try:
                    fileitemaccess.fileitem = fileitem
                    fileitemaccess.partner = Organization.objects.get(uid=uid)
                    instances.append(fileitemaccess)
                except Organization.DoesNotExist:
                    continue
            # Also add the owner to be able find all related accessors with one query
            fileitemaccess = FileItemAccess()
            fileitemaccess.fileitem = fileitem
            fileitemaccess.partner = fileitem.organization
            instances.append(fileitemaccess)
            FileItemAccess.objects.bulk_create(instances)
        return super().patch(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.status = FileStatus.REMOVED
        instance.save()
