import logging
import uuid

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from common.serializers import BaseModelSerializer

from core.models import User

from invitio.models import OrganizationInvite

from tagio.models import Tag

from weapi.rest.serializers.tags import PrivateTagSerializer

from ...choices import OrganizationUserRole, OrganizationUserStatus

from ...models import Organization, OrganizationUser

from versatileimagefield.serializers import VersatileImageFieldSerializer


logger = logging.getLogger(__name__)


class PublicParentOrganizationSerializer(BaseModelSerializer):
    class Meta:
        model = Organization
        read_only_fields = ("__all__",)


class PublicOrganizationListSerializer(BaseModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    country = serializers.CharField(min_length=2, max_length=2, required=True)
    tags = serializers.SerializerMethodField("get_tags", required=False)
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
            ("at128", "thumbnail__128x128"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("at1024x384", "thumbnail__1024x384"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("at512x256", "thumbnail__512x256"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "slug",
            "name",
            "registration_no",
            "address",
            "postal_code",
            "postal_area",
            "city",
            "country",
            "email",
            "phone",
            "website_url",
            "summary",
            "description",
            "status",
            "avatar",
            "hero",
            "logo_wide",
            "image",
            "kind",
            "tags",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("__all__",)

    def get_name(self, instance):
        return instance.display_name or instance.name

    def get_tags(self, instance):
        # Tag list for connected organization
        tag_connectors = instance.tagconnector_set.filter().values_list(
            "tag_id", flat=True
        )
        tags = Tag.objects.filter(id__in=tag_connectors)
        return PrivateTagSerializer(tags, many=True).data


class PublicOrganizationDetailSerializer(BaseModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    country = serializers.CharField(min_length=2, max_length=2, required=True)
    tags = serializers.SerializerMethodField("get_tags", required=False)
    has_partner_services = serializers.SerializerMethodField(read_only=True)
    request_sent = serializers.SerializerMethodField(read_only=True)
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
            ("at128", "thumbnail__128x128"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("at1024x384", "thumbnail__1024x384"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("at512x256", "thumbnail__512x256"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "name",
            "registration_no",
            "address",
            "postal_code",
            "postal_area",
            "city",
            "country",
            "email",
            "phone",
            "website_url",
            "summary",
            "description",
            "status",
            "avatar",
            "hero",
            "logo_wide",
            "image",
            "kind",
            "tags",
            "request_sent",
            "has_partner_services",
        ]
        read_only_fields = ("__all__",)

    def get_name(self, instance):
        return instance.display_name or instance.name

    def get_tags(self, instance):
        # Tag list for connected organization
        tag_connectors = instance.tagconnector_set.filter().values_list(
            "tag_id", flat=True
        )
        tags = Tag.objects.filter(id__in=tag_connectors)
        return PrivateTagSerializer(tags, many=True).data

    def get_has_partner_services(self, instance):
        try:
            has_partner_services = instance.has_partner_services()
            return has_partner_services
        except:
            return ""

    def get_request_sent(self, instance):
        try:
            organization_invite = OrganizationInvite.objects.filter(
                target=instance,
                organization=self.context["request"].user.get_organization(),
            )
            if organization_invite.exists():
                return True
        except:
            return False


class PublicOrganizationSlimSerializer(BaseModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField()
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x256", "crop__1024x256"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "slug",
            "name",
            "avatar",
            "hero",
            "logo_wide",
            "image",
            "summary",
            "country",
            "kind",
        ]
        read_only_fields = ("__all__",)

    def get_name(self, instance):
        return instance.display_name or instance.name


class PublicUserSlimSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]
        read_only_fields = ("__all__",)


class PublicOrganizationUserSlimSerializer(BaseModelSerializer):
    headline = serializers.SerializerMethodField()
    user = PublicUserSlimSerializer()
    organization = PublicOrganizationSlimSerializer()

    class Meta:
        model = OrganizationUser
        fields = [
            "uid",
            "organization",
            "headline",
            "user",
            "role",
            "status",
            "updated_at",
        ]
        read_only_fields = ("__all__",)

    def get_headline(self, instance):
        return instance.user.headline


class PublicOrganizationUserWriteSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(min_length=2, max_length=50, write_only=True)
    last_name = serializers.CharField(min_length=2, max_length=50, write_only=True)
    role = serializers.ChoiceField(
        OrganizationUserRole.choices, default=OrganizationUserRole.STAFF
    )

    class Meta:
        model = OrganizationUser
        fields = ("email", "first_name", "last_name", "role")
        read_only_fields = ("__all__",)

    def create(self, validated_data, *args, **kwargs):
        email = self.validated_data["email"].lower()
        request = self.context["request"]
        organization = self.context.get("organization", None)
        if organization is None:
            organization = request.user.get_organization()
        referrer = request.user.get_organization_user()
        try:
            user = User.objects.get(email=email)
            organization_user, _ = user.users.get_or_create(
                organization=organization,
                user=user,
            )

            if organization_user.role != validated_data["role"]:
                organization_user.role = validated_data["role"]
                organization_user.save(update_fields=["role"])
        except User.DoesNotExist:
            user = User.objects.create(
                email=email,
                username=email,
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                is_active=False,
            )
            logger.debug(f"Created new user: {user.email}")

            organization_user, _ = OrganizationUser.objects.get_or_create(
                user=user,
                organization=organization,
                is_default=True,
                status=OrganizationUserStatus.PENDING,
                defaults={"role": validated_data["role"]},
            )
            logger.debug(f"Created new organization user: {organization_user}")

        if referrer:
            organization_user.referrer = referrer
            organization_user.save(update_fields=["referrer"])
        return organization_user

    def update(self, instance, validated_data):
        fields = []
        if instance.user.email != validated_data["email"]:
            email = validated_data["email"].lower()
            instance.user.email = email
            instance.user.username = email
            fields.append("email")
        if instance.user.first_name != validated_data["first_name"]:
            instance.user.first_name = validated_data["first_name"]
            fields.append("first_name")
        if instance.user.last_name != validated_data["last_name"]:
            instance.user.last_name = validated_data["last_name"]
            fields.append("last_name")
        instance.user.save(update_fields=fields)

        if not instance.role == validated_data["role"]:
            instance.role = validated_data["role"]
            instance.save(update_fields=["role"])
        return instance


class PublicOrganizationUserInviteSerializer(BaseModelSerializer):
    first_name = serializers.CharField(min_length=2, max_length=50, write_only=True)
    last_name = serializers.CharField(min_length=2, max_length=50, write_only=True)
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    confirm_password = serializers.CharField(
        min_length=8, max_length=50, write_only=True
    )
    user = PublicUserSlimSerializer(read_only=True)
    referrer = PublicOrganizationUserSlimSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = (
            "user",
            "referrer",
            "token",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        )
        read_only_fields = (
            "user",
            "referrer",
        )

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords must match.")
        return data

    def update(self, instance, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        user = instance.user
        user.first_name = validated_data.pop("first_name")
        user.last_name = validated_data.pop("last_name")
        user.set_password(validated_data.pop("password"))
        user.save_dirty_fields()
        user.activate()
        instance.set_status_active()
        instance.select()
        instance.token = uuid.uuid4()
        instance.save_dirty_fields()
        return super().update(instance, validated_data)
