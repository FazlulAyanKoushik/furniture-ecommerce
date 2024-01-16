from django.urls import path

from ..views.onboarding import GlobalUserRegistration, GlobalUserActivation

urlpatterns = [
    path(r"/register", GlobalUserRegistration.as_view(), name="user-registration"),
    path(r"/activate", GlobalUserActivation.as_view(), name="user-activation"),
]
