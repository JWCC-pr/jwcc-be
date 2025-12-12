from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.board_comment.v1.views import BoardCommentViewSet

router = DefaultRouter()
router.register("comment", BoardCommentViewSet, basename="board_comment")

urlpatterns = [
    path("board/<int:board_id>/", include(router.urls)),
]
