from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.priest_history.v1.views import PriestHistoryViewSet

router = DefaultRouter()
router.register("priest_history", PriestHistoryViewSet, basename="priest_history")

urlpatterns = [
    path("", include(router.urls)),
]
