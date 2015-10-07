from rest_framework.permissions import BasePermission
from .auth import AdhocracyUser

class IsAdhocracyGod(BasePermission):
    """
    Allow only adhocracy users of group god to access
    """
    def has_permission(self, request, view):
        return request.user and type(request.user) is AdhocracyUser and request.user.is_god
