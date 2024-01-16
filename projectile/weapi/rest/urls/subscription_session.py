from django.urls import path
from weapi.rest.views.subscription_session import (
    # PrivateSubscriptionSessionDetail,
    PrivateSubscriptionSessionList,
    PrivateOrganizationProSubscriptionDetail,
)

urlpatterns = [
    # path(
    #     r"/<uuid:uid>",
    #     PrivateSubscriptionSessionDetail.as_view(),
    #     name="we.subscription-session-detail",
    # ),
    path(
        r"/<slug:organization_slug>",
        PrivateOrganizationProSubscriptionDetail.as_view(),
        name="has-pro-subscription-check",
    ),
    path(
        r"",
        PrivateSubscriptionSessionList.as_view(),
        name="we.subscription-session-list",
    ),
]
