from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.liturgy_flower_hit.v1.views import LiturgyFlowerHitViewSet

router = DefaultRouter()
router.register("liturgy_flower_hit", LiturgyFlowerHitViewSet, basename="liturgy_flower_hit")

urlpatterns = [
    path("", include(router.urls)),
]
