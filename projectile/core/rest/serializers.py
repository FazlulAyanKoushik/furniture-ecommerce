import logging

from twilio.rest import Client

from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import APIException

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import OrganizationUser, Organization
from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from catalogio.models import Product, ProductDiscount

from collabio.models import Project

from common.serializers import BaseModelSerializer

from fileroomio.models import FileItem, FileItemAccess

from gruppio.models import Group, Member

from invitio.models import OrganizationInvite

from newsdeskio.models import NewsdeskPost

from notificationio.choices import NotificationKind
from notificationio.models import Notification

from otpio.models import UserPhone, UserPhoneOTP
from otpio.generate_otp import otp_generator

from threadio.choices import InboxKind, ThreadKind
from threadio.models import Thread, Inbox

from ..models import (
    User,
    UserEmail,
)

logger = logging.getLogger(__name__)


class BaseUserSerializer(BaseModelSerializer):
    name = serializers.CharField(max_length=100, source="get_name")

    class Meta:
        model = User
        fields = [
            "uid",
            "first_name",
            "last_name",
            "name",
            "date_joined",
            "last_login",
            "country",
            "model",
        ]


class MeSerializer(BaseUserSerializer):
    headline = serializers.CharField(min_length=2, max_length=50, required=False)
    summary = serializers.CharField(min_length=2, max_length=160, required=False)
    description = serializers.CharField(min_length=2, max_length=500, required=False)
    designation = serializers.SerializerMethodField(read_only=True)
    # firebase_token = serializers.SerializerMethodField()

    # def get_firebase_token(self, instance):
    #     return auth.create_custom_token(str(instance.slug))
    subscription_plans = serializers.SerializerMethodField(read_only=True)
    has_pro_subscription = serializers.SerializerMethodField(read_only=True)
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

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "uid",
            "first_name",
            "last_name",
            "email",
            "phone",
            "slug",
            "date_joined",
            "last_login",
            "country",
            "headline",
            "summary",
            "description",
            "subscription_plans",
            "has_pro_subscription",
            # "firebase_token",
            "gender",
            "objective",
            "date_of_birth",
            "hero",
            "avatar",
            "website_url",
            "blog_url",
            "facebook_url",
            "instagram_url",
            "linkedin_url",
            "twitter_url",
            "status",
            "designation",
        ]
        read_only_fields = [
            "first_name",
            "last_name",
            "phone",
            "last_login",
            "date_joined",
            "status",
        ]

    def get_subscription_plans(self, instance):
        subscription = (
            instance.get_organization()
            .subscriptionsession_set.filter()
            .values(
                "plan__name",
                "start_date",
                "next_payment_date",
                "stop_date",
                "status",
                "client_secret",
            )
        )
        return subscription

    def get_has_pro_subscription(self, instance):
        has_pro = instance.get_organization().has_pro_subscription()

        return has_pro

    def get_designation(self, instance):
        return instance.profiles.first().designation


class MeUserEmailSerializer(BaseUserSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=UserEmail.objects.get_status_active(),
                message="Email already exists!",
            )
        ]
    )

    class Meta:
        model = UserEmail
        fields = ["uid", "email", "is_primary", "status"]


class MePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50, write_only=True, required=True)
    password = serializers.CharField(
        min_length=8, max_length=50, write_only=True, required=True
    )
    confirm_password = serializers.CharField(
        min_length=8, max_length=50, write_only=True, required=True
    )

    class Meta:
        fields = ("old_password", "password", "confirm_password")

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Your old password is incorrect."))
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords must match.")
        return data

    def save(self, *args, **kwargs):
        user = self.context["request"].user
        password = self.validated_data.get("password", None)
        if user and password:
            user.set_password(password)
            user.save(update_fields=["password"])


class UserSerializer(BaseUserSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "thumbnail__256x256"),
            ("at512", "thumbnail__512x512"),
        ],
        required=False,
    )

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "uid",
            "first_name",
            "last_name",
            "name",
            "date_joined",
            "last_login",
            "avatar",
            "headline",
        ]


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=50)
    confirm_password = serializers.CharField(min_length=8, max_length=50)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        )

    def validate(self, data):
        email = data.get("email")
        if User.objects.filter(email=email).exists():
            # Should send mail to User that already exists
            raise serializers.ValidationError("An error occured. Cannot proceed.")

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords must match.")

        return data

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"].lower(),
            username=validated_data["email"],
            is_active=False,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class MeOrganizationListSerializer(BaseModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "uid",
            "name",
            "slug",
            "registration_no",
            "postal_area",
            "city",
            "country",
            "summary",
            "description",
            "status",
            "avatar",
            "kind",
            "created_at",
            "updated_at",
        ]


