from rest_framework import permissions

from app.user.models import UserGradeChoices


class RoomReservationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(view, "basename", "") == "repeat_room_reservation":
            return request.user.grade == UserGradeChoices.GRADE_01

        if view.action == "create":
            return request.user.grade <= UserGradeChoices.GRADE_04

        return True

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(view, "basename", "") == "repeat_room_reservation":
            return request.user.grade == UserGradeChoices.GRADE_01

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.grade == UserGradeChoices.GRADE_01:
            return True

        return obj.created_by_id == request.user.id


class CatechismRoomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
