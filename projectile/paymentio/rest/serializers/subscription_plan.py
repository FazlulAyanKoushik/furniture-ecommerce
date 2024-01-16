from rest_framework import serializers

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from paymentio.models import (
    SubscriptionPlan,
    SubscriptionSession,
)


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionPlan
        fields = [
            "uid",
            "slug",
            "name",
            "description",
            "features",
            "price",
            "currency",
            "status",
        ]
        read_only_fields = ["__all__"]

    def get_features(self, obj):
        feature_names = obj.subscriptionplanfeatureconnector_set.filter().values_list(
            "feature__name", flat=True
        )
        return list(feature_names)


class SubscriptionSessionSerializer(serializers.ModelSerializer):
    organization = PublicOrganizationSlimSerializer(read_only=True)
    plan = serializers.SlugRelatedField(
        slug_field="uid", queryset=SubscriptionPlan.objects.all()
    )

    class Meta:
        model = SubscriptionSession
        fields = [
            "uid",
            "plan",
            "organization",
            "client_secret",
            "start_date",
            "stop_date",
            "next_payment_date",
            "status",
        ]
        read_only_fields = [
            "uid",
            "client_secret",
            "start_date",
            "stop_date",
            "next_payment_date",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        organization = user.get_organization()
        return SubscriptionSession.objects.create(
            organization=organization, **validated_data
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        plan = instance.plan
        # Add plan details to the representation
        representation["plan"] = {
            "name": plan.name,
            "description": plan.description,
            "features": plan.subscriptionplanfeatureconnector_set.filter().values_list(
                "feature__name", flat=True
            ),
            "price": plan.price,
            "currency": plan.currency,
            "status": plan.status,
        }
        return representation
