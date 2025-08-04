from rest_framework import serializers
from .models import Favorite
from user_app.models import User

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']  # Add 'username' if needed

class FavoriteSerializer(serializers.ModelSerializer):
    user_favorites = UserSummarySerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user_favorites', 'restaurant', 'review']
