from django.urls import path

from post.views import (
    FollowingFeedAPIView,
    LikedPostsAPIView,
    PostDetailAPIView,
    PostListCreateAPIView,
    ToggleLikeAPIView,
    UserPostsAPIView,
)


urlpatterns = [
    path("", PostListCreateAPIView.as_view()),
    path("<int:pk>/", PostDetailAPIView.as_view()),
    path("toggle-like/<int:post_id>/", ToggleLikeAPIView.as_view()),
    path("likes/", LikedPostsAPIView.as_view()),
    path("following/", FollowingFeedAPIView.as_view()),
    path("user/<int:user_id>/", UserPostsAPIView.as_view()),
]
