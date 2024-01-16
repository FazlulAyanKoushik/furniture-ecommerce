from django.db.models import Q

from accountio.models import Descendant

from accountio.rest.serializers import organizations, organization_users

from common.serializers import BaseModelSerializer

from invitio.choices import OrganizationInviteResponse
from invitio.models import OrganizationInvite


class PrivatePartnerOutgoingInviteSerializer(BaseModelSerializer):
    organization = organizations.PublicOrganizationSlimSerializer(source="target")
    sender = organization_users.PublicUserSerializer(read_only=True)

    class Meta:
        model = OrganizationInvite
        fields = ["uid", "organization", "response", "message", "sender", "token"]
        read_only_fields = ["__all__"]


class PrivatePartnerIncomingInviteSerializer(BaseModelSerializer):
    organization = organizations.PublicOrganizationSlimSerializer()
    sender = organization_users.PublicUserSerializer(read_only=True)

    class Meta:
        model = OrganizationInvite
        fields = ["uid", "organization", "response", "message", "sender", "token"]
        read_only_fields = ["__all__"]


class PrivateInviteResponseSerializer(BaseModelSerializer):
    organization = organizations.PublicOrganizationSlimSerializer(read_only=True)
    sender = organization_users.PublicUserSerializer(read_only=True)

    class Meta:
        model = OrganizationInvite
        fields = ["uid", "organization", "sender", "response"]
        read_only_fields = ["organization", "sender"]
        write_only_fields = ["response"]

    def update(self, instance, validated_data):
        organization = instance.organization
        target = instance.target

        invites = OrganizationInvite.objects.filter(
            Q(organization=organization, target=target)
            | Q(organization=target, target=organization)
        ).filter(response=OrganizationInviteResponse.PENDING)

        if validated_data["response"] == OrganizationInviteResponse.ACCEPTED:
            # Creating partner instance at "Descendant" for parent and child both
            Descendant.objects.create(
                parent=instance.organization, child=instance.target
            )
            Descendant.objects.create(
                parent=instance.target, child=instance.organization
            )

        # If the invite is accepted or rejected, update all pending invites
        invites.update(response=validated_data["response"])

        validated_data["responder"] = self.context["request"].user
        return super().update(instance, validated_data)
