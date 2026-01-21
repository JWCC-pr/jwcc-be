from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.board_image.v1.views import BoardImageViewSet

router = DefaultRouter()
router.register("board_image", BoardImageViewSet, basename="board_image")

urlpatterns = [
    path("", include(router.urls)),
]
