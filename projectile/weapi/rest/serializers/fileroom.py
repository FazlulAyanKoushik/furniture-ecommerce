import logging

from common.serializers import BaseModelSerializer

from fileroomio.models import FileItem

logger = logging.getLogger(__name__)


class PrivateFileItemSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "uid",
            "fileitem",
            "size",
            "dotextension",
            "name",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
            "organization_slug",
            "created_at",
            "updated_at",
        ]
    
    def create(self, validated_data):
        return FileItem.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )