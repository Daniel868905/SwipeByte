import os
import json
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RestaurantSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latitude = request.query_params.get('lat', '40.7128')
        longitude = request.query_params.get('lon', '-74.0060')
        distance = request.query_params.get('distance', '1600')
        price = request.query_params.get('price')

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

        restaurants = []
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
            restaurants.append({
                'id': result.get('place_id'),
                'name': result.get('name'),
                'image_url': image_url,
                'rating': result.get('rating'),
                'price': result.get('price_level'),
                'url': (
                    'https://www.google.com/maps/place/?q=place_id:'
                    f"{result.get('place_id')}"
                ),
            })
        return Response(restaurants)