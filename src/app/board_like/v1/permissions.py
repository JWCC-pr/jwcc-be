from rest_framework import permissions


class BoardLikePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
