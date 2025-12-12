from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.board_hit.v1.views import BoardHitViewSet

router = DefaultRouter()
router.register("board_hit", BoardHitViewSet, basename="board_hit")

urlpatterns = [
    path("", include(router.urls)),
]
