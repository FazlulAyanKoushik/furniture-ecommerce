from rest_framework import serializers

from ...models import Service, OrganizationServiceConnector



class GlobalPresetServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "uid",
            "title",
            "slug",
            "description",
            "status",
            "kind",            
        ]
        read_only_fields = ("__all__",)