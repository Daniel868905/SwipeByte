from django.urls import path
from .views import restaurant_photo,  restaurant_search, RestaurantSearchView

urlpatterns = [
    path('restaurants/photo/', restaurant_photo, name='restaurant-photo'),
    path('', restaurant_search, name='restaurant-search')
]