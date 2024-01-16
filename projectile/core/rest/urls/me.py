from django.urls import path


from ..views.me import (
    PrivateMeDetail,
    PrivateMeStatus,
    PrivateMeUserEmailList,
    PrivateMeUserEmailDetail,
    PrivateMePassword,
    PrivateMeOrganizationUserList,
    PrivateMeOrganizationUserSelect,
    PrivateUserPhoneDetail,
    PrivateUserPhoneList,
    PrivateUserPhoneResendOtp,
    PrivateNotificationList,
    PrivateNotificationDetail,
    PrivateThreadList,
    PrivateThreadReplyList,
)

urlpatterns = [
    path(r"", PrivateMeDetail.as_view(), name="me-detail"),
    path(r"/password", PrivateMePassword.as_view(), name="me-password"),
    path(r"/status", PrivateMeStatus.as_view(), name="me-status"),
    # UserEmail
    path(r"/emails", PrivateMeUserEmailList.as_view(), name="me-email-list"),
    path(
        r"/emails/<uuid:uid>",
        PrivateMeUserEmailDetail.as_view(),
        name="me-email-detail",
    ),
    path(
        r"/organizations",
        PrivateMeOrganizationUserList.as_view(),
        name="me-organization-list",
    ),
    path(
        r"/organizations/<uuid:uid>/select",
        PrivateMeOrganizationUserSelect.as_view(),
        name="me-organization-set_default",
    ),
    path(
        r"/phone/<uuid:uid>",
        PrivateUserPhoneDetail.as_view(),
        name="me-phone-detail",
    ),
    path(
        r"/phone",
        PrivateUserPhoneList.as_view(),
        name="me-phone-list",
    ),
    path(
        r"/notifications/<uuid:uid>",
        PrivateNotificationDetail.as_view(),
        name="notification-detail",
    ),
    path(
        r"/notifications", PrivateNotificationList.as_view(), name="notification-list"
    ),
    path(
        r"/inbox/<uuid:uid>", PrivateThreadReplyList.as_view(), name="thread-reply-list"
    ),
    path(r"/inbox", PrivateThreadList.as_view(), name="thread-list"),
    path(
        r"/phone/<uuid:uid>/resend-otp",
        PrivateUserPhoneResendOtp.as_view(),
        name="userphone-resend-otp",
    ),
]
