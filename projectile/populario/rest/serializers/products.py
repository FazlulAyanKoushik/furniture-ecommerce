from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization

from catalogio.models import Product

from common.serializers import BaseModelSerializer

from populario.models import PopularProduct


class GlobalPopularProductSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "slug",
            "title",
            "display_title",
            "description",
            "image",
        ]
        read_only_fields = ["__all__"]


class GlobalOrganizationSlimSerializer(serializers.ModelSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("at512x256", "thumbnail__512x256"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "slug",
            "name",
            "display_name",
            "avatar",
            "logo_wide",
            "kind",
            "country",
        ]
        read_only_fields = ["__all__"]
