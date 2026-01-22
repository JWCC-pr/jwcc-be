from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.department_board_hit.v1.views import DepartmentBoardHitViewSet

router = DefaultRouter()
router.register("department_board_hit", DepartmentBoardHitViewSet, basename="department_board_hit")

urlpatterns = [
    path("", include(router.urls)),
]
