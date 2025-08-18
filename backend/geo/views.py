import os, requests
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

try:
    from rest_framework.throttling import UserRateThrottle
    class GeoThrottle(UserRateThrottle):
        rate = "60/min"
except Exception:
    class GeoThrottle:  # no-op if throttling not available
        pass

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([GeoThrottle])
def set_location_from_address(request):
    """
    Body: {"address": "1600 Amphitheatre Pkwy, Mountain View, CA"}
    Server looks up lat/lng with Google key and stores it on the user.
    """
    if not GOOGLE_MAPS_API_KEY:
        return Response({"detail":"Server not configured for geocoding."}, status=503)

    address = (request.data.get("address") or "").strip()
    if not address:
        return Response({"detail":"address is required"}, status=400)

    try:
        r = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": address, "key": GOOGLE_MAPS_API_KEY},
            timeout=10,
        )
        r.raise_for_status()
        payload = r.json()
        results = payload.get("results") or []
        if not results:
            return Response({"detail":"No results for that address"}, status=404)

        loc = results[0]["geometry"]["location"]
        lat, lng = float(loc["lat"]), float(loc["lng"])

        user = request.user
        # Adjust these field names if your User model uses different ones:
        setattr(user, "latitude", lat)
        setattr(user, "longitude", lng)
        user.save(update_fields=["latitude","longitude"])

        return Response({"latitude": lat, "longitude": lng})
    except requests.RequestException as e:
        return Response({"detail":"Geocoding failed","error":str(e)}, status=502)
