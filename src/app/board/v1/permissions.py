from rest_framework import permissions

from app.user.models import UserGradeChoices


class BoardPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            if UserGradeChoices.GRADE_05 < request.user.grade:
                return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
