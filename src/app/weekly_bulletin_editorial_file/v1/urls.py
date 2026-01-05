from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.weekly_bulletin_editorial_file.v1.views import WeeklyBulletinEditorialFileViewSet

router = DefaultRouter()
router.register(
    "weekly_bulletin_editorial_file", WeeklyBulletinEditorialFileViewSet, basename="weekly_bulletin_editorial_file"
)

urlpatterns = [
    path("", include(router.urls)),
]
