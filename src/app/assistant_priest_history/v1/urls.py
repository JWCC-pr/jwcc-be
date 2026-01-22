from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.assistant_priest_history.v1.views import AssistantPriestHistoryViewSet

router = DefaultRouter()
router.register("assistant_priest_history", AssistantPriestHistoryViewSet, basename="assistant_priest_history")

urlpatterns = [
    path("", include(router.urls)),
]
