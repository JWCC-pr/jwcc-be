from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.board_like.v1.views import BoardLikeViewSet

router = DefaultRouter()
router.register("like", BoardLikeViewSet, basename="board_like")

urlpatterns = [
    path("board/<int:board_id>/", include(router.urls)),
]
