from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.weekly_bulletin_hit.v1.views import WeeklyBulletinHitViewSet

router = DefaultRouter()
router.register("weekly_bulletin_hit", WeeklyBulletinHitViewSet, basename="weekly_bulletin_hit")

urlpatterns = [
    path("", include(router.urls)),
]
