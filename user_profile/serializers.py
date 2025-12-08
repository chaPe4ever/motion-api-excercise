from rest_framework.serializers import ModelSerializer
from user_profile.models import UserProfile
from user.models import User


class NestedUserSerializer(ModelSerializer):
    """User serializer for nesting in UserProfileSerializer (excludes profile to avoid circular reference)"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]
        read_only_fields = ["id"]


class UserProfileSerializer(ModelSerializer):
    user = NestedUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "job",
            "avatar",
            "location",
            "phone_number",
            "about_me",
            "user_hashtags",
            "updated",
            "user",
        ]
