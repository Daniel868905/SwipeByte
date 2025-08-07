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
        latitude = float(request.query_params.get("lat", "40.7128"))
        longitude = float(request.query_params.get("lon", "-74.0060"))
        distance_miles = float(request.query_params.get("distance", "15"))
        distance = distance_miles * 1609.34
        price = request.query_params.get('price')
        # Restaurants the user has already liked should be filtered out.
        liked_names = set(
            Favorite.objects.filter(user_favorites=request.user).values_list(
                "restaurant", flat=True
            )
        )
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        params = {
            "location": f"{latitude},{longitude}",
            "radius": distance,
            "type": "restaurant",
            "key": api_key,
        }
        if price:
            params["minprice"] = price
            params["maxprice"] = price

        results = []
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=params,
        )
        results.extend(resp.json().get("results", []))

        # Include fast food results when the cheapest price level is requested.
        if price == "1":
            ff_params = params.copy()
            ff_params["type"] = "fast_food"
            ff_resp = requests.get(
                "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                params=ff_params,
            )
            results.extend(ff_resp.json().get("results", []))

        restaurants = []
        seen_place_ids = set()
        for result in results:
            place_id = result.get("place_id")
            if not place_id or place_id in seen_place_ids:
                continue
            seen_place_ids.add(place_id)

            name = result.get("name")
            if name in liked_names:
                continue


            photo_reference = None
            photos = result.get("photos")
            if photos:
                photo_reference = photos[0].get("photo_reference")

            image_url = None
            if photo_reference:
                image_url = (
                    "https://maps.googleapis.com/maps/api/place/photo"
                    f"?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                )
            loc = result.get("geometry", {}).get("location", {})
            Restaurant.objects.update_or_create(
                place_id=place_id,
                defaults={
                    "name": name,
                    "location": f"{loc.get('lat')},{loc.get('lng')}",
                    "rating": result.get("rating"),
                    "price": result.get("price_level"),
                    "image_url": image_url,
                    "url": (
                        "https://www.google.com/maps/place/?q=place_id:"
                        f"{place_id}"
                    ),
                },
            )

            restaurants.append(
                {
                    "id": place_id,
                    "name": name,
                    "image_url": image_url,
                    "rating": result.get("rating"),
                    "price": result.get("price_level"),
                    "url": "https://www.google.com/maps/place/?q=place_id:" + place_id,
                }
            )
        return Response(restaurants)