from django.db import models
from user_app.models import User


# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=255, blank=True)
    members = models.ManyToManyField(User, related_name='group')
    
class GroupSwipe(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='swipes')
    restaurant = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_swipes', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_swipes', blank=True)

    def record_vote(self, user, liked=True):
        if liked:
            self.liked_by.add(user)
            self.disliked_by.remove(user)
        else:
            self.disliked_by.add(user)
            self.liked_by.remove(user)

    def has_match(self):
        total = self.group.members.count()
        return total > 0 and self.liked_by.count() >= total