from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.liturgy_flower_comment.v1.views import LiturgyFlowerCommentViewSet

router = DefaultRouter()
router.register("comment", LiturgyFlowerCommentViewSet, basename="liturgy_flower_comment")

urlpatterns = [
    path("liturgy_flower/<int:liturgy_flower_id>/", include(router.urls)),
]
