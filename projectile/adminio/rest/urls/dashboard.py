from django.urls import path

from ..views import dashboard


urlpatterns = [
    path(
        r"/organizations",
        dashboard.PrivateSalesDashboard.as_view(),
        name="admin.organization-sales-dashboard",
    ),
    path(
        r"/products",
        dashboard.PrivateProductSalesDashboard.as_view(),
        name="admin.product-sales-dashboard",
    ),
]
