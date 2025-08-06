from rest_framework import serializers
from .models import Favorite
from user_app.models import User
import os
import requests
from group_app.models import Group

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class GroupSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name']

class FavoriteSerializer(serializers.ModelSerializer):
    user_favorites = UserSummarySerializer(read_only=True)
    group_favorites = GroupSummarySerializer(read_only=True)
    yelp_review = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = [
            'id',
            'user_favorites',
            'group_favorites',
            'restaurant',
            'location',
            'review',
            'yelp_review',
        ]

    def get_yelp_review(self, obj):
        api_key = os.environ.get('YELP_API_KEY')
        if not api_key or not obj.restaurant:
            return None
        headers = {'Authorization': f'Bearer {api_key}'}
        try:
            params = {'term': obj.restaurant, 'location': obj.location or 'US', 'limit': 1}
            resp = requests.get(
                'https://api.yelp.com/v3/businesses/search',
                headers=headers,
                params=params,
                timeout=5,
            )
            business = resp.json().get('businesses', [{}])
            if not business:
                return None
            business_id = business[0].get('id')
            if not business_id:
                return None
            review_resp = requests.get(
                f'https://api.yelp.com/v3/businesses/{business_id}/reviews',
                headers=headers,
                timeout=5,
            )
            reviews = review_resp.json().get('reviews')
            if reviews:
                return reviews[0].get('text')
        except Exception:
            return None
        return None
