from rest_framework import serializers

from paymentio.models import SubscriptionSession, SubscriptionTransaction


class SubscriptionSessionSlimSerializer(serializers.ModelSerializer):
    plan = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionSession
        fields = ["organization", "plan", "start_date", "next_payment_date"]
        read_only_fields = ["__all__"]

    def get_plan(self, instance):
        plan_name = instance.plan.name if instance.plan else None
        return plan_name

    def get_organization(self, instance):
        organization_name = (
            instance.organization.name if instance.organization else None
        )
        return organization_name


class SubscriptionTransactionListSerializer(serializers.ModelSerializer):
    session = SubscriptionSessionSlimSerializer(read_only=True)

    class Meta:
        model = SubscriptionTransaction
        fields = [
            "uid",
            "session",
            "status",
        ]
        read_only_fields = ["__all__"]


class SubscriptionTransactionDetailSerializer(serializers.ModelSerializer):
    session = SubscriptionSessionSlimSerializer(read_only=True)

    class Meta:
        model = SubscriptionTransaction
        fields = [
            "session",
            "status",
            "response_payload",
        ]
        read_only_fields = ["__all__"]
