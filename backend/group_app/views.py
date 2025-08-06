
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Group
from .serializers import GroupDetailSerializer
from user_app.models import User


class GroupWithFavoritesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        groups = Group.objects.filter(members__in=[user])
        serializer = GroupDetailSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        group_name = request.data.get('group_name', '')
        member_usernames = request.data.get('members', [])

        if not group_name:
            return Response({'error': 'Group name is required'}, status=400)

        if not isinstance(member_usernames, list):
            member_usernames = [member_usernames]

        group = Group.objects.create(group_name=group_name)
        group.members.add(request.user)

        users = User.objects.filter(email__in=member_usernames)
        if users:
            group.members.add(*users)

        serializer = GroupDetailSerializer(group)
        return Response(serializer.data, status=201)