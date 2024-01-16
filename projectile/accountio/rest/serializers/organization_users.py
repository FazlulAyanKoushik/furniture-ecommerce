from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from common.serializers import BaseModelSerializer

from core.models import User

from ...models import OrganizationUser

from .organizations import PublicOrganizationSlimSerializer


class PublicUserSerializer(BaseModelSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
            ("at128", "thumbnail__128x128"),
        ],
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "slug",
            "first_name",
            "last_name",
            "headline",
            "avatar",
        ]
        read_only_fields = ("__all__",)


class UserPrivateSerializer(BaseModelSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
            ("at128", "thumbnail__128x128"),
        ],
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "uid",
            "slug",
            "first_name",
            "last_name",
            "last_login",
            "date_joined",
            "headline",
            "avatar",
        ]
        read_only_fields = ("__all__",)


class PrivateUserSlimSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "first_name",
            "last_name",
        ]


class PublicOrganizationUserSerializer(BaseModelSerializer):
    user = PublicUserSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            "uid",
            "organization",
            "user",
            "role",
            "status",
        ]
        read_only_fields = ("__all__",)


class PrivateOrganizationPartnerUserListSerializer(BaseModelSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
            ("at128", "thumbnail__128x128"),
        ],
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "uid", 
            "slug",           
            "first_name",
            "last_name",
            "slug",
            "last_login",
            "date_joined",
            "headline",
            "avatar",
        ]
        read_only_fields = ["__all__"]
