from django.urls import path
from .views import set_location_from_address, geocode_proxy

urlpatterns = [
    path('location-from-address/', set_location_from_address),
    path('geocode-proxy/', geocode_proxy),  # <-- the new one for your shim
]
