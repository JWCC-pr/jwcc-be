from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.liturgy_flower.v1.views import LiturgyFlowerViewSet

router = DefaultRouter()
router.register("liturgy_flower", LiturgyFlowerViewSet, basename="liturgy_flower")

urlpatterns = [
    path("", include(router.urls)),
]
