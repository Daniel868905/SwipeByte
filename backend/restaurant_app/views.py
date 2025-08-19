import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

def _empty_or_error(detail, code=400):
    """Return [] with HTTP 200 so the UI never crashes, but include reason in headers."""
    import os
    if os.environ.get("RESTAURANT_SEARCH_EMPTY_ON_ERROR", "1") == "1":
        resp = Response([], status=200)
        resp["X-Error-Detail"] = detail
        resp["X-Error-Code"] = str(code)
        return resp
    return Response({"detail": detail}, status=code)

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

# --- BEGIN: drop-in Google Places search shim ---
import os, requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse

def _get_google_places_key():
    return os.environ.get("GOOGLE_PLACES_API_KEY") or os.environ.get("GOOGLE_MAPS_API_KEY")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def restaurant_search(request):
    key = _get_google_places_key()

    # Accept q or search; allow empty -> generic 'nearby restaurants'
    q = (request.GET.get("q") or request.GET.get("search") or "").strip() or None

    # Accept lat/lng OR lat/lon; fall back to user profile
    lat = request.GET.get("lat") or getattr(request.user, "latitude", None)
    lng = (request.GET.get("lng") or request.GET.get("lon") or getattr(request.user, "longitude", None))

    if not key:
        return _empty_or_error("Server is missing Google Places key", 503)
    if not lat or not lng:
        return _empty_or_error("lat/lng required or set your location first", 400)

    # distance (miles) -> radius (meters), clamp 100..50000
    radius = request.GET.get("radius")
    if not radius:
        dist = request.GET.get("distance")
        if dist:
            try:
                radius = int(float(dist) * 1609.34)
            except Exception:
                radius = 2500
        else:
            radius = 2500
    radius = max(100, min(int(radius), 50000))

    params = {
        "location": f"{lat},{lng}",
        "radius": str(radius),
        "type": "restaurant",
        "key": key,
    }
    if q:
        params["keyword"] = q

    # price (0–4) -> minprice/maxprice
    price = request.GET.get("price")
    if price is not None:
        try:
            pr = int(price)
            if 0 <= pr <= 4:
                params["minprice"] = pr
                params["maxprice"] = pr
        except Exception:
            pass

    try:
        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
            params=params, timeout=10
        )
        r.raise_for_status()
        data = r.json()
        results = []
        for it in data.get("results", []):
            photos = (it.get("photos") or [])
            photo_ref = (photos[0] or {}).get("photo_reference") if photos else None
    
            loc = (it.get("geometry") or {}).get("location") or {}
            results.append({
                "id": it.get("place_id"),
                
                "name": it.get("name"),
                "rating": it.get("rating"),
                "user_ratings_total": it.get("user_ratings_total"),
                "vicinity": it.get("vicinity") or it.get("formatted_address"),
                "location": {"lat": loc.get("lat"), "lng": loc.get("lng")},
                "photo_ref": photo_ref,
                "photo_url": (f"/api/v1/restaurants/photo?ref={photo_ref}" if photo_ref else None),
                "image": (f"/api/v1/restaurants/photo?ref={photo_ref}" if photo_ref else None),
                "open_now": (it.get("opening_hours") or {}).get("open_now"),
                "price_level": it.get("price_level"),
                "url": f"https://www.google.com/maps/place/?q=place_id:{it.get('place_id')}",
            })
        return Response(results)
    except requests.HTTPError as e:
        try:
            payload = e.response.json()
        except Exception:
            payload = {"detail": str(e)}
        return _empty_or_error(str(payload), e.response.status_code)


@api_view(["GET"])
@permission_classes([])  # AllowAny so <img> can load without auth header
def restaurant_photo(request):
    key = _get_google_places_key()
    ref = (request.GET.get("ref") or "").strip()
    maxwidth = str(request.GET.get("maxwidth", "400"))
    if not key or not ref:
        return Response({"detail":"photo ref required"}, status=400)
    try:
        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/photo",
            params={"maxwidth": maxwidth, "photo_reference": ref, "key": key},
            timeout=10, allow_redirects=True
        )
        r.raise_for_status()
    except Exception as e:
        return Response({"detail": str(e)}, status=502)
    resp = HttpResponse(r.content, content_type=r.headers.get("Content-Type","image/jpeg"))
    resp["Cache-Control"] = "public, max-age=86400"
    return resp
