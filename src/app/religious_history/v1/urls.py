from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.religious_history.v1.views import ReligiousHistoryViewSet

router = DefaultRouter()
router.register("religious_history", ReligiousHistoryViewSet, basename="religious_history")

urlpatterns = [
    path("", include(router.urls)),
]
