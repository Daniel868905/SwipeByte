"""Database models for the restaurant app.

This module defines the ``Restaurant`` model which stores basic
information about a restaurant returned from the Google Places API. In
the original implementation the geographic location was persisted using
GeoDjango's ``PointField`` which required a spatial database. The test
environment used for this kata does not provide the spatial database
dependencies, causing migrations to fail with an
``AttributeError: 'DatabaseOperations' object has no attribute 'geo_db_type'``.

To keep the application lightweight and remove the dependency on
GeoDjango we instead store the latitude and longitude as a simple
character field. This is sufficient for the project's needs and allows
the Django ORM to operate with the standard SQLite backend.
"""
from django.db import models

class Restaurant(models.Model):
    """Represents a restaurant returned from an external API."""

    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # Store ``lat,lon`` string to avoid GeoDjango dependency
    location = models.CharField(max_length=100)
    rating = models.FloatField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.name