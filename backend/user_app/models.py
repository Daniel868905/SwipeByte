from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['first_name', 'last_name']


class UserSwipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swipes')
    restaurant = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    liked = models.BooleanField(default=True)

    def record_vote(self, liked=True):
        self.liked = liked
        self.save()

    def has_match(self):
        return self.liked