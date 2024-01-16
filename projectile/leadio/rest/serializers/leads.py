from rest_framework import serializers

from ...models import PotentialLead


class GlobalPotentialLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotentialLead
        fields = (
            "uid",
            "name",
            "organization_no",
            "email",
            "phone",
            "address",
            "postal_code",
            "postal_area",
            "created_at",
            "updated_at",
        )
