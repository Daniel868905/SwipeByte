from .models import User, UserSwipe
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from favorite_app.models import Favorite
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .authentication import CookieTokenAuthentication
from django.conf import settings
   
class UserPermission(APIView):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

class Info(UserPermission):
    def get(self, request):
        return Response(
            {
                "username": request.user.email,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "token": request.user.auth_token.key,
                "latitude": request.user.latitude,
                "longitude": request.user.longitude
            }
        )
    
class SignUp(APIView):
    def post(self, request):
        """Create a new user and return an auth token.

        Only the ``email`` and ``password`` fields are required.  Any extra
        fields supplied by the client are ignored so that front‑end payloads
        containing values such as ``confirmPassword`` do not cause the request
        to fail with a ``400`` response.
        """

        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        if not email or not password:
            return Response(
                {"detail": "Email and password required"},
                status=s.HTTP_400_BAD_REQUEST,
            )
        
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=s.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,
                is_superuser=False,
                is_active=True,
            )
        except IntegrityError:
            return Response(
                {"error": "User with this email already exists"},
                status=s.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=s.HTTP_400_BAD_REQUEST)

        return Response({"detail": "User created"}, status=s.HTTP_201_CREATED)
        
class LogIn(APIView):
    
    def post(self, request):
        data = request.data.copy()

        email = data.get('email') or data.get('username')
        password = data.get('password')
        if not email or not password:
            return Response(
                {'detail': 'Email and password required'},
                status=s.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=email, password=password)
        if user:
            token_obj, _ = Token.objects.get_or_create(user=user)
            login(request=request, user=user)
            response = Response(
                {'detail': 'Logged in', 'token': token_obj.key},
                status=s.HTTP_200_OK,
            )
            secure_cookie = not settings.DEBUG
            samesite = 'None' if secure_cookie else 'Lax'
            response.set_cookie(
                'auth_token',
                token_obj.key,
                httponly=True,
                secure=secure_cookie,
                samesite=samesite,
            )
            return response
        else:
            return Response(
                {'detail': 'Invalid credentials or inactive account'},
                status=s.HTTP_401_UNAUTHORIZED,
            )

class LogOut(UserPermission):

    def post(self, request):
        user = request.user
        token = user.auth_token
        logout(request)
        token.delete()
        response = Response({"success": True})
        response.delete_cookie('auth_token')
        return response
    

class Location(UserPermission):
    def post(self, request):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        if latitude is None or longitude is None:
            return Response(
                {"detail": "latitude and longitude required"},
                status=s.HTTP_400_BAD_REQUEST,
            )
        user = request.user
        user.latitude = latitude
        user.longitude = longitude
        user.save()
        return Response({"success": True})


class UserSwipeView(UserPermission):
    def post(self, request):
        restaurant = request.data.get('restaurant')
        location = request.data.get('location', '')
        liked = request.data.get('liked', True)
        if not restaurant:
            return Response({'error': 'Restaurant is required'}, status=s.HTTP_400_BAD_REQUEST)

        swipe, _ = UserSwipe.objects.get_or_create(
            user=request.user,
            restaurant=restaurant,
            defaults={'location': location, 'liked': liked},
        )
        if location and not swipe.location:
            swipe.location = location
        swipe.record_vote(liked)

        result = {'matched': False}
        if swipe.has_match():
            Favorite.objects.get_or_create(
                user_favorites=request.user,
                restaurant=swipe.restaurant,
                defaults={'location': swipe.location},
            )
            result = {
                'matched': True,
                'restaurant': swipe.restaurant,
                'location': swipe.location,
            }

        return Response(result)


class UserMatchResetView(UserPermission):
    def post(self, request):
        request.user.swipes.all().delete()
        Favorite.objects.filter(user_favorites=request.user).delete()
        return Response({'status': 'reset'})


class PasswordResetView(UserPermission):
    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response(
                {"detail": "old_password and new_password required"},
                status=s.HTTP_400_BAD_REQUEST,
            )

        if not request.user.check_password(old_password):
            return Response(
                {"detail": "Invalid password"},
                status=s.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save()
        return Response({"success": True})
