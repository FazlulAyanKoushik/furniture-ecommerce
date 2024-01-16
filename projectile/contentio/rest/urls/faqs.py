from django.urls import path

from ..views import faqs

urlpatterns = [
    path(r"/<slug:slug>", faqs.GlobalFAQDetail.as_view(), name="global.faq-detail"),
    path(r"", faqs.GlobalFAQList.as_view(), name="global.faq-list"),
]
