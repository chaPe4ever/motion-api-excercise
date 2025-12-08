from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from motion.permissions import IsOwnerOrAdmin
from user.models import User
from post.models import Post
from .serializers import (
    PostSerializer,
)


# Create your views here.
class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by("-created")


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrAdmin]


class ToggleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"status": "unliked"})
        else:
            post.likes.add(user)
            return Response({"status": "liked"})


class LikedPostsAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.liked_posts.all().order_by("-created")


class FollowingFeedAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.values_list(
            "following", flat=True
        )
        return Post.objects.filter(user__user__in=following_users).order_by("-created")


class UserPostsAPIView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs["user_id"])
        return user.profile.posts.all().order_by("-created")
