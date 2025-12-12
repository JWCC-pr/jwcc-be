from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.banner.v1.views import BannerViewSet

router = DefaultRouter()
router.register("banner", BannerViewSet, basename="banner")

urlpatterns = [
    path("", include(router.urls)),
]
