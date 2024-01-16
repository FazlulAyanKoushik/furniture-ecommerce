from rest_framework import generics

from accountio.rest.permissions import IsOrganizationStaff

from paymentio.models import SubscriptionTransaction
from paymentio.rest.serializers.subscription_transaction import (
    SubscriptionTransactionListSerializer,
    SubscriptionTransactionDetailSerializer,
)


class SubscriptionTransactionList(generics.ListAPIView):
    queryset = SubscriptionTransaction.objects.filter()
    serializer_class = SubscriptionTransactionListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(session__organization=organization)


class SubscriptionTransactionDetail(generics.RetrieveAPIView):
    queryset = SubscriptionTransaction.objects.filter()
    serializer_class = SubscriptionTransactionDetailSerializer
    permission_classes = [IsOrganizationStaff]
    lookup_field = "uid"
