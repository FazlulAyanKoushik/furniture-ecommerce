from django.urls import path

from ..views.subscription_plan import (
    PublicSubscriptionPlanDetail,
    PublicSubscriptionPlanList,
)

urlpatterns = [
    path(
        "/<slug:slug>",
        PublicSubscriptionPlanDetail.as_view(),
        name="public-subscription-plan-detail",
    ),
    path(
        "", PublicSubscriptionPlanList.as_view(), name="public-subscription-plan-list"
    ),
]