class MeOrganizationUserSerializer(BaseModelSerializer):
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            "uid",
            "organization",
            "role",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["__all__"]


class PrivateUserPhoneSerializer(BaseModelSerializer):
    class Meta:
        model = UserPhone
        fields = ["uid", "phone", "status", "is_primary"]

        read_only_fields = ["uid"]

    def create(self, validated_data):
        user_phone = UserPhone.objects.create(
            user=self.context["request"].user, **validated_data
        )

        otp = otp_generator()

        UserPhoneOTP.objects.create(phone=user_phone, otp=otp)

        # send OTP via SMS using Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=validated_data.get("phone"),
        )

        return user_phone


class PrivateNewsdeskPostSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024", "crop__1024x1024"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        read_only=True,
    )

    class Meta:
        model = NewsdeskPost
        fields = [
            "slug",
            "title",
            "summary",
            "description",
            "kind",
            "image",
            "status",
            "created_at",
        ]
        read_only_fields = ("__all__",)


class PrivateProductSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "slug",
            "title",
            "display_title",
            "description",
            "seo_title",
            "seo_description",
            "image",
            "status",
            "created_at",
        ]
        read_only_fields = ("__all__",)


class PrivateProjectSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024", "crop__1024x1024"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        read_only=True,
    )

    class Meta:
        model = Project
        fields = [
            "slug",
            "title",
            "summary",
            "description",
            "location",
            "image",
            "status",
        ]
        read_only_fields = ("__all__",)


class PrivateOrganizationInviteSlimSerializer(serializers.ModelSerializer):
    target = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = OrganizationInvite
        fields = [
            "target",
            "message",
            "response",
        ]
        read_only_fields = ("__all__",)


class PrivateGroupSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "description", "avatar", "slug", "kind"]


class PrivateGroupInviteSlimSerializer(serializers.ModelSerializer):
    group = PrivateGroupSlimSerializer(read_only=True)

    class Meta:
        model = Member
        fields = [
            "group",
            "role",
            "status",
            "token",
        ]
        read_only_fields = ("__all__",)


class PrivateProductDiscountSlimSerializer(serializers.ModelSerializer):
    target = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = ProductDiscount
        fields = [
            "category",
            "kind",
            "percent",
            "amount",
            "start_date",
            "stop_date",
            "target",
        ]
        read_only_fields = ("__all__",)


class PrivateFileItemSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileItem
        fields = ["fileitem", "name", "kind", "visibility", "status"]


class PrivateFileItemAccessSlimSerializer(serializers.ModelSerializer):
    fileitem = PrivateFileItemSlimSerializer(read_only=True)
    partner = PublicOrganizationSlimSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = FileItemAccess
        fields = [
            "fileitem",
            "partner",
            "user",
            "kind",
        ]
        read_only_fields = ("__all__",)


class NotificationSerializer(serializers.ModelSerializer):
    organization = PublicOrganizationSlimSerializer(read_only=True)
    related = serializers.SerializerMethodField()

    def get_related(self, object_):
        if object_.kind == NotificationKind.NEW_PRODUCT:
            if object_.product:
                product = Product.objects.filter(uid=object_.product.uid).first()
                if product:
                    return {
                        "slug": product.slug,
                        "product": PrivateProductSlimSerializer(product).data,
                    }
        elif object_.kind == NotificationKind.NEW_PROJECT:
            if object_.project:
                project = Project.objects.filter(uid=object_.project.uid).first()
                if project:
                    return {
                        "slug": project.slug,
                        "project": PrivateProjectSlimSerializer(project).data,
                    }
        elif object_.kind == NotificationKind.NEWS_POST:
            if object_.post:
                news_post = NewsdeskPost.objects.filter(uid=object_.post.uid).first()
                if news_post:
                    return {
                        "uid": news_post.uid,
                        "news_post": PrivateNewsdeskPostSlimSerializer(news_post).data,
                    }
        elif object_.kind == NotificationKind.EVENT_POST:
            if object_.post:
                event_post = NewsdeskPost.objects.filter(uid=object_.post.uid).first()
                if event_post:
                    return {
                        "uid": event_post.uid,
                        "event_post": PrivateNewsdeskPostSlimSerializer(
                            event_post
                        ).data,
                    }
        elif (
            object_.kind == NotificationKind.INVITE_REQUEST
            or object_.kind == NotificationKind.INVITE_ACCEPTED
            or object_.kind == NotificationKind.INVITE_REJECTED
        ):
            if object_.organization_invite:
                invite = OrganizationInvite.objects.filter(
                    uid=object_.organization_invite.uid
                ).first()
                if invite:
                    return {
                        "uid": invite.uid,
                        "invite": PrivateOrganizationInviteSlimSerializer(invite).data,
                    }

        elif (
            object_.kind == NotificationKind.GROUP_INVITE_REQUEST
            or object_.kind == NotificationKind.GROUP_INVITE_ACCEPTED
            or object_.kind == NotificationKind.GROUP_INVITE_REJECTED
        ):
            if object_.member:
                invite = Member.objects.filter(uid=object_.member.uid).first()
                if invite:
                    return {
                        "uid": invite.uid,
                        "invite": PrivateGroupInviteSlimSerializer(invite).data,
                    }

        elif object_.kind == NotificationKind.PRODUCT_PRICING:
            if object_.discount:
                discount = ProductDiscount.objects.filter(
                    uid=object_.discount.uid
                ).first()
                if discount:
                    return {
                        "uid": discount.uid,
                        "discount": PrivateProductDiscountSlimSerializer(discount).data,
                    }

        elif object_.kind == "FILE":
            if object_.file:
                fileitem_access = FileItemAccess.objects.filter(
                    uid=object_.file.uid
                ).first()
                if fileitem_access:
                    return {
                        "uid": fileitem_access.partner.uid,
                        "fileitem_access": PrivateFileItemAccessSlimSerializer(
                            fileitem_access
                        ).data,
                    }

        else:
            return object_

    class Meta:
        model = Notification
        fields = [
            "uid",
            "slug",
            "model_kind",
            "related",
            "organization",
            "kind",
            "message",
            "is_unread",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("__all__",)


class UserSlimSerializer(BaseUserSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "thumbnail__256x256"),
            ("at512", "thumbnail__512x512"),
        ],
        required=False,
    )
    organization = serializers.SerializerMethodField(read_only=True)

    def get_organization(self, object):
        return object.get_organization().name if object.get_organization() else None

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "uid",
            "first_name",
            "last_name",
            "name",
            "avatar",
            "headline",
            "organization",
        ]
        read_only_fields = ("__all__",)


class PrivateThreadReplySerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)
    participants = serializers.SerializerMethodField()

    def get_participants(self, object_):
        if object_.parent:
            return UserSlimSerializer(object_.parent.participants, many=True).data
        else:
            return UserSlimSerializer(object_.participants, many=True).data

    class Meta:
        model = Thread
        fields = [
            "uid",
            "content",
            "author",
            "participants",
            "created_at",
        ]

    def create(self, validated_data):
        request_user = self.context["request"].user
        parent_uid = self.context["request"].parser_context["kwargs"].get("uid")
        parent = get_object_or_404(Thread.objects.filter(), uid=parent_uid)
        thread = Thread.objects.create(
            parent=parent,
            author=request_user,
            kind=ThreadKind.CHILD,
            **validated_data,
        )
        return thread


class PrivateThreadSerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)
    user_slugs = serializers.ListField(child=serializers.CharField(), write_only=True)
    participants = UserSlimSerializer(read_only=True, many=True)
    last_message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Thread
        fields = [
            "uid",
            "title",
            "content",
            "author",
            "participants",
            "last_message",
            "user_slugs",
            "created_at",
        ]

    # Getting the last message
    def get_last_message(self, object_):
        last_message = (
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(Q(parent=object_) | Q(pk=object_.pk))
            .order_by("-created_at")
            .first()
        )
        return PrivateThreadReplySerializer(last_message).data

    def validate_participants(self, user_slugs, request_user):
        participants = []
        for slug in user_slugs:
            user = get_object_or_404(User.objects.filter(), slug=slug)
            if (
                user.profiles.filter(
                    organization__in=request_user.get_organization()
                    .get_descendants()
                    .values_list("id", flat=True)
                ).exists()
                or request_user.get_organization() == user.get_organization()
            ):
                participants.append(user)
        participants.append(request_user)
        return participants

    def create(self, validated_data):
        user_slugs = validated_data.pop("user_slugs", [])
        request_user = self.context["request"].user

        participants = self.validate_participants(user_slugs, request_user)

        if len(participants) == 1:
            raise APIException(detail="You can't open a conversation")

        if len(participants) == 2:
            threads = Inbox.objects.filter(user=participants[0]).values_list(
                "thread", flat=True
            )
            inbox = Inbox.objects.filter(
                user=participants[1], thread__in=threads
            ).first()

            if inbox:
                thread = Thread.objects.create(
                    parent=inbox.thread,
                    author=participants[1],
                    kind=ThreadKind.CHILD,
                    **validated_data,
                )
                return thread

        thread = Thread.objects.create(
            author=request_user,
            kind=ThreadKind.PARENT,
            **validated_data,
        )
        thread.participants.set(participants)

        Inbox.objects.filter(user__in=participants).update(kind=InboxKind.PRIVATE)
        return thread
