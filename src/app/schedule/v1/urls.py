from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.schedule.v1.views import ScheduleViewSet

router = DefaultRouter()
router.register("schedule", ScheduleViewSet, basename="schedule")

urlpatterns = [
    path("", include(router.urls)),
]
