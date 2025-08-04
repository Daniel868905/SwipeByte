from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    #add creds later here

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['first_name', 'last_name']