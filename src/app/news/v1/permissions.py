from rest_framework import permissions

from app.user.models import UserGradeChoices

"""
TODO : 본당 소식 접근 권한 관련 
본당 신자 이상 - 상세 조회 가능 [v]
타본당 신자 이상 - 리스트 조회 가능 [v]
비회원 - 최신 소식 조회 가능 [v]
"""


class NewsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 비회원: 접근 불가
        if not request.user.is_authenticated:
            return False

        # 본당 신자(GRADE_06) 이상: 모든 접근 가능
        if request.user.grade <= UserGradeChoices.GRADE_06:
            return True

        # 타본당 신자(GRADE_07): 리스트만 접근 가능
        if view.action == "list" and request.user.grade == UserGradeChoices.GRADE_07:
            return True

        return False
