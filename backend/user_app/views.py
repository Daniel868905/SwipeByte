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
        data = request.data.copy()
        data['username'] = data.get('email')
        data['is_staff'] = False
        data['is_superuser'] = False
        new_user = User(**data)

        try:
            new_user.full_clean()
            user = User.objects.create_user(

                **data
            )
            token_obj = Token.objects.create(user=user)
            return Response({'token':token_obj.key}, status=s.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=s.HTTP_400_BAD_REQUEST)
        
class LogIn(APIView):
    
    def post(self, request):
        data = data.request.copy()

        user =authenticate(
            username=data.get('username'), password=data.get('password')
        )
        if user:
            token_obj, _ = Token.objects.get_or_create(user=user)
            login(request=request, user=user)
            return Response({'token': token_obj.key}, status=s.HTTP_200_OK)
        else:
            return Response(
                'No user matching these credentials', status=s.HTTP_404_NOT_FOUND
            )

class LogOut(UserPermission):

    def post(self, request):
        user = request.user
        token = user.auth_token
        logout(request)
        token.delete()
        return Response({'success':True})