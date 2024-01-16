from django.urls import path

from weapi.rest.views.subscription_transaction import (
    SubscriptionTransactionList,
    SubscriptionTransactionDetail,
)
from weapi.rest.views.transaction_status import TransactionStatusWebhook

urlpatterns = [
    path(
        r"/status",
        TransactionStatusWebhook.as_view(),
        name="transaction-status-webhook",
    ),
    path(
        r"/<uuid:uid>",
        SubscriptionTransactionDetail.as_view(),
        name="we.subscription-transaction-detail",
    ),
    path(
        r"",
        SubscriptionTransactionList.as_view(),
        name="we.subscription-transaction-list",
    ),
]
