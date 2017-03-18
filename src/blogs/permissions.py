from rest_framework.permissions import BasePermission


class PostPermission(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return request.user.is_superuser or request.user == obj.author or obj.status() == "Published"
        else:
            # PUT and DELETE permissions
            return request.user.is_superuser or request.user == obj.author


