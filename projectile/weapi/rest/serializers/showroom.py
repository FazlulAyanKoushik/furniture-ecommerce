import logging

from rest_framework.generics import get_object_or_404
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from common.serializers import BaseModelSerializer

from mediaroomio.choices import MediaImageSpot, MediaImageKind
from mediaroomio.models import MediaImage, ShowRoomImageConnector

logger = logging.getLogger(__name__)


class PrivateOrganizationShowroomListSerializer(BaseModelSerializer):
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
            "title",
            "caption",
            "copyright",
            "priority",
            "kind",
        ]

        read_only_fields = [
            "uid",
            "image",
            "width",
            "height",
            "kind",
        ]

    def create(self, validated_data):
        image = MediaImage.objects.create(
            organization=self.context["request"].user.get_organization(),
            kind=MediaImageKind.IMAGE,
            spot=MediaImageSpot.SHOWROOM,
            **validated_data
        )
    
        ShowRoomImageConnector.objects.create(
            image=image,
            gallery_image=image,
            organization=self.context["request"].user.get_organization(),
        )
    
        return image


class PrivateOrganizationShowroomDetailSerializer(BaseModelSerializer):
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
            "title",
            "caption",
            "copyright",
            "priority",
            "kind",
            "organization_slug",
        ]

        read_only_fields = ["width", "height", "organization_slug"]


class PrivateGalleryListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "uid",
            "image",
            "title",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
        ]
        read_only_fields = ["width", "height"]


class PrivateShowroomListSerializer(BaseModelSerializer):
    showroom_image = PrivateGalleryListSerializer(read_only=True)
    gallery_images = PrivateGalleryListSerializer(many=True, read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
        write_only=True,
    )

    class Meta:
        model = MediaImage
        fields = [
            "showroom_image",
            "gallery_images",
            "image",
            "title",
            "caption",
            "copyright",
            "priority",
        ]
        write_only_fields = (
            "title",
            "caption",
            "copyright",
            "priority",
        )

    def create(self, validated_data):
        gallery_image = MediaImage.objects.create(
            organization=self.context["request"].user.get_organization(),
            kind=MediaImageKind.IMAGE,
            **validated_data
        )

        image_uid = {"uid": self.context["uid"]}
        ShowRoomImageConnector.objects.create(
            image=get_object_or_404(MediaImage.objects.get_spot_showroom(), **image_uid),
            gallery_image=gallery_image,
            organization=self.context["request"].user.get_organization(),
        )
        return validated_data


class PrivateShowroomImageDetailSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "image",
            "title",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
        ]
        read_only_fields = ["width", "height"]
