from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from motion.permissions import IsAdmin, IsOwnerOrAdmin
from user.models import User
from user.serializers import UserSerializer, UserCreateSerializer


class ListCreateUserView(ListCreateAPIView):
    """
    GET: List all users (admins only)
    POST: Create new user (public access for registration)
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Use different serializers for read vs write"""
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        """Allow public registration but require admin for listing"""
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdmin()]


class RetrieveUpdateDestroyUserView(RetrieveUpdateDestroyAPIView):
    """
    GET: View user profile (everyone can view)
    PUT/PATCH: Update user profile (owner only)
    DELETE: Delete user (owner only)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Everyone can view, only owner can update/delete"""
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsOwnerOrAdmin()]
