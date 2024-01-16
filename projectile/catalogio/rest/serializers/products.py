import logging

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from common.serializers import BaseModelSerializer

from fileroomio.models import FileItem

from mediaroomio.models import MediaImage

from tagio.models import Tag

from weapi.rest.serializers.tags import PrivateTagSerializer

from ...models import Product, ProductCollection
from ..serializers.brands import GlobalProductBrandSerializer


logger = logging.getLogger(__name__)


class GlobalProductListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024", "crop__1024x1024"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        required=False,
    )

    brand = GlobalProductBrandSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "uid",
            "slug",
            "organization",
            "title",
            "display_title",
            "description",
            "seo_title",
            "seo_description",
            "image",
            "sku",
            "status",
            "channels",
            "published_at",
            "like_count",
            "view_count",
            "brand",
            "tags",
        ]
        read_only_fields = ("__all__",)

    def get_tags(self, instance):
        tag_uids = instance.tagconnector_set.filter().values_list("tag_id", flat=True)
        tag_query = Tag.objects.filter(id__in=tag_uids)
        return PrivateTagSerializer(tag_query, many=True).data


class GlobalProductDetailSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024", "crop__1024x1024"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        required=False,
    )

    brand = GlobalProductBrandSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "organization",
            "title",
            "display_title",
            "description",
            "seo_title",
            "seo_description",
            "image",
            "sku",
            "status",
            "channels",
            "published_at",
            "like_count",
            "view_count",
            "brand",
            "tags",
            "categories",
            "category",
            "color",
            "material",
        ]
        read_only_fields = ("__all__",)

    def get_tags(self, instance):
        tag_uids = instance.tagconnector_set.filter().values_list("tag_id", flat=True)
        tag_query = Tag.objects.filter(id__in=tag_uids)
        return PrivateTagSerializer(tag_query, many=True).data


class GlobalProductImageListSerializer(BaseModelSerializer):
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
            "kind",
        ]
        read_only_fields = ("__all__",)


class GlobalProductImageDetailSerializer(BaseModelSerializer):
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
            "image",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
            "kind",
        ]
        read_only_fields = ("__all__",)


class GlobalProductCollectionListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = ProductCollection
        fields = [
            "slug",
            "title",
            "kind",
            "image",
            "visibility",
            "organization",
        ]
        read_only_fields = ("__all__",)


class GlobalProductCollectionDetailSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = ProductCollection
        fields = [
            "title",
            "kind",
            "image",
            "visibility",
            "organization",
        ]
        read_only_fields = ("__all__",)


class GlobalCollectionProductListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "crop__400x400"),
        ],
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "slug",
            "display_title",
            "description",
            "seo_title",
            "seo_description",
            "image",
            "status",
            "channels",
            "like_count",
            "view_count",
            "brand",
        ]

        read_only_fields = ["__all__"]


class GlobalProductFileListSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "fileitem",
            "name",
            "size",
            "dotextension",
            "kind",
            "extension",
            "visibility",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("__all__",)
