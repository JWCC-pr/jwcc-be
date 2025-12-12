from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.liturgy_flower_image.v1.views import LiturgyFlowerImageViewSet

router = DefaultRouter()
router.register("liturgy_flower_image", LiturgyFlowerImageViewSet, basename="liturgy_flower_image")

urlpatterns = [
    path("", include(router.urls)),
]
