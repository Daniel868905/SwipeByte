
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Group
from .serializers import GroupDetailSerializer

class GroupWithFavoritesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = Group.objects.filter(members=user)
        serializer = GroupDetailSerializer(groups, many=True)
        return Response(serializer.data)
