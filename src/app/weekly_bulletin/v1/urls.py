from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.weekly_bulletin.v1.views import WeeklyBulletinViewSet

router = DefaultRouter()
router.register("weekly_bulletin", WeeklyBulletinViewSet, basename="weekly_bulletin")

urlpatterns = [
    path("", include(router.urls)),
]
