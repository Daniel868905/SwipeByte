"""Database models for the restaurant app.

This module defines the ``Restaurant`` model which stores basic
information about a restaurant returned from the Google Places API. The
model uses GeoDjango's ``PointField`` to persist the geographic
location, enabling efficient geospatial queries.
"""

from django.contrib.gis.db import models


class Restaurant(models.Model):
    """Represents a restaurant returned from an external API."""

    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    location = models.PointField()
    rating = models.FloatField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return self.name