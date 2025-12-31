from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.department_board_comment.v1.views import DepartmentBoardCommentViewSet

router = DefaultRouter()
router.register("department_board_comment", DepartmentBoardCommentViewSet, basename="department_board_comment")

urlpatterns = [
    path("", include(router.urls)),
]
