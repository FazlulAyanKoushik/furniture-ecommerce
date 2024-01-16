from rest_framework import serializers

from common.serializers import BaseModelSerializer

from catalogio.models import Product, ProductBrand

from mediaroomio.models import MediaImage

from versatileimagefield.serializers import VersatileImageFieldSerializer

from .organizations import PublicOrganizationSlimSerializer


class PublicBrandSlimSerializer(BaseModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ["title", "slug"]


class PublicOrganizationProductListSerializer(BaseModelSerializer):
    brand = PublicBrandSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)

    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024", "crop__1024x1024"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "slug",
            "organization",
            "title",
            "description",
            "seo_title",
            "seo_description",
            "image",
            "sku",
            "status",
            "published_at",
            "like_count",
            "view_count",
            "brand",
        ]
        read_only_fields = ("__all__",)

    def get_title(self, instance):
        return instance.display_title or instance.title


class PublicOrganizationProductDetailSerializer(BaseModelSerializer):
    brand = PublicBrandSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "organization",
            "title",
            "description",
            "seo_title",
            "seo_description",
            "image",
            "sku",
            "status",
            "published_at",
            "like_count",
            "view_count",
            "brand",
        ]
        read_only_fields = ("__all__",)

    def get_title(self, instance):
        return instance.display_title or instance.title


class PublicOrganizationProductImageListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "uid",
            "image",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
        ]
        read_only_fields = ("__all__",)
