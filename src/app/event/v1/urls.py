from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.event.v1.views import EventViewSet

router = DefaultRouter()
router.register("event", EventViewSet, basename="event")

urlpatterns = [
    path("", include(router.urls)),
]
