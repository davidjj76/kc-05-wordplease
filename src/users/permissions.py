from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj
