"""URL routing for favorite_app."""

from django.urls import path

from .views import FavoriteListCreateView, FavoriteDetailView


urlpatterns = [
    path('', FavoriteListCreateView.as_view(), name='favorite-list'),
    path('<int:pk>/', FavoriteDetailView.as_view(), name='favorite-detail'),
]
