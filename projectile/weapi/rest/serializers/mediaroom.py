import logging

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from catalogio.models import Product

from collabio.models import Project

from common.serializers import BaseModelSerializer

from gruppio.models import Group

from mediaroomio.models import MediaImage, MediaImageConnector

from mediaroomio.choices import MediaImageConnectorKind

from versatileimagefield.serializers import VersatileImageFieldSerializer

logger = logging.getLogger(__name__)


class PrivateMediaRelatedImageConnectorSerializer(BaseModelSerializer):
    uid = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = MediaImageConnector
        fields = (
            "kind",
            "uid",
            "title",
        )

        read_only_fields = (
            "kind",
            "uid",
            "title",
        )

    def get_uid(self, instance):
        if instance.kind == "GROUP" and instance.group:
            return instance.group.uid
        if instance.kind == "NEWSPOST" and instance.newspost:
            return instance.newspost.uid
        if instance.kind == "PRODUCT" and instance.product:
            return instance.product.uid
        if instance.kind == "PROJECT" and instance.project:
            return instance.project.uid
        return None

    def get_title(self, instance):
        if instance.kind == "GROUP" and instance.group:
            return instance.group.name
        if instance.kind == "NEWSPOST" and instance.newspost:
            return instance.newspost.title
        if instance.kind == "PRODUCT" and instance.product:
            return instance.product.title
        if instance.kind == "PROJECT" and instance.project:
            return instance.project.title
        return None


class PrivateOrganizationImageListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    related = serializers.SerializerMethodField(read_only=True)

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
            "related",
            "organization_slug",
        ]

        read_only_fields = [
            "uid",
            "image",
            "width",
            "height",
            "kind",
            "related",
            "organization_slug",
        ]

    def get_related(self, instance):
        return PrivateMediaRelatedImageConnectorSerializer(
            instance.mediaimageconnector_set.filter().select_related(
                "group", "newspost", "product", "project"
            ),
            many=True,
        ).data


class PrivateOrganizationImageDetailSerializer(BaseModelSerializer):
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
            "organization_slug",
        ]

        read_only_fields = ["width", "height", "organization_slug"]


class PrivateProductImageSerializer(BaseModelSerializer):
    image = serializers.SlugRelatedField(
        slug_field="uid", queryset=MediaImage.objects.all()
    )

    class Meta:
        model = MediaImageConnector
        fields = (
            "uid",
            "image",
            "kind",
            "organization_slug",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("uid", "kind", "created_at", "updated_at")

    def create(self, validated_data):
        image = validated_data.pop("image")
        uid = self.context["uid"]
        product = get_object_or_404(Product.objects.filter(), uid=uid)

        connector = MediaImageConnector.objects.create(
            organization=self.context["request"].user.get_organization(),
            image=image,
            product=product,
            kind=MediaImageConnectorKind.PRODUCT,
            **validated_data
        )
        return connector


class PrivateProjectImageSerializer(BaseModelSerializer):
    image = serializers.SlugRelatedField(
        slug_field="uid", queryset=MediaImage.objects.all()
    )

    class Meta:
        model = MediaImageConnector
        fields = (
            "uid",
            "image",
            "kind",
            "organization_slug",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("uid", "kind", "created_at", "updated_at")

    def create(self, validated_data):
        image = validated_data.pop("image")
        uid = self.context["uid"]
        project = get_object_or_404(Project.objects.filter(), uid=uid)

        connector = MediaImageConnector.objects.create(
            organization=self.context["request"].user.get_organization(),
            image=image,
            project=project,
            kind=MediaImageConnectorKind.PROJECT,
            **validated_data
        )
        return connector


class PrivateGroupImageSerializer(BaseModelSerializer):
    image = serializers.SlugRelatedField(
        slug_field="uid", queryset=MediaImage.objects.all()
    )

    class Meta:
        model = MediaImageConnector
        fields = (
            "uid",
            "image",
            "kind",
            "organization_slug",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("uid", "kind", "created_at", "updated_at")

    def create(self, validated_data):
        image = validated_data.pop("image")
        uid = self.context["uid"]
        group = get_object_or_404(Group.objects.filter(), uid=uid)

        connector = MediaImageConnector.objects.create(
            organization=self.context["request"].user.get_organization(),
            image=image,
            group=group,
            kind=MediaImageConnectorKind.GROUP,
            **validated_data
        )
        return connector
