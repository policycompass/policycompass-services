"""
Permission class for the Metrics Manager.
Work in Progress!
"""
from rest_framework import permissions


class IsAuthenticatedCanCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method == 'POST' and request.user and request.user.is_authenticated():
            return True

        else:
            return False