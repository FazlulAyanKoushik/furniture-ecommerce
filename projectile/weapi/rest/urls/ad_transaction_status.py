from django.urls import path

from weapi.rest.views.ad_transaction_status import AdTransactionStatusWebhook


urlpatterns = [
    path(
        r"/transactions",
        AdTransactionStatusWebhook.as_view(),
        name="we.single-transaction-status",
    ),
]
