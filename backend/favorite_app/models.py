from django.db import models
from group_app.models import Group
from user_app.models import User

class Favorite(models.Model):
    user_favorites = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    group_favorites = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    restaurant = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, default='')
    review = models.TextField(max_length=1000, blank=True, default='')
    visited = models.BooleanField(default=False)