from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.sub_department.v1.views import SubDepartmentViewSet

router = DefaultRouter()
router.register("sub_department", SubDepartmentViewSet, basename="sub_department")

urlpatterns = [
    path("", include(router.urls)),
]
