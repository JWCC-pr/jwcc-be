from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.notice.v1.views import NoticeViewSet

router = DefaultRouter()
router.register("notice", NoticeViewSet, basename="notice")

urlpatterns = [
    path("", include(router.urls)),
]
