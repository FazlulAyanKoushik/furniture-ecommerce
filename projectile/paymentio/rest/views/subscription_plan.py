from rest_framework import generics

from accountio.rest.permissions import IsSameUser

from paymentio.models import SubscriptionPlan
from ..serializers.subscription_plan import SubscriptionPlanSerializer


class PublicSubscriptionPlanList(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.get_status_active()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsSameUser]


class PublicSubscriptionPlanDetail(generics.RetrieveAPIView):
    queryset = SubscriptionPlan.objects.get_status_active()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsSameUser]
    lookup_field = "slug"
