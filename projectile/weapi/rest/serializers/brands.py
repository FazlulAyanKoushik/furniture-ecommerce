import logging

from catalogio.models import ProductBrand
from common.serializers import BaseModelSerializer

logger = logging.getLogger(__name__)


class PrivateBrandSlimSerializer(BaseModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ["uid", "title"]


class PrivateProductBrandListSerializer(BaseModelSerializer):
    class Meta:
        model = ProductBrand
        fields = [
            "uid",
            "title",
            "slug",
            "description",
            "image",
        ]

    def create(self, validated_data):
        return ProductBrand.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )


class PrivateProductBrandDetailSerializer(BaseModelSerializer):
    class Meta:
        model = ProductBrand
        fields = [
            "title",
            "slug",
            "description",
            "image",
        ]
        read_only_fields = ["slug"]
