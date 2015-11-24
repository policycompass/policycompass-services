from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .auth import AdhocracyUser


class IsAdhocracyGod(BasePermission):
    """
    Allow only adhocracy users of group god to access
    """

    def has_permission(self, request, view):
        return request.user and type(
            request.user) is AdhocracyUser and request.user.is_god


class IsCreatorOrReadOnly(BasePermission):
    """
    Allows the Creator of an object and Gods to alter the object
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated():
            if request.user.is_god:
                return True
            elif hasattr(obj,
                         'creator_path') and obj.creator_path == request.user.resource_path:
                return True
            else:
                return False
        else:
            return False
