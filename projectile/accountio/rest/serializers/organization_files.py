import logging

from common.serializers import BaseModelSerializer

from fileroomio.models import FileItem


logger = logging.getLogger(__name__)


class PublicFileListSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "uid",
            "fileitem",
            "size",
            "dotextension",
            "name",
            "description",
        ]
        read_only_fields = ("__all__",)


class PublicFileDetailSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "fileitem",
            "size",
            "dotextension",
            "name",
            "description",
        ]
        read_only_fields = ("__all__",)
