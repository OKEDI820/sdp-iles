from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CurrentUserView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("me/", CurrentUserView.as_view({"get": "list"}), name="auth-me"),
    path(
        "change-password/",
        CurrentUserView.as_view({"post": "change_password"}),
        name="auth-change-password",
    ),
]
