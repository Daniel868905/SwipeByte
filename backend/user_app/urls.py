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

)


urlpatterns = [
    path("", Info.as_view()),
    path("signup/", SignUp.as_view()),
    path("login/", LogIn.as_view()),
    path("logout/", LogOut.as_view()),
    path("location/", Location.as_view()),
    path("swipe/", UserSwipeView.as_view()),
    path("reset/", UserMatchResetView.as_view()),
    path("password/", PasswordResetView.as_view()),
]