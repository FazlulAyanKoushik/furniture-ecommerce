from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from accountio.rest.serializers.organization_users import PrivateUserSlimSerializer

from common.serializers import BaseModelSerializer

from core.emails import send_group_member_invitation_mail, send_user_activation_mail


from gruppio.models import Group, Member
from gruppio.choices import MemberRole, MemberStatus

from fileroomio.models import FileItem, FileItemConnector
from fileroomio.choices import FileItemConnectorKind

from mediaroomio.models import MediaImage, MediaImageConnector
from mediaroomio.choices import MediaImageConnectorKind

from versatileimagefield.serializers import VersatileImageFieldSerializer

User = get_user_model()


class PrivateGroupListSerializer(BaseModelSerializer):
    first_name = serializers.CharField(min_length=2, max_length=50, write_only=True)
    last_name = serializers.CharField(min_length=2, max_length=50, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)

    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x256", "crop__1024x256"),
        ],
        required=False,
    )
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = Group
        fields = [
            "uid",
            "name",
            "description",
            "avatar",
            "hero",
            "slug",
            "kind",
            "status",
            "country",
            "faq",
            "post_count",
            "member_count",
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

        read_only_fields = [
            "uid",
            "slug",
            "post_count",
            "member_count",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        group = Group.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )

        get_user = User.objects.filter(email=email)

        if get_user.exists():
            user = get_user.first()

            Member.objects.create(
                group=group,
                user=user,
                role=MemberRole.MEMBER,
                status=MemberStatus.USER_ACCEPTED,
            )

            send_group_member_invitation_mail(user)
        else:
            try:
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email.lower(),
                    username=email,
                    is_active=False,
                )
                user.set_password(password)
                user.save()

                Member.objects.create(
                    group=group,
                    user=user,
                    role=MemberRole.MEMBER,
                    status=MemberStatus.USER_ACCEPTED,
                )

                new_user = User.objects.get(email=email)

                send_user_activation_mail(new_user)
            except user.DoesNotExist:
                return False

        return group


class PrivateGroupDetailSerializer(BaseModelSerializer):
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x256", "crop__1024x256"),
        ],
        required=False,
    )
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = Group
        fields = [
            "name",
            "description",
            "avatar",
            "hero",
            "slug",
            "kind",
            "status",
            "country",
            "faq",
            "post_count",
            "member_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "slug",
            "post_count",
            "member_count",
            "created_at",
            "updated_at",
        ]


class PrivateMemberListSerializer(BaseModelSerializer):
    user = serializers.SlugRelatedField(slug_field="slug", queryset=User.objects.all())

    class Meta:
        model = Member
        fields = ["uid", "user", "role", "status", "referrer"]
        read_only_fields = ["uid"]

    def create(self, validated_data):
        return Member.objects.create(
            group=get_object_or_404(
                Group.objects.filter(), uid=self.context["group_uid"]
            ),
            **validated_data
        )


class PrivateMemberDetailSerializer(BaseModelSerializer):
    user = PrivateUserSlimSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ["user", "role", "status", "referrer"]


class PrivateGroupFileListSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "uid",
            "fileitem",
            "name",
            "size",
            "extension",
            "dotextension",
            "kind",
            "description",
            "visibility",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uid",
            "size",
            "extension",
            "dotextension",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        file_item = FileItem.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )
        group_uid = {"uid": self.context["uid"]}

        FileItemConnector.objects.create(
            fileitem=file_item,
            group=get_object_or_404(Group, **group_uid),
            kind=FileItemConnectorKind.GROUP,
            organization=self.context["request"].user.get_organization(),
        )
        return file_item


class PrivateGroupFileDetailSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "fileitem",
            "name",
            "size",
            "extension",
            "dotextension",
            "description",
            "kind",
            "visibility",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["__all__"]


class PrivateGroupImageListSerializer(BaseModelSerializer):
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
        group_post = get_object_or_404(Group.objects.filter(), uid=uid)

        MediaImageConnector.objects.create(
            image=media_image,
            group=group_post,
            kind=MediaImageConnectorKind.GROUP,
            organization=self.context["request"].user.get_organization(),
        )

        return media_image


class PrivateGroupImageDetailSerializer(BaseModelSerializer):
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["width", "height", "created_at", "updated_at"]
