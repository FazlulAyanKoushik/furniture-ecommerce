from django.urls import path

from ..views.verify import (
    UserEmailTokenConsume,
    UserPhoneVerifyOtp

)

urlpatterns = [
    path(
        r"/associated-emails/<slug:token>",
        UserEmailTokenConsume.as_view(),
        name="user-email-token-consume",
    ),
    path(r"/phone/verify", UserPhoneVerifyOtp.as_view(), name="userphone-verify-otp")
]
