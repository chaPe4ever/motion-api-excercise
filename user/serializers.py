from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class UserSerializer(ModelSerializer):
    """
    Serializer for listing users (read-only operations)
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
        ]
        read_only_fields = ["id", "created"]
        ref_name = "User"


class UserCreateSerializer(ModelSerializer):
    """
    Serializer for creating new users with password validation
    """

    password = CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],
    )
    password2 = CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, attrs):
        """
        Verify that the two password entries match
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create user with hashed password
        Author profile is automatically created via signal
        """
        # Remove password2 as it's not needed for user creation
        validated_data.pop("password2")

        # Create user with hashed password using create_user method
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        return user
