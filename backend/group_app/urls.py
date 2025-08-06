from django.urls import path
from .views import GroupWithFavoritesView, GroupSwipeView

urlpatterns = [
    path('', GroupWithFavoritesView.as_view()),
    path('<int:group_id>/swipe/', GroupSwipeView.as_view()),

    
]