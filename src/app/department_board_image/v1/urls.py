from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.department_board_image.v1.views import DepartmentBoardImageViewSet

router = DefaultRouter()
router.register("department_board_image", DepartmentBoardImageViewSet, basename="department_board_image")

urlpatterns = [
    path("", include(router.urls)),
]
