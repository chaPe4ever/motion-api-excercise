from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger(__name__)


class IsInGroup(BasePermission):
    """
    Base class to check if user is in a specific group.
    """

    required_groups = []

    def has_permission(self, request, view):
        logger.info(f"Checking permission for user: {request.user}")
        logger.info(f"Is authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated:
            logger.warning("User is not authenticated")
            return False

        user_groups = list(request.user.groups.values_list("name", flat=True))
        logger.info(f"User groups: {user_groups}")
        logger.info(f"Required groups: {self.required_groups}")

        # Check if user is in any of the required groups
        has_perm = request.user.groups.filter(name__in=self.required_groups).exists()
        logger.info(f"Has permission: {has_perm}")

        return has_perm


class IsModerator(IsInGroup):
    """
    Only users in 'Moderators' group can access.
    """

    required_groups = ["Moderators"]


class IsAdmin(BasePermission):
    """
    Only admins (staff, superuser, or Admins group) can access.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.user.is_staff
            or request.user.is_superuser
            or request.user.groups.filter(name__in=["Admins", "Moderators"]).exists()
        )


class IsOwnerOrAdmin(BasePermission):
    """
    Only the owner of the object or admins can access.
    """

    def has_object_permission(self, request, view, obj):
        # Allow admins
        if request.user.is_authenticated and (
            request.user.is_staff
            or request.user.is_superuser
            or request.user.groups.filter(name__in=["Admins", "Moderators"]).exists()
        ):
            return True

        # Allow the owner
        return obj == request.user
