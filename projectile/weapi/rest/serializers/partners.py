import logging

from random import randrange

import pandas as pd
import numpy as np

from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from common.serializers import BaseModelSerializer

from accountio.choices import OrganizationUserRole, OrganizationUserStatus
from accountio.emails import send_organization_user_invite
from accountio.models import Descendant, Organization, OrganizationUser
from accountio.rest.serializers.organization_users import PublicUserSerializer

from catalogio.choices import (
    ProductDiscountKind,
    ProductDiscountStatus,
    ProductDiscountVariant,
)
from catalogio.models import ProductDiscount

from fileroomio.models import FileItem

from invitio.helpers.emails import send_connect_email
from invitio.models import OrganizationInvite
from ..serializers.organizations import PrivateOrganizationSlimSerializer

User = get_user_model()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PrivateOrganizationPartnerSerializer(BaseModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    registration_number = serializers.CharField(required=False, write_only=True)
    message = serializers.CharField(max_length=1000, required=False, write_only=True)
    country = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

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
            "uid",
            "name",
            "slug",
            "registration_number",
            "postal_area",
            "city",
            "country",
            "summary",
            "description",
            "avatar",
            "hero",
            "logo_wide",
            "website_url",
            "image",
            "status",
            "kind",
            "email",
            "phone",
            "message",
        ]
        read_only_fields = ["uid"]

    def create(self, validated_data):
        request = self.context["request"]
        organization = request.user.get_organization()
        email = validated_data.get("email").lower()
        message = validated_data.pop("message", "")

        registration_no = validated_data.pop(
            "registration_number", f"1111-{randrange(100000, 999999)}"
        )
        validated_data.update({"registration_no": registration_no})

        # Check if Organization instance already exists with given email
        target = (
            Organization.objects.filter(email=email).order_by("-updated_at").first()
        )

        if target is None:
            target = Organization.objects.create(**validated_data)

        # Create OrganizationInvite
        try:
            invite = OrganizationInvite.objects.get_or_create(
                target=target,
                sender=request.user,
                organization=organization,
                message=message,
            )
        except IntegrityError:
            logger.exception("Invitation already exists!")
            invite = OrganizationInvite.objects.get_or_create(
                target=target,
                organization=organization,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email, username=email)

        # Create OrganizationUser
        try:
            profile = OrganizationUser.objects.create(
                user=user,
                organization=target,
                role=OrganizationUserRole.OWNER,
                status=OrganizationUserStatus.PENDING,
                referrer=request.user.get_organization_user(),
            )
        except IntegrityError:
            logger.exception("OrganizationUser already exists!")
            profile = OrganizationUser.objects.filter(
                user=user, organization=target
            ).first()
            pass

        if profile and profile.status == OrganizationUserStatus.PENDING:
            send_organization_user_invite(
                profile=profile, domain=request.get_host(), message=message
            )
        else:
            if invite:
                send_connect_email(invite)

        return target

    def get_name(self, instance):
        return instance.display_name or instance.name


class PrivateOrganizationPartnerDiscountSerializer(BaseModelSerializer):
    category = serializers.CharField(max_length=50)
    percent = serializers.DecimalField(max_digits=19, decimal_places=3, required=False)
    kind = serializers.ChoiceField(ProductDiscountKind.choices)
    variant = serializers.ChoiceField(ProductDiscountVariant.choices)
    status = serializers.ChoiceField(ProductDiscountStatus.choices)
    amount = serializers.DecimalField(max_digits=19, decimal_places=3, required=False)
    start_date = serializers.DateField()
    stop_date = serializers.DateField(required=False, allow_null=True)
    partner_uids = serializers.ListField(child=serializers.CharField(), write_only=True)
    target = PrivateOrganizationSlimSerializer(read_only=True)
    organization = PrivateOrganizationSlimSerializer(read_only=True)
    # FKs
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = ProductDiscount
        fields = [
            "uid",
            "category",
            "kind",
            "percent",
            "variant",
            "amount",
            "currency",
            "status",
            "start_date",
            "stop_date",
            "partner_uids",
            "target",
            "organization",
            "user",
        ]
        read_only_fields = [
            "uid",
            "user",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        organization = request.user.get_organization()
        # Get uid for target organization
        target_uids = validated_data.pop("partner_uids")
        targets = Organization.objects.get_status_fair().filter(uid__in=target_uids)

        user = request.user
        validated_data["user"] = user
        category = validated_data.pop("category")
        for target in targets:
            discount, _ = ProductDiscount.objects.get_or_create(
                organization=organization,
                target=target,
                category=category,
                defaults=validated_data,
            )
        validated_data["category"] = category

        return validated_data


class PrivateOrganizationPartnerFileItemSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "uid",
            "fileitem",
            "name",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
            "organization_slug",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "uid",
            "size",
            "dotextension",
            "organization_slug",
            "created_at",
            "updated_at",
        ]


class PrivateBulkCreatePartnersSerializers(BaseModelSerializer):
    partner_list = serializers.FileField(write_only=True)

    class Meta:
        model = Organization
        fields = ["partner_list"]

    def create(self, validated_data):
        file = validated_data.pop("partner_list", None)
        if file:
            try:
                # Converting excel file to pandas dataframe (df)
                df = pd.read_excel(file)
                # Replace empty values with 0 so that we can change the value when creating DB instances
                df = df.replace(np.nan, 0, regex=True)

                existing_emails = Organization.objects.values_list("email", flat=True)
                existing_organization_emails = []

                for _, row in df.iterrows():
                    if row["organization_email"] in existing_emails:
                        existing_organization_emails.append(row["organization_email"])
                        continue

                    username = (
                        row["username"]
                        if row["username"]
                        else str(row["user_email"]).split("@")[0]
                    )

                    # Creating user according to Excel file information
                    if User.objects.filter(email=row["user_email"]).exists():
                        continue
                    else:
                        user = User.objects.create(
                            username=username,
                            email=row["user_email"],
                            first_name=row["first_name"],
                            last_name=row["last_name"],
                            is_active=True,
                            status=row["status"],
                        )
                        user.set_password(row["password"])
                        user.save()
                        user.activate()
                        logger.debug(f"Created new user: {user}")

                    # Creating organization according to Excel file information
                    organization = Organization.objects.create(
                        name=row["name"],
                        display_name=row["display_name"]
                        if row["display_name"]
                        else row["name"],
                        email=row["organization_email"],
                        country=row["country"],
                        registration_no=row["registration_no"]
                        if row["registration_no"] != 0
                        else f"1111-{randrange(100000, 999999)}",
                        status=row["organization_status"],
                    )
                    logger.debug(f"Created new organization: {organization}")

                    # Set user as the organization owner
                    organization_user = organization.add_owner(user)
                    logger.debug(f"Created new organization user: {organization_user}")

                    # Creating descendants
                    Descendant.objects.create(
                        parent=self.context["request"].user.get_organization(),
                        child=organization,
                    )
                    Descendant.objects.create(
                        child=self.context["request"].user.get_organization(),
                        parent=organization,
                    )

                if existing_organization_emails:
                    logging.warning("These organization are already exist:")

            except IntegrityError as _:
                logging.info("Can not create new instaces. User already exists.")

        return validated_data


class PrivatePartnerDiscountListSerializer(BaseModelSerializer):
    target = PrivateOrganizationSlimSerializer(read_only=True)
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = ProductDiscount
        fields = [
            "uid",
            "category",
            "kind",
            "percent",
            "variant",
            "amount",
            "currency",
            "status",
            "start_date",
            "stop_date",
            "user",
            "target",
        ]
        read_only_fields = ["__all__"]
