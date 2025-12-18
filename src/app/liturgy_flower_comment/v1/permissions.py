from rest_framework import permissions


class LiturgyFlowerCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return request.user.is_authenticated
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id
