import os
import json
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

        headers = {
            'Authorization': f"Bearer {os.environ.get('YELP_API_KEY', '')}"
        }
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'radius': distance,
            'term': 'restaurants'
        }
        if price:
            params['price'] = price

        url = 'https://api.yelp.com/v3/businesses/search?' + urlencode(params)
        req = Request(url, headers=headers)
        resp = urlopen(req)
        data = json.loads(resp.read())
        restaurants = []
        for biz in data.get('businesses', []):
            restaurants.append({
                'id': biz.get('id'),
                'name': biz.get('name'),
                'image_url': biz.get('image_url'),
                'rating': biz.get('rating'),
                'price': biz.get('price'),
                'url': biz.get('url'),
            })
        return Response(restaurants)