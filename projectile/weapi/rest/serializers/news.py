from django.shortcuts import get_object_or_404

from rest_framework import serializers

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer
from accountio.rest.serializers.organization_news import PublicAuthorSlimSerializer

from common.serializers import BaseModelSerializer

from fileroomio.choices import FileItemConnectorKind
from fileroomio.models import FileItem, FileItemConnector

from mediaroomio.choices import MediaImageConnectorKind
from mediaroomio.models import MediaImage, MediaImageConnector

from newsdeskio.models import NewsdeskPost

from versatileimagefield.serializers import VersatileImageFieldSerializer


class NewsListSerializer(serializers.ModelSerializer):
    author = PublicAuthorSlimSerializer(read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x400", "crop__400x400"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = NewsdeskPost
        fields = [
            "uid",
            "slug",
            "title",
            "summary",
            "description",
            "image",
            "organization",
            "kind",
            "status",
            "author",
            "is_featured",
            "created_at",
        ]

    def create(self, validated_data):
        return NewsdeskPost.objects.create(
            author=self.context["request"].user,
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )


class NewsDetailSerializer(serializers.ModelSerializer):
    author = PublicAuthorSlimSerializer(read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x400", "crop__400x400"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = NewsdeskPost
        fields = [
            "uid",
            "title",
            "slug",
            "summary",
            "description",
            "image",
            "organization",
            "kind",
            "status",
            "author",
            "is_featured",
            "created_at",
        ]


class PrivateNewsPostFileListSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "uid",
            "fileitem",
            "size",
            "dotextension",
            "name",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["uid", "size", "dotextension", "created_at", "updated_at"]

    def create(self, validated_data):
        file_item = FileItem.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )
        newspost_uid = {"uid": self.context["uid"]}

        FileItemConnector.objects.create(
            fileitem=file_item,
            newspost=get_object_or_404(NewsdeskPost, **newspost_uid),
            kind=FileItemConnectorKind.NEWS_POST,
            organization=self.context["request"].user.get_organization(),
        )
        return file_item


class PrivateNewsPostFileDetailSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "fileitem",
            "size",
            "dotextension",
            "name",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
        ]

        read_only_fields = ["size", "dotextension"]


class PrivatePostImageListSerializer(BaseModelSerializer):
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "width", "height", "created_at", "updated_at"]

    def create(self, validated_data):
        media_image = MediaImage.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )
        uid = self.context["uid"]
        news_post = get_object_or_404(NewsdeskPost.objects.filter(), uid=uid)

        MediaImageConnector.objects.create(
            image=media_image,
            newspost=news_post,
            kind=MediaImageConnectorKind.NEWS_POST,
            organization=self.context["request"].user.get_organization(),
        )

        return media_image


class PrivatePostImageDetailSerializer(BaseModelSerializer):
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
        read_only_fields = ["width", "height"]
