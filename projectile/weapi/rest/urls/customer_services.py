from django.urls import path

from ..views.customer_services import (
    PrivateCustomerServiceList,
    PrivateCustomerServiceDetail,
)

urlpatterns = [
    path(
        r"/<uuid:uid>",
        PrivateCustomerServiceDetail.as_view(),
        name="we.customer-service-detail",
    ),
    path(r"", PrivateCustomerServiceList.as_view(), name="we.customer-service-list"),
]
