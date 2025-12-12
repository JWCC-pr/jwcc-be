from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.department.v1.views import DepartmentViewSet

router = DefaultRouter()
router.register("department", DepartmentViewSet, basename="department")

urlpatterns = [
    path("", include(router.urls)),
]
