from gruppio.models import Group

from common.serializers import BaseModelSerializer
from .organizations import PublicOrganizationSlimSerializer


class PublicOrganizationGroupListSerializer(BaseModelSerializer):
    """Serializer for Organization Group view"""

    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            "slug",
            "name",
            "description",
            "kind",
            "status",
            "country",
            "faq",
            "organization",
            "post_count",
            "member_count",
        ]
        read_only_fields = ("__all__",)


class PublicOrganizationGroupDetailSerializer(BaseModelSerializer):
    """Serializer for Organization Group Detail view"""

    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            "name",
            "description",
            "kind",
            "status",
            "country",
            "faq",
            "organization",
            "post_count",
            "member_count",
        ]
        read_only_fields = ("__all__",)
