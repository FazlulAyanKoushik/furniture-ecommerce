from django.urls import path

from ..views import login


urlpatterns = [
    path(
        r"",
        login.PrivateSalesLogin.as_view(),
        name="admin.sales-login",
    ),
]
