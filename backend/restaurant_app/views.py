import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Restaurant
from favorite_app.models import Favorite

class RestaurantSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latitude = float(request.query_params.get('lat', '40.7128'))
        longitude = float(request.query_params.get('lon', '-74.0060'))
        distance_miles = float(request.query_params.get('distance', '15'))
        distance = distance_miles * 1609.34
        price = request.query_params.get('price')

        user_likes = Favorite.objects.filter(
            user_favorites=request.user
        ).values_list('restaurant', flat=True)

        qs = Restaurant.objects.all()

        if user_likes:
            qs = qs.exclude(place_id__in=list(user_likes))

        if not qs.exists():
            api_key = os.environ.get('GOOGLE_API_KEY', '')
            params = {
                'location': f"{latitude},{longitude}",
                'radius': distance,
                'type': 'restaurant',
                'key': api_key,
            }
            if price:
                params['minprice'] = price
                params['maxprice'] = price

            resp = requests.get(
                'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
                params=params,
            )
            data = resp.json()

            for result in data.get('results', []):
                photo_reference = None
                photos = result.get('photos')
                if photos:
                    photo_reference = photos[0].get('photo_reference')

                image_url = None
                if photo_reference:
                    image_url = (
                        'https://maps.googleapis.com/maps/api/place/photo'
                        f'?maxwidth=400&photoreference={photo_reference}&key={api_key}'
                    )

                loc = result.get('geometry', {}).get('location', {})
                Restaurant.objects.get_or_create(
                    place_id=result.get('place_id'),
                    defaults={
                        'name': result.get('name'),
                        'location': f"{loc.get('lat')},{loc.get('lng')}",
                        'rating': result.get('rating'),
                        'price': result.get('price_level'),
                        'image_url': image_url,
                        'url': (
                            'https://www.google.com/maps/place/?q=place_id:'
                            f"{result.get('place_id')}"
                        ),
                    },
                )
            qs = Restaurant.objects.all()
            if user_likes:
                qs = qs.exclude(place_id__in=list(user_likes))

        restaurants = [
            {
                'id': r.place_id,
                'name': r.name,
                'image_url': r.image_url,
                'rating': r.rating,
                'price': r.price,
                'url': r.url,
            }
            for r in qs
        ]
        return Response(restaurants)