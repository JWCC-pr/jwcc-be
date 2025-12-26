from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.pastor_history.v1.views import PastorHistoryViewSet

router = DefaultRouter()
router.register("pastor_history", PastorHistoryViewSet, basename="pastor_history")

urlpatterns = [
    path("", include(router.urls)),
]
