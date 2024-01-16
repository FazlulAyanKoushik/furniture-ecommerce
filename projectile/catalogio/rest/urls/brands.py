from django.urls import path

from ..views import brands


urlpatterns = [
    path(r"", brands.GlobalBrandList.as_view(), name="brands.brand-list"),
]
