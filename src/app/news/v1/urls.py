from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.news.v1.views import NewsViewSet

router = DefaultRouter()
router.register("news", NewsViewSet, basename="news")

urlpatterns = [
    path("", include(router.urls)),
]
