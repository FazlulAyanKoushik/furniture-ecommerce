import logging

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from accountio.emails import send_organization_onboarding_email

from core.models import User
from core.choices import UserStatus

from ...models import Organization

logger = logging.getLogger(__name__)


class PublicOrganizationUserOnboardingSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=50)
    phone = serializers.CharField(min_length=7, max_length=20)
    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=50)
    organization_name = serializers.CharField(min_length=2, max_length=50)
    organization_no = serializers.CharField(min_length=2, max_length=50)
    country = serializers.CharField(min_length=2, max_length=2)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "phone",
            "first_name",
            "last_name",
            "organization_name",
            "organization_no",
        )
        read_only_fields = ("__all__",)

    def validate_email(self, data):
        email = data.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with email already exists!")
        return data

    def validate_phone(self, data):
        phone = data
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("User with phone already exists!")
        return data

    def create(self, validated_data, *args, **kwargs):
        email = validated_data["email"].lower()
        password = validated_data["password"]
        phone = validated_data["phone"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        organization_name = validated_data["organization_name"]
        organization_no = validated_data["organization_no"]
        country = validated_data["country"]

        # get and removing tag uid list
        if Organization.objects.filter(
            registration_no=organization_no, country=country
        ).exists():
            logger.warn("Will not save due to same organization already exists!")
            logger.info(validated_data)
            raise serializers.ValidationError(
                {"organization_no": ["Organization already exists! Contact support."]}
            )

        user = User.objects.create(
            email=email,
            username=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            status=UserStatus.ACTIVE,
        )
        user.set_password(password)
        user.save()
        user.activate()
        logger.debug(f"Created new user: {user}")

        organization = Organization.objects.create(
            name=organization_name, registration_no=organization_no, country=country
        )

        # creating tag connector with tag uid(s) provided by the user and
        # organization which is created

        logger.debug(f"Created new organization: {organization}")
        request = self.context["request"]

        organization_user = organization.add_owner(user)

        organization_user.save()

        send_organization_onboarding_email(organization_user, domain=request.get_host())

        logger.debug(f"Created new organization user: {organization_user}")

        return organization_user
