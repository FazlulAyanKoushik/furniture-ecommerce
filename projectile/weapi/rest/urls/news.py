from django.urls import path

from ..views import news

urlpatterns = [
    path(
        r"/<uuid:uid>/images",
        news.PrivatePostImageList.as_view(),
        name="we.news_image-list",
    ),
    path(
        r"/<uuid:uid>/images/<uuid:newsimage_uid>",
        news.PrivatePostImageDetail.as_view(),
        name="we.news_image-detail",
    ),
    path(
        r"/<uuid:uid>/files/<uuid:newspost_uid>",
        news.PrivateNewsPostFileDetail.as_view(),
        name="we.newspost_file-detail",
    ),
    path(
        r"/<uuid:uid>/files",
        news.PrivateNewsPostFileList.as_view(),
        name="we.newspost_file-list",
    ),
    path(r"/<uuid:uid>", news.PrivateNewsDetail.as_view(), name="we.news-detail"),
    path(r"", news.PrivateNewsList.as_view(), name="we.news-list"),
]
