from django.urls import path
from .views import GroupWithFavoritesView

urlpatterns = [
    path('', GroupWithFavoritesView.as_view()),
    
]