from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.department_board.v1.views import DepartmentBoardViewSet

router = DefaultRouter()
router.register("department_board", DepartmentBoardViewSet, basename="department_board")

urlpatterns = [
    path("", include(router.urls)),
]
