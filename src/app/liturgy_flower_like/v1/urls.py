from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.liturgy_flower_like.v1.views import LiturgyFlowerLikeViewSet

router = DefaultRouter()
router.register("like", LiturgyFlowerLikeViewSet, basename="liturgy_flower_like")

urlpatterns = [
    path("liturgy_flower/<int:liturgy_flower_id>/", include(router.urls)),
]
