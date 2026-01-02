from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.department_board_like.v1.views import DepartmentBoardLikeViewSet

router = DefaultRouter()
router.register("like", DepartmentBoardLikeViewSet, basename="department_board_like")

urlpatterns = [
    path("department_board/<int:department_board_id>/", include(router.urls)),
]
