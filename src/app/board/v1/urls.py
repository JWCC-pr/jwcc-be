from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.board.v1.views import BoardViewSet

router = DefaultRouter()
router.register("board", BoardViewSet, basename="board")

urlpatterns = [
    path("", include(router.urls)),
]
