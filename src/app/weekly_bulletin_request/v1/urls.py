from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.weekly_bulletin_request.v1.views import WeeklyBulletinRequestViewSet

router = DefaultRouter()
router.register("weekly_bulletin_request", WeeklyBulletinRequestViewSet, basename="weekly_bulletin_request")

urlpatterns = [
    path("", include(router.urls)),
]
