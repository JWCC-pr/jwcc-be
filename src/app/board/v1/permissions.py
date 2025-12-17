from rest_framework import permissions

from app.user.models import UserGradeChoices


class BoardPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            # 본당 신자 등급 이상부터 게시물 작성 가능
            if UserGradeChoices.GRADE_06 < request.user.grade:
                return False
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
