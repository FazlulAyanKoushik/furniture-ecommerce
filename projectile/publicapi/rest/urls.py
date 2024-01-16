from django.urls import path, include

from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_confirm,
    reset_password_validate_token,
)

from .emails import EmailContactAPIView

urlpatterns = [
    path(
        r"/email-contact-form",
        EmailContactAPIView.as_view(),
        name="public.email-contact-form",
    ),
    path(r"/password-reset", reset_password_request_token, name="password-reset"),
    path(
        r"/password-reset-confirm",
        reset_password_confirm,
        name="password-reset-confirm",
    ),
    path(
        r"/password-reset-validate-token",
        reset_password_validate_token,
        name="password-reset-validate-token",
    ),
]
