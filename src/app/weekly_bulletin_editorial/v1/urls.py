from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.weekly_bulletin_editorial.v1.views import WeeklyBulletinEditorialViewSet

router = DefaultRouter()
router.register("weekly_bulletin_editorial", WeeklyBulletinEditorialViewSet, basename="weekly_bulletin_editorial")

urlpatterns = [
    path("", include(router.urls)),
]
