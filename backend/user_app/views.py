from django.shortcuts import render
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
   
class UserPermission(APIView):  
    authentication_classes = [TokenAuthentication]
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
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=False,
                is_superuser=False,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=s.HTTP_400_BAD_REQUEST)

        token_obj, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token_obj.key}, status=s.HTTP_201_CREATED)
        
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
            return Response({'token': token_obj.key}, status=s.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Invalid credentials'},
                status=s.HTTP_401_UNAUTHORIZED,
            )

class LogOut(UserPermission):

    def post(self, request):
        user = request.user
        token = user.auth_token
        logout(request)
        token.delete()
        return Response({'success': True})