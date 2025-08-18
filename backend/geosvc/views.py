import os, requests
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

# Optional throttling to protect your key
try:
    from rest_framework.throttling import UserRateThrottle
    class GeoThrottle(UserRateThrottle):
        rate = "60/min"
except Exception:
    class GeoThrottle:  # no-op
        pass

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([GeoThrottle])
def set_location_from_address(request):
    """
    Body: {"address": "..."} — server geocodes and STORES lat/lng on the user.
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
        data = r.json()
        results = data.get("results") or []
        if not results:
            return Response({"detail":"No results for that address"}, status=404)

        loc = results[0]["geometry"]["location"]
        lat, lng = float(loc["lat"]), float(loc["lng"])

        # Update current user record (adjust field names if different)
        user = request.user
        # Expect your User model has latitude/longitude fields:
        setattr(user, "latitude", lat)
        setattr(user, "longitude", lng)
        user.save(update_fields=["latitude", "longitude"])

        return Response({"lat": lat, "lng": lng, "status": "saved"})
    except requests.RequestException:
        return Response({"detail":"Geocoding failed"}, status=502)

@api_view(["GET"])
@permission_classes([AllowAny])  # allow pre-login usage from your site; keep throttled
@throttle_classes([GeoThrottle])
def geocode_proxy(request):
    """
    Query: ?address=... — server geocodes and returns Google's JSON (no user update).
    Used by the frontend shim to replace direct Google calls.
    """
    if not GOOGLE_MAPS_API_KEY:
        return Response({"error":"Server not configured for geocoding."}, status=503)

    address = (request.query_params.get("address") or "").strip()
    if not address:
        return Response({"error":"address is required"}, status=400)

    try:
        r = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": address, "key": GOOGLE_MAPS_API_KEY},
            timeout=10,
        )
        r.raise_for_status()
        return Response(r.json(), status=r.status_code)
    except requests.RequestException:
        return Response({"error":"Geocoding upstream error"}, status=502)
