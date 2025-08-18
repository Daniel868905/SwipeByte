from django.urls import path
from .views import set_location_from_address

urlpatterns = [
    path("location-from-address/", set_location_from_address, name="location-from-address"),
]
