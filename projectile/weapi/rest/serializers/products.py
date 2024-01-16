import os

import logging

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from catalogio.models import (
    Material,
    Product,
    ProductBrand,
    ProductMaterialConnector,
)

from common.fields import FileSizeField
from common.lists import FILE_EXTENSIONS
from common.serializers import BaseModelSerializer

from fileroomio.choices import FileItemConnectorKind
from fileroomio.models import FileItem, FileItemConnector

from mediaroomio.choices import MediaImageConnectorKind
from mediaroomio.models import MediaImage, MediaImageConnector, MediaImageKind

from tagio.choices import TagEntity
from tagio.models import Tag, TagConnector

from ..serializers import tags
from .brands import PrivateBrandSlimSerializer


logger = logging.getLogger(__name__)


class PrivateMaterialSlimSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="material.uid")
    name = serializers.CharField(max_length=255, read_only=True, source="material.name")
    description = serializers.CharField(
        max_length=400, read_only=True, source="material.description"
    )
    status = serializers.CharField(
        max_length=30, read_only=True, source="material.status"
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "crop__400x400"),
        ],
        read_only=True,
        source="material.image",
    )


class PrivateProductListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "crop__400x400"),
        ],
        required=False,
    )
    brand = PrivateBrandSlimSerializer(read_only=True)
    brand_uid = serializers.UUIDField(write_only=True, required=False)
    tags = serializers.SerializerMethodField("get_tags", required=False)
    tag_uids = serializers.ListField(write_only=True, required=False)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    material_uids = serializers.ListField(write_only=True, required=False)
    materials = PrivateMaterialSlimSerializer(
        read_only=True, many=True, source="productmaterialconnector_set"
    )

    class Meta:
        model = Product
        fields = [
            "uid",
            "title",
            "slug",
            "description",
            "seo_title",
            "seo_description",
            "categories",
            "color",
            "material",
            "image",
            "sku",
            "status",
            "channels",
            "display_title",
            "published_at",
            "like_count",
            "view_count",
            "brand",
            "brand_uid",
            "organization",
            "tags",
            "tag_uids",
            "materials",
            "material_uids",
        ]
        read_only_fields = ["uid", "slug", "brand", "tags", "like_count", "view_count"]

    def get_tags(self, instance):
        """show the connected tag list"""
        tag_connectors = instance.tagconnector_set.filter().values_list(
            "tag_id", flat=True
        )
        tag_queryset = Tag.objects.filter(id__in=tag_connectors)
        return tags.PrivateTagSerializer(tag_queryset, many=True).data


    def create(self, validated_data):
        """overriding the method to get brand instance by the brand uid provided by frontend"""

        # removing Kwargs uid(s)
        tag_uid_list = validated_data.pop("tag_uids", None)
        material_uids = validated_data.pop("material_uids", None)
        brand_uid = validated_data.pop("brand_uid", None)
        
        
        if brand_uid:
            kwargs = {"uid": str(brand_uid)}
            validated_data["brand"] = get_object_or_404(
                ProductBrand.objects.filter(), **kwargs
            )
        product = Product.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )
        # Create an image instance if the user placed an image when creating the product
        try:
            if product.image:
                image_object, _ = MediaImage.objects.get_or_create(
                    image=product.image,
                    defaults={
                        "organization": self.context["request"].user.get_organization(),
                        "kind": MediaImageKind.IMAGE,
                    },
                )
                MediaImageConnector.objects.create(
                    image=image_object,
                    kind=MediaImageConnectorKind.PRODUCT,
                    product=product,
                    organization=self.context["request"].user.get_organization(),
                )
        except:
            pass
        tag_connectors = []
        if tag_uid_list:
            tags = Tag.objects.filter(uid__in=tag_uid_list).distinct()
            tag_connectors = [
                TagConnector(tag=tag, product=product, entity=TagEntity.PRODUCT)
                for tag in tags
            ]
            TagConnector.objects.bulk_create(tag_connectors)

        product_material_connectors = []
        if material_uids:
            materials = Material.objects.filter(uid__in=material_uids).distinct()
            product_material_connectors = [
                ProductMaterialConnector(product=product, material=material)
                for material in materials
            ]
            ProductMaterialConnector.objects.bulk_create(product_material_connectors)

        return product


class PrivateProductDetailSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "crop__400x400"),
        ],
        required=False,
    )
    brand = PrivateBrandSlimSerializer(read_only=True)
    brand_uid = serializers.UUIDField(write_only=True, required=False)
    tags = serializers.SerializerMethodField("get_tags", required=False)
    tag_uids = serializers.ListField(write_only=True, required=False)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    materials = PrivateMaterialSlimSerializer(
        read_only=True, many=True, source="productmaterialconnector_set"
    )
    materials_uids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            "uid",
            "title",
            "slug",
            "description",
            "seo_title",
            "seo_description",
            "categories",
            "color",
            "material",
            "image",
            "sku",
            "status",
            "channels",
            "display_title",
            "published_at",
            "like_count",
            "view_count",
            "brand",
            "brand_uid",
            "organization",
            "tags",
            "materials",
            "tag_uids",
            "materials_uids",
        ]
        read_only_fields = ["uid", "slug", "brand", "tags"]

    def get_tags(self, instance):
        """show the connected tag list"""
        tag_connectors = instance.tagconnector_set.filter().values_list(
            "tag_id", flat=True
        )
        tag_queryset = Tag.objects.filter(id__in=tag_connectors)
        return tags.PrivateTagSerializer(tag_queryset, many=True).data


    def update(self, instance, validated_data):
        """overriding the method to get brand instance by the brand uid provided by frontend"""

        # removed brand uid from validated data to find brand instance with it
        brand_uid = validated_data.pop("brand_uid", None)
        image = validated_data.pop("image", None)

        if brand_uid:
            kwargs = {"uid": str(brand_uid)}
            validated_data["brand"] = get_object_or_404(
                ProductBrand.objects.filter(), **kwargs
            )
        # try exception for updating material
        try:
            materials_uids_list = validated_data.pop("materials_uids")

            if not materials_uids_list:
                instance.productmaterialconnector_set.all().delete()

            material_connectors = []
            if materials_uids_list:
                instance.productmaterialconnector_set.all().delete()

                for material in Material.objects.filter(
                    uid__in=materials_uids_list
                ).distinct():
                    material_connectors.append(
                        ProductMaterialConnector(product=instance, material=material)
                    )

                ProductMaterialConnector.objects.bulk_create(material_connectors)
        except KeyError:
            pass

        # Not using none as if user wants to update product without updating tags
        # it will not remove existing tags
        try:
            tag_uid_list = validated_data.pop("tag_uids")

            # if user send a empty list of tag delete all the connection
            if not tag_uid_list:
                instance.tagconnector_set.all().delete()

            tag_connectors = []
            if tag_uid_list:  # TODO: check if uid(s) is valid
                # removing existing connection other wish we will need to check one by one uid
                # if the connection already exits
                instance.tagconnector_set.all().delete()

                # recreating the connection with patch tag uid(s)
                for tag in Tag.objects.filter(
                    uid__in=tag_uid_list
                ).distinct():  # added distinct to avoid duplicate uid(s)
                    # collecting tag instance with uid and creating a list
                    # for bulk create with specific product which is created
                    tag_connectors.append(
                        TagConnector(
                            tag=tag, product=instance, entity=TagEntity.PRODUCT
                        )
                    )
                TagConnector.objects.bulk_create(tag_connectors)
        except KeyError:
            pass

        # Create an image instance if the user placed an image when updating the product
        try:
            if image is not None:
                instance.image = image
                instance.save()
                image_object, _ = MediaImage.objects.get_or_create(
                    image=instance.image,
                    defaults={
                        "organization": self.context["request"].user.get_organization(),
                        "kind": MediaImageKind.IMAGE,
                    },
                )
                MediaImageConnector.objects.create(
                    image=image_object,
                    kind=MediaImageConnectorKind.PRODUCT,
                    product=instance,
                    organization=self.context["request"].user.get_organization(),
                )
        except:
            pass

        return super().update(instance, validated_data)


class PrivateProductImageListSerializer(BaseModelSerializer):
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
        read_only_fields = ["width", "height"]

    def create(self, validated_data):
        image_object = MediaImage.objects.create(
            organization=self.context["request"].user.get_organization(),
            kind=MediaImageKind.IMAGE,
            **validated_data
        )

        product_uid = {"uid": self.context["uid"]}
        MediaImageConnector.objects.create(
            image=image_object,
            kind=MediaImageConnectorKind.PRODUCT,
            product=get_object_or_404(Product, **product_uid),
            organization=self.context["request"].user.get_organization(),
        )
        return image_object


class PrivateProductImageDetailSerializer(BaseModelSerializer):
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
        read_only_fields = ["width", "height"]


class PrivateProductFileListSerializer(BaseModelSerializer):
    size = FileSizeField(read_only=True)

    class Meta:
        model = FileItem
        fields = [
            "uid",
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
        read_only_fields = [
            "uid",
            "size",
            "dotextension",
            "extension",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        file = validated_data.get("fileitem", None)
        filename = validated_data.get("name", None)

        if file:
            name, dotextension = os.path.splitext(file.name)
            dotextension = dotextension.lower()
            if filename:
                file.name = filename + dotextension

        validated_data.update(
            {
                "size": file.size,
                "name": file.name,
                "dotextension": dotextension[1:],
                "extension": FILE_EXTENSIONS.get(dotextension, "Others"),
            }
        )

        file_item = FileItem.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )
        product_uid = {"uid": self.context["uid"]}

        FileItemConnector.objects.create(
            fileitem=file_item,
            product=get_object_or_404(Product, **product_uid),
            kind=FileItemConnectorKind.PRODUCT,
            organization=self.context["request"].user.get_organization(),
        )
        return file_item


class PrivateProductFileDetailSerializer(BaseModelSerializer):
    size = FileSizeField(read_only=True)

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
        read_only_fields = [
            "fileitem",
            "name",
            "size",
            "dotextension",
            "extension",
            "created_at",
            "updated_at",
        ]


class PrivateProductTagDetailSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "uid",
            "parent",
            "category",
            "name",
            "status",
        ]
        read_only_field = ["uid", "category", "status", "parent"]


class PrivateProductCoverImageDetailSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["__all__"]
