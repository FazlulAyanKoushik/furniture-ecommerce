from django.shortcuts import get_object_or_404

from rest_framework import generics

from fileroomio.models import FileItem
from fileroomio.choices import FileStatus

from ..serializers.organization_files import (
    PublicFileListSerializer,
    PublicFileDetailSerializer,
)


class PublicFileItemList(generics.ListAPIView):
    queryset = FileItem.objects.get_status_active()
    serializer_class = PublicFileListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("organization_slug", None)
        return self.queryset.filter(organization__slug=slug)


class PublicFileItemDetail(generics.RetrieveAPIView):
    queryset = FileItem.objects.get_status_active()
    serializer_class = PublicFileDetailSerializer

    def get_object(self):
        kwargs = {
            "organization__slug": self.kwargs.get("organization_slug", None),
            "uid": self.kwargs.get("file_uid", None),
        }
        return get_object_or_404(FileItem, **kwargs)
