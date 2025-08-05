from rest_framework import serializers
from .models import Group
from favorite_app.serializers import FavoriteSerializer
from user_app.serializers import UserSerializer  # from before

class GroupDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    favorites = FavoriteSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'members', 'favorites']
