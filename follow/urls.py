from django.urls import path

from follow.views import (
    FollowersListAPIView,
    FollowingListAPIView,
    ToggleFollowAPIView,
)

urlpatterns = [
    path("toggle-follow/<int:user_id>/", ToggleFollowAPIView.as_view()),
    path("followers/", FollowersListAPIView.as_view()),
    path("following/", FollowingListAPIView.as_view()),
]
