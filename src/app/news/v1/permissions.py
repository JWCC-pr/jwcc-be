from rest_framework import permissions

from app.user.models import UserGradeChoices


class NewsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 본당 신자(GRADE_06) 이상만 접근 가능
        if UserGradeChoices.GRADE_06 < request.user.grade:
            return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
