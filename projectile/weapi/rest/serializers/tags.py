import logging

from common.serializers import BaseModelSerializer

from tagio.models import Tag

logger = logging.getLogger(__name__)


class PrivateTagSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "uid",
            "slug",
            "parent",
            "category",
            "name",
            "status",
        ]
        read_only = ["uid","slug"]
