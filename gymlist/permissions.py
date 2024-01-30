from rest_framework import permissions


class IsManagerAndOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only users who are managers and own the gym to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == 'manager' and request.user.manager and obj.manager == request.user.manager

class IsManagerAndOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to users to edit their information.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == 'manager' and request.user.manager and obj.manager == request.user.manager
    # Done