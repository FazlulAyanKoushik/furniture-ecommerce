from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import generics, serializers

from common.serializers import BaseModelSerializer

from invitio.models import OrganizationInvite

from notificationio.choices import NotificationKind
from notificationio.helpers import NotificationHelper
from notificationio.utils import create_notification

from ...models import Organization


class PublicPartnerInviteSerializer(BaseModelSerializer):
    class Meta:
        model = OrganizationInvite
        fields = ["message"]

    def create(self, validated_data):
        kwargs = {"slug": self.context["slug"]}
        target = get_object_or_404(Organization.objects.filter(), **kwargs)
        request = self.context["request"]

        try:
            return OrganizationInvite.objects.create(
                target=target,
                organization=request.user.get_organization(),
                sender=request.user,
                **validated_data,
            )
        except IntegrityError as e:
            organization = request.user.get_organization()
            kwargs = {"organization": organization, "target": target}
            message = f"You have a pending invitation from {request.user.get_organization().name}"
            organization_invite = generics.get_object_or_404(
                OrganizationInvite.objects.filter(), **kwargs
            )
            create_notification(
                organization,
                organization_invite,
                [target],
                message,
                NotificationKind.INVITE_REQUEST,
            )
            raise serializers.ValidationError(
                {"non_field_errors": "Invite already exists!"}
            )
