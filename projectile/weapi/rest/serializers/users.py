import logging

from django.contrib.auth import get_user_model

from rest_framework import serializers

from accountio.emails import (
    send_organization_user_invite,
    send_added_user_set_password_mail,
)
from accountio.models import OrganizationUser
from accountio.rest.serializers.organization_users import UserPrivateSerializer

from common.serializers import BaseModelSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


class PrivateOrganizationUserSerializer(BaseModelSerializer):
    user = UserPrivateSerializer(read_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(max_length=40, write_only=True)
    last_name = serializers.CharField(max_length=40, write_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            "uid",
            "user",
            "email",
            "first_name",
            "last_name",
            "role",
            "status",
            "reminded_at",
            "designation",
        ]

    def create(self, validated_data):
        """On creating new Organization User"""

        email = validated_data.pop("email").lower()
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        user_exists = False
        try:
            user = User.objects.get(email=email)
            user_exists = True
        except User.DoesNotExist:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,
            )
            user.save_dirty_fields()

        request = self.context["request"]
        referrer = request.user.get_organization_user()
        organization_user = OrganizationUser.objects.create(
            organization=request.user.get_organization(),
            user=user,
            referrer=referrer,
            is_default=not user_exists,
            **validated_data,
        )
        # send_organization_user_invite(organization_user, domain=request.get_host())

        # Send email to user
        send_added_user_set_password_mail(organization_user, domain=request.get_host())
        return organization_user


class PrivateOrganizationUserSetDefaultSerializer(BaseModelSerializer):
    class Meta:
        model = OrganizationUser
        fields = [
            "role",
            "status",
            "is_default",
        ]


class  PrivateOrganizationUserSetPasswordSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["password", "confirm_password"]
