from rest_framework import permissions

from app.user.models import UserGradeChoices


class DepartmentBoardPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.grade == UserGradeChoices.GRADE_01:
            return True

        if request.method in permissions.SAFE_METHODS:
            if not request.user.sub_department_set.filter(department_id=obj.department_id).exists():
                return False
            if obj.is_secret and not request.user.sub_department_set.filter(id=obj.sub_department_id).exists():
                return False
            return True

        if obj.is_pinned and request.user.grade == UserGradeChoices.GRADE_01:
            return True

        return obj.user == request.user
