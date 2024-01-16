from django.urls import path

from .views import ScrapedProductList

urlpatterns = [
    path(r"", ScrapedProductList.as_view(), name="scrapio.scraped_product_list"),
]
