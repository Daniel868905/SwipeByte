from django.urls import path
from .views import Info, LogIn, LogOut, SignUp, Location


urlpatterns = [
    path("", Info.as_view()),
    path("signup/", SignUp.as_view()),
    path("login/", LogIn.as_view()),
    path("logout/", LogOut.as_view()),
    path("location/", Location.as_view()),

]