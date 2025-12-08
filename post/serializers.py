from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from image.models import Image
from image.serializers import ImageSerializer
from post.models import Post
from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class PostSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    images = ImageSerializer(many=True, required=False)
    likes_count = IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "created",
            "updated",
            "likes_count",
            "images",
        ]

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        user = self.context["request"].user
        # Ensure user has a profile, create one if it doesn't exist
        user_profile, _ = UserProfile.objects.get_or_create(user=user)

        post = Post.objects.create(user=user_profile, **validated_data)

        for img in images_data:
            Image.objects.create(post=post, **img)

        return post
