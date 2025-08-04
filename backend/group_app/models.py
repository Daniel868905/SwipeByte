from django.db import models
from user_app.models import User


# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=255, blank=True)
    members = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group')
    