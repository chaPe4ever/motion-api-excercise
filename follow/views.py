from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from follow.models import Follow
from user.models import User
from user.serializers import UserSerializer


# Create your views here.
class FollowersListAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return [f.follower for f in self.request.user.followers.all()]


class FollowingListAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return [f.following for f in self.request.user.following.all()]


class ToggleFollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        following = User.objects.get(id=user_id)

        relation, created = Follow.objects.get_or_create(
            follower=follower, following=following
        )

        if not created:
            relation.delete()
            return Response({"status": "unfollowed"})

        return Response({"status": "followed"})
