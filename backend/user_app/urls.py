from django.urls import path
from .views import (
    Info,
    LogIn,
    LogOut,
    SignUp,
    Location,
    UserSwipeView,
    UserMatchResetView,
    PasswordResetView,
    VerifyEmail,
)


urlpatterns = [
    path("", Info.as_view()),
    path("signup/", SignUp.as_view()),
    path("login/", LogIn.as_view()),
    path("logout/", LogOut.as_view()),
    path("location/", Location.as_view()),
    path("swipe/", UserSwipeView.as_view()),
    path("reset/", UserMatchResetView.as_view()),
    path("verify/<uidb64>/<token>/", VerifyEmail.as_view(), name="verify-email"),
        path("password/", PasswordResetView.as_view()),
]