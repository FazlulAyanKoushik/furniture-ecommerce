from rest_framework import serializers

from catalogio.models import Service, OrganizationServiceConnector


class PrivateServiceSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["uid", "slug"]

    def create(self, validated_data):
        title = validated_data.pop("title", None)
        service, _ = Service.objects.get_or_create(
            title=title,
            defaults=validated_data,
        )
        connector, _ = OrganizationServiceConnector.objects.get_or_create(
            organization=self.context["request"].user.get_organization(),
            service=service,
        )
        return service
