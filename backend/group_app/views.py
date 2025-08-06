
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Group, GroupSwipe
from .serializers import GroupDetailSerializer
from user_app.models import User
from favorite_app.models import Favorite


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


class GroupSwipeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        if request.user not in group.members.all():
            return Response({'error': 'Not a member of this group'}, status=status.HTTP_403_FORBIDDEN)

        restaurant = request.data.get('restaurant')
        location = request.data.get('location', '')
        liked = request.data.get('liked', True)
        if not restaurant:
            return Response({'error': 'Restaurant is required'}, status=status.HTTP_400_BAD_REQUEST)

        swipe, _ = GroupSwipe.objects.get_or_create(
            group=group,
            restaurant=restaurant,
            defaults={'location': location},
        )
        if location and not swipe.location:
            swipe.location = location
            swipe.save()

        swipe.record_vote(request.user, liked)

        matched = False
        if swipe.has_match():
            Favorite.objects.get_or_create(
                group_favorites=group,
                restaurant=swipe.restaurant,
                defaults={'location': swipe.location},
            )
            matched = True

        return Response({'matched': matched})