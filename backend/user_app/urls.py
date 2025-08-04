from django.urls import path
from .views import Info


urlpatterns = [
    path("", Info.as_view()),
]