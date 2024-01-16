import logging

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from common.serializers import BaseModelSerializer

from ...models import ProductBrand

logger = logging.getLogger(__name__)


class GlobalProductBrandSerializer(BaseModelSerializer):
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = ProductBrand
        fields = [
            "uid",
            "title",
            "slug",
            "description",
            "image",
            "organization",
        ]
