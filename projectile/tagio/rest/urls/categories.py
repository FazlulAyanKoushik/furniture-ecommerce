from django.urls import path

from ..views.categories import CategoryList


urlpatterns = [
    path(
        r"",
        CategoryList.as_view(),
        name="tagio.category-list",
    ),
]
