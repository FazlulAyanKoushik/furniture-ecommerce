from django.urls import path

from ..views import tags

urlpatterns = [
    path("/<uuid:uid>", tags.PrivateTagDetail.as_view(), name="we.tag-detail"),
    path("", tags.PrivateTagList.as_view(), name="we.tags-list"),
]
