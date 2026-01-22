from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.department_board_comment.v1.views import DepartmentBoardCommentViewSet

router = DefaultRouter()
router.register("comment", DepartmentBoardCommentViewSet, basename="department_board_comment")

urlpatterns = [
    path("department_board/<int:department_board_id>/", include(router.urls)),
]
