from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import ProfileUpdateView, RegisterView

app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "profile/",
        ProfileUpdateView.as_view(),
        name="profile",
    ),
]
