"""Views for the favorite_app.

These views provide CRUD functionality for the ``Favorite`` model using
the existing ``FavoriteSerializer``. All endpoints require token
authentication and only operate on favorites that belong to the
authenticated user.
"""

from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteListCreateView(generics.ListCreateAPIView):
    """List authenticated user's favorites or create a new one."""

    serializer_class = FavoriteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return favorites for the current user, optionally filtered."""
        user = self.request.user
        restaurant = self.request.query_params.get('restaurant')
        group_id = self.request.query_params.get('group')
        if restaurant:
            return Favorite.objects.filter(restaurant=restaurant).filter(
                Q(user_favorites=user) | Q(group_favorites__members=user)  # type: ignore
            )
        if group_id:
            return Favorite.objects.filter(
                group_favorites_id=group_id,
                group_favorites__members=user,
            )
        return Favorite.objects.filter(user_favorites=user)
    def perform_create(self, serializer):
        """Associate the created favorite with the current user."""
        serializer.save(user_favorites=self.request.user)


class FavoriteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific favorite."""

    serializer_class = FavoriteSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Allow access to user's favorites and group favorites they belong to."""
        user = self.request.user
        return Favorite.objects.filter(
            Q(user_favorites=user) | Q(group_favorites__members=user) # type: ignore
        )
